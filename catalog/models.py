from django.db import models
from django.urls import reverse
from django.conf import settings

from .managers import ApprovadNovelManager

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

    class ApprovalStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        SUSPENDED = 'suspended','Suspended'  

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

    approval_status = models.CharField(
        max_length=10,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
        blank=True,
        null=True,
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
    authors = models.ManyToManyField(
        'Creator',
        related_name='written_novels',
    )
    artists = models.ManyToManyField(
        'Creator',
        blank=True,
        related_name='illustrated_novels',
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('catalog:novel-detail', kwargs={'public_id': self.public_id})

    objects = models.Manager()
    approved = ApprovadNovelManager()


class NovelSubmission(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CHANGES_REQUESTED = 'changes_requested', 'Changes Requested'

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='submitted_novels',
    )
    
    # Which team submitted it? (Optional if individual users can also submit)
    team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='novel_submissions',
    )

    novel = models.OneToOneField(
        'Novel',
        on_delete=models.CASCADE,
        related_name='submission_request',
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    moderator_notes = models.TextField(
        blank=True,
        help_text="Provide feedback to the submitter (e.g., reason for rejection or needed edits)."
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_submissions',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        team_str = f" [{self.team.name}]" if self.team else ""
        return f"Submission: {self.novel.title}{team_str} - ({self.get_status_display()})"


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
        max_length=250,
        unique=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Chapter(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    novel = models.ForeignKey(
        'Novel', 
        on_delete=models.CASCADE,
        related_name='chapters',
    )
    title = models.CharField(
        max_length=250,
        blank=True,
    )
    number = models.IntegerField()
    content = models.TextField()

    class Meta:
        ordering = ['-number']

    def __str__(self):
        return f"Chapter {self.number}"
    
    def get_absolute_url(self):
        return reverse('catalog:chapter-detail', kwargs={'public_id': self.public_id})


class Team(models.Model):
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


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:team-detail', kwargs={'public_id': self.public_id})


class TeamMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = 'owner','Owner'
        ADMIN = 'admin', 'Admin'
        EDITOR = 'editor', 'Editor'
        MEMBER = 'member', 'Member'

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='memberships',
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['team', 'user'],
                name='unique_team_member',
            ),
        ]

    def __str__(self):
        return f"{self.team}: {self.role} {self.user}"

