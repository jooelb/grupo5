# capa de servicio/lógica de negocio

import requests
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user


# Obtiene un listado de imágenes desde la API de Rick and Morty
def getAllImages(input=None):
    # Obtiene datos crudos desde la API
    url = "https://rickandmortyapi.com/api/character"
    if input:
        url += f"?name={input}"  # Filtrar personajes por nombre si se proporciona un input
    response = requests.get(url)
    
    if response.status_code == 200:
        json_collection = response.json().get("results", [])
    else:
        json_collection = []

    # Transformar los datos en una lista de diccionarios para renderizarlos en el template
    images = []
    for item in json_collection:
        images.append({
            "id": item.get("id"),
            "name": item.get("name"),
            "status": item.get("status"),
            "image": item.get("image"),
            "location": {
                "name": item.get("location", {}).get("name")
            },
            "first_seen": get_first_episode(item.get("episode", []))  # Obtener primer episodio
        })
    
    return images


# Helper para obtener el primer episodio en el que aparece un personaje
def get_first_episode(episode_urls):
    if episode_urls:
        first_episode_url = episode_urls[0]  # Tomar el primer episodio
        response = requests.get(first_episode_url)
        if response.status_code == 200:
            return response.json().get("name", "Desconocido")
    return "Desconocido"


# Añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    if request.method == 'POST':
        # Transformamos el request en un objeto de tipo Card (o estructura similar)
        fav = {
            "name": request.POST.get("name"),
            "image": request.POST.get("url"),
            "status": request.POST.get("status"),
            "last_location": request.POST.get("last_location"),
            "first_seen": request.POST.get("first_seen"),
            "user": get_user(request)  # Asociamos el favorito al usuario actual
        }

        return repositories.saveFavourite(fav)  # Guardamos en la base de datos
    return None


# Usado desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        # Buscar en la base de datos todos los favoritos del usuario
        favourite_list = repositories.getUserFavourites(user)
        mapped_favourites = []

        # Transformar cada favorito en un formato manejable por el template
        for favourite in favourite_list:
            card = {
                "id": favourite.id,
                "name": favourite.name,
                "image": favourite.image,
                "status": favourite.status,
                "last_location": favourite.last_location,
                "first_seen": favourite.first_seen,
            }
            mapped_favourites.append(card)

        return mapped_favourites


# Borrar un favorito (usado desde el template 'favourites.html')
def deleteFavourite(request):
    if request.method == 'POST':
        favId = request.POST.get('id')  # Obtener el ID del favorito a eliminar
        return repositories.deleteFavourite(favId)  # Borramos de la base de datos
    return None
