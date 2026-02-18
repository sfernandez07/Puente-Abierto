# 📘 Documento de Diseño Técnico y Propuesta Tecnológica  
## Proyecto: Sistema de Gestión – Asociación Cultural “Puente Abierto”

**Duración estimada:** 2 días  
**Modalidad:** Desarrollo individual  
**Arquitectura:** Monolítica MVT (Django)

---

# 1. Objetivo del Documento

Definir:

- Arquitectura técnica del sistema  
- Modelo de datos  
- Diseño funcional  
- Diseño de seguridad  
- Estrategia de validación  
- Consideraciones de rendimiento  
- Justificación tecnológica  
- Plan de implementación en 2 días  

Este documento responde al **“cómo” técnico** que materializa las historias de usuario definidas.

---

# 2. Contexto del Problema (Resumen Ejecutivo)

La asociación actualmente:

- Gestiona inscripciones manualmente.
- Usa múltiples hojas de cálculo no centralizadas.
- Tiene errores por sobrecupos.
- No dispone de trazabilidad económica consolidada.
- Presenta ineficiencia administrativa.

El sistema propuesto debe:

✅ Centralizar información  
✅ Automatizar control de plazas  
✅ Evitar duplicidades  
✅ Gestionar pagos  
✅ Generar resúmenes económicos  
✅ Ser simple y usable  
✅ Implementarse sin interrumpir actividades  

**Restricciones:**

- Presupuesto limitado.  
- Sin equipo técnico interno.  
- Desarrollo en 2 días.  
- Bajo volumen de concurrencia.  

---

# 3. Arquitectura Técnica

## 3.1 Tipo de Arquitectura

Aplicación web **monolítica** basada en patrón **MVT (Model–View–Template)**.

### Justificación

Para un proyecto:

- De bajo presupuesto  
- Con un único desarrollador  
- Con bajo volumen transaccional  
- Sin necesidad de API pública  

Una arquitectura monolítica:

- Reduce complejidad  
- Reduce tiempo de implementación  
- Minimiza riesgos  
- Es más mantenible en entornos pequeños  

---

## 3.2 Diagrama Conceptual de Capas

```text
Usuario (Equipo Administrativo)
        ↓
Django Views (Controladores)
        ↓
Django ORM (Lógica de negocio en modelos)
        ↓
SQLite Database
```text

### Separación de responsabilidades

| Capa | Responsabilidad |
|------|-----------------|
| Model | Reglas de negocio, validaciones, integridad |
| View | Flujo de usuario y control |
| Template | Interfaz y presentación |
| ORM | Persistencia |
| Forms | Validación de entrada |

---

# 4. Modelo de Datos (Diseño Entidad-Relación)

## 4.1 Entidades Principales

### 1️⃣ Actividad

Representa un taller o evento.

**Campos clave:**

- `nombre`
- `descripcion`
- `fecha_inicio`
- `fecha_fin`
- `precio`
- `plazas_maximas`

**Propiedades calculadas:**

- `total_inscripciones`
- `plazas_disponibles`
- `ingresos_totales`

---

### 2️⃣ Participante

Representa una persona.

**Campos:**

- `nombre`
- `apellidos`
- `email` (único)
- `telefono`

**Restricción:**

```python
UniqueConstraint(email)
```text

---

### 3️⃣ Inscripcion

Relaciona Participante y Actividad.

**Campos:**

- `actividad` (FK)
- `participante` (FK)
- `fecha_inscripcion`
- `pagado` (boolean)

**Restricciones:**

```python
UniqueConstraint(actividad, participante)
```text

**Validaciones:**

- No permitir sobrecupo.
- No permitir inscripción duplicada.

---

## 4.2 Relaciones

```text
Actividad 1 --- N Inscripcion N --- 1 Participante
```text

---

# 5. Lógica de Negocio Crítica

La lógica principal está en los **modelos**, no en las vistas.

## 5.1 Control de Sobrecupo

Implementado en:

```python
Inscripcion.clean()
```text

### ¿Por qué en el modelo?

- Garantiza integridad independientemente del punto de entrada.
- Evita dependencia de formularios.
- Cumple principio de encapsulamiento.

---

## 5.2 Cálculo de Ingresos

```python
@property
def ingresos_totales(self):
```text

**Beneficio:**

- Evita almacenar datos redundantes.
- Reduce riesgo de inconsistencias.
- Siempre refleja estado real.

---

# 6. Diseño de Seguridad

## 6.1 Autenticación

- Sistema de autenticación integrado de Django.
- `@login_required` en todas las vistas críticas.
- Protección CSRF por defecto.
- Gestión de sesiones segura.

---

## 6.2 Control de Acceso

Solo usuarios autenticados pueden:

- Crear actividades
- Inscribir participantes
- Marcar pagos
- Exportar datos
- Ver resúmenes

---

## 6.3 Protección de Datos

Consideraciones:

- No hay datos financieros sensibles.
- Se almacenan emails y teléfonos.
- Base de datos local (SQLite).
- Sin exposición pública API.

**Riesgo:** Bajo–moderado.

---

# 7. Diseño de Interfaz

**Principios:**

- Simplicidad  
- Claridad visual  
- Acciones evidentes  
- Minimizar clics  

**Características:**

- Navegación superior fija.
- Tablas claras.
- Indicadores visuales ✅ ❌.
- Confirmación de eliminación.
- Feedback de errores en formularios.

---

# 8. Exportación CSV

## Objetivo

- Permitir compartir datos.
- Facilitar informes externos.
- Compatibilidad con Excel.

## Implementación

```python
HttpResponse(content_type="text/csv")
```text

Se contempla eliminación de acentos para compatibilidad.

**Riesgo mitigado:** Problemas de codificación.

---

# 9. Rendimiento y Escalabilidad

## 9.1 Volumen estimado

- ~120 actividades/año
- 3 usuarios administrativos
- Bajo volumen concurrente

SQLite es suficiente.

---

## 9.2 Consultas optimizadas

Uso de:

```python
select_related("participante")
```text

Para evitar **N+1 queries** en exportación.

---

# 10. Calidad y Testing

### Tests incluidos

✅ Validaciones de modelo  
✅ Sobrecupo  
✅ Duplicidad  
✅ Pagos  
✅ Autenticación requerida  
✅ Flujo completo  
✅ Exportación CSV  
✅ Resumen económico  

Cobertura funcional adecuada para alcance del proyecto.

---

# 11. Propuesta Tecnológica

## 11.1 Stack Seleccionado

| Capa | Tecnología |
|------|------------|
| Lenguaje | Python 3.12.7 |
| Framework | Django 6.0.2 |
| Base de Datos | SQLite |
| ORM | Django ORM |
| Frontend | Django Templates |
| Autenticación | Sistema Django |
| Hosting | PythonAnywhere |
| Versionado | Git |

---

## 11.2 Justificación Estratégica

### ¿Por qué Django?

- Framework maduro.
- ORM robusto.
- Seguridad incorporada.
- Ideal para backoffice.
- Desarrollo rápido (crítico en 2 días).

### ¿Por qué SQLite?

- Cero configuración.
- Adecuado para baja concurrencia.
- Reduce complejidad.
- Migrable a PostgreSQL sin cambiar modelos.

---

# 12. Riesgos Identificados

| Riesgo | Impacto | Mitigación |
|--------|----------|------------|
| Sobrecupo simultáneo | Bajo | Validación en modelo |
| Error humano | Medio | Validaciones automáticas |
| Pérdida de datos | Medio | Copias periódicas |
| Escalabilidad futura | Bajo | Migración sencilla a PostgreSQL |

---

# 13. Mantenibilidad

El sistema:

✅ Tiene separación clara de responsabilidades  
✅ Lógica en modelos (no en vistas)  
✅ Uso de ModelForms  
✅ Constraints en base de datos  
✅ Tests automatizados  

Esto facilita:

- Cambios futuros
- Migración de base de datos
- Escalado moderado

---

# 14. Cumplimiento de Objetivos Estratégicos

| Problema Inicial | Solución Implementada |
|------------------|----------------------|
| Sobrecupos | Validación automática |
| Datos dispersos | Base centralizada |
| Errores en pagos | Campo `pagado` |
| Falta de trazabilidad | Historial por participante |
| Dificultad en reportes | Resumen general |
| Comunicación lenta | Acceso rápido a contacto |

---

# 15. Conclusión

La solución propuesta:

- Es técnicamente sólida.  
- Es coherente con el contexto organizativo.  
- Minimiza complejidad.  
- Maximiza eficiencia.  
- Cumple todas las historias de usuario.  
- Es sostenible a medio plazo.  
- Es realista para un desarrollo de 2 días por un solo desarrollador.  

La arquitectura monolítica basada en Django es la decisión óptima para:

- Restricciones presupuestarias  
- Bajo volumen de usuarios  
- Necesidad de rapidez  
- Mantenibilidad futura  
