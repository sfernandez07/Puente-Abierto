from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Actividad(models.Model):
    """
    Representa una actividad formativa o evento organizado por la asociación.
    """

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    plazas_maximas = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_inicio"]
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"

    def __str__(self):
        return f"{self.nombre} ({self.fecha_inicio})"

    @property
    def total_inscripciones(self):
        return self.inscripciones.count()

    @property
    def plazas_disponibles(self):
        return self.plazas_maximas - self.total_inscripciones

    @property
    def ingresos_totales(self):
        return sum(
            inscripcion.actividad.precio
            for inscripcion in self.inscripciones.filter(pagado=True)
        )

    def clean(self):
        """
        Validaciones de negocio:
        - La fecha fin no puede ser anterior a la fecha inicio.
        """
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError(
                "La fecha de fin no puede ser anterior a la fecha de inicio."
            )


class Participante(models.Model):
    """
    Representa una persona que puede inscribirse en actividades.
    """

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["apellidos", "nombre"]
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                name="unique_participante_email"
            )
        ]

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Inscripcion(models.Model):
    """
    Relaciona un Participante con una Actividad.
    Controla pago y evita sobrecupos.
    """

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name="inscripciones"
    )

    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name="inscripciones"
    )

    fecha_inscripcion = models.DateTimeField(default=timezone.now)
    pagado = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha_inscripcion"]
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        constraints = [
            models.UniqueConstraint(
                fields=["actividad", "participante"],
                name="unique_inscripcion_actividad_participante"
            )
        ]

    def __str__(self):
        return f"{self.participante} → {self.actividad}"

    def clean(self):
    # Asegurarnos de que existe actividad antes de validar
        if not self.actividad_id:
            return

        # Solo validar si es nueva inscripción
        if not self.pk:
            if self.actividad.plazas_disponibles <= 0:
                raise ValidationError(
                    "No hay plazas disponibles para esta actividad."
                )


    def save(self, *args, **kwargs):
        """
        Sobrescribimos save para asegurar que clean() se ejecute siempre,
        incluso si se crea desde el admin o desde código.
        """
        self.full_clean()
        super().save(*args, **kwargs)
