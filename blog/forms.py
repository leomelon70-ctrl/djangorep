from django import forms
from .models import Publicacion
from .models import Comentario
class FormPublicacion(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ('titulo', 'texto',)


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('texto',)
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'texto': 'Escribe tu comentario'
        }