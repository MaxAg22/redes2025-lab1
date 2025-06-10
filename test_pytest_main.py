# test.py

import pytest
from main import app

@pytest.fixture
def client():
    app.testing = True  # activa el modo de testing de Flask
    with app.test_client() as client:
        yield client

def test_obtener_peliculas(client):
    response = client.get('/peliculas')
    assert response.status_code == 200
    data = response.get_json()
    # Dependiendo del estado inicial de 'peliculas', ajustar la cantidad de elementos esperados
    assert isinstance(data, list)
    # Ejemplo: verificar que haya al menos 12 películas
    assert len(data) >= 12

def test_agregar_pelicula(client):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = client.post('/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    data = response.get_json()
    assert data['titulo'] == 'Pelicula de prueba'
    # Puedes agregar más aserciones según la lógica de 'obtener_nuevo_id'

def test_obtener_detalle_pelicula(client):
    response = client.get('/peliculas/1')
    # Esto dependerá de que la función 'obtener_pelicula' esté implementada correctamente
    # Aquí se espera un 200 y los detalles de la película con id 1
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'Indiana Jones'

def test_actualizar_detalle_pelicula(client):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = client.put('/peliculas/1', json=datos_actualizados)
    # Verifica el status code y los cambios realizados
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'Nuevo título'

def test_eliminar_pelicula(client):
    response = client.delete('/peliculas/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'mensaje' in data
    response = client.get('/peliculas/1')
    assert 'mensaje' in data
    assert response.status_code == 404
    
def test_get_movie_by_genre(client):
    genre_list = ['Drama', 'Acción', 'Ciencia ficción',
              'Aventura', 'Fantasía', 'Crimen']
    for index in genre_list:
        response = client.get(f'/peliculas/get_movie_by_genre?genre={index}')
        assert response.status_code == 200
        # Verificar que sea una lista de peliculas solo del genero solicitado
        data = response.get_json()
        for element in data:
            assert index == element['genero']

def test_get_movie_by_title_keyword(client):
    keyword = "Th"
    response = client.get(f'/peliculas/get_movie_by_title_keyword?kw={keyword}')
    assert response.status_code == 200
    data = response.get_json()
    # Verificar que keyword efectivamente esta en el titulo de las peliculas encontradas
    for element in data:
        assert keyword.lower() in element['titulo'].lower()

def test_random_movie(client):
    response = client.get('/peliculas/random')
    assert response.status_code == 200

def test_random_movie_by_genre(client):
    genre_list = ['Drama', 'Acción', 'Ciencia ficción',
              'Aventura', 'Fantasía', 'Crimen']
    for index in genre_list:
        response = client.get(f'/peliculas/random_by_genre?genre={index}')
        assert response.status_code == 200
        data = response.get_json()
        # Verificar que sea el genero solicitado
        assert data['genero'] == index
 
def test_film_for_holiday(client):
    genre_list = ['Drama', 'Acción', 'Ciencia ficción',
              'Aventura', 'Fantasía', 'Crimen']
    for index in genre_list:
        response = client.get(f'/peliculas/holiday?genre={index}')
        assert response.status_code == 200
        data = response.get_json()
        assert "feriado" in data
        assert "pelicula" in data

def test_film_for_holiday_type(client):
    genre_list = ['Drama', 'Acción', 'Ciencia ficción',
              'Aventura', 'Fantasía', 'Crimen']
    for index in genre_list:
        response = client.get(f'/peliculas/holiday_type?genre={index}&h_type=trasladable')
        assert response.status_code == 200
        data = response.get_json()
        assert "trasladable" in data['feriado']['tipo']
        assert index in data['pelicula']['genero']
