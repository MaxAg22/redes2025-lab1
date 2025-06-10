from flask import Flask, jsonify, request, Response
from typing import Optional, Tuple
import random
from proximo_feriado import NextHoliday


app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


def get_all_movies() -> Response:
    """
    Return all movies as a JSON response.

    This function retrieves the entire list of movies from the
    'peliculas' list and returns it as a JSON array. No input
    parameters are required.

    Returns:
        Response: A JSON response containing all movies.
    """
    return jsonify(peliculas)


def get_movie(id: int) -> Response:
    """
    Retrieve a movie by its integer ID.

    Searches the 'peliculas' list for a movie whose 'id' matches
    the given parameter. If no match is found, returns an error
    message with status code 404.

    Args:
        id (int): The unique ID of the movie.

    Returns:
        Response: A JSON response with the matching movie or
        an error message if not found.
    """
    for movie in peliculas:
        if movie['id'] == id:
            return jsonify(movie)
    return jsonify({"error": "Movie could not be found or does not exist"}), 404


def add_movie() -> Response:
    """
    Add a new movie to the list.

    Expects a JSON body with 'titulo' (str) and 'genero' (str).
    Automatically generates a unique integer ID for the movie
    and appends the movie to the 'peliculas' list.

    Returns:
        tuple[Response, int]: A JSON response with the new movie
        and HTTP status code 201.
    """
    new_movie = {
        'id': get_new_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(new_movie)
    print(peliculas)
    return jsonify(new_movie), 201


def update_movie(id: int) -> Response:
    """
    Update the title and genre of an existing movie by ID.

    Expects a JSON body with 'titulo' (str) and 'genero' (str).
    If the given ID is invalid (out of range), returns a 404
    error message. Otherwise, updates the movie in place.

    Args:
        id (int): The unique ID of the movie to update.

    Returns:
        Response: A JSON response with the updated movie or an
        error message if not found.
    """
    if id <= 0 or id > len(peliculas):
        return jsonify({"error": "Movie could not be found"}), 404
    updated_movie = {
        'id': id,
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas[id - 1].update(updated_movie)
    return jsonify(updated_movie)


def remove_movie(id: int) -> Response:
    """
    Remove a movie by its integer ID.

    Searches for the movie with the given ID in the 'peliculas'
    list. If not found, returns a 404 error. If found, removes
    it and returns a success message. (Note: This function no
    longer reassigns IDs sequentially in this version.)

    Args:
        id (int): The unique ID of the movie to remove.

    Returns:
        Response: A JSON response with a success message or a
        404 error message if not found.
    """
    movie_aux = next((movie for movie in peliculas if movie['id'] == id), None)
    
    if movie_aux is None:
        return jsonify({'mensaje' : 'Movie not in list'}), 404
    
    peliculas.remove(peliculas[id - 1])

    return jsonify({'mensaje' : 'Movie successfully removed'})


def get_new_id():
    """
    Generate a new unique integer ID for a movie.

    Checks the last movie in the 'peliculas' list for its ID
    and returns one higher. If the list is empty, returns 1.

    Returns:
        int: The next available unique movie ID.
    """
    if len(peliculas) > 0:
        last_id = peliculas[-1]['id']
        return last_id + 1
    else:
        return 1


def get_movie_by_genre(genre: Optional[str] = None) -> Response:
    """
    Return a list of movies matching a given genre.

    It filters the 'peliculas' list by comparing the genre. If no genre is
    provided or no matches are found, an error response with status 404 is returned.

    Query Parameters:
        genre (str): The genre to filter by when not passed as a function
            argument.

    Args:
        genre (str, optional): The genre to filter by. If None, the function
            reads the value from the request's query parameters.

    Returns:
        Response: A JSON response containing a list of matching movies, or an
        error message with status code 404 if no genre is provided or no matches
        are found.

    Example usage (via curl):
        curl http://localhost:5000/peliculas/get_movie_by_genre?genre=Drama

    Example usage (from another function):
        get_movie_by_genre("Acción")
    """
    if genre is None:
        genre = request.args.get("genre")
    if not genre:
        return jsonify({'error' : 'Missing genre'}), 404
    
    genre_list = []
    new_id = 1
    for movie in peliculas:
        if movie['genero'].lower() == genre.lower():
            copy_aux = movie.copy()
            copy_aux['id'] = new_id
            genre_list.append(copy_aux)
            new_id += 1
    if not genre_list:
        return jsonify({"error" : "No movies found for that genre"}), 404
    return jsonify(genre_list)


def get_movie_by_title_keyword() -> Response:
    """
    Return movies whose titles contain a given keyword.

    Reads the 'kw' (keyword) query parameter from the request.
    Searches each movie title (case-insensitive) for the keyword.
    If none is provided or no matches are found, returns an error.

    Query Parameters:
        kw (str): The keyword to look for in movie titles.

    Returns:
        Response: A JSON list of matching movies or an error
        message if none match.
    """
    kw = request.args.get("kw")
    if not kw:
        return jsonify({'error' : 'Missing keyword'}), 404
    
    match_list = []
    new_id = 1
    for movie in peliculas:
        if kw.lower() in movie['titulo'].lower():
            copy_aux = movie.copy()
            copy_aux['id'] = new_id
            match_list.append(copy_aux)
            new_id += 1

    if not match_list:
        return jsonify({'error' : f'There is no movie with keyword: "{kw}"'}), 404

    return jsonify(match_list)


def random_movie():
    """
    Return a random movie from the 'peliculas' list.

    If the list is empty, returns an error message with a 404
    status code.

    Returns:
        Response: A JSON response with one randomly selected
        movie or an error if no movies exist.
    """
    if not peliculas:
        return jsonify({"error": "No movies found"}), 404
    
    movie = random.choice(peliculas)
    return jsonify(movie)


def random_movie_by_genre(genre: Optional[str] = None) -> Response:
    """
    Return a random movie from a specific genre.

    It obtains a list of movies for the specified genre by calling get_movie_by_genre() 
    and then returns a random selection.
    If no genre is provided or no matching movies exist, an error is returned.

    Query Parameters:
        genre (str): The genre to filter by when not passed as a function
            argument.

    Args:
        genre (str, optional): The genre to filter by. Defaults to None, in which
            case the function reads it from the request's query parameters.

    Returns:
        Response: A JSON response containing a randomly selected movie from
        the given genre, or an error message if no match is found.

    Example usage (via curl):
        curl http://localhost:5000/peliculas/random_by_genre?genre=Acción

    Example usage (from another function):
        random_movie_by_genre("Acción")
    """
    if genre is None:
        genre = request.args.get("genre")
    if not genre:
        return jsonify({'error': 'Missing genre'}, 404)
    list_aux = get_movie_by_genre(genre).get_json()
    movie = random.choice(list_aux)
    return jsonify(movie)


def film_for_holiday() -> Response:
    """
    Suggest a movie based on the next holiday and a specified genre.

    Reads the 'genre' query parameter from the request. Uses
    NextHoliday() to fetch the upcoming holiday, then calls
    random_movie_by_genre() to select a random movie from the
    specified genre. Returns both as a JSON object.

    Returns:
        Response: A JSON object containing the holiday info and a
        recommended movie. If 'genre' is missing, returns an error.
    """
    genre = request.args.get("genre")
    if not genre:
        return jsonify({"error": "Missing parameters genre"}, 404)

    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()

    movie = random_movie_by_genre(genre).get_json()

    return jsonify({"feriado": next_holiday.holiday, "pelicula": movie})
    

def film_for_holiday_type() -> Response:
    """
    Suggest a movie based on the next holiday given a specific holiday type, 
    and a specified genre.

    Reads the 'genre' and 'h_type' query parameters from the request. Uses
    NextHoliday() to fetch the upcoming holiday based on h_type, then calls
    random_movie_by_genre() to select a random movie from the
    specified genre. Returns both as a JSON object.

    Returns:
        Response: A JSON object containing the holiday info and a
        recommended movie. If either 'genre' or 'h_type' are missing, 
        returns an error.
    """
    genre = request.args.get("genre")
    h_type = request.args.get("h_type")

    if not genre:
        return jsonify({"error": "Missing parameters genre"}, 404)

    if not h_type:
        return jsonify({"error": "Missing parameters h_type"}, 404)

    next_holiday = NextHoliday()
    next_holiday.fetch_holidays(h_type)

    movie = random_movie_by_genre(genre).get_json()

    return jsonify({"feriado": next_holiday.holiday, "pelicula": movie})


app.add_url_rule(
    '/peliculas',
    'get_all_movies',
    get_all_movies,
    methods=['GET']
)


app.add_url_rule(
    '/peliculas/<int:id>',
    'get_movie',
    get_movie,
    methods=['GET']
)


app.add_url_rule(
    '/peliculas',
    'add_movie',
    add_movie,
    methods=['POST']
)


app.add_url_rule(
    '/peliculas/<int:id>',
    'update_movie',
    update_movie,
    methods=['PUT']
)


app.add_url_rule(
    '/peliculas/<int:id>',
    'remove_movie',
    remove_movie,
    methods=['DELETE']
)


app.add_url_rule(
    '/peliculas/get_movie_by_genre',
    'get_movie_by_genre',
    get_movie_by_genre,
    methods=['GET']
)


app.add_url_rule(
    '/peliculas/get_movie_by_title_keyword',
    'get_movie_by_title_keyword',
    get_movie_by_title_keyword,
    methods=['GET']
)


app.add_url_rule(
    '/peliculas/random',
    'random_movie',
    random_movie,
    methods=['GET']
)


app.add_url_rule(
    '/peliculas/random_by_genre',
    'random_movie_by_genre',
    random_movie_by_genre,
    methods=['GET']
)


app.add_url_rule(
    '/peliculas/holiday',
    'film_for_holiday',
    film_for_holiday,
    methods=['GET'])
    
app.add_url_rule(
    '/peliculas/holiday_type',
    'film_for_holiday_type',
    film_for_holiday_type,
    methods=['GET'])


if __name__ == '__main__':
    app.run()
