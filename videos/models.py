from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import ForeignKey, SET_NULL, CASCADE


class Playlists(models.Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    video_ids = ArrayField(
        models.PositiveIntegerField()
    )

    class Meta:
        verbose_name_plural = "Playlists"

    def __str__(self):
        return f"{self.user}'s playlist"


class Video(models.Model):
    title = models.CharField(max_length=255)
    video_id = models.CharField(max_length=100, unique=True)
    views = models.PositiveIntegerField()
    likes = models.PositiveIntegerField()
    comments = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    thumbnail_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
