from django import forms
from .models import Actividad, Inscripcion, Participante
from django.utils import timezone



class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = [
            "nombre",
            "descripcion",
            "fecha_inicio",
            "fecha_fin",
            "precio",
            "plazas_maximas",
        ]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }

class InscripcionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Mostrar solo actividades que no hayan finalizado
        self.fields["actividad"].queryset = Actividad.objects.filter(
            fecha_fin__gte=timezone.now().date()
        )

    class Meta:
        model = Inscripcion
        fields = ["actividad", "participante"]


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ["nombre", "apellidos", "email", "telefono"]
