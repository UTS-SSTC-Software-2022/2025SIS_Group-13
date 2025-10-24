# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.dateparse import parse_datetime
from .services import call_gemini
from itinerary.models import Itinerary
from utils.response import ResponseHandler

class GenerateView(APIView):
    """POST /api/ai/generate/ -> returns Gemini output"""
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        form_data = request.data  # 前端直接发送整个 formData 对象

        # 可选：你可以把整个 formData 转成字符串 prompt
        prompt = f"Generate a travel plan based on: {form_data}"

        model_name = form_data.get('model')  # 如果前端传了模型参数

        try:
            output_json, raw = call_gemini(prompt, model_name)

            # 自动保存生成的行程到数据库
            if output_json and request.user.is_authenticated:
                # 从LLM响应中提取信息
                title = output_json.get('title', f"行程计划 - {form_data.get('destination', '未知目的地')}")
                destination = output_json.get('destination') or form_data.get('destination', '')
                duration = output_json.get('duration') or form_data.get('days', 1)
                start_time = None
                
                # 尝试解析start_time
                if output_json.get('start_time'):
                    start_time = parse_datetime(output_json.get('start_time'))
                
                # 创建行程记录 - 默认为临时状态
                itinerary = Itinerary.objects.create(
                    user=request.user,
                    title=title,
                    destination=destination,
                    duration=duration,
                    start_time=start_time,
                    llm_response=output_json,
                    isCompleted='Temporary'
                )

            # 可选：写入 DB
            # interaction = Interaction.objects.create(
            #     prompt_json=form_data,
            #     output_json=output_json,
            #     status='success',
            # )

            return Response({
                'output': output_json,
                'itinerary_id': itinerary.itinerary_id if 'itinerary' in locals() else None,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaveItineraryView(APIView):
    """POST /api/ai/save-itinerary/ -> saves itinerary to user's trip plan"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        itinerary_id = request.data.get('itinerary_id')
        
        if not itinerary_id:
            return Response({
                'error': 'itinerary_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取行程并验证用户权限
            itinerary = Itinerary.objects.get(
                itinerary_id=itinerary_id,
                user=request.user
            )
            
            # 更新状态为Generated（添加到Generated Plan列表）
            itinerary.isCompleted = 'Generated'
            itinerary.save()

            return Response({
                'message': '行程已保存到Generated Plan列表',
                'itinerary_id': itinerary.itinerary_id
            }, status=status.HTTP_200_OK)

        except Itinerary.DoesNotExist:
            return ResponseHandler.error(
                msg='Itinerary not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return ResponseHandler.error(
                msg=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetItineraryView(APIView):
    """GET /api/ai/itinerary/{id}/ -> returns specific itinerary details"""
    permission_classes = [IsAuthenticated]

    def get(self, request, itinerary_id):
        try:
            # 获取行程并验证用户权限
            itinerary = Itinerary.objects.get(
                itinerary_id=itinerary_id,
                user=request.user
            )
            
            return ResponseHandler.success(
                data={
                    'itinerary_id': itinerary.itinerary_id,
                    'title': itinerary.title,
                    'destination': itinerary.destination,
                    'duration': itinerary.duration,
                    'start_time': itinerary.start_time,
                    'isCompleted': itinerary.isCompleted,
                    'llm_response': itinerary.llm_response,
                    'create_time': itinerary.create_time,
                },
                msg='Itinerary retrieved successfully'
            )

        except Itinerary.DoesNotExist:
            return Response({
                'error': '行程不存在或您没有权限访问'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompleteItineraryView(APIView):
    """POST /api/ai/complete-itinerary/ -> marks itinerary as completed"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        itinerary_id = request.data.get('itinerary_id')
        
        if not itinerary_id:
            return Response({
                'error': 'itinerary_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取行程并验证用户权限
            itinerary = Itinerary.objects.get(
                itinerary_id=itinerary_id,
                user=request.user
            )
            
            # 更新状态为Completed
            itinerary.isCompleted = 'Completed'
            itinerary.save()

            return Response({
                'message': '行程已标记为完成',
                'itinerary_id': itinerary.itinerary_id
            }, status=status.HTTP_200_OK)

        except Itinerary.DoesNotExist:
            return Response({
                'error': '行程不存在或您没有权限访问'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                 'error': str(e)
             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
