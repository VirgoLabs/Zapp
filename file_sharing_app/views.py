from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import SharedFile
from django.utils import timezone  
from datetime import timedelta
import os

def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Grab custom expiry days
        try:
            expiry_days = int(request.POST.get('expiry_days', 1))
        except ValueError:
            expiry_days = 1
            
        # Grab custom max downloads
        try:
            max_downloads = int(request.POST.get('max_downloads', 1))
        except ValueError:
            max_downloads = 1
            
        custom_expiry = timezone.now() + timedelta(days=expiry_days)

        # Create file with both limits
        new_file = SharedFile.objects.create(
            file=uploaded_file, 
            expires_at=custom_expiry,
            max_downloads=max_downloads
        )
        
        share_url = f"{request.build_absolute_uri('/')}download/{new_file.id}/"
        
        return render(request, 'file_sharing_app/home.html', {
            'share_url': share_url,
            'expiry_days': expiry_days,
            'max_downloads': max_downloads # Pass it to the success message
        })
    
    return render(request, 'file_sharing_app/home.html')


def download_file(request, file_id):    
    try:
        shared_file = SharedFile.objects.get(id=file_id)
    except SharedFile.DoesNotExist:
        return render(request, 'file_sharing_app/expired.html', status=404)
    
    # Check Expiration
    if shared_file.is_expired():
        if shared_file.file:
            shared_file.file.delete(save=False)
        shared_file.delete()
        return render(request, 'file_sharing_app/expired.html', status=410)
    
    # Handle Download Click
    if request.GET.get('action') == 'download':
        file_data = shared_file.file.read()
        file_name = os.path.basename(shared_file.file.name)
        
        response = HttpResponse(file_data, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        # NEW: Increment download count
        shared_file.current_downloads += 1
        
        # If they hit the limit, delete everything. Otherwise, just save the new count.
        if shared_file.current_downloads >= shared_file.max_downloads:
            if shared_file.file:
                shared_file.file.delete(save=False)
            shared_file.delete()
        else:
            shared_file.save()
            
        return response
    
    # Show the landing page
    downloads_remaining = shared_file.max_downloads - shared_file.current_downloads
    context = {
        'shared_file': shared_file,
        'filename': os.path.basename(shared_file.file.name),
        'downloads_remaining': downloads_remaining # Pass remaining count to UI
    }
    return render(request, 'file_sharing_app/download_page.html', context)

def how_it_works(request):
    return render(request, 'file_sharing_app/how_it_works.html')