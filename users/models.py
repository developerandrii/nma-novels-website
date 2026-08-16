from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse
from django.conf.urls.static import static

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


class CreatorGroup(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        VERIFIED = 'verified', 'Verified'
        SUSPENDED = 'suspended','Suspended'

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)


class CreatorGroupMember(models.Model):
    class Role(models.TextChoices):
        OWNER = 'owner','Owner'
        ADMIN = 'admin', 'Admin'
        EDITOR = 'editor', 'Editor'
        MEMBER = 'member', 'Member'

    group = models.ForeignKey(
        CreatorGroup,
        on_delete=models.CASCADE,
        related_name='members',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships',
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    joined_at = models.DateTimeField(auto_now_add=True)

