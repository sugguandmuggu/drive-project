from django.urls import path, include
from drive_app.views import google_drive_upload, google_drive_list_files, google_drive_download_file

urlpatterns = [
    path('upload/', google_drive_upload),
    path('list-file/', google_drive_list_files),
    path('download-file/', google_drive_download_file),

]