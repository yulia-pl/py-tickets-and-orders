from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie, Genre, Actor


def get_movies(
        genres_ids: list[int] = None,
        actors_ids: list[int] = None,
        title: str = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
        movie_title: str,
        movie_description: str,
        genres_ids: list[int],
        actors_ids: list[int]
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description
    )

    genres = Genre.objects.filter(id__in=genres_ids)
    movie.genres.set(genres)

    actors = Actor.objects.filter(id__in=actors_ids)
    movie.actors.set(actors)

    return movie
