from django.urls import path
from .views import PlaylistsViewset, VideosViewset

urlpatterns = [
    path('', VideosViewset.as_view({"get": "list"}), name='videos'),
    path('playlist/', PlaylistsViewset.as_view({"get": "retrieve", "post": "create"}), name='playlist'),
    path('playlist/<int:pk>/', PlaylistsViewset.as_view({"put": "update"}), name='update-playlist'),
    path('playlist/video/<int:pk>/', PlaylistsViewset.as_view({"delete": "destroy"}), name='remove-from-playlist'),
]
