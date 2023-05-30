

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)


class MusicFile(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    FILE_TYPES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music_files/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default=PUBLIC)
    allowed_emails = models.ManyToManyField(User, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

