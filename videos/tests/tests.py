import json

from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from videos.models import Playlists, Video
from rest_framework_simplejwt.tokens import RefreshToken


class PlaylistsViewsetTestCase(TestCase):
    fixtures = ['users.json', 'videos.json', 'playlist.json']

    def setUp(self):
        self.client = APIClient()

        # Get the test user and generate JWT token
        self.user = User.objects.get(username='testuser')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.playlist = Playlists.objects.get(pk=1)
        self.video = Video.objects.get(pk=1)

    def test_destroy_playlist_video(self):
        response = self.client.delete(reverse('remove-from-playlist', kwargs={'pk': self.video.id}))
        self.playlist.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.video.id, self.playlist.video_ids)

    def test_destroy_playlist_video_not_found(self):
        response = self.client.delete(reverse('remove-from-playlist', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_playlist_no_playlist(self):
        self.playlist.delete()

        response = self.client.delete(reverse('remove-from-playlist', kwargs={'pk': self.video.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "User does not have a playlist.")

    def test_retrieve_playlist(self):
        response = self.client.get(reverse('playlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.playlist.id)

    def test_create_playlist(self):
        Playlists.objects.all().delete()

        response = self.client.post(reverse('playlist'),
                                    data=json.dumps({"video_ids": [self.video.id]}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.video.id, response.data['video_ids'])

    def test_update_playlist(self):
        new_video = Video.objects.create(
            title="New Video",
            video_id="1000",
            views=0,
            likes=0,
            comments=0,
            description="New Test",
            thumbnail_url="http://newtest.com",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        )

        response = self.client.put(reverse('update-playlist',
                                           kwargs={'pk': self.playlist.id}),
                                   data=json.dumps({"video_ids": [new_video.id]}),
                                   content_type='application/json')
        self.playlist.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(new_video.id, self.playlist.video_ids)


class VideosViewsetTestCase(TestCase):
    fixtures = ['videos.json', 'users.json']

    def setUp(self):
        self.client = APIClient()

        # Get the test user and generate JWT token
        self.user = User.objects.get(username='testuser')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_video_search(self):
        response = self.client.get(f"{reverse('videos')}?search=Another")
        response_data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['id'], 2)

    def test_video_search_no_results(self):
        response = self.client.get(f"{reverse('videos')}?search=NonExistent")
        response_data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 0)

    def test_video_list(self):
        response = self.client.get(reverse('videos'))
        response_data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 20)  # 20 a batch
