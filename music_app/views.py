from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import models

from .forms import MusicFileForm
from .models import MusicFile


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid login credentials.'})
    return render(request, 'registration/login.html')


@login_required
def upload_music(request):
    if request.method == 'POST':
        form = MusicFileForm(request.POST, request.FILES)
        if form.is_valid():
            music_file = form.save(commit=False)
            music_file.user = request.user
            music_file.save()
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = MusicFileForm()
    return render(request, 'music/upload.html', {'form': form})


@login_required
def homepage(request):
    user_email = request.user.email
    music_files = MusicFile.objects.filter(
        models.Q(access=MusicFile.PUBLIC) |
        models.Q(access=MusicFile.PRIVATE, user=request.user) |
        models.Q(access=MusicFile.PROTECTED, allowed_emails__contains=user_email)
    )
    return render(request, 'music/homepage.html', {'music_files': music_files})
