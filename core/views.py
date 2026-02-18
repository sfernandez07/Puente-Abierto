from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Actividad, Participante, Inscripcion
from .forms import ActividadForm, InscripcionForm, ParticipanteForm
from django.db.models import Sum
import csv
from django.http import HttpResponse
import unicodedata


@login_required
def lista_actividades(request):
    actividades = Actividad.objects.all()
    return render(request, "core/lista_actividades.html", {
        "actividades": actividades
    })

@login_required
def crear_actividad(request):
    if request.method == "POST":
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_actividades")
    else:
        form = ActividadForm()

    return render(request, "core/form_actividad.html", {"form": form})

@login_required
def editar_actividad(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)

    if request.method == "POST":
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            return redirect("lista_actividades")
    else:
        form = ActividadForm(instance=actividad)

    return render(request, "core/form_actividad.html", {"form": form})

@login_required
def crear_inscripcion(request):
    if request.method == "POST":
        form = InscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_actividades")
    else:
        form = InscripcionForm()

    return render(request, "core/form_inscripcion.html", {"form": form})

@login_required
def participantes_por_actividad(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)
    inscripciones = actividad.inscripciones.all()

    return render(request, "core/participantes_actividad.html", {
        "actividad": actividad,
        "inscripciones": inscripciones,
    })

@login_required
def historial_participante(request, pk):
    participante = get_object_or_404(Participante, pk=pk)
    inscripciones = participante.inscripciones.all()

    return render(request, "core/historial_participante.html", {
        "participante": participante,
        "inscripciones": inscripciones,
    })

@login_required
def crear_participante(request):
    if request.method == "POST":
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_actividades")
    else:
        form = ParticipanteForm()

    return render(request, "core/form_participante.html", {
        "form": form
    })

@login_required
def resumen_general(request):
    actividades = Actividad.objects.all()

    total_ingresos = sum(a.ingresos_totales for a in actividades)

    return render(request, "core/resumen.html", {
        "actividades": actividades,
        "total_ingresos": total_ingresos,
    })

@login_required
def marcar_pago(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    inscripcion.pagado = True
    inscripcion.save()
    return redirect("participantes_actividad", pk=inscripcion.actividad.pk)

@login_required
def eliminar_actividad(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)

    if request.method == "POST":
        actividad.delete()
        return redirect("lista_actividades")

    return render(request, "core/confirmar_eliminacion.html", {
        "actividad": actividad
    })

def quitar_acentos(texto):
    """
    Convierte texto Unicode con acentos a ASCII simple.
    Ejemplo: Fernández -> Fernandez
    """
    if not texto:
        return ""

    texto_normalizado = unicodedata.normalize("NFKD", str(texto))
    texto_sin_acentos = texto_normalizado.encode("ascii", "ignore").decode("utf-8")
    return texto_sin_acentos

@login_required
def exportar_participantes(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)
    inscripciones = actividad.inscripciones.select_related("participante")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="participantes_{actividad.pk}.csv"'
    )

    writer = csv.writer(response)

    # Cabecera sin acentos
    writer.writerow([
        "Nombre",
        "Apellidos",
        "Email",
        "Telefono",
        "Fecha inscripcion",
        "Pagado"
    ])

    for inscripcion in inscripciones:
        writer.writerow([
            quitar_acentos(inscripcion.participante.nombre),
            quitar_acentos(inscripcion.participante.apellidos),
            quitar_acentos(inscripcion.participante.email),
            quitar_acentos(inscripcion.participante.telefono),
            quitar_acentos(inscripcion.fecha_inscripcion),
            "Si" if inscripcion.pagado else "No"
        ])

    return response


@login_required
def crear_inscripcion_actividad(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)

    if request.method == "POST":
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.actividad = actividad
            inscripcion.save()
            return redirect("participantes_actividad", pk=actividad.pk)
    else:
        form = InscripcionForm()

    return render(request, "core/form_inscripcion.html", {
        "form": form,
        "actividad": actividad
    })
