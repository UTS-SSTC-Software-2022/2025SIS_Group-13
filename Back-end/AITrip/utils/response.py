"""
Unified response handler for AITrip project
Provides consistent API response format across all endpoints
"""

from rest_framework.response import Response
from rest_framework import status, viewsets
from typing import Any


class ResponseHandler:
    """
    Simplified response handler for consistent API responses
    
    All responses follow the format:
    {
        "success": int,    // 1 for success, 0 for error
        "msg": str,        // Response message
        "data": any        // Response data (always present)
    }
    """
    
    @staticmethod
    def success(
        data: Any = None,
        msg: str = "Operation successful",
        status_code: int = status.HTTP_200_OK
    ) -> Response:
        """
        Generate a successful response
        
        Args:
            data: Response data
            msg: Success message
            status_code: HTTP status code (default: 200)
            
        Returns:
            Response object with success format
        """
        response_data = {
            'success': 1,
            'msg': msg,
            'data': data
        }
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(
        msg: str = "Operation failed",
        data: Any = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> Response:
        """
        Generate an error response
        
        Args:
            msg: Error message
            data: Error data (optional)
            status_code: HTTP status code (default: 400)
            
        Returns:
            Response object with error format
        """
        response_data = {
            'success': 0,
            'msg': msg,
            'data': data
        }
        
        return Response(response_data, status=status_code)

class CustomModelViewSet(viewsets.ModelViewSet):
    def finalize_response(self, request, response, *args, **kwargs):
        if isinstance(response.data, dict) and 'success' in response.data:
            return super().finalize_response(request, response, *args, **kwargs)

        if response.status_code < 400:
            response.data = ResponseHandler.success(data=response.data).data
        else:
            response.data = ResponseHandler.error(data=response.data).data

        return super().finalize_response(request, response, *args, **kwargs)



