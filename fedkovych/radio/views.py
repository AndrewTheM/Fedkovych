import os
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def stream_player(request):
    return render(request, 'index.html')

def radio_schedule(request):
    schedule_file = os.path.join(os.path.dirname(os.getcwd()), 'music-bot', 'radio_schedule.txt')
    with open(schedule_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    return JsonResponse({'schedule': lines})