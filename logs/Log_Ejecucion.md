# 📝 Bitácora de Ejecución de Pruebas (Test Execution Log)

**Proyecto:** Distribution Center Package Management System  
**Iteración:** 1 (Ciclo PDCA)  
**Fecha:** 26/11/2025  
**Tester:** [Tu Nombre / Equipo QoQ]  
**Versión del Software:** v1.0  

---

## 📊 Resumen de Ejecución (Dashboard)

| Métrica | Valor |
| :--- | :--- |
| **Total Casos Ejecutados** | 0 |
| **✅ Pasaron (Pass)** | 0 |
| **❌ Fallaron (Fail)** | 0 |
| **⚠️ Bloqueados** | 0 |
| **Defectos Encontrados** | 0 |

---

## 🧪 Detalle de Pruebas (Test Cards)

### 📦 GRUPO 1: Registro y Lógica (FR1 & FR2)

#### 🆔 TC-FR1-001: Registro Exitoso de Paquete Standard
> **Objetivo:** Verificar que se puede registrar un paquete con datos válidos.
- **Datos de Entrada:** `Barcode: 100000000001`, `Peso: 10`, `Dest: Mexico`, `Prio: Standard`.
- **Resultado Esperado:** Mensaje "Package registered successfully" y asignación a Categoría Standard.
- **Resultado Real:** Se registró correctamente
- **Estado:** ✅ Pasaron (Pass) - **Evidencia:** --- REGISTER NEW PACKAGE ---
Enter barcode (or press Enter to generate random): 100000000001
Enter weight (kg): 10
Enter width (cm): 20      
Enter height (cm): 20     
Enter destination: Mexico 
Enter priority (Standard/Express): Standard
✅ Package registered successfully!
   Barcode: 100000000001  
   Category: Standard     
   Location: A01-01 

#### 🆔 TC-FR1-002: Detección de Duplicados
> **Objetivo:** Verificar que el sistema rechaza códigos de barras repetidos.
- **Datos de Entrada:** `Barcode: 100000000001` (El mismo de arriba).
- **Resultado Esperado:** Error "Barcode already exists".
- **Resultado Real:** [Escribe aquí lo que pasó...]
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR1-003: Validación de Peso Negativo (Bug Hunt)
> **Objetivo:** Verificar que el sistema rechaza pesos inválidos.
- **Datos de Entrada:** `Barcode: 666`, `Peso: -5.0`.
- **Resultado Esperado:** Error "Invalid input" o rechazo del registro.
- **Resultado Real:** [Escribe aquí si lo guardó o no...]
- **Estado:** ⏳ PENDIENTE
- **Defecto Relacionado:** [Si falla, pon aquí el ID del Bug, ej: DEF-001]

#### 🆔 TC-FR2-003: Categorización Heavy (> 50kg)
> **Objetivo:** Verificar regla de negocio para paquetes pesados.
- **Datos de Entrada:** `Barcode: 300000000003`, `Peso: 60`.
- **Resultado Esperado:** Categoría asignada debe ser "Heavy" (Zona D).
- **Resultado Real:** [Escribe aquí qué categoría asignó el sistema...]
- **Estado:** ⏳ PENDIENTE

---

### 🏭 GRUPO 2: Ubicaciones (FR3)

#### 🆔 TC-FR3-003: Ocupación de Ubicación
> **Objetivo:** Verificar que la ubicación se marca como ocupada en la DB.
- **Acción:** Consultar la tabla `Locations` para la ubicación asignada al TC-FR1-001.
- **Resultado Esperado:** Columna `is_occupied` debe ser `1` (True).
- **Resultado Real:** [Escribe lo que viste en SQLite Viewer...]
- **Estado:** ⏳ PENDIENTE

---

### 🛡️ GRUPO 3: Pruebas No Funcionales (NFR)

#### 🆔 TC-NFR6-002: Prueba de Inyección SQL (Seguridad)
> **Objetivo:** Verificar vulnerabilidad en búsqueda.
- **Datos de Entrada:** En Search, ingresar: `' OR '1'='1`.
- **Resultado Esperado:** Mensaje "Package not found" o manejo seguro del error.
- **Resultado Real:** [Escribe aquí lo que pasó...]
- **Estado:** ⏳ PENDIENTE

---

## 🐛 Reporte de Defectos (Bug Report)

*Llena esta sección solo si encuentras errores (Estados FAIL)*

### 🐞 DEF-001: [Título del Error, ej. Sistema acepta pesos negativos]
- **Severidad:** [Alta/Media/Baja]
- **Descripción:** El sistema permite registrar paquetes con peso `-5.0` kg, violando la integridad de datos.
- **Pasos para reproducir:**
  1. Ir a opción 1 (Register).
  2. Ingresar un código nuevo.
  3. En peso, poner `-10`.
- **Evidencia:** `logs/DEF-001_peso_negativo.png`
- **Solución Propuesta (Act):** Agregar validación `if weight <= 0` en `distribution_center.py`.

---