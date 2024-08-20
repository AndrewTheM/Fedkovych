from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def stream_player(request):
    return render(request, 'index.html')