"""LLM QA forms."""

from django import forms


class QuestionForm(forms.Form):
    """Question form."""
    question = forms.CharField(widget=forms.Textarea, label='您的问题')
