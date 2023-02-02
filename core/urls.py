from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # home/index de la app
    path('signup', views.signup, name='signup'),  # /signup url para el registro de usuarios en la app
    path('signin', views.signin, name='signin'),  # /signin url para el inicio de sesión en la app
    path('logout', views.logout, name='logout'),  # /logout url para desconectarse del usuario activo en la app
    path('profile/<str:pk>', views.profile, name='profile'),  # /profile/</str:pk> url para el acceso a los perfiles existentes en la app, cada perfil tendrá como pk su username
    path('setting', views.settings, name='setting'),  # /setting url para acceder a la configuración del perfil del usuario activo en la app
    path('upload', views.upload, name='upload'),  # sistema de subida de imágenes/archivos a la app
    path('like_post', views.like_post, name='like_post'),  # sistema de like a imágenes subidas a la app
    path('follow', views.follow, name='follow'),  # sistema de seguimiento entre usuarios registrados en la app
    path('search', views.search, name='search'),  # sistema de búsqueda por usuarios
    path('filter', views.filters, name='filter'),  # sistema de búsqueda de imágenes en la app basado en género/autor de la imagen
]
