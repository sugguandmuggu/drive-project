import io
import os
import logging
from pathlib import Path
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from drive_app.utils import upload_on_drive




# Create your views here.
@csrf_exempt
def google_drive_upload(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST requests are allowed", "status": 405}, status=405)

    access_token = request.headers.get('Authorization')
    if not access_token:
        return JsonResponse({"error": "No access token provided"}, status=401)

    access_token = access_token.split(' ')[1]
    creds = Credentials(token=access_token)
    service = build("drive", "v3", credentials=creds)

    if not request.FILES:
        return JsonResponse({"error": "No files provided", "status": 400}, status=400)

    for key in request.FILES:
        files = request.FILES.getlist(key)
        if len(files) > 1:
            # Create a folder for multiple files
            folder_metadata = {
                'name': key,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            folder_id = folder.get('id')

            for file in files:
                file_metadata = {"name": file.name, "parents": [folder_id]}
                upload_on_drive(file, file_metadata, service)
        else:
            # Upload single file directly
            file = files[0]
            file_metadata = {"name": file.name}
            upload_on_drive(file, file_metadata, service)

    return JsonResponse({"message": "Successfully uploaded all files", "status": 200}, status=200)


@csrf_exempt
def google_drive_list_files(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET requests are allowed", "status": 405}, status=405)

    access_token = request.headers.get('Authorization')
    if not access_token:
        return JsonResponse({"error": "No access token provided"}, status=401)

    access_token = access_token.split(' ')[1]
    creds = Credentials(token=access_token)
    service = build("drive", "v3", credentials=creds)

    # Get query parameters
    query = request.GET.get('query', '')
    mime_type = request.GET.get('mimeType', '')

    # Build the search query
    search_query = []
    if query:
        search_query.append(f"name contains '{query}'")
    if mime_type:
        search_query.append(f"mimeType='{mime_type}'")
    search_query = " and ".join(search_query)


    # Call the Drive API to list files based on the search query
    results = service.files().list(q=search_query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])


    if not items:
        return JsonResponse({"message": "No files found", "status": 200}, status=200)
    else:
        files_list = [{"id": item['id'], "name": item['name']} for item in items]
        return JsonResponse({"files": files_list, "status": 200}, status=200)

@csrf_exempt
def google_drive_download_file(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET requests are allowed", "status": 405}, status=405)

    access_token = request.headers.get('Authorization')
    if not access_token:
        return JsonResponse({"error": "No access token provided"}, status=401)

    access_token = access_token.split(' ')[1]
    creds = Credentials(token=access_token)
    service = build("drive", "v3", credentials=creds)

    # Get the file ID from the query parameters
    file_id = request.GET.get('fileId')
    if not file_id:
        return JsonResponse({"error": "No file ID provided"}, status=400)

    try:
        # Fetch the file metadata to get the name
        file_metadata = service.files().get(fileId=file_id).execute()
        file_name = file_metadata.get('name', 'downloaded_file')

        # Download the file into memory (BytesIO)
        file_stream = io.BytesIO()
        request = service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(file_stream, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}% complete.")

        # Move the stream to the beginning
        file_stream.seek(0)

        # Serve the file as an HTTP response for download
        response = FileResponse(file_stream, as_attachment=True, filename=file_name)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
