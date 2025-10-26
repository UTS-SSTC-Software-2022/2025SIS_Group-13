from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .models import Itinerary, DailySchedule, POI
from .serializers import ItinerarySerializer, DailyScheduleSerializer, POISerializer
from django_filters.rest_framework import DjangoFilterBackend

from utils.response import CustomModelViewSet
from utils.customPagination import CustomPagination

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def test_itinerary_list(request):
    """简单的测试API视图"""
    itineraries = Itinerary.objects.filter(user=request.user)
    serializer = ItinerarySerializer(itineraries, many=True)
    return Response({
        'success': 1,
        'msg': 'Success',
        'data': serializer.data
    })

class ItineraryViewSet(viewsets.ModelViewSet):
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]  # 暂时注释掉过滤
    # filterset_fields = ['user', 'title', 'destination', 'isCompleted', 'create_time']
    # pagination_class = CustomPagination  # 暂时注释掉分页

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        # 只返回当前用户的行程
        return Itinerary.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """更新行程状态"""
        itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
        new_status = request.data.get('isCompleted')
        
        if new_status not in ['Temporary', 'Generated', 'Completed']:
            return Response(
                {'error': 'Invalid status. Must be one of: Temporary, Generated, Completed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        itinerary.isCompleted = new_status
        itinerary.save()
        
        return Response({
            'message': 'Status updated successfully',
            'isCompleted': itinerary.isCompleted
        })

class DailyScheduleViewSet(CustomModelViewSet):
    queryset = DailySchedule.objects.all()
    serializer_class = DailyScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['itinerary', 'day_number', 'create_time']
    pagination_class = CustomPagination

class POIViewSet(CustomModelViewSet):
    queryset = POI.objects.all()
    serializer_class = POISerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['schedule', 'name', 'category', 'create_time']
    pagination_class = CustomPagination