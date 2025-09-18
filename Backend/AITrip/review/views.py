from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from utils.response import CustomModelViewSet
from utils.customPagination import CustomPagination

from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(CustomModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
