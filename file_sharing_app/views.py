from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import SharedFile
import os

def home(request):
    # user uploads the file and it is stored in database
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        new_file = SharedFile.objects.create(file=uploaded_file)
        share_url = f"{request.build_absolute_uri('/')}download/{new_file.id}/"
        return render(request, 'file_sharing_app/home.html', {'share_url': share_url})
    
    return render(request, 'file_sharing_app/home.html')


def download_file(request, file_id):    
# 1. Try to find the file. If it was already downloaded and deleted, catch the error.
    try:
        shared_file = SharedFile.objects.get(id=file_id)
    except SharedFile.DoesNotExist:
        # File has already been downloaded or the link is invalid
        return render(request, 'file_sharing_app/expired.html', status=404)
    
    # 2. Check if the file has passed its 24-hour expiration time
    if shared_file.is_expired():
        # Clean up the actual file from the media folder, then delete DB record
        if shared_file.file:
            shared_file.file.delete(save=False)
        shared_file.delete()
        # Show the expired page
        return render(request, 'file_sharing_app/expired.html', status=410)
    
    # 3. If the user clicks the "Download" button
    if request.GET.get('action') == 'download':
        # Read the file data into memory so we can delete the actual file safely
        file_data = shared_file.file.read()
        file_name = os.path.basename(shared_file.file.name)
        
        # Prepare the file to be sent to the user
        response = HttpResponse(file_data, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        # 🔥 ONE-TIME DOWNLOAD LOGIC 🔥
        # Delete the actual file from the "uploads" folder
        if shared_file.file:
            shared_file.file.delete(save=False)
        # Delete the record from the database
        shared_file.delete()
        
        # Send the file to the user
        return response
    
    # 4. Otherwise, just show the landing page
    context = {
        'shared_file': shared_file,
        'filename': os.path.basename(shared_file.file.name)
    }
    return render(request, 'file_sharing_app/download_page.html', context)