# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .services import call_gemini

class GenerateView(APIView):
    """POST /api/ai/generate/ -> returns Gemini output"""

    @transaction.atomic
    def post(self, request):
        form_data = request.data  # 前端直接发送整个 formData 对象

        # 可选：你可以把整个 formData 转成字符串 prompt
        prompt = f"Generate a travel itinerary based on: {form_data}"

        model_name = form_data.get('model')  # 如果前端传了模型参数

        try:
            output_json, raw = call_gemini(prompt, model_name)

            # 可选：写入 DB
            # interaction = Interaction.objects.create(
            #     prompt_json=form_data,
            #     output_json=output_json,
            #     status='success',
            # )

            return Response({
                'output': output_json,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
