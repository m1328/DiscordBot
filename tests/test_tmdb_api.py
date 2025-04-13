import src.tmdb_api as tmdb


def test_get_person_id():
    id = tmdb.get_person_id("Tom Hanks")
    assert isinstance(id, int)


def test_get_genre_id():
    id = tmdb.get_genre_id("Comedy")
    assert isinstance(id, int)
