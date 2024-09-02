from rest_framework import serializers

from videos.models import Playlists


class PlaylistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlists
        fields = ('id', 'video_ids', 'user')


class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=256)
    video_id = serializers.CharField(max_length=100)
    views = serializers.IntegerField()
    likes = serializers.IntegerField()
    comments = serializers.IntegerField()
    description = serializers.CharField(max_length=10000, allow_blank=True, allow_null=True)
    thumbnail_url = serializers.URLField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
