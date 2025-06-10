import requests
import string
import random
# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(
          f"ID: {pelicula['id']},"
          f"fTítulo: {pelicula['titulo']}, "
          f"Género: {pelicula['genero']} "
         )
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas',
                         json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(
          f"ID: {pelicula_agregada['id']}, "
          f"Título: {pelicula_agregada['titulo']}, "
          f"Género: {pelicula_agregada['genero']} "
         )
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(
    f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(
          f"ID: {pelicula['id']}, "
          f"Título: {pelicula['titulo']}, "
          f"Género: {pelicula['genero']} "
         )
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(
    f'http://localhost:5000/peliculas/{id_pelicula}',
    json=datos_actualizados
    )
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(
          f"ID: {pelicula_actualizada['id']}, "
          f"Título: {pelicula_actualizada['titulo']}, "
          f"Género: {pelicula_actualizada['genero']} "
         )
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(
    f'http://localhost:5000/peliculas/{id_pelicula}'
    )
if response.status_code == 200:
    print("Película eliminada correctamente.\n")
else:
    print("Error al eliminar la película.\n")

# Obtener peliculas por genero
genre_list = ['Drama', 'Acción', 'Ciencia ficción',
              'Aventura', 'Fantasía', 'Crimen']
for index in genre_list:
    response = requests.get(
        f'http://localhost:5000/peliculas/get_movie_by_genre?genre={index}'
        )
    if response.status_code == 200:
        print(f"Pelicula de {index} obtenida correctamente\n")
    else:
        print(f"Error al buscar peliculas del genero {index}\n")

# Obtener las peliculas que en el titulo contenga determinada letra o palabra
keyword = random.choice(string.ascii_lowercase)
response = requests.get(
    f'http://localhost:5000/peliculas/get_movie_by_title_keyword?kw={keyword}'
    )
if response.status_code == 200:
    for index in response.json():
        print(f"Peliculas obtenidas con el keyword {keyword}")
        print(
              f"ID: {index['id']}, "
              f"Título: {index['titulo']}, "
              f"Género: {index['genero']}\n "
             )
else:
    print(f"No se obtuvieron peliculas con el keyword {keyword}\n")

# Obtener una pelicula aleatoria
response = requests.get('http://localhost:5000/peliculas/random')
pelicula = response.json()
if response.status_code == 200:
    print("Pelicula aleatoria obtenida con exito\n")
    print(
        f"ID: {pelicula['id']}, "
        f"Título: {pelicula['titulo']}, "
        f"Género: {pelicula['genero']}\n "
        )

else:
    print("No se pudo obtener ninguna pelicula aleatoria"
          " o la lista estaba vacia\n")

# Obtener una pelicula aleatoria por genero
genre_list = ['Drama', 'Acción', 'Ciencia ficción',
              'Aventura', 'Fantasía', 'Crimen']
random_genre = random.choice(genre_list)
response = requests.get(
    f'http://localhost:5000/peliculas/random_by_genre?genre={random_genre}'
    )
pelicula = response.json()

if response.status_code == 200:
    print(f"Pelicula de genero aleatoria {random_genre}, obtenida con exito\n")
    print(
        f"ID: {pelicula['id']}, "
        f"Título: {pelicula['titulo']}, "
        f"Género: {pelicula['genero']}\n "
        )
else:
    print(
          "No se pudo obtener ninguna"
          f"película aleatoria del género {random_genre} "
          "o la lista estaba vacía\n"
         )


response = requests.get('http://localhost:5000/peliculas/holiday?genre=Drama')
pelicula = response.json()
if response.status_code == 200:
    print("Pelicula para ver el proximo feriado se obtuvo con exito")
    print(f"Pelicula: {pelicula['pelicula']}\n")
    
else:
    print("No se pudo obterner ninguna pelicula para ver el feriado")
response = requests.get('http://localhost:5000/peliculas/holiday_type?genre=Drama&h_type=trasladable')
data = response.json()
if response.status_code == 200:
    print("Pelicula para ver el proximo feriado trasladable se obtuvo con exito")
    print(f"Pelicula: {data['pelicula']['titulo']}, "
          f"Feriado: {data['feriado']['id']} con motivo {data['feriado']['motivo']}")
else:
    print("No se pudo obterner ninguna pelicula para ver el feriado de este tipo")
