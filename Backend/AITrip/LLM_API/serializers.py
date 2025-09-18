# LLM_API/serializers.py
from rest_framework import serializers


class PromptIn(serializers.Serializer):
    # Required: the instruction/prompt. Can be text or a small JSON blob string field.
    prompt = serializers.CharField()


    # Optional: model name (defaults to a fast JSON-friendly model)
    model = serializers.CharField(required=False, allow_blank=True)


    # Optional: JSON schema to constrain the output (either OpenAPI-style dict
    # or a simplified schema supported by the SDK). If provided, we send it through.
    schema = serializers.JSONField(required=False)


    # Optional: extra generation config (e.g., temperature). Kept minimal here.
    config = serializers.DictField(required=False)