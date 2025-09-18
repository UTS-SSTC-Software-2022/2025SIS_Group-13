# LLM_API/models.py
from django.db import models


class Interaction(models.Model):
    """Stores the original prompt and the JSON output from Gemini."""
    prompt_json = models.JSONField(help_text="Raw input payload from client")
    output_json = models.JSONField(help_text="Structured JSON returned by Gemini")
    status = models.CharField(max_length=32, default='success')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"Interaction {self.id} ({self.status})"