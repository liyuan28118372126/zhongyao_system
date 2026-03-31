"""Image recognition forms."""

from django import forms


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField(label='上传中药材图片')
