from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from decimal import Decimal
from datetime import date, timedelta

from .models import Actividad, Participante, Inscripcion


# =====================================================
# TESTS MODELO ACTIVIDAD
# =====================================================

class ActividadModelTest(TestCase):

    def setUp(self):
        self.actividad = Actividad.objects.create(
            nombre="Taller de Pintura",
            descripcion="Curso intensivo",
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=1),
            precio=Decimal("50.00"),
            plazas_maximas=10,
        )

    def test_fecha_fin_no_puede_ser_anterior_a_inicio(self):
        actividad = Actividad(
            nombre="Actividad inválida",
            fecha_inicio=date.today(),
            fecha_fin=date.today() - timedelta(days=1),
            precio=Decimal("20.00"),
            plazas_maximas=5,
        )

        with self.assertRaises(ValidationError):
            actividad.full_clean()

    def test_plazas_disponibles_inicialmente_correctas(self):
        self.assertEqual(self.actividad.plazas_disponibles, 10)

    def test_calculo_plazas_disponibles(self):
        participante = Participante.objects.create(
            nombre="Juan",
            apellidos="Pérez",
            email="juan@example.com",
        )

        Inscripcion.objects.create(
            actividad=self.actividad,
            participante=participante,
        )

        self.assertEqual(self.actividad.plazas_disponibles, 9)

    def test_ingresos_totales_solo_pagados(self):
        p1 = Participante.objects.create(
            nombre="Ana",
            apellidos="López",
            email="ana@example.com",
        )
        p2 = Participante.objects.create(
            nombre="Carlos",
            apellidos="Ruiz",
            email="carlos@example.com",
        )

        Inscripcion.objects.create(
            actividad=self.actividad,
            participante=p1,
            pagado=True,
        )

        Inscripcion.objects.create(
            actividad=self.actividad,
            participante=p2,
            pagado=False,
        )

        self.assertEqual(
            self.actividad.ingresos_totales,
            Decimal("50.00")
        )


# =====================================================
# TESTS MODELO PARTICIPANTE
# =====================================================

class ParticipanteModelTest(TestCase):

    def test_email_debe_ser_unico(self):
        Participante.objects.create(
            nombre="Laura",
            apellidos="García",
            email="laura@example.com",
        )

        with self.assertRaises(IntegrityError):
            Participante.objects.create(
                nombre="Laura2",
                apellidos="García2",
                email="laura@example.com",
            )


# =====================================================
# TESTS MODELO INSCRIPCION
# =====================================================

class InscripcionModelTest(TestCase):

    def setUp(self):
        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            descripcion="Clase semanal",
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=30),
            precio=Decimal("30.00"),
            plazas_maximas=1,
        )

        self.participante1 = Participante.objects.create(
            nombre="Mario",
            apellidos="Santos",
            email="mario@example.com",
        )

        self.participante2 = Participante.objects.create(
            nombre="Lucía",
            apellidos="Fernández",
            email="lucia@example.com",
        )

    def test_no_permitir_sobrecupo(self):
        Inscripcion.objects.create(
            actividad=self.actividad,
            participante=self.participante1,
        )

        with self.assertRaises(ValidationError):
            Inscripcion.objects.create(
                actividad=self.actividad,
                participante=self.participante2,
            )

    def test_no_permitir_inscripcion_duplicada(self):
    # Creamos actividad con más de una plaza
        actividad = Actividad.objects.create(
            nombre="Pilates",
            descripcion="Clase duplicada",
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=10),
            precio=Decimal("20.00"),
            plazas_maximas=5,
        )

        Inscripcion.objects.create(
            actividad=actividad,
            participante=self.participante1,
        )

        with self.assertRaises(ValidationError):
            Inscripcion.objects.create(
                actividad=actividad,
                participante=self.participante1,
            )


    def test_registro_pago_correcto(self):
        inscripcion = Inscripcion.objects.create(
            actividad=self.actividad,
            participante=self.participante1,
            pagado=True,
        )

        self.assertTrue(inscripcion.pagado)
