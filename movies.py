import random
import statistics

import movie_storage


def print_menu():
    """Display the application menu."""
    print("\nMenu:")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Create Rating Histogram")
    print("10. Movies sorted by year")
    print("0. Exit")


def get_non_empty_text(prompt):
    """Ask repeatedly until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Error: This field cannot be empty. Please try again.")


def get_rating(prompt):
    """Ask repeatedly until the user enters a valid rating."""
    while True:
        try:
            rating = float(input(prompt))

            if 1 <= rating <= 10:
                return rating

            print("Error: Rating must be between 1 and 10.")

        except ValueError:
            print("Error: Please enter a number, such as 8.5.")


def get_year(prompt):
    """Ask repeatedly until the user enters a valid year."""
    while True:
        try:
            year = int(input(prompt))

            if year > 0:
                return year

            print("Error: Year must be greater than 0.")

        except ValueError:
            print("Error: Please enter a whole number, such as 1999.")


def get_menu_choice():
    """Ask repeatedly until the user enters a valid menu choice."""
    while True:
        choice = input("\nEnter choice (0-10): ").strip()

        if choice in {
            "0", "1", "2", "3", "4",
            "5", "6", "7", "8", "9", "10"
        }:
            return choice

        print("Error: Please enter a number from 0 to 10.")


def list_movies():
    """Print all movies, ratings, and years."""
    movies = movie_storage.get_movies()

    print(f"\n{len(movies)} movies in total")

    if not movies:
        print("There are no movies in the database.")
        return

    for movie, movie_data in movies.items():
        rating = movie_data["rating"]
        year = movie_data["year"]

        print(f"{movie} ({year}): {rating}")


def add_movie():
    """Ask for movie details and save the movie."""
    movies = movie_storage.get_movies()

    movie_name = get_non_empty_text(
        "\nEnter movie name: "
    )

    if movie_name in movies:
        print(f'Error: "{movie_name}" already exists.')
        return

    rating = get_rating("Enter movie rating: ")
    year = get_year("Enter year of release: ")

    movie_storage.add_movie(
        movie_name,
        year,
        rating
    )

    print(f'"{movie_name}" was added successfully.')


def delete_movie():
    """Ask for a movie title and delete the movie."""
    movies = movie_storage.get_movies()

    movie_name = get_non_empty_text(
        "\nEnter movie name to delete: "
    )

    if movie_name not in movies:
        print(f'Error: "{movie_name}" was not found.')
        return

    movie_storage.delete_movie(movie_name)

    print(f'"{movie_name}" was deleted successfully.')


def update_movie():
    """Ask for a movie title and update its rating."""
    movies = movie_storage.get_movies()

    movie_name = get_non_empty_text(
        "\nEnter movie name to update: "
    )

    if movie_name not in movies:
        print(f'Error: "{movie_name}" was not found.')
        return

    new_rating = get_rating("Enter the new rating: ")

    movie_storage.update_movie(
        movie_name,
        new_rating
    )

    print(f'"{movie_name}" was updated successfully.')


def get_best_movies(movies):
    """Return all movies with the highest rating."""
    highest_rating = max(
        movie_data["rating"]
        for movie_data in movies.values()
    )

    return [
        movie
        for movie, movie_data in movies.items()
        if movie_data["rating"] == highest_rating
    ]


def get_worst_movies(movies):
    """Return all movies with the lowest rating."""
    lowest_rating = min(
        movie_data["rating"]
        for movie_data in movies.values()
    )

    return [
        movie
        for movie, movie_data in movies.items()
        if movie_data["rating"] == lowest_rating
    ]


def print_movie_names(movie_names, movies):
    """Print movie names with their ratings and years."""
    for movie in movie_names:
        rating = movies[movie]["rating"]
        year = movies[movie]["year"]

        ratings = [
            movie_data["rating"]
            for movie_data in movies.values()
        ]


def show_stats():
    """Display average, median, best, and worst movie statistics."""
    movies = movie_storage.get_movies()

    if not movies:
        print("\nThere are no movies to calculate statistics.")
        return

    ratings = [
        movie_data["rating"]
        for movie_data in movies.values()
    ]

    average_rating = statistics.mean(ratings)
    median_rating = statistics.median(ratings)

    best_movies = get_best_movies(movies)
    worst_movies = get_worst_movies(movies)

    best_rating = movies[best_movies[0]]["rating"]
    worst_rating = movies[worst_movies[0]]["rating"]

    print(f"\nAverage rating: {average_rating:.2f}")
    print(f"Median rating: {median_rating:.2f}")

    print(f"\nBest movie rating: {best_rating}")
    print_movie_names(best_movies, movies)

    print(f"\nWorst movie rating: {worst_rating}")
    print_movie_names(worst_movies, movies)


def show_random_movie():
    """Display one randomly selected movie."""
    movies = movie_storage.get_movies()

    if not movies:
        print("\nThere are no movies in the database.")
        return

    movie_name = random.choice(list(movies.keys()))
    movie_data = movies[movie_name]

    print(f"\nRandom movie: {movie_name}")
    print(f"Year: {movie_data['year']}")
    print(f"Rating: {movie_data['rating']}")


def search_movies():
    """Search for movies using part of a movie name."""
    movies = movie_storage.get_movies()

    search_text = get_non_empty_text(
        "\nEnter part of movie name: "
    ).lower()

    matching_movies = [
        movie
        for movie in movies
        if search_text in movie.lower()
    ]

    if not matching_movies:
        print(f'No movies found matching "{search_text}".')
        return

    print("\nMatching movies:")
    print_movie_names(matching_movies, movies)


def show_movies_sorted_by_rating():
    """Print movies from highest rating to lowest rating."""
    movies = movie_storage.get_movies()

    sorted_movies = sorted(
        movies.items(),
        key=lambda movie_data: movie_data[1]["rating"],
        reverse=True
    )

    print("\nMovies sorted by rating:")

    for movie, movie_data in sorted_movies:
        rating = movie_data["rating"]
        year = movie_data["year"]

        print(f"{movie} ({year}): {rating}")


def create_histogram():
    """Create and save a histogram of movie ratings."""
    movies = movie_storage.get_movies()

    if not movies:
        print("\nThere are no ratings to display.")
        return

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib is not installed.")
        return

    file_name = get_non_empty_text(
        "\nEnter the file name for the histogram "
        "(for example, ratings.png): "
    )

    ratings = [
        movie_data["rating"]
        for movie_data in movies.values()
    ]

    plt.hist(
        ratings,
        bins=range(1, 12),
        edgecolor="black",
        align="left"
    )

    plt.title("Movie Ratings Histogram")
    plt.xlabel("Rating")
    plt.ylabel("Number of Movies")
    plt.xticks(range(1, 11))
    plt.xlim(0.5, 10.5)

    plt.savefig(file_name)
    plt.close()

    print(f"Histogram saved as {file_name}.")


def show_movies_sorted_by_year():
    """Display movies in chronological order."""
    movies = movie_storage.get_movies()

    if not movies:
        print("\nThere are no movies to sort.")
        return

    while True:
        order = input(
            "\nDo you want the latest movies first or last? "
            "(first/last): "
        ).strip().lower()

        if order == "first":
            reverse = True
            break

        if order == "last":
            reverse = False
            break

        print(
            'Invalid choice. Please enter "first" or "last".'
        )

    sorted_movies = sorted(
        movies.items(),
        key=lambda movie_data: movie_data[1]["year"],
        reverse=reverse
    )

    print("\nMovies sorted by year:")

    for movie, movie_data in sorted_movies:
        year = movie_data["year"]
        rating = movie_data["rating"]

        print(f"{movie} ({year}): {rating}")


def pause_before_menu():
    input("\nPress Enter to return to the menu...")


def main():
    """Run the movie database application."""
    print("********** My Movies Database **********")

    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == "1":
            list_movies()

        elif choice == "2":
            add_movie()

        elif choice == "3":
            delete_movie()

        elif choice == "4":
            update_movie()

        elif choice == "5":
            show_stats()

        elif choice == "6":
            show_random_movie()

        elif choice == "7":
            search_movies()

        elif choice == "8":
            show_movies_sorted_by_rating()

        elif choice == "9":
            create_histogram()

        elif choice == "10":
            show_movies_sorted_by_year()

        elif choice == "0":
            print("\nGoodbye!")
            break

        pause_before_menu()


if __name__ == "__main__":
    main()