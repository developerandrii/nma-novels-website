from django.db import models

class ApprovadNovelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approval_status='approved')