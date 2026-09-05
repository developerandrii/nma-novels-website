from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


import uuid

from config import settings


def create_user_picture_path(instance, filename):
    return f"users/{instance.public_id}/picture.jpg"


class User(AbstractUser):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    
    picture = models.ImageField(
        upload_to=create_user_picture_path,
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return reverse('users:user-detail', kwargs={'pk': self.pk})
    
    @property
    def picture_url(self):
        if self.picture:
            return self.picture
        
        return f"{settings.STATIC_URL}users/default/picture.jpg"

    def __str__(self):
        return self.username