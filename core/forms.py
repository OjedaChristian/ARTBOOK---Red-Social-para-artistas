from django import forms


class PostGenreFilterForm(forms.Form):  # class para el filtro de imágenes
    genre = forms.CharField()
