import django_filters
from core.models import Post


class PostFilter(django_filters.FilterSet):  # class para el filtrado de imagen
    class Meta:
        model = Post  # nos basamos en el .model Post, que serán las imágenes subidas
        fields = {
            'user': ['istartswith'],  # campo para búsqueda por 'letra' por la que empiece un usuario en la base de datos
            'genre': ['exact'],  # campo para seleccionar el género de la ilustración (retratos, entornos, ilustración, etc...)
        }
