from django.db import models
from django.urls import reverse

import uuid


def create_cover_path(instance, filename):
    return f"novels/{instance.public_id}/cover.jpg"


class Novel(models.Model):

    class Format(models.TextChoices):
        WEB_NOVEL = "web_novel", "Web novel"
        LIGHT_NOVEL = "light_novel", "Light novel"
        SHORT_STORY = "short_story", "Short story"

    class Status(models.TextChoices):
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        HIATUS = "hiatus", "Hiatus"
        CANCELLED = "cancelled", "Cancelled"
        UPCOMING = "upcoming", "Upcoming"

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    title = models.CharField(
        max_length=250,
    )
    format = models.CharField(
        max_length=20,
        choices=Format.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
    )
    description = models.TextField(
        blank=True,    
    )
    release_date = models.DateField(
        blank=True, 
        null=True,
    )
    cover = models.ImageField(
        upload_to=create_cover_path, 
        blank=True,
        null=True
    )
    genres = models.ManyToManyField(
        'Genre',
        blank=True,
        related_name='novels'
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='novels'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('catalog:novel-detail', kwargs={'public_id': self.public_id})


class Genre(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True
    )
    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True
    )
    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Creator(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    name = models.CharField(
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

