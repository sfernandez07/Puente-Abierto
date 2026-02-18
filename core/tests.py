from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.models import User
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


# =====================================================
# TESTS DE VISTAS (FUNCIONALES)
# =====================================================

class VistasTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.actividad = Actividad.objects.create(
            nombre="Curso Django",
            descripcion="Curso completo",
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=5),
            precio=Decimal("100.00"),
            plazas_maximas=5,
        )

        self.participante = Participante.objects.create(
            nombre="Elena",
            apellidos="Martínez",
            email="elena@example.com",
            telefono="123456789"
        )

    # -------------------------
    # Autenticación requerida
    # -------------------------

    def test_lista_actividades_requiere_login(self):
        response = self.client.get(reverse("lista_actividades"))
        self.assertEqual(response.status_code, 302)

    # -------------------------
    # Flujo autenticado
    # -------------------------

    def test_crear_actividad(self):
        self.client.login(username="admin", password="1234")

        response = self.client.post(reverse("crear_actividad"), {
            "nombre": "Nueva Actividad",
            "descripcion": "Descripción",
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() + timedelta(days=2),
            "precio": "40.00",
            "plazas_maximas": 10,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Actividad.objects.count(), 2)

    def test_crear_participante(self):
        self.client.login(username="admin", password="1234")

        response = self.client.post(reverse("crear_participante"), {
            "nombre": "Carlos",
            "apellidos": "López",
            "email": "carlos@test.com",
            "telefono": "999999999"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Participante.objects.count(), 2)

    def test_crear_inscripcion_actividad(self):
        self.client.login(username="admin", password="1234")

        response = self.client.post(
            reverse("crear_inscripcion_actividad", args=[self.actividad.pk]),
            {"participante": self.participante.pk}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.actividad.inscripciones.count(), 1)

    def test_marcar_pago(self):
        self.client.login(username="admin", password="1234")

        inscripcion = Inscripcion.objects.create(
            actividad=self.actividad,
            participante=self.participante,
        )

        self.client.get(reverse("marcar_pago", args=[inscripcion.pk]))

        inscripcion.refresh_from_db()
        self.assertTrue(inscripcion.pagado)

    def test_eliminar_actividad(self):
        self.client.login(username="admin", password="1234")

        response = self.client.post(
            reverse("eliminar_actividad", args=[self.actividad.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Actividad.objects.filter(pk=self.actividad.pk).exists()
        )

    def test_exportar_csv(self):
        self.client.login(username="admin", password="1234")

        Inscripcion.objects.create(
            actividad=self.actividad,
            participante=self.participante,
            pagado=True
        )

        response = self.client.get(
            reverse("exportar_participantes", args=[self.actividad.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment;", response["Content-Disposition"])

    def test_resumen_general(self):
        self.client.login(username="admin", password="1234")

        Inscripcion.objects.create(
            actividad=self.actividad,
            participante=self.participante,
            pagado=True
        )

        response = self.client.get(reverse("resumen_general"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "100.00")

    def test_historial_participante(self):
        self.client.login(username="admin", password="1234")

        Inscripcion.objects.create(
            actividad=self.actividad,
            participante=self.participante,
            pagado=True
        )

        response = self.client.get(
            reverse("historial_participante", args=[self.participante.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Curso Django")
