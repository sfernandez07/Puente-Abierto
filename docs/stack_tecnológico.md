# Stack Tecnológico Recomendado  
Proyecto: Sistema de Gestión – Asociación Cultural “Puente Abierto"

## Backend y Aplicación Web
**Django 5 (Python 3.12)**

### ¿Por qué Django?
- Incluye sistema de autenticación integrado.
- Permite crear formularios y listados rápidamente.
- Genera panel administrativo automático.
- Incluye protección de seguridad básica.
- Ideal para sistemas internos de gestión.

---

## Base de Datos
**PostgreSQL**

### ¿Por qué PostgreSQL?
- Maneja bien relaciones entre actividades, participantes e inscripciones.
- Permite generar reportes fácilmente.
- Es estable y ampliamente soportado.

> Alternativa rápida para desarrollo inicial: SQLite (incluida por defecto en Django).  
> Luego puede migrarse a PostgreSQL sin reescribir la aplicación.

---

## ORM
**Django ORM (incluido)**

Permite:
- Definir modelos como Actividad, Participante, Inscripción y Pago.
- Consultar datos sin escribir SQL manual.
- Reducir errores y mejorar mantenibilidad.

---

## Frontend
**Django Templates + HTML + Bootstrap**

### ¿Por qué esta opción?
- No requiere framework frontend separado.
- Permite desarrollar vistas funcionales rápidamente.
- Bootstrap mejora apariencia sin mucho esfuerzo.
- Reduce complejidad técnica.

---

## Autenticación
**Sistema integrado de Django**

Permite:
- Control de acceso por usuario.
- Gestión de sesiones.
- Protección de datos internos.

Solo el equipo administrativo tendrá acceso.

---

## Despliegue
Opciones recomendadas:

- **Render**
- **Railway**
- **Servidor VPS básico**
- **PythonAnywhere**

Criterios:
- Bajo costo
- Configuración simple
- Soporte para PostgreSQL

---

## Control de Versiones
- **Git**
- Repositorio en GitHub o GitLab

Permite:
- Control de cambios
- Respaldo del código
- Posible ampliación futura

---

# 🏗 Arquitectura Simplificada

- Aplicación monolítica
- Sin microservicios
- Sin frontend separado
- Sin APIs complejas innecesarias

---

# 📦 Resumen del Stack

| Capa | Tecnología |
|------|------------|
| Lenguaje | Python 3.12 |
| Framework | Django 5 |
| Base de Datos | PostgreSQL |
| ORM | Django ORM |
| Frontend | Django Templates + Bootstrap |
| Autenticación | Sistema integrado Django |
| Hosting | PythonAnywhere |
| Versionado | Git |
