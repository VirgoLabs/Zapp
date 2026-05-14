from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download/<uuid:file_id>/', views.download_file, name='download_file'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
]