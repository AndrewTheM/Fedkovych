import os
from django.http import JsonResponse
from django.shortcuts import render
from google.cloud import storage

def stream_player(request):
    return render(request, 'index.html')

def radio_schedule(request):
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.getenv('GS_BUCKET_NAME'))
    blob = bucket.blob('radio_schedule.txt')
    schedule = blob.download_as_text().split(os.linesep)
    schedule.pop()
    return JsonResponse({'schedule': schedule})
