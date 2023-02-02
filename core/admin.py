from django.contrib import admin
from .models import Profile, Post, LikePost, Followers

# Register your models here.
admin.site.register(Profile)  # registramos a la url de admin el model (Profile) de core
admin.site.register(Post)  # registramos el model para almacenar los posts del usuario
admin.site.register(LikePost)  # model para el sistema de likes
admin.site.register(Followers)  # model para el sistema de seguidores (seguir/dejar de seguir un usuario)
