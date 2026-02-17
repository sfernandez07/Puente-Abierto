from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_actividades, name="lista_actividades"),
    path("actividad/nueva/", views.crear_actividad, name="crear_actividad"),
    path("actividad/<int:pk>/editar/", views.editar_actividad, name="editar_actividad"),
    path("inscripcion/nueva/", views.crear_inscripcion, name="crear_inscripcion"),
    path("actividad/<int:pk>/participantes/", views.participantes_por_actividad, name="participantes_actividad"),
    path("participante/<int:pk>/historial/", views.historial_participante, name="historial_participante"),
    path("resumen/", views.resumen_general, name="resumen_general"),
    path("inscripcion/<int:pk>/pago/", views.marcar_pago, name="marcar_pago"),
]
