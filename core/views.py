from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Actividad, Participante, Inscripcion
from .forms import ActividadForm, InscripcionForm


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

from django.db.models import Sum


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
