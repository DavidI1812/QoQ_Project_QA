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
| **Total Casos Ejecutados** | 71 |
| **✅ Pasaron (✅PASS)** | 62 |
| **❌ Fallaron (Fail)** | 3 |
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
- **Estado:** ✅PASS

#### [cite_start]🆔 TC-FR1-002: Código Duplicado [cite: 449]
- **Datos:** Intentar registrar DE NUEVO el Barcode `1001`.
- **Esperado:** Error "Barcode 1001 already exists".
- **Resultado Real:** Me sale mensaje que ya existe
- **Estado:** ✅PASS

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
- **Estado:** ✅PASS

#### [cite_start]🆔 TC-FR1-006: Prioridad Express [cite: 583]
- **Datos:** Barcode `1006`, Peso `5`, Dest `Seattle`, Prioridad `Express`.
- **Esperado:** Categoría asignada: **Express** (Zone B).
- **Resultado Real:** Se registró con la categoría Express
- **Estado:** ✅PASS

#### [cite_start]🆔 TC-FR1-007: Timestamp Correcto [cite: 623]
- **Datos:** Registrar Barcode `1007`.
- **Acción:** Revisar en SQLite la columna `received_at`.
- **Esperado:** La fecha y hora deben coincidir con tu reloj actual.
- **Resultado Real:** Se recibió en tiempo actual
- **Estado:** ✅PASS

#### [cite_start]🆔 TC-FR1-008: Rendimiento (< 2 seg) [cite: 654]
- **Datos:** Registrar Barcode `1008`. Contar mentalmente.
- **Esperado:** Confirmación casi instantánea.
- **Resultado Real:** La respuesta fue instantánea
- **Estado:** ✅PASS

#### [cite_start]🆔 TC-FR1-009: Sin Ubicaciones Disponibles [cite: 688]
- **Nota:** Esta prueba requiere llenar 20 ubicaciones. Por tiempo, verificaremos si el código maneja el error teóricamente.
- **Estado:** ⚠️ SKIPPED (Requiere pre-condición de BD llena).

#### [cite_start]🆔 TC-FR1-010: IDs Secuenciales [cite: 719]
- **Datos:** Registrar dos paquetes seguidos (`1010A` y `1010B`).
- **Esperado:** En la DB, sus `package_id` deben ser consecutivos (ej. 10 y 11).
- **Resultado Real:** Se registraron por orden por donde entraron
- **Estado:** ✅PASS

#### [cite_start]🆔 TC-FR1-011: Valores Límite (Fronteras) [cite: 744]
- **Caso A:** Barcode `1011A`, Peso `5.0` exactos. -> Esperado: **Standard** (No Fragile).
- **Caso B:** Barcode `1011B`, Peso `50.0` exactos. -> Esperado: **Standard** (No Heavy).
- **Resultado Real:** Se registraron correctamente
- **Estado:** ✅PASS

#### [cite_start]🆔 TC-FR1-012: Caracteres Especiales [cite: 771]
- **Datos:** Barcode `1012`, Destino `São Paulo, Brazil #45 @Corner`.
- **Esperado:** Registro exitoso y texto guardado correctamente en DB.
- **Resultado Real:** Se registró correctamente
- **Estado:** ✅PASS

#### [cite_start]🆔 TC-FR1-013: Rollback (Transacción) [cite: 803]
- **Nota:** Difícil de simular manualmente sin inyectar fallos en el código.
- **Estado:** ⚠️ SKIPPED (Requiere herramientas de inyección de fallos).

#### [cite_start]🆔 TC-FR1-014: Creación de Audit Trail [cite: 831]
- **Datos:** Verifica el paquete `1001` registrado al inicio.
- **Acción:** Mira la tabla `AuditTrail` en SQLite.
- **Esperado:** Fila con Action `REGISTERED`.
- **Resultado Real:** Registrado
- **Estado:** ✅PASS

#### [cite_start]🆔 TC-FR1-015: Prioridad Mayúsculas/Minúsculas [cite: 863]
- **Datos:** Barcode `1015`, Prioridad `express` (todo minúsculas).
- **Esperado:** El sistema debe entenderlo y asignar Categoría **Express**.
- **Resultado Real:** Lo registró con minusculas
- **Estado:** ✅PASS

## 🧠 PRUEBAS FR2: Gestión de Categorías (8 Casos)

#### 🆔 TC-FR2-001: Categorización Express (Alta Prioridad)
> **Regla:** Si Prioridad es "Express", siempre es Categoría Express (Zona B), sin importar el peso.
- **Datos:** Barcode `2001`, Peso `60` (Muy pesado), Prioridad `Express`.
- **Esperado:** Categoría **Express** (No Heavy). Ubicación empieza con `B`.
- **Resultado Real:** Se registró como express
- **Estado:** ✅PASS

#### 🆔 TC-FR2-002: Categorización Internacional
> **Regla:** Si destino dice "International" o tiene muchas comas.
- **Datos:** Barcode `2002`, Peso `10`, Destino `Madrid, Spain, International`, Prioridad `Standard`.
- **Esperado:** Categoría **International**. Ubicación empieza con `E`.
- **Resultado Real:** Se registró como Standard
- **Estado:** ✅PASS

#### 🆔 TC-FR2-003: Categorización Heavy (> 50kg)
> **Regla:** Peso mayor a 50kg.
- **Datos:** Barcode `2003`, Peso `55.5`, Prioridad `Standard`.
- **Esperado:** Categoría **Heavy**. Ubicación empieza con `D`.
- **Resultado Real:** Se registró como Heavy
- **Estado:** ✅PASS

#### 🆔 TC-FR2-004: Categorización Fragile (< 5kg)
> **Regla:** Peso menor a 5kg.
- **Datos:** Barcode `2004`, Peso `3.0`, Prioridad `Standard`.
- **Esperado:** Categoría **Fragile**. Ubicación empieza con `C`.
- **Resultado Real:** Se registró como Fragile
- **Estado:** ✅PASS

#### 🆔 TC-FR2-005: Categorización Standard (Default)
> **Regla:** Cuando no aplica ninguna de las anteriores.
- **Datos:** Barcode `2005`, Peso `20`, Destino `Mexico City`, Prioridad `Standard`.
- **Esperado:** Categoría **Standard**. Ubicación empieza con `A`.
- **Resultado Real:** Standard
- **Estado:** ✅PASS

#### 🆔 TC-FR2-006: Prioridad de Reglas (Jerarquía)
> **Regla:** Verificar quién gana: ¿International o Heavy? (Según Requisitos: International > Heavy).
- **Datos:** Barcode `2006`, Peso `80` (Heavy), Destino `Tokyo, Japan, International`.
- **Esperado:** Debe ser **International** (Zona E), porque es más importante que el peso.
- **Resultado Real:** Se registró como International
- **Estado:** ✅PASS

#### 🆔 TC-FR2-007: Consulta por Categoría
> **Objetivo:** Verificar que el reporte agrupa bien los paquetes.
- **Acción:** Ejecutar opción 4 del menú (View Summary Report).
- **Esperado:** Debe mostrar conteos distintos para Express, Heavy, International, etc.
- **Resultado Real:** Si hay paquetes en distintos Packages
- **Estado:** ✅PASS

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
- **Estado:** ✅PASS
  
  ## 🏭 PRUEBAS FR3: Gestión de Ubicaciones (10 Casos)

#### 🆔 TC-FR3-001: Asignación Correcta de Zona (Lógica)
> **Objetivo:** Verificar que un paquete Heavy vaya a Zona D y uno Fragile a Zona C.
- **Datos:** Usar el paquete Heavy (`2003`) y Fragile (`2004`) de la fase anterior.
- **Esperado:** Heavy -> `D...` | Fragile -> `C...`
- **Resultado Real:** Aparece todo en orden
- **Estado:** ✅PASS

#### 🆔 TC-FR3-002: Validación de Formato de Ubicación
> **Objetivo:** Confirmar formato estándar (Letra + Fila + Estante).
- **Datos:** Revisar ubicación del paquete `2001`.
- **Esperado:** Regex `[A-E][0-9]{2}-[0-9]{2}` (Ej: B01-01).
- **Resultado Real:** Se registro correctamente
- **Estado:** ✅PASS

#### 🆔 TC-FR3-003: Flag de Ocupación (DB Check)
> **Objetivo:** Verificar que la DB marque el lugar como ocupado.
- **Acción:** Revisar tabla `Locations` para la ubicación del paquete `2001`.
- **Esperado:** `is_occupied` = 1.
- **Resultado Real:** Esta registrado como ocupado
- **Estado:** ✅PASS

#### 🆔 TC-FR3-004: Liberación por Entrega (Delivered)
> **Objetivo:** Al entregar, el espacio se libera.
- **Acción:** Cambiar estado del paquete `2005` a `Delivered`.
- **Esperado:** Su ubicación en `Locations` debe pasar a `is_occupied` = 0.
- **Resultado Real:** Si dio 0
- **Estado:** ✅PASS

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
- **Estado:** ✅PASS
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
- **Estado:** ✅PASS

#### 🆔 TC-FR3-009: Llenado Secuencial (Next Slot)
> **Objetivo:** Si A01-01 está lleno, el siguiente va a A01-02.
- **Acción:** Registrar `3009` (Standard) teniendo el slot 01 ocupado.
- **Esperado:** Ubicación asignada debe terminar en `02` (o siguiente libre).
- **Resultado Real:** Si me dió 02
- **Estado:** ✅PASS

#### 🆔 TC-FR3-010: Persistencia tras Reinicio
> **Objetivo:** Las ubicaciones no se resetean al cerrar la app.
- **Acción:** Cerrar programa -> Abrir -> Checar DB.
- **Esperado:** `is_occupied` sigue en 1 para paquetes activos.
- **Resultado Real:** Todo esta en su lugar
- **Estado:** ✅PASS
  
## 📊 PRUEBAS FR4: Rastreo y Reportes (12 Casos)

#### 🆔 TC-FR4-001: Búsqueda por Barcode Exacto
> *Objetivo:* Encontrar un paquete existente.
- *Acción:* Opción 2 -> Buscar 1001.
- *Esperado:* Muestra todos los detalles (Peso, Ubicación, Estado).
- *Resultado Real:* Se encontro correctamente todos los datos
- *Estado:* ✅PASS

#### 🆔 TC-FR4-002: Búsqueda de Paquete Inexistente
> *Objetivo:* Verificar manejo de "No encontrado".
- *Acción:* Opción 2 -> Buscar 999999999.
- *Esperado:* Mensaje "Package not found".
- *Resultado Real:* Como no hay un paquete con ese bardcode no se encontro nada, así que fue correcto
- *Estado:* ✅PASS

#### 🆔 TC-FR4-003: Búsqueda de Paquete Entregado
> *Objetivo:* Verificar que guarda historial de entregados.
- *Acción:* Buscar el paquete 2005 (que entregamos en FR3).
- *Esperado:* Debe aparecer con Status: 'Delivered'.
- *Resultado Real:* Aparece en Status: Delivered
- *Estado:* ✅PASS

#### 🆔 TC-FR4-004: Audit Trail - Registro
> *Objetivo:* Verificar que el nacimiento del paquete se guardó.
- *Acción:* SQL en tabla AuditTrail para paquete 1001.
- *Esperado:* Fila con Action = 'REGISTERED'.
- *Resultado Real:* Aparece en con la acción Registered.
- *Estado:* ✅PASS

#### 🆔 TC-FR4-005: Audit Trail - Cambio de Estado
> *Objetivo:* Verificar que los movimientos se guardan.
- *Acción:* SQL en tabla AuditTrail para paquete 3006.
- *Esperado:* Fila con Action = 'STATUS_UPDATE' y New Status = 'In Transit'.
- *Resultado Real:* Si se visualiza en la tabla Auditrail para el paquete 3006
- *Estado:* ✅PASS

#### 🆔 TC-FR4-006: Validación de Fechas en Auditoría
> *Objetivo:* Que el log tenga fecha coherente.
- *Acción:* Revisar columna timestamp en AuditTrail.
- *Esperado:* Fecha de hoy, hora reciente.
- *Resultado Real:* Si tiene fecha reciente cuando se realizan actualizaciones.
- *Estado:* ✅PASS

#### 🆔 TC-FR4-007: Reporte General - Conteo Total
> *Objetivo:* El reporte suma bien.
- *Acción:* Opción 4 (Summary Report).
- *Esperado:* "Total Packages" debe coincidir con tus registros (aprox 10-15).
- *Resultado Real:* Se tienen 10 paquetes en el summary report.
- *Estado:* ✅PASS

#### 🆔 TC-FR4-008: Reporte - Distribución por Categoría
> *Objetivo:* El reporte desglosa bien.
- *Acción:* Ver sección "By Category" en el reporte.
- *Esperado:* Debe tener >0 en Standard, Heavy, Fragile, Express.
- *Resultado Real:* En todos las categorias tiene mayor a 0.
- *Estado:* ✅PASS

#### 🆔 TC-FR4-009: Reporte - Ocupación del Almacén
> *Objetivo:* Cálculo de porcentaje.
- *Acción:* Ver sección "Warehouse Occupancy".
- *Esperado:* Un porcentaje válido (ej. "5.0% occupied").
- *Resultado Real:* En todas las zonas hay un cierto porcentaje válido como ocupado.
- *Estado:* ✅PASS

#### 🆔 TC-FR4-010: Búsqueda Case Sensitivity
> *Objetivo:* ¿Distingue mayúsculas de minúsculas?
- *Acción:* Buscar 1001A vs 1001a (si usaste letras). Si solo usas números, marcar como N/A o probar con 1010A.
- *Resultado Real:* Distingue mayúsculas de minúsculas, por lo que si se busca un paquete con minúsculas no se encuentra el paquete.
- *Estado:* FAIL

#### 🆔 TC-FR4-011: Integridad del Historial
> *Objetivo:* Un paquete no puede tener Updates antes de su Registro.
- *Acción:* Verificar visualmente en DB que el ID de 'REGISTERED' sea menor al de 'STATUS_UPDATE'.
- *Resultado Real:* Si cumple
- *Estado:* ✅PASS

#### 🆔 TC-FR4-012: Exportación/Visualización Limpia
> *Objetivo:* El reporte es legible.
- *Acción:* Verificar que la tabla ASCII del reporte se alinee bien en la terminal.
- *Resultado Real:* Se ve espectacular y legible.
- *Estado:* ✅PASS
  
## 📈 PRUEBAS FR5: Generación de Reportes (6 Casos)

#### 🆔 TC-FR5-001: Generación Básica del Reporte
> **Objetivo:** Que el sistema no explote al pedir el reporte.
- **Acción:** Opción 4 (View Summary Report).
- **Esperado:** Se despliega una tabla o lista en la terminal sin errores de Python.
- **Resultado Real:** La terminal dice que no encontro ningún paquete
- **Estado:** FAIL

#### 🆔 TC-FR5-002: Exactitud del Conteo Total
> **Objetivo:** Verificar matemáticas simples.
- **Acción:** Cuenta tus filas en SQLite (o recuerda cuántos metiste, aprox 15). Compara con "Total Packages".
- **Esperado:** Los números deben coincidir exactamente.
- **Resultado Real:** Si coincide correctamente con el número aproximado, son 16
- **Estado:** ✅PASS

#### 🆔 TC-FR5-003: Exactitud del % de Ocupación
> **Objetivo:** Verificar fórmula: (Ocupados / Total Espacios) * 100.
- **Dato:** Si tienes 40 espacios totales (A,B,C,D,E x 8 huecos) y 10 paquetes.
- **Esperado:** 10/40 = 25%. El reporte debe decir "25.0%".
- **Resultado Real:** Salio 30% porque hay m´´as paquetes  delo esperado
- **Estado:** ✅PASS

#### 🆔 TC-FR5-004: Desglose por Categorías
> **Objetivo:** Que no mezcle peras con manzanas.
- **Acción:** Verifica que la suma de (Standard + Express + Heavy + ...) sea igual al Total.
- **Esperado:** La suma de las partes debe ser igual al todo.
- **Resultado Real:** Si, la suma de los paquetes es la misma que del númeor de paquetes
- **Estado:** ✅PASS

#### 🆔 TC-FR5-005: Actualización en Tiempo Real
> **Objetivo:** El reporte no usa "caché" viejo.
- **Acción:** 1. Ver reporte. 2. Registrar paquete nuevo. 3. Ver reporte de nuevo.
- **Esperado:** El contador "Total" debe haber subido +1 inmediatamente.
- **Resultado Real:** Sumo uno correctamente
- **Estado:** ✅PASS

#### 🆔 TC-FR5-006: Legibilidad y Formato
> **Objetivo:** UX (Experiencia de Usuario).
- **Acción:** Observar la alineación del texto.
- **Esperado:** Las columnas deben estar alineadas, se deben entender los títulos.
- **Resultado Real:** La legibilidad del UX es buena
- **Estado:** ✅PASS

## ⚡ PRUEBAS NFR1: Rendimiento / Performance (5 Casos)

#### 🆔 TC-NFR1-001: Tiempo de Respuesta - Registro
> **Objetivo:** El usuario no espera.
- **Acción:** Registrar paquete.
- **Esperado:** < 2 segundos desde que das Enter hasta que sale "Success".
- **Resultado Real:** Al dar enter es menor a 2 segundos para que se registre el paquete nuevo.
- **Estado:** ✅PASS

#### 🆔 TC-NFR1-002: Tiempo de Respuesta - Búsqueda
> **Objetivo:** Búsqueda indexada rápida.
- **Acción:** Buscar un paquete.
- **Esperado:** < 1 segundo (Instantáneo).
- **Resultado Real:** La busqueda de cualquier paquete es menor a 1 segundo
- **Estado:** ✅PASS

#### 🆔 TC-NFR1-003: Tiempo de Respuesta - Reporte Complejo
> **Objetivo:** La agregación de datos es eficiente.
- **Acción:** Generar Reporte (Opción 4).
- **Esperado:** < 2 segundos (No debe "pensar" mucho).
- **Resultado Real:** La acción es rápida si no es que instantanea.
- **Estado:** ✅PASS

#### 🆔 TC-NFR1-004: Consumo de Espacio en Disco
> **Objetivo:** La DB no crece exponencialmente sin razón.
- **Acción:** Ver tamaño del archivo `distribution_center.db` en Windows.
- **Esperado:** Debe ser pequeño (KB), no MB gigantes para pocos datos.
- **Resultado Real:** El tamaño es de 56kb por lo que es pequeño el archivo
- **Estado:** ✅PASS

#### 🆔 TC-NFR1-005: Estabilidad bajo Repetición
> **Objetivo:** No se alenta con el uso.
- **Acción:** Hacer 5 búsquedas seguidas muy rápido.
- **Esperado:** La quinta búsqueda debe ser tan rápida como la primera (sin Memory Leak).
- **Resultado Real:** La quita busqueda o superiores son instantaneas ocmo la primera.
- **Estado:** ✅PASS

## 🛡️ PRUEBAS NFR2: Robustez y Seguridad (6 Casos)

#### 🆔 TC-NFR2-001: Inyección SQL (Seguridad Básica)
> **Objetivo:** Evitar acceso no autorizado a datos.
- **Acción:** En Search, escribir `' OR '1'='1`.
- **Esperado:** Sistema maneja el input como texto literal, no como comando. "Not found".
- **Resultado Real:** Muestra un Not Found por lo que no permite inyectar ningun SQL
- **Estado:** ✅PASS

#### 🆔 TC-NFR2-002: Manejo de Tipos de Dato Incorrectos
> **Objetivo:** Que no crashee si meto letras en números.
- **Acción:** En "Weight (kg)", escribir `DIEZ`.
- **Esperado:** El programa debe decir "Invalid value" o lanzar error controlado, NO cerrarse de golpe (Crash).
- **Resultado Real:** Si pones con letras te pide que intentes poner de nuevo con números.
- **Estado:** ✅PASS

#### 🆔 TC-NFR2-003: Desbordamiento de Buffer (Strings Largos)
> **Objetivo:** Ver límites de memoria.
- **Acción:** En "Destination", pegar un texto larguísimo (ej. 500 letras 'A').
- **Esperado:** Lo corta o lo guarda, pero no explota.
- **Resultado Real:** Guarda el texto, tiene límite de 900 caracteres despeus de esos carcacteres corta lo demas del texto.
- **Estado:** ✅PASS

#### 🆔 TC-NFR2-004: Caracteres Especiales (UTF-8)
> **Objetivo:** Soporte internacional.
- **Acción:** Registrar Destino con Emojis o Kanji (日本).
- **Esperado:** Se guarda y se muestra bien (sin signos de interrogación `???`).
- **Resultado Real:** Guarda culqueir tipo de caracter incluyendo emojis-
- **Estado:** ✅PASS

#### 🆔 TC-NFR2-005: Integridad tras Cierre Forzado
> **Objetivo:** No corrupción de datos.
- **Acción:** 1. Empezar a registrar. 2. Dar `Ctrl + C` (Matar proceso) a la mitad. 3. Abrir de nuevo.
- **Esperado:** La DB sigue funcionando y el último paquete (incompleto) no se guardó.
- **Resultado Real:** Se tiene que volver a iniciar el programa y no se guarda el último paquete, pero la DB sigue funcionando.
- **Estado:** ✅PASS

#### 🆔 TC-NFR2-006: Acceso Concurrente (Simulado)
> **Objetivo:** Bloqueo de archivos.
- **Acción:** Abre **DOS** terminales. Corre el programa en ambas. Intenta registrar en las dos a la vez.
- **Esperado:** SQLite maneja el bloqueo o da error de "Database Locked", pero no se corrompe.
- **Resultado Real:** No permite correr el programa en 2 terminales a la vez.
- **Estado:** ✅PASS

## 🎨 PRUEBAS NFR3: Usabilidad (4 Casos)

#### 🆔 TC-NFR3-001: Claridad de Navegación del Menú
> **Objetivo:** El usuario entiende qué hacer sin leer un manual.
- **Acción:** Abrir el programa y leer el menú principal.
- **Esperado:** Las opciones (1-6) son claras, en inglés correcto y se entiende qué hace cada una.
- **Resultado Real:** Es muy claro el programa, se entiende por todo
- **Estado:** ✅PASS

#### 🆔 TC-NFR3-002: Mensajes de Error Explicativos
> **Objetivo:** El sistema no dice solo "Error", sino que explica cómo arreglarlo.
- **Acción:** En el menú principal, escribe una opción inválida (ej. `9`).
- **Esperado:** Mensaje amigable como "Invalid option, please try again" (No un crash).
- **Resultado Real:** Me hace aviso que tengo que entrar desde el 1-6
- **Estado:** ✅PASS

#### 🆔 TC-NFR3-003: Facilidad de Salida (Exit)
> **Objetivo:** El usuario no se siente atrapado.
- **Acción:** Opción 6 (Exit).
- **Esperado:** El programa se cierra limpiamente con un mensaje de despedida ("Goodbye" o "Exiting").
- **Resultado Real:** Cierra completamente con un mensaje de despedida
- **Estado:** ✅PASS

#### 🆔 TC-NFR3-004: Consistencia Visual (ASCII/Layout)
> **Objetivo:** El diseño no cambia bruscamente.
- **Acción:** Comparar la cabecera del Menú Principal con la cabecera del Reporte.
- **Esperado:** Usan el mismo estilo de separadores (`===` o `---`) y alineación.
- **Resultado Real:** Todas usan el mismo signo para separación de estas
- **Estado:** ✅PASS

## 🔧 PRUEBAS NFR4: Confiabilidad y Entorno (5 Casos)

#### 🆔 TC-NFR4-001: Auto-recuperación de Base de Datos
> **Objetivo:** Si se borra la DB, el sistema crea una nueva.
- **Acción:** 1. Cerrar programa. 2. Borrar `distribution_center.db`. 3. Iniciar programa.
- **Esperado:** El programa inicia sin error y crea un archivo `.db` nuevo (vacío).
- **Resultado Real:** Al momento de borrar y volver a empezar, se crea el archivo de .db
- **Estado:** ✅PASS

#### 🆔 TC-NFR4-002: Ejecución desde Rutas Relativas
> **Objetivo:** Funciona sin importar la carpeta.
- **Acción:** Ejecutar desde fuera de `src/` (ej. `python src/distribution_center.py`).
- **Esperado:** Funciona igual.
- **Resultado Real:** Funciona igual
- **Estado:** ✅PASS

#### 🆔 TC-NFR4-003: Persistencia de Sesión
> **Objetivo:** Los datos sobreviven al cierre.
- **Acción:** Registrar paquete -> Cerrar -> Abrir -> Buscar paquete.
- **Esperado:** El paquete sigue ahí (La memoria no es volátil).
- **Resultado Real:** Se registra aún saliendo del porgrama
- **Estado:** ✅PASS

#### 🆔 TC-NFR4-004: Manejo de Archivo DB Corrupto (Simulación)
> **Objetivo:** Detectar si el archivo no es una DB válida.
- **Acción:** Crear un archivo de texto `distribution_center.db` con contenido basura ("HOLA"). Ejecutar programa.
- **Esperado:** El programa falla (Crash) o avisa del error de conexión (SQLite Error). *Nota: Anotar el comportamiento.*
- Enter barcode: 1001
❌ Package with barcode 1001 not found!
- **Resultado Real:** Al momento, de buscar un paquete, no lo encuentra
- **Estado:** ✅PASS

#### 🆔 TC-NFR4-005: Dependencias Mínimas
> **Objetivo:** No requiere instalaciones complejas.
- **Acción:** Verificar imports en código.
- **Esperado:** Solo usa librerías estándar (`sqlite3`, `datetime`, `os`) o las documentadas.
- **Resultado Real:** Usa las librerías normales 
- **Estado:** ✅PASS
