# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
from app.layers.services import services

def home(request):
    images = services.getAllImages() # Usa el nombre correcto de la función
    return render(request, 'home.html', { 'images': images })

    favourite_list = services.get_user_favourites(request.user) if request.user.is_authenticated else []

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if search_msg != '':
        images = services.search_images(search_msg)
        favourite_list = services.get_user_favourites(request.user) if request.user.is_authenticated else []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'search_msg': search_msg })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.get_user_favourites(request.user)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        if image_id:
            services.add_to_favourites(request.user, image_id)
    return redirect('getAllFavouritesByUser')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        if image_id:
            services.remove_from_favourites(request.user, image_id)
    return redirect('getAllFavouritesByUser')

@login_required
def exit(request):
    logout(request)
    return redirect('index_page')