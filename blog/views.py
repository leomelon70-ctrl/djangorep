# ...existing code...
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Publicacion, equipo, Comentario
from .forms import FormPublicacion, ComentarioForm


def lista_public(request):
    publicaciones = list(Publicacion.objects.all().order_by('-fecha_creacion'))
    usuarios = User.objects.all()
    usuarioActivo = request.user if request.user.is_authenticated else None

    # preparar formulario de comentario (por si viene POST inválido)
    form_coment = ComentarioForm()

    # Si llega un comentario desde el formulario (POST a esta vista)
    if request.method == 'POST':
        form_coment = ComentarioForm(request.POST)
        if form_coment.is_valid() and request.user.is_authenticated:
            comentario = form_coment.save(commit=False)
            comentario.autor = request.user
            comentario.fecha_creacion = timezone.now()
            # obtener y validar publicacion_id
            try:
                pub_id = int(request.POST.get('publicacion_id') or 0)
                comentario.publicacion = get_object_or_404(Publicacion, pk=pub_id)
                comentario.save()
                return redirect('lista_public')  # evitar doble envío
            except (ValueError, TypeError):
                # dejar el form con errores para mostrar en plantilla
                form_coment.add_error(None, "ID de publicación inválido.")
        # si no está autenticado o form inválido, caemos al render mostrando errores

    # Agrupar comentarios por publicación
    pub_ids = [p.id for p in publicaciones]
    comentarios_qs = Comentario.objects.filter(publicacion_id__in=pub_ids).order_by('fecha_creacion')
    comentarios_por_pub = {}
    for c in comentarios_qs:
        comentarios_por_pub.setdefault(c.publicacion_id, []).append(c)

    for pub in publicaciones:
        pub.comentarios_list = comentarios_por_pub.get(pub.id, [])

    form_public = FormPublicacion()

    return render(request, 'blog/lista_public.html', {
        'publicaciones': publicaciones,
        'usuarios': usuarios,
        'usuario_activo': usuarioActivo,   # compatibilidad con plantillas que usan este nombre
        'usuarioActivo': usuarioActivo,    # también pasar con el otro nombre si lo usas
        'form_public': form_public,
        'form_coment': form_coment,
    })
def evaluacion2(request):
    # el modelo equipo no tiene campo de fecha_publicacion; listar por id
    equipos = equipo.objects.all().order_by('-id')
    usr_id = request.GET.get('usuario')
    usuarios = User.objects.all()

    if usr_id:
        try:
            equipos = equipos.filter(autor__id=int(usr_id))
            usuario_activo = int(usr_id)
        except (ValueError, TypeError):
            usuario_activo = None
    else:
        usuario_activo = None

    return render(request, 'blog/lista_equipos.html', {
        'equi': equipos,
        'usuarios': usuarios,
        'usuario_activo': usuario_activo,
    })

def nueva_public(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('admin:login')
        form = FormPublicacion(request.POST)
        if form.is_valid():
            pub = form.save(commit=False)
            pub.autor = request.user
            pub.fecha_creacion = timezone.now()
            pub.save()
            return redirect('lista_public')
    else:
        form = FormPublicacion()
    return render(request, 'blog/editar_public.html', {'form': form})

def editar_public(request, pk):
    pub = get_object_or_404(Publicacion, pk=pk)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('admin:login')
        form = FormPublicacion(request.POST, instance=pub)
        if form.is_valid():
            pub = form.save(commit=False)
            pub.autor = request.user
            pub.fecha_creacion = timezone.now()
            pub.save()
            return redirect('lista_public')
    else:
        form = FormPublicacion(instance=pub)
    return render(request, 'blog/editar_public.html', {'form': form})

def detalle_public(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    comentarios = Comentario.objects.filter(publicacion=publicacion).order_by('-fecha_creacion')

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('admin:login')
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.publicacion = publicacion
            comentario.fecha_creacion = timezone.now()
            comentario.save()
            # cuando el formulario se envía desde lista_public queremos volver a la lista
            return redirect('lista_public')
    else:
        form = ComentarioForm()

    return render(request, 'blog/detalle_public.html', {
        'publicacion': publicacion,
        'comentarios': comentarios,
        'form': form
    })
# ...existing code...