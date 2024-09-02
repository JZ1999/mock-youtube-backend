from django.contrib import admin

from videos.models import Playlists, Video


class PlaylistAdmin(admin.ModelAdmin):
    model = Playlists


class VideoAdmin(admin.ModelAdmin):
    model = Video


admin.site.register(Video, VideoAdmin)
admin.site.register(Playlists, PlaylistAdmin)
