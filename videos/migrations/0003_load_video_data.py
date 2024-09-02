# Generated by Django 5.1 on 2024-09-01 18:31
from itertools import count

from django.conf import settings
from django.db import migrations
import requests


def load_video_data(apps, schema_editor):
    video = apps.get_model('videos', 'Video')

    video_data_list = []

    try:
        for page in count(1):
            full_url = f"{settings.MOCK_API_URL}/videos?page={page}"
            response = requests.get(full_url)
            response.raise_for_status()
            response_json = response.json()
            if not response_json["videos"]:
                break
            video_data_list.extend(response_json["videos"])
            print(f"\nObtained {len(response_json['videos'])} from API")
    except requests.RequestException as e:
        print(f"Failed to fetch data from the API: {e}")
        return

    video_data_list = [
        video(
            title=video_data['title'],
            video_id=video_data['video_id'],
            views=video_data['views'],
            likes=video_data['likes'],
            comments=video_data['comments'],
            description=video_data.get('description', ''),
            thumbnail_url=video_data['thumbnail_url'],
            created_at=video_data['created_at'],
            updated_at=video_data['updated_at'],
        ) for video_data in video_data_list
    ]

    print(f"Created {len(video.objects.bulk_create(video_data_list))} videos.")


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_video_alter_playlists_options'),
    ]

    operations = [
        migrations.RunPython(load_video_data)
    ]
