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
| **✅ Pasaron (Pass)** | 11|
| **❌ Fallaron (Fail)** | 1 |
| **⚠️ Bloqueados** | 2 |
| **Defectos Encontrados** | 1 |

---

## 🧪 Detalle de Pruebas (Test Cards)

### 📦 GRUPO 1: Registro y Lógica (FR1 & FR2)

## 📦 PRUEBAS FR1: Registro de Paquetes (15 Casos)

#### [cite_start]🆔 TC-FR1-001: Registro Exitoso (Happy Path) 
- **Datos:** Barcode `1001`, Peso `15.5`, Largo `30`, Ancho `20`, Alto `15`, Dest `New York`, Prio `Standard`.
- **Esperado:** Mensaje de éxito, Categoría Standard, Ubicación asignada.
- **Resultado Real:** Registro correctamente.
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-002: Código Duplicado [cite: 449]
- **Datos:** Intentar registrar DE NUEVO el Barcode `1001`.
- **Esperado:** Error "Barcode 1001 already exists".
- **Resultado Real:** Me sale mensaje que ya existe
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-003: Peso Negativo (Bug Esperado) [cite: 484]
- **Datos:** Barcode `1003`, Peso `-5.0`.
- **Esperado:** Error "Invalid input".
- **Resultado Real:** Acepto el producto
- **Estado:** DEF (DEF-001)

#### [cite_start]🆔 TC-FR1-004: Destino Vacío [cite: 513]
- **Datos:** Barcode `1004`, Peso `12`, Destino `` (Solo dar Enter).
- **Esperado:** Error o solicitud del campo nuevamente.
- **Resultado Real:** Se registro sin el Destino
- **Estado:** FAIL

#### [cite_start]🆔 TC-FR1-005: Generación Automática de Barcode [cite: 547]
- **Datos:** En Barcode, no escribas nada, solo presiona **Enter**. Resto de datos normales.
- **Esperado:** Mensaje "Generated barcode: [números]".
- **Resultado Real:** Me genero un barcode random
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-006: Prioridad Express [cite: 583]
- **Datos:** Barcode `1006`, Peso `5`, Dest `Seattle`, Prioridad `Express`.
- **Esperado:** Categoría asignada: **Express** (Zone B).
- **Resultado Real:** Se registró con la categoría Express
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-007: Timestamp Correcto [cite: 623]
- **Datos:** Registrar Barcode `1007`.
- **Acción:** Revisar en SQLite la columna `received_at`.
- **Esperado:** La fecha y hora deben coincidir con tu reloj actual.
- **Resultado Real:** Se recibió en tiempo actual
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-008: Rendimiento (< 2 seg) [cite: 654]
- **Datos:** Registrar Barcode `1008`. Contar mentalmente.
- **Esperado:** Confirmación casi instantánea.
- **Resultado Real:** La respuesta fue instantánea
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-009: Sin Ubicaciones Disponibles [cite: 688]
- **Nota:** Esta prueba requiere llenar 20 ubicaciones. Por tiempo, verificaremos si el código maneja el error teóricamente.
- **Estado:** ⚠️ SKIPPED (Requiere pre-condición de BD llena).

#### [cite_start]🆔 TC-FR1-010: IDs Secuenciales [cite: 719]
- **Datos:** Registrar dos paquetes seguidos (`1010A` y `1010B`).
- **Esperado:** En la DB, sus `package_id` deben ser consecutivos (ej. 10 y 11).
- **Resultado Real:** Se registraron por orden por donde entraron
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-011: Valores Límite (Fronteras) [cite: 744]
- **Caso A:** Barcode `1011A`, Peso `5.0` exactos. -> Esperado: **Standard** (No Fragile).
- **Caso B:** Barcode `1011B`, Peso `50.0` exactos. -> Esperado: **Standard** (No Heavy).
- **Resultado Real:** Se registraron correctamente
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-012: Caracteres Especiales [cite: 771]
- **Datos:** Barcode `1012`, Destino `São Paulo, Brazil #45 @Corner`.
- **Esperado:** Registro exitoso y texto guardado correctamente en DB.
- **Resultado Real:** Se registró correctamente
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-013: Rollback (Transacción) [cite: 803]
- **Nota:** Difícil de simular manualmente sin inyectar fallos en el código.
- **Estado:** ⚠️ SKIPPED (Requiere herramientas de inyección de fallos).

#### [cite_start]🆔 TC-FR1-014: Creación de Audit Trail [cite: 831]
- **Datos:** Verifica el paquete `1001` registrado al inicio.
- **Acción:** Mira la tabla `AuditTrail` en SQLite.
- **Esperado:** Fila con Action `REGISTERED`.
- **Resultado Real:** Registrado
- **Estado:** PASS

#### [cite_start]🆔 TC-FR1-015: Prioridad Mayúsculas/Minúsculas [cite: 863]
- **Datos:** Barcode `1015`, Prioridad `express` (todo minúsculas).
- **Esperado:** El sistema debe entenderlo y asignar Categoría **Express**.
- **Resultado Real:** Lo registró con minusculas
- **Estado:** PASS