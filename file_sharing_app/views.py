from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import SharedFile
import os

def home(request):
    # user uploads the file and it is stored in database
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Create the database record
        new_file = SharedFile.objects.create(file=uploaded_file)

        # creates a download link of the file that user uploads
        share_url = f"{request.build_absolute_uri('/')}download/{new_file.id}/"

        return render(request, 'file_sharing_app/home.html', {'share_url': share_url})
    
    return render(request, 'file_sharing_app/home.html')

def download_file(request, file_id):    
    # finds the file in the database
    shared_file = get_object_or_404(SharedFile, id=file_id)
    
    if shared_file.is_expired():
        # if file is expired the file gets deleted from the database
        shared_file.delete()
        return HttpResponse("This file link has expired and was deleted.", status=410)
    
    # 1. If the user clicks the "Download" button, serve the actual file
    if request.GET.get('action') == 'download':
        response = HttpResponse(shared_file.file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(shared_file.file.name)}"'
        return response
    
    # 2. Otherwise, just show the landing page with the file details
    context = {
        'shared_file': shared_file,
        'filename': os.path.basename(shared_file.file.name)
    }
    return render(request, 'file_sharing_app/download_page.html', context)