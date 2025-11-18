from django.conf import settings
from django.db import models
from django.utils import timezone


class Publicacion(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    hora_creacion = models.DateTimeField(blank=True, null=True)

    def publicar(self):
         self.fecha_publicacion = timezone.now()
         self.save()

    def __str__(self):
         return self.titulo
class equipo(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    historia = models.TextField()
    titulos = models.IntegerField()
    copas= models.IntegerField()
    pais = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)


class Comentario(models.Model):
    # permitir null temporalmente para evitar prompts durante migraciones
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name="comentarios",
        null=True,
        blank=True,
    )
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        pub = self.publicacion.titulo if self.publicacion else "sin publicacion"
        return f"Comentario de {self.autor} en {pub}"

# Create your models here.
