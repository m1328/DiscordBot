import src.tmdb_api as tmdb
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")


def test_env_loaded():
    import os
    assert os.getenv("TMDB_API_KEY") is not None, "TMDB_API_KEY is not set"


def test_get_person_id():
    id = tmdb.get_person_id("Tom Hanks")
    assert isinstance(id, int)


def test_get_genre_id():
    id = tmdb.get_genre_id("Comedy")
    assert isinstance(id, int)
