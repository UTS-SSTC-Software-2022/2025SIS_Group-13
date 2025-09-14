# LLM_API/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Interaction
from .serializers import PromptIn
from .services import call_gemini


class GenerateView(APIView):
    """POST /api/ai/generate/ -> { id, output } and writes to DB"""

    @transaction.atomic
    def post(self, request):
        ser = PromptIn(data=request.data)
        ser.is_valid(raise_exception=True)
        prompt = ser.validated_data['prompt']
        model = ser.validated_data.get('model')
        schema = ser.validated_data.get('schema')
        extra = ser.validated_data.get('config')

        try:
            output_json, raw = call_gemini(prompt, model, schema, extra)
            interaction = Interaction.objects.create(
                prompt_json=ser.validated_data,
                output_json=output_json,
                status='success',
            )
            return Response({
                'id': interaction.id,
                'output': output_json,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            interaction = Interaction.objects.create(
                prompt_json=ser.validated_data,
                output_json={'error': str(e)},
                status='error',
                error_message=str(e),
            )
        return Response({
            'id': interaction.id,
            'error': str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)