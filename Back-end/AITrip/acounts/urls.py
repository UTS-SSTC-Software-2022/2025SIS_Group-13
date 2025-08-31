from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Authentication endpoints
    path('api/auth/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('api/auth/login/', views.UserLoginView.as_view(), name='user-login'),
    path('api/auth/logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('api/auth/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('api/auth/change-password/', views.UserPasswordChangeView.as_view(), name='user-change-password'),
]
