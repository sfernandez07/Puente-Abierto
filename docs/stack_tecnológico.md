# Stack Tecnológico  
Proyecto: Sistema de Gestión – Asociación Cultural “Puente Abierto”

---

## 1. Lenguaje de Programación

**Python 3.12.7**

### Justificación

- Sintaxis clara y mantenible.
- Alta productividad (crítico en proyecto de 2 días).
- Excelente integración con Django.
- Bajo coste de mantenimiento futuro.
- Adecuado para aplicaciones administrativas internas.

---

## 2. Framework Backend

**Django 6.0.2**

Dependencias:

- asgiref==3.11.1  
- sqlparse==0.5.5  
- tzdata==2025.3  

### Justificación

- Framework robusto y maduro.
- ORM integrado.
- Sistema de autenticación incorporado.
- Protección CSRF por defecto.
- Permite estructurar el proyecto de forma profesional sin sobreingeniería.
- Ideal para aplicaciones internas con bajo presupuesto.

---

## 3. Arquitectura de la Aplicación

### Tipo de arquitectura

- Aplicación web monolítica.
- Patrón **MVT (Model – View – Template)**.
- Backend y frontend integrados en Django.
- Sin microservicios.
- Sin API pública.
- Sin frontend desacoplado.

### Estructura real del proyecto

```
config/
    settings.py
    urls.py
    asgi.py
    wsgi.py

core/
    models.py
    views.py
    admin.py
    tests.py
    migrations/

docs/
    historias_de_usuario.md
    stack_tecnológico.md
```

La lógica de negocio se implementará principalmente en:

- `core/models.py`
- `core/views.py`
- Formularios basados en `ModelForm`

---

## 4. Base de Datos

**SQLite (motor por defecto de Django)**

### Justificación técnica

- No requiere servidor adicional.
- Configuración mínima.
- Ideal para bajo volumen de concurrencia.
- Reduce complejidad y tiempos de despliegue.
- Compatible con PythonAnywhere.

### Adecuación al contexto

- ~120 actividades/año.
- 3 usuarios administrativos.
- Aplicación interna.
- Baja carga transaccional.
- Proyecto con limitación de tiempo (2 días).

Permite migración futura a PostgreSQL sin modificar los modelos gracias al ORM.

---

## 5. ORM

**Django ORM**

Permite:

- Definir modelos como:
  - `Actividad`
  - `Participante`
  - `Inscripcion`
- Establecer relaciones con `ForeignKey`.
- Definir restricciones (`UniqueConstraint`).
- Implementar validaciones en `clean()`.
- Controlar sobrecupos desde la lógica de modelo.
- Generar consultas agregadas para resúmenes económicos.

El ORM será la base para garantizar:

- Centralización de información (HU-14).
- Control de plazas disponibles (HU-04).
- Trazabilidad de pagos (HU-09, HU-10).
- Resumen general (HU-13).

---

## 6. Interfaz de Usuario

### ✅ Vistas Personalizadas (Interfaz Principal)

La interfaz principal del sistema se implementará mediante:

- Vistas en `core/views.py`
- Plantillas HTML en `core/templates/`
- Formularios Django (`ModelForm`)

Se desarrollarán vistas específicas para cubrir las historias de usuario:

- Crear actividad (HU-01)
- Editar actividad (HU-02)
- Listado de actividades (HU-03)
- Visualización automática de plazas disponibles (HU-04)
- Registro de inscripción (HU-05)
- Validación automática de cupo (HU-06)
- Lista de participantes por actividad (HU-07)
- Historial de participante (HU-08)
- Registro de pago (HU-09)
- Estado de pagos (HU-10)
- Exportación de listados (HU-12)
- Resumen general económico y de participación (HU-13)

## 7. Formularios

**Django Forms / ModelForms**

Permiten:

- Validación automática.
- Gestión de errores de forma clara.
- Integración directa con modelos.
- Implementación de reglas de negocio.
- Prevención de sobrecupos (HU-06).

Son esenciales para garantizar calidad de datos y reducción de errores administrativos.

---

## 8. Autenticación y Seguridad

Sistema integrado de autenticación de Django.

Incluye:

- Gestión de usuarios.
- Decorador `@login_required`.
- Protección CSRF.
- Gestión de sesiones.
- Control de acceso a vistas.

Solo el equipo administrativo tendrá acceso al sistema.

---

## 9. Despliegue

**Entorno previsto: PythonAnywhere**

### Justificación

- Bajo coste.
- Configuración sencilla.
- Compatible con Django + SQLite.
- No requiere infraestructura propia.
- Adecuado para organización sin ánimo de lucro.

---

## 10. Control de Versiones

- Git
- Repositorio en GitHub o GitLab

Permite:

- Trazabilidad de cambios.
- Historial de versiones.
- Control profesional del desarrollo.
- Buenas prácticas incluso en proyecto individual.

---

# 🏗 Arquitectura General Actualizada

- Aplicación monolítica.
- Backend y frontend integrados en Django.
- Vistas personalizadas como interfaz principal.
- Base de datos SQLite embebida.
- Autenticación integrada.
- Optimizado para desarrollo en 2 días por un único desarrollador.

---

# 📦 Resumen del Stack

| Capa | Tecnología |
|------|------------|
| Lenguaje | Python 3.12.7 |
| Framework | Django 6.0.2 |
| Base de Datos | SQLite |
| ORM | Django ORM |
| Interfaz principal | Django Templates + Vistas personalizadas |
| Formularios | Django Forms / ModelForms |
| Autenticación | Sistema integrado Django |
| Hosting | PythonAnywhere |
| Versionado | Git |

---