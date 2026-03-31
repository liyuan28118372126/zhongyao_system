"""Image recognition views."""

from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import RecognitionRecord
from .utils.recognition import recognize_medicine


def recognize(request):
    """Image recognition view."""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            # Create recognition record
            record = RecognitionRecord(image=image)
            if request.user.is_authenticated:
                record.user = request.user
            # Call recognition function
            result, confidence = recognize_medicine(image)
            # Update record with result
            record.result = result
            record.confidence = confidence
            record.save()
            return render(request, 'image_recognition/result.html', {
                'result': result,
                'confidence': confidence,
                'image': record.image
            })
    else:
        form = ImageUploadForm()
    return render(request, 'image_recognition/recognize.html', {'form': form})
