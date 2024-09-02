# Introduction

The goal of this project is to provide minimalistic django API that
gives the necessary endpoints to display videos and make/edit playlists.
It also has a migration system integrated, with one of the migrations
making a query to a 3rd party API for the videos, then saves them to
the postgres DB.


# Usage

To use this template to start your own project:

## Environment variables

Using `django-dotenv` we read from a .env file. Here is an example of what it should have

    POSTGRES_DB=mock_youtube
    POSTGRES_USER=hello_django
    POSTGRES_PASSWORD=hello_django
    DATABASE_URL=postgres://hello_django:hello_django@postgres:5432/mock_youtube
    ALLOWED_HOSTS=*
      
## Docker Compose

This assumes that `docker compose` is installed. The docker compose
will run the Dockerfile to get the django server running
and will get a postgres instance up and running.

```bash
docker compose up --build
```

## Migrations

Once you have the docker containers running, to run the migrations:

```bash
docker compose exec web python manage.py migrate
```

## Tests

Once you have the docker containers running, to run the unittests:
```bash
docker compose exec web python manage.py test
```

   
## Endpoints

By entering the localhost instance of the server that is running
you can view all of the endpoints. A notable one is `/admin` which
allows you to view database data in an admin page.
    