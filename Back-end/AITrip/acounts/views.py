from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
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

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
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
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'success': True,
                    'data': {
                        'user': UserProfileSerializer(user).data,
                        'tokens': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    },
                    'message': 'User registered successfully'
                }, status=status.HTTP_201_CREATED)
            
            logger.warning(f"User registration failed: {serializer.errors}")
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Registration failed'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"User registration error: {str(e)}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                
                return Response({
                    'success': True,
                    'data': {
                        'user': UserProfileSerializer(user).data,
                        'tokens': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    },
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            
            logger.warning(f"Login failed: {serializer.errors}")
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Login failed'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return Response({
                'success': False,
                'message': 'Logout failed'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    User profile management endpoint
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current user profile"""
        try:
            serializer = UserProfileSerializer(request.user)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Profile retrieved successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Profile retrieval error: {str(e)}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
                
                return Response({
                    'success': True,
                    'data': serializer.data,
                    'message': 'Profile updated successfully'
                }, status=status.HTTP_200_OK)
            
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Profile update failed'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Profile update error: {str(e)}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                
                return Response({
                    'success': True,
                    'message': 'Password changed successfully'
                }, status=status.HTTP_200_OK)
            
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Password change failed'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Password change error: {str(e)}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
