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

    class Meta:
        model = Inscripcion
        fields = ["participante"]



class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ["nombre", "apellidos", "email", "telefono"]
