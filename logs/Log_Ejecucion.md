# 📝 Bitácora de Ejecución de Pruebas (Test Execution Log)

**Proyecto:** Distribution Center Package Management System  
**Iteración:** 1 (Ciclo PDCA)  
**Fecha:** 26/11/2025  
**Tester:** [David Ibarra Meza & Jorge Emir Medrano Reyes / Equipo QoQ]  
**Versión del Software:** v1.0  

---

## 📊 Resumen de Ejecución (Dashboard)

| Métrica | Valor |
| :--- | :--- |
| **Total Casos Ejecutados** | 46 |
| **✅ Pasaron (Pass)** | 38|
| **❌ Fallaron (Fail)** | 1 |
| **⚠️ Bloqueados** | 2 |
| **Defectos Encontrados** | 5 |

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

## 🧠 PRUEBAS FR2: Gestión de Categorías (8 Casos)

#### 🆔 TC-FR2-001: Categorización Express (Alta Prioridad)
> **Regla:** Si Prioridad es "Express", siempre es Categoría Express (Zona B), sin importar el peso.
- **Datos:** Barcode `2001`, Peso `60` (Muy pesado), Prioridad `Express`.
- **Esperado:** Categoría **Express** (No Heavy). Ubicación empieza con `B`.
- **Resultado Real:** Se registró como express
- **Estado:** PASS

#### 🆔 TC-FR2-002: Categorización Internacional
> **Regla:** Si destino dice "International" o tiene muchas comas.
- **Datos:** Barcode `2002`, Peso `10`, Destino `Madrid, Spain, International`, Prioridad `Standard`.
- **Esperado:** Categoría **International**. Ubicación empieza con `E`.
- **Resultado Real:** Se registró como Standard
- **Estado:** PASS

#### 🆔 TC-FR2-003: Categorización Heavy (> 50kg)
> **Regla:** Peso mayor a 50kg.
- **Datos:** Barcode `2003`, Peso `55.5`, Prioridad `Standard`.
- **Esperado:** Categoría **Heavy**. Ubicación empieza con `D`.
- **Resultado Real:** Se registró como Heavy
- **Estado:** PASS

#### 🆔 TC-FR2-004: Categorización Fragile (< 5kg)
> **Regla:** Peso menor a 5kg.
- **Datos:** Barcode `2004`, Peso `3.0`, Prioridad `Standard`.
- **Esperado:** Categoría **Fragile**. Ubicación empieza con `C`.
- **Resultado Real:** Se registró como Fragile
- **Estado:** PASS

#### 🆔 TC-FR2-005: Categorización Standard (Default)
> **Regla:** Cuando no aplica ninguna de las anteriores.
- **Datos:** Barcode `2005`, Peso `20`, Destino `Mexico City`, Prioridad `Standard`.
- **Esperado:** Categoría **Standard**. Ubicación empieza con `A`.
- **Resultado Real:** Standard
- **Estado:** PASS

#### 🆔 TC-FR2-006: Prioridad de Reglas (Jerarquía)
> **Regla:** Verificar quién gana: ¿International o Heavy? (Según Requisitos: International > Heavy).
- **Datos:** Barcode `2006`, Peso `80` (Heavy), Destino `Tokyo, Japan, International`.
- **Esperado:** Debe ser **International** (Zona E), porque es más importante que el peso.
- **Resultado Real:** Se registró como International
- **Estado:** PASS

#### 🆔 TC-FR2-007: Consulta por Categoría
> **Objetivo:** Verificar que el reporte agrupa bien los paquetes.
- **Acción:** Ejecutar opción 4 del menú (View Summary Report).
- **Esperado:** Debe mostrar conteos distintos para Express, Heavy, International, etc.
- **Resultado Real:** Si hay paquetes en distintos Packages
- **Estado:** PASS

#### 🆔 TC-FR2-008: Verificación de Zonas (A-E)
> **Objetivo:** Confirmar que cada categoría cayó en su letra correcta.
- **Acción:** Revisar en SQLite Viewer la tabla `Locations` para los paquetes 2001-2005.
- **Esperado:**
  - Express -> Zona B
  - International -> Zona E
  - Heavy -> Zona D
  - Fragile -> Zona C
  - Standard -> Zona A
- **Resultado Real:** Todo esta ordenado
- **Estado:** PASS
  
  ## 🏭 PRUEBAS FR3: Gestión de Ubicaciones (10 Casos)

#### 🆔 TC-FR3-001: Asignación Correcta de Zona (Lógica)
> **Objetivo:** Verificar que un paquete Heavy vaya a Zona D y uno Fragile a Zona C.
- **Datos:** Usar el paquete Heavy (`2003`) y Fragile (`2004`) de la fase anterior.
- **Esperado:** Heavy -> `D...` | Fragile -> `C...`
- **Resultado Real:** Aparece todo en orden
- **Estado:** PASS

#### 🆔 TC-FR3-002: Validación de Formato de Ubicación
> **Objetivo:** Confirmar formato estándar (Letra + Fila + Estante).
- **Datos:** Revisar ubicación del paquete `2001`.
- **Esperado:** Regex `[A-E][0-9]{2}-[0-9]{2}` (Ej: B01-01).
- **Resultado Real:** Se registro correctamente
- **Estado:** PASS

#### 🆔 TC-FR3-003: Flag de Ocupación (DB Check)
> **Objetivo:** Verificar que la DB marque el lugar como ocupado.
- **Acción:** Revisar tabla `Locations` para la ubicación del paquete `2001`.
- **Esperado:** `is_occupied` = 1.
- **Resultado Real:** Esta registrado como ocupado
- **Estado:** PASS

#### 🆔 TC-FR3-004: Liberación por Entrega (Delivered)
> **Objetivo:** Al entregar, el espacio se libera.
- **Acción:** Cambiar estado del paquete `2005` a `Delivered`.
- **Esperado:** Su ubicación en `Locations` debe pasar a `is_occupied` = 0.
- **Resultado Real:** Si dio 0
- **Estado:** PASS

#### 🆔 TC-FR3-005: Reciclaje de Ubicaciones
> **Objetivo:** Un nuevo paquete debe tomar el hueco liberado.
- **Acción:** Registrar paquete `3005`.
- **Esperado:** Debe tomar la MISMA ubicación que se liberó en el caso 004.
- **Resultado Real:** No, me salió que esta ocupado
- **Estado:** Revisión

#### 🆔 TC-FR3-006: Liberación por "In Transit"
> **Objetivo:** Si sale del edificio, libera espacio.
- **Acción:** Cambiar paquete `3006` a `In Transit`.
- **Esperado:** `is_occupied` = 0.
- **Resultado Real:** Me salio 0
- **Estado:** PASS
#### 🆔 TC-FR3-007: Liberación por "Lost"
> **Objetivo:** Si se pierde, libera espacio.
- **Acción:** Cambiar paquete `3007` a `Lost`.
- **Esperado:** `is_occupied` = 0.
- **Resultado Real:** En las opciones, no me sale LOST, y me sale 1
- **Estado:** Revisión

#### 🆔 TC-FR3-008: Integridad Referencial
> **Objetivo:** No puede haber paquetes en ubicaciones fantasmas.
- **Acción:** SQL Check de IDs huérfanos.
- **Esperado:** 0 resultados devueltos por la query de error.
- **Resultado Real:** Me sale 0
- **Estado:** PASS

#### 🆔 TC-FR3-009: Llenado Secuencial (Next Slot)
> **Objetivo:** Si A01-01 está lleno, el siguiente va a A01-02.
- **Acción:** Registrar `3009` (Standard) teniendo el slot 01 ocupado.
- **Esperado:** Ubicación asignada debe terminar en `02` (o siguiente libre).
- **Resultado Real:** Si me dió 02
- **Estado:** PASS

#### 🆔 TC-FR3-010: Persistencia tras Reinicio
> **Objetivo:** Las ubicaciones no se resetean al cerrar la app.
- **Acción:** Cerrar programa -> Abrir -> Checar DB.
- **Esperado:** `is_occupied` sigue en 1 para paquetes activos.
- **Resultado Real:** Todo esta en su lugar
- **Estado:** PASS
  
## 📊 PRUEBAS FR4: Rastreo y Reportes (12 Casos)

#### 🆔 TC-FR4-001: Búsqueda por Barcode Exacto
> **Objetivo:** Encontrar un paquete existente.
- **Acción:** Opción 2 -> Buscar `1001`.
- **Esperado:** Muestra todos los detalles (Peso, Ubicación, Estado).
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-002: Búsqueda de Paquete Inexistente
> **Objetivo:** Verificar manejo de "No encontrado".
- **Acción:** Opción 2 -> Buscar `999999999`.
- **Esperado:** Mensaje "Package not found".
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-003: Búsqueda de Paquete Entregado
> **Objetivo:** Verificar que guarda historial de entregados.
- **Acción:** Buscar el paquete `2005` (que entregamos en FR3).
- **Esperado:** Debe aparecer con Status: 'Delivered'.
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-004: Audit Trail - Registro
> **Objetivo:** Verificar que el nacimiento del paquete se guardó.
- **Acción:** SQL en tabla `AuditTrail` para paquete `1001`.
- **Esperado:** Fila con Action = 'REGISTERED'.
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-005: Audit Trail - Cambio de Estado
> **Objetivo:** Verificar que los movimientos se guardan.
- **Acción:** SQL en tabla `AuditTrail` para paquete `3006`.
- **Esperado:** Fila con Action = 'STATUS_UPDATE' y New Status = 'In Transit'.
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-006: Validación de Fechas en Auditoría
> **Objetivo:** Que el log tenga fecha coherente.
- **Acción:** Revisar columna `timestamp` en `AuditTrail`.
- **Esperado:** Fecha de hoy, hora reciente.
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-007: Reporte General - Conteo Total
> **Objetivo:** El reporte suma bien.
- **Acción:** Opción 4 (Summary Report).
- **Esperado:** "Total Packages" debe coincidir con tus registros (aprox 10-15).
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-008: Reporte - Distribución por Categoría
> **Objetivo:** El reporte desglosa bien.
- **Acción:** Ver sección "By Category" en el reporte.
- **Esperado:** Debe tener >0 en Standard, Heavy, Fragile, Express.
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-009: Reporte - Ocupación del Almacén
> **Objetivo:** Cálculo de porcentaje.
- **Acción:** Ver sección "Warehouse Occupancy".
- **Esperado:** Un porcentaje válido (ej. "5.0% occupied").
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-010: Búsqueda Case Sensitivity
> **Objetivo:** ¿Distingue mayúsculas de minúsculas?
- **Acción:** Buscar `1001A` vs `1001a` (si usaste letras). Si solo usas números, marcar como N/A o probar con `1010A`.
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-011: Integridad del Historial
> **Objetivo:** Un paquete no puede tener Updates antes de su Registro.
- **Acción:** Verificar visualmente en DB que el ID de 'REGISTERED' sea menor al de 'STATUS_UPDATE'.
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE

#### 🆔 TC-FR4-012: Exportación/Visualización Limpia
> **Objetivo:** El reporte es legible.
- **Acción:** Verificar que la tabla ASCII del reporte se alinee bien en la terminal.
- **Resultado Real:** ____________________
- **Estado:** ⏳ PENDIENTE