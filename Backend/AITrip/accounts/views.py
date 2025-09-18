from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from utils.response import CustomModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout

import logging

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserPasswordChangeSerializer,
    UserListSerializer
)
from utils.response import ResponseHandler

logger = logging.getLogger(__name__)


class UserViewSet(CustomModelViewSet,viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['retrieve', 'update', 'partial_update']:
            return UserProfileSerializer
        return UserListSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action == 'create':
            # Allow anyone to register
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list']:
            # Only staff can list all users
            permission_classes = [permissions.IsAdminUser]
        else:
            # Users can only access their own data
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class UserRegistrationView(APIView):
    """
    User registration endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Register a new user"""
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                logger.info(f"New user registered: {user.email}")
                
                return ResponseHandler.success(
                    data= None,
                    msg='User registered successfully',
                    status_code=status.HTTP_201_CREATED
                )
            
            return ResponseHandler.error(
                msg='Registration failed',
                data=serializer.errors
            )
            
        except Exception as e:
            print(e)
            return ResponseHandler.error(
                msg=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class UserLoginView(APIView):
    """
    User login endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Authenticate user and return tokens"""
        try:
            serializer = UserLoginSerializer(
                data=request.data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                
                logger.info(f"User logged in: {user.email}")
                
                data = {
                    'user': UserProfileSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
                
                return ResponseHandler.success(
                    data=data,
                    msg='Login successful'
                )
            
            return ResponseHandler.error(
                msg='Login failed',
                data=serializer.errors
            )
            
        except Exception as e:
            return ResponseHandler.error(
                msg=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserLogoutView(APIView):
    """
    User logout endpoint
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Logout user by blacklisting refresh token"""
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            logout(request)
            logger.info(f"User logged out: {request.user.email}")
            
            return ResponseHandler.success(
                msg='Logout successful'
            )
            
        except Exception as e:
            return ResponseHandler.error(
                msg=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    """
    User profile management endpoint
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current user profile"""
        try:
            serializer = UserProfileSerializer(request.user)
            return ResponseHandler.success(
                data=serializer.data,
                msg='Profile retrieved successfully'
            )
            
        except Exception as e:
            return ResponseHandler.error(
                msg=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request):
        """Update user profile"""
        try:
            serializer = UserProfileSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                user = serializer.save()
                logger.info(f"Profile updated: {user.email}")
                
                return ResponseHandler.success(
                    data=serializer.data,
                    msg='Profile updated successfully'
                )
            
            return ResponseHandler.error(
                msg='Profile update failed',
                data=serializer.errors
            )
            
        except Exception as e:
            return ResponseHandler.error(
                msg=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserPasswordChangeView(APIView):
    """
    Password change endpoint
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Change user password"""
        try:
            serializer = UserPasswordChangeSerializer(
                data=request.data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Password changed: {request.user.email}")
                
                return ResponseHandler.success(
                    msg='Password changed successfully'
                )
            
            return ResponseHandler.error(
                msg='Password change failed',
                data=serializer.errors
            )
            
        except Exception as e:
            return ResponseHandler.error(
                msg=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
