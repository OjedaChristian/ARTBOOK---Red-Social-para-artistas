from django.db import models
from django.contrib.auth import get_user_model  # user_model
import uuid  # ids únicas para identificar cada blog-post
from django.utils import timezone

User = get_user_model()


# Create your models here.

class Profile(models.Model):  # model para los perfiles de usuario y su configuración del perfil posterior.
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # nombre de usuario a través del built-in model User para obtener los usuarios de la sesión
    id_user = models.IntegerField()  # id del usuario
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')  # imagen de perfil subida por el usuario, almacenada en media/profile_images
    banner_img = models.ImageField(upload_to='banner_images', default='blog-detailfull.jpg')
    location = models.CharField(max_length=50, blank=True)  # localización/país del usuario
    specialization = models.CharField(max_length=50, blank=True)  # especialización del usuario
    employment = models.CharField(max_length=50, blank=True)  # empleo actual o compañia para la que trabaja
    bio = models.TextField(blank=True)  # biografía
    website = models.CharField(max_length=50, blank=True)
    email = models.EmailField()  # email de contacto

    def __str__(self):
        return self.user.username  # nombre del user_model que se visualizará en el admin panel


class Post(models.Model):  # model para cada imagen subida a la app
    class GenreChoices(models.TextChoices):  # tipos de género de arte clasificados de la imagen subida
        Fantasy = 'Fantasy'
        Ilustración = 'Ilustración'
        Conceptual = 'Conceptual'
        Paisajes = 'Paisajes'
        Diseño = 'Diseño'
        Retratos = 'Retratos'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=50)  # usuario que sube la imagen
    image = models.ImageField(upload_to='post_images')  # imagen subida
    caption = models.TextField()  # descripción/texto de la imagen
    genre = models.CharField(max_length=11, choices=GenreChoices.choices, default='General')  # género al que pertenece la imagen, esto se utilizará para clasificarlas posteriormente
    created_at = models.DateTimeField(default=timezone.now)  # fecha de subida de la imagen
    num_of_likes = models.IntegerField(default=0)  # likes que ha recibido de otros usuarios

    def __str__(self):
        return self.user


class LikePost(models.Model):  # model para el sistema de likes
    post_id = models.CharField(max_length=500)  # id de la imagen a la que se le ha dado like
    username = models.CharField(max_length=50)  # usuario que ha dado like a la imagen (post_id)

    def __str__(self):
        return self.username


class Followers(models.Model):  # model para el sistema de seguimiento entre usuarios
    follower = models.CharField(max_length=50)  # seguidor
    user = models.CharField(max_length=50)  # usuario que recibe los seguidores

    def __str__(self):
        return self.user
