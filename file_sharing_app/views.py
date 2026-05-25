from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import SharedFile
from django.utils import timezone  
from datetime import timedelta

def home(request):
    if request.method == 'POST':
        # Grab the URL and Name sent from the JavaScript fetch request
        file_url = request.POST.get('file_url')
        file_name = request.POST.get('file_name')
        
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

        # Create file record with the Cloudinary URL
        new_file = SharedFile.objects.create(
            file_url=file_url, 
            file_name=file_name,
            expires_at=custom_expiry,
            max_downloads=max_downloads
        )
        
        # Generate both the Share Link and the Tracking Link
        share_url = f"{request.build_absolute_uri('/')}download/{new_file.id}/"
        tracking_url = f"{request.build_absolute_uri('/')}track/{new_file.id}/"
        
        return render(request, 'file_sharing_app/home.html', {
            'share_url': share_url,
            'tracking_url': tracking_url, 
            'expiry_days': expiry_days,
            'max_downloads': max_downloads 
        })
    
    return render(request, 'file_sharing_app/home.html')


def download_file(request, file_id):    
    try:
        shared_file = SharedFile.objects.get(id=file_id)
    except SharedFile.DoesNotExist:
        return render(request, 'file_sharing_app/expired.html', status=404)
    
    # Check Expiration
    if shared_file.is_expired():
        shared_file.delete()
        return render(request, 'file_sharing_app/expired.html', status=410)
    
    # Handle Download Click
    if request.GET.get('action') == 'download':
        raw_link = shared_file.file_url
        
        # --- NEW: Inject 'fl_attachment' into the URL ---
        # This tells Cloudinary to force a download instead of displaying the image
        if '/upload/' in raw_link:
            cloudinary_link = raw_link.replace('/upload/', '/upload/fl_attachment/')
        else:
            cloudinary_link = raw_link
        
        # Increment download count
        shared_file.current_downloads += 1
        
        if shared_file.current_downloads >= shared_file.max_downloads:
            shared_file.delete()
        else:
            shared_file.save()
            
        # Redirect to the new attachment-enabled URL
        return redirect(cloudinary_link)
    
    # Show the landing page
    downloads_remaining = shared_file.max_downloads - shared_file.current_downloads
    context = {
        'shared_file': shared_file,
        'filename': shared_file.file_name,
        'downloads_remaining': downloads_remaining 
    }
    return render(request, 'file_sharing_app/download_page.html', context)

def how_it_works(request):
    return render(request, 'file_sharing_app/how_it_works.html')

def track_file(request, file_id):
    try:
        shared_file = SharedFile.objects.get(id=file_id)
    except SharedFile.DoesNotExist:
        return render(request, 'file_sharing_app/track.html', {'status': 'deleted'})

    if shared_file.is_expired():
        shared_file.delete()
        return render(request, 'file_sharing_app/track.html', {'status': 'deleted'})

    # Calculate exact time remaining
    time_left = shared_file.expires_at - timezone.now()
    days = time_left.days
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60

    if days > 0:
        time_string = f"{days} day(s), {hours} hour(s)"
    elif hours > 0:
        time_string = f"{hours} hour(s), {minutes} minute(s)"
    else:
        time_string = f"{minutes} minute(s)"

    downloads_left = shared_file.max_downloads - shared_file.current_downloads

    context = {
        'status': 'active',
        'filename': shared_file.file_name,
        'time_string': time_string,
        'downloads_left': downloads_left,
        'max_downloads': shared_file.max_downloads,
        'current_downloads': shared_file.current_downloads
    }
    return render(request, 'file_sharing_app/track.html', context)