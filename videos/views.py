from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from videos.models import Playlists, Video
from videos.serializers import PlaylistsSerializer, VideoSerializer


class PlaylistsViewset(ModelViewSet):
    serializer_class = PlaylistsSerializer
    queryset = Playlists.objects.all()

    def destroy(self, request, *args, **kwargs):
        video = get_object_or_404(Video.objects.all(), id=kwargs.get("pk"))
        playlist = self.queryset.filter(user=request.user)
        if playlist := playlist.first():
            playlist.video_ids.remove(video.id)
            playlist.save()
        else:
            return Response({"error": "User does not have a playlist."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset.filter(user=request.user.id).first()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if playlist := Playlists.objects.filter(user=request.user).first():
            serializer = self.serializer_class(playlist)
        else:
            serializer = self.get_serializer(data={
                "video_ids": request.data.get("video_ids", []), "user_id": request.user.id}
            )
            serializer.is_valid()
            Playlists.objects.create(user=request.user, video_ids=serializer.data.get("video_ids"))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data
        if new_video_ids := data.get("video_ids"):
            playlist = Playlists.objects.filter(user=request.user).first()

            data.update({"user_id": playlist.user.id, "video_ids": list(set(playlist.video_ids+new_video_ids))})
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class VideosViewset(ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_queryset(self):
        queryset = Video.objects.all()
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(title__icontains=search)
        return queryset
