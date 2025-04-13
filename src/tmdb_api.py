import requests
from src.config import TMDB_API_KEY

BASE_URL = "https://api.themoviedb.org/3"

def search_movies(genre=None, year=None, actor=None, director=None):
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": False
    }

    if year:
        params["primary_release_year"] = year

    if genre:
        gid = get_genre_id(genre)
        if gid:
            params["with_genres"] = gid

    if actor:
        actor_id = get_person_id(actor)
        if actor_id:
            params["with_cast"] = actor_id

    if director:
        director_id = get_person_id(director)
        if director_id:
            params["with_crew"] = director_id

    response = requests.get(f"{BASE_URL}/discover/movie", params=params)
    data = response.json()

    if "results" in data:
        return data["results"]

    print("TMDb error (search_movies):", data)
    return []

def get_person_id(name):
    r = requests.get(f"{BASE_URL}/search/person", params={"api_key": TMDB_API_KEY, "query": name})
    data = r.json()

    if "results" in data and data["results"]:
        return data["results"][0]["id"]

    print(f"No person found: {name}")
    print("TMDb response:", data)
    return None

def get_genre_id(name):
    r = requests.get(f"{BASE_URL}/genre/movie/list", params={"api_key": TMDB_API_KEY, "language": "en-US"})
    data = r.json()

    if "genres" in data:
        for genre in data["genres"]:
            if genre["name"].lower() == name.lower():
                return genre["id"]

    print(f"Genre not found: {name}")
    print("TMDb response:", data)
    return None

def get_movie_details(movie_id):
    r = requests.get(f"{BASE_URL}/movie/{movie_id}", params={
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    })
    return r.json()

def get_movie_director(movie_id):
    r = requests.get(f"{BASE_URL}/movie/{movie_id}/credits", params={
        "api_key": TMDB_API_KEY
    })
    data = r.json()
    if "crew" in data:
        for person in data["crew"]:
            if person.get("job") == "Director":
                return person["name"]
    return None

def search_movie_by_title(title):
    r = requests.get(f"{BASE_URL}/search/movie", params={
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "en-US"
    })
    data = r.json()

    if "results" in data and data["results"]:
        return max(data["results"], key=lambda x: x.get("popularity", 0))

    return None


def get_movie_watch_providers(movie_id, country="PL"):
    r = requests.get(f"{BASE_URL}/movie/{movie_id}/watch/providers", params={
        "api_key": TMDB_API_KEY
    })
    data = r.json()
    return data.get("results", {}).get(country, {})
