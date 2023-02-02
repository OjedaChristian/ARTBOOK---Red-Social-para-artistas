from django.shortcuts import render, redirect  # redirecciones entre diferentes path de la url
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required  # para denegar acceso a path específicos si no existe un usuario activo
from django.contrib import messages  # envío de mensajes al usuario, se usará para comunicar si se han guardado correctamente datos en la database
from core.models import Profile, Post, LikePost, Followers  # models/database
from core.filters import PostFilter  # class para el filtrado/búsqueda imágenes

# herramientas para operaciones específicas:
from itertools import chain
import random


# Create your views here.

@login_required(login_url='/signin')  # decorator para no permitir al usuario acceder al feed de la app sin haber iniciado sesión previamente.
def index(request):
    user_object = User.objects.get(username=request.user.username)  # obtenemos el usuario a través del model user
    user_profile = Profile.objects.get(user=user_object)  # usamos los datos del model user para obtener el usuario activo en el model Profile

    # SISTEMA DE FEED PARA EL HOME - solo podremos visualizar las imágenes de los usuarios a los que seguimos

    user_following_list = []
    feed = []

    user_following = Followers.objects.filter(follower=request.user.username)  # obtenemos el usuario al que seguimos con la cuenta activa

    for users in user_following:  # por cada usuario que seguimos lo añadimos a la lista de following_list
        user_following_list.append(users.user)

    for usernames in user_following_list:  # por cada username en la following_list
        feed_lists = Post.objects.filter(user=usernames)  # añadimos cada usuario que seguimos que subio un post a la feed_lists
        feed.append(feed_lists)  # añadimos los usuarios de la feed_list al feed

    feed_lists = list(chain(*feed))

    # SISTEMAS DE SUGERENCIAS/USUARIOS A SEGUIR

    all_users = User.objects.all()  # obtenemos todos los usuarios en la database
    user_following_all = []

    for user in user_following:  # por cada usuario que seguimos
        user_list = User.objects.get(username=user.user)  # obtenemos los usernames de todos los usuarios siguiendo
        user_following_all.append(user_list)  # añadimos el usuario a la lista de following

    # loop en list de all_users en la db, si esta lista de usuarios no existe en la lista de los usuarios a los que sigue, se creará la lista de sugerencias de nuevos usuarios
    suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]

    # eliminamos nuestro usuario activo para que no nos recomiende seguirnos a nosotros mismos
    active_user = User.objects.filter(username=request.user.username)  # obtenemos el usuario activo

    # lista final de sugerencias, comprobamos que no existe el usuario activo y creamos la lista de sugerencias
    suggestions_list_final = [x for x in list(suggestions_list) if (x not in list(active_user))]
    random.shuffle(suggestions_list_final)  # mezclamos la lista para ofrecer sugerencias 'aleatorias' al usuario

    username_profile = []  # lista con usuario/perfil
    username_profile_list = []  # lista usuarios/perfil

    for users in suggestions_list_final:  # por cada usuario listado de sugerencias
        username_profile.append(users.id)  # añadimos la id del usuario al perfil del usuario

    for ids in username_profile:  # por cada id obtenida de cada perfil de usuario
        profile_lists = Profile.objects.filter(id_user=ids)  # creamos la lista de perfiles con las ids de usuario del model Profile
        username_profile_list.append(profile_lists)  # añadimos todos los usuarios al listado de perfiles de usuario

    suggestions_username_profile_list = list(chain(*username_profile_list))  # combinamos la lista de perfiles de usuarios finales para visualizarlos como sugerencias al usuario activo

    posts = Post.objects.all()

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_lists, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})


@login_required(login_url='/signin')
def filters(request):  # sistema de filtrado de imágenes por género de las mismas
    post_filter = PostFilter(request.GET, queryset=Post.objects.all())  # obtenemos todas las imágenes en la database
    context = {
        'form': post_filter.form,
        'posts': post_filter.qs
    }

    return render(request, 'filter.html', context)


@login_required(login_url='/signin')
def upload(request):
    if request.method == 'POST':  # recibimos los datos del frontend de la imagen subida
        user = request.user.username  # usuario/autor
        image = request.FILES.get('image_upload')  # imagen subida
        caption = request.POST['caption']  # descripción/texto de la imagen

        new_post = Post.objects.create(user=user, image=image, caption=caption)  # creamos/guardamos el nuevo objeto con los datos en el model Post
        new_post.save()

        return redirect('/')

    else:
        return redirect('/')


@login_required(login_url='/signin')
def like_post(request):
    username = request.user.username  # obtenemos el username del usuario que da like a una publicación
    post_id = request.GET.get('post_id')  # obtenemos el id del post del feed

    post = Post.objects.get(id=post_id)  # obtenemos el id del post desde la database de los Posts

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()  # comprobamos si existe algún object en el post_id, username esto nos indicará si se ha dado o no un like.

    if like_filter is None:  # si en la database no existen ambas entries, es decir se ha dado like por primera vez a la publicación, crearemos la entrada del like en la database.
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()

        post.num_of_likes = post.num_of_likes + 1  # añadimos +1 like a la base de datos de los posts.
        post.save()
        return redirect('/')

    else:  # si ya existen los datos en la database, ya se dio like a la publicación, por lo que el usuario podrá quitar ese like si quiere
        like_filter.delete()  # eliminamos post_id y username de la db Post.
        post.num_of_likes = post.num_of_likes - 1
        post.save()
        return redirect('/')


@login_required(login_url='/signin')
def settings(request):  # panel de configuración del perfil del usuario activo en la app
    user_profile = Profile.objects.get(user=request.user)  # obtenemos los datos de la database del usuario actualmente conectado

    if request.method == 'POST':  # almacenamiento de los datos del usuario del frontend

        if request.FILES.get('image_prof') is None:  # si obtenemos todos los datos requeridos los almacenaremos en la database
            image_prof = user_profile.profile_img
            bio = request.POST['bio']
            location = request.POST['location']
            employment = request.POST['employment']
            specialization = request.POST['specialization']
            website = request.POST['website']

            user_profile.profile_img = image_prof
            user_profile.bio = bio
            user_profile.location = location
            user_profile.employment = employment
            user_profile.specialization = specialization
            user_profile.website = website

            user_profile.save()

        if request.FILES.get('image_bann') is None:  # misma funcionalidad pero utilizada para almacenar el banner del perfil de usuario
            image_bann = user_profile.banner_img
            user_profile.banner_img = image_bann

            user_profile.save()

        if request.FILES.get('image_prof') is not None:
            image_prof = request.FILES.get('image_prof')
            bio = request.POST['bio']
            location = request.POST['location']
            employment = request.POST['employment']
            specialization = request.POST['specialization']
            website = request.POST['website']

            user_profile.profile_img = image_prof
            user_profile.bio = bio
            user_profile.location = location
            user_profile.employment = employment
            user_profile.specialization = specialization
            user_profile.website = website

            user_profile.save()

        if request.FILES.get('image_bann') is not None:
            image_bann = request.FILES.get('image_bann')
            user_profile.banner_img = image_bann

            user_profile.save()

        messages.success(request, 'El perfil ha sido actualizado correctamente.')
        return redirect('setting')

    return render(request, 'setting.html', {'user_profile': user_profile})


def signup(request):  # registro del usuario en la database
    if request.method == 'POST':  # almacenamos los datos recibimos del frontend
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:  # comprobamos si ambas password coinciden
            if User.objects.filter(email=email).exists():  # seguimos el filtro, comprobamos si el email introducido ya existe en la database
                messages.info(request, 'Ya existe un usuario con ese correo electrónico.')  # informamos al usuario / añadimos funcionalidad en el frontend/html
                return redirect('signup')
            elif User.objects.filter(username=username).exists():  # comprobación de la existencia del username en la database
                messages.info(request, 'El nombre de usuario ya está en uso.')  # informamos al usuario / añadimos funcionalidad en el frontend/html
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)  # si es correcto procedemos a crear el usuario en la database
                user.save()  # guardamos la configuración del nuevo usuario

                # inicia sesión con el usuario creado - redirección a la profile.html para configurar los ajustes de su usuario
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # Crear Profile(model) object para almacenar al nuevo usuario en la database
                user_model = User.objects.get(username=username)  # obtenemos los datos del model users
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)  # creamos el user/user_id basado en la data del user_model creado
                new_profile.save()  # guardamos los datos en el model
                return redirect('/setting')

        else:
            messages.info(request, 'Las contraseñas no coinciden.')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':  # tomamos los datos del frontend que usaremos para iniciar sesión:
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)  # comprobamos los datos recibidos con la base de datos

        if user is not None:  # si se verifica la autentificación del usuario en la base de datos:
            auth.login(request, user)  # hacemos el login con los datos del usuario
            return redirect('/')  # redigirimos al usuario a la home/feed de la red social
        else:
            messages.info(request, 'Los datos introducidos son incorrectos.')  # avisamos al usuario sobre el error producido
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='/signin')
def profile(request, pk):  # datos y perfil de usuarios registrados
    user_object = User.objects.get(username=pk)  # obtenemos el pk del model User para acceder a ese perfil
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    num_of_posts = len(user_posts)  # número de publicaciones hechas por el usuario

    # sistema para obtener botón dinámico seguir/dejar de seguir según sea el caso
    # nota: el usuario no podrá seguirse a sí mismo, si ese fuera el caso, aparecerá un botón diferente para acceder a configurar su perfil
    follower = request.user.username  # obtenemos el seguidor
    user = pk  # el usuario seguido será el usuario buscado/perfil

    if Followers.objects.filter(follower=follower, user=user):
        follow_button = 'Dejar de seguir'
    else:
        follow_button = 'Seguir'

    # contador de seguidores/usuarios seguidos

    user_followers = len(Followers.objects.filter(user=pk))
    user_following = len(Followers.objects.filter(follower=pk))

    context = {  # creamos un dict para almacenar los datos
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'num_of_posts': num_of_posts,
        'follow_button': follow_button,
        'user_followers': user_followers,
        'user_following': user_following,

    }

    return render(request, 'profile.html', context)


@login_required(login_url='/signin')
def follow(request):  # sistema de seguimiento entre usuarios registrados en la app
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():  # si el usuario al que trata de seguir, ya lo está siguiendo, eliminará el seguimiento.
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('profile/' + user)  # regresa al usuario a la web del perfil del usuario que ha dejado de seguir
        else:  # si no existe el seguimiento en la db, se creará un entry en la db para iniciar el seguimiento al usuario.
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('profile/' + user)  # añadimos el pk con el nombre del usuario para acceder al perfil correcto

    else:
        return redirect('/')


@login_required(login_url='/signin')
def logout(request):  # desconexión del usuario activo en la app
    auth.logout(request)  # cerramos sesión con el usuario autenticado.
    return redirect('signin')


@login_required(login_url='/signin')
def search(request):  # sistema de búsqueda de usuarios por nombre
    user_object = User.objects.get(username=request.user.username)  # obtenemos el nombre de usuario del model User para las comprobaciones
    user_profile = Profile.objects.get(user=user_object)  # obtenemos el nombre de usuario del model Profile para las comprobaciones

    if request.method == 'POST':  # si el usuario en el frontend ha introducido datos, los almacenaremos
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)  # comprobamos si existe algún usuario en el model User que contenga alguna letra de las que han introducido

        username_profile = []  # lista para usuarios encontrados
        username_profile_list = []  # lista perfiles de usuarios encontrados

        for users in username_object:  # por cada usuario que contenga alguna letra y coincida con algún usuario de la database, agregaremos dicho usuario por id a la lista de usuario encontrado
            username_profile.append(users.id)

        for ids in username_profile:  # por cada id en el listado de usuarios encontrados, filtraremos usuarios por su id en el model Profile
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)  # agregamos el usuario filtrado al listado de perfiles encontrados

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
