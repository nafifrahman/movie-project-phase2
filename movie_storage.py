import json

FILE_NAME = "data.json"


def get_movies():
    """
    Return all movies from the JSON file.
    """
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        print(
            f"Error: The storage file '{FILE_NAME}' was not found."
        )
        return {}

    except json.JSONDecodeError:
        print(
            f"Error: The storage file '{FILE_NAME}' "
            "contains invalid JSON."
        )
        return {}


def save_movies(movies):
    """
    Gets all movies as an argument and saves them to the JSON file.
    """
    with open(FILE_NAME, "w") as file:
        json.dump(movies, file, indent=2)


def add_movie(title, year, rating):
    """
    Add a movie to the JSON database.
    """
    movies = get_movies()

    movies[title] = {
        "rating": rating,
        "year": year
    }

    save_movies(movies)


def delete_movie(title):
    """
    Delete a movie from the movies database.
    """
    movies = get_movies()

    if title not in movies:
        return False

    del movies[title]
    save_movies(movies)

    return True


def update_movie(title, rating):
    """
    Update a movie's rating in the movies database.
    """
    movies = get_movies()

    if title not in movies:
        return False

    movies[title]["rating"] = rating
    save_movies(movies)

    return True
