from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import VideoUploadForm
from .models import Video
from .utils import compute_sha256_of_uploaded_file

def home(request):
    """
    Display all videos and show the upload form.
    """
    # Get all uploaded videos — newest first
    videos = Video.objects.order_by('-uploaded_at')

    # Create an empty upload form
    form = VideoUploadForm()

    # Render homepage with videos + form
    return render(request, 'videos/home.html', {'videos': videos, 'form': form})


@login_required  # Only logged-in users can upload videos
def upload_video(request):

    # If request is not POST, redirect back to home
    if request.method != 'POST':
        return redirect('videos:home')

    # Create form with submitted data + uploaded file
    form = VideoUploadForm(request.POST, request.FILES)

    # If form has errors, reload page with messages
    if not form.is_valid():
        messages.error(request, "Upload failed. Please fix the errors.")
        videos = Video.objects.order_by('-uploaded_at')
        return render(request, 'videos/home.html', {'videos': videos, 'form': form})

    # Get the uploaded file object
    uploaded_file = request.FILES['file']

    # Generate unique SHA-256 hash for the file
    file_hash = compute_sha256_of_uploaded_file(uploaded_file)

    # Check database for duplicate video using hash
    existing = Video.objects.filter(file_hash=file_hash).first()
    if existing:
        messages.warning(
            request,
            f"Duplicate video detected. Already uploaded by {existing.uploaded_by} on {existing.uploaded_at}."
        )
        return redirect('videos:home')

    # Create a Video object but don't save yet
    video = form.save(commit=False)
    video.uploaded_by = request.user  # Set uploader
    video.file_hash = file_hash       # Store hash
    video.size = uploaded_file.size   # Store file size

    # Try saving — catch duplicate race condition
    try:
        video.save()
    except IntegrityError:
        messages.warning(request, "Duplicate detected while saving. The file was not saved.")
        return redirect('videos:home')

    # Success message after upload
    messages.success(request, "Video uploaded successfully.")
    return redirect('videos:home')


