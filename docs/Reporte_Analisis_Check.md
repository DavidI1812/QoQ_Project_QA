# 📊 Fase CHECK: Reporte de Análisis de Resultados (Iteración 1)

**Equipo:** QoQ (David & Emir)
**Fecha:** 28/11/2025
**Estado:** Análisis Pre-Corrección

## 1. Métricas de Ejecución (KPIs)

| Métrica | Valor | Análisis |
| :--- | :--- | :--- |
| **Total de Casos** | 71 | Cobertura completa del plan (100%) |
| **✅ Pasaron (Pass)** | 65 | El flujo principal y NFRs son estables |
| **❌ Fallaron / Defectos** | 6 | Se detectaron fallos de validación y UI |
| **📈 Tasa de Éxito**| 91.5% | Software funcional pero requiere parches de calidad |

## 2. Hallazgos Críticos (Defectos Detectados)

### 🔴 DEF-001: Peso Negativo (TC-FR1-003)
* **Severidad:** Alta.
* **Problema:** El sistema permite ingresar `-5.0 kg`.
* **Causa:** Falta validación `if weight <= 0` en el código.

### 🟠 DEF-002: Destino Vacío (TC-FR1-004)
* **Severidad:** Media.
* **Problema:** El sistema permite registrar paquetes sin destino (string vacío).
* **Impacto:** Paquetes imposibles de entregar en la vida real.

### 🟠 DEF-003: Menú Incompleto "Lost" (TC-FR3-007)
* **Severidad:** Media.
* **Problema:** El requerimiento pide marcar paquetes como "Lost", pero la opción no existe en el menú de actualización de estado.

### 🟡 DEF-004: Lógica de Reciclaje de Ubicaciones (TC-FR3-005)
* **Severidad:** Baja.
* **Problema:** El sistema no reutilizó la ubicación liberada inmediatamente.
* **Nota:** Puede ser un comportamiento intencional del algoritmo de asignación secuencial.

### 🟡 DEF-005: Case Sensitivity en Búsqueda (TC-FR4-010)
* **Severidad:** Baja.
* **Problema:** Buscar `1001a` no encuentra `1001A`.
* **Mejora:** Se sugiere hacer la búsqueda insensible a mayúsculas (Case Insensitive).

## 3. Conclusiones y Plan de Acción (ACT)
El sistema es rápido y robusto (pasó todas las pruebas NFR de rendimiento y seguridad), pero carece de **validaciones de entrada de datos**.

**Plan de Acción para Fase ACT:**
1.  Implementar validación de Peso > 0.
2.  Implementar validación de Destino no vacío.
3.  Re-ejecutar pruebas de regresión para confirmar arreglos.