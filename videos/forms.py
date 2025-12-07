from django import forms
from .models import Video

class VideoUploadForm(forms.ModelForm):
    """Form used to upload a video."""

    class Meta:
        # Connect this form to the Video model
        model = Video

        # Fields that will appear in the upload form
        fields = ['title', 'description', 'file']

    # Custom validation for uploaded file
    def clean_file(self):
        # Get the uploaded file
        f = self.cleaned_data.get('file')

        # Check if file is missing
        if not f:
            raise forms.ValidationError("No file provided.")

        # Set maximum allowed file size (500 MB)
        max_mb = 500

        # If file is too large, show error
        if f.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f"File too large. Max {max_mb} MB allowed.")

        # File is valid — return it
        return f
