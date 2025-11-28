# 📊 Fase CHECK: Reporte de Análisis de Resultados

**Fecha:** 28/11/2025
**Iteración:** 1
**Estado:** Análisis Pre-Corrección

## 1. Métricas de Ejecución (KPIs)

| Métrica | Resultado | Notas |
| :--- | :--- | :--- |
| **Total de Casos Planeados** | 42 | Cobertura FR1-FR5 y NFR1-NFR4 |
| **Casos Ejecutados** | 42 | 100% de Ejecución |
| **✅ Casos Exitosos (Pass)** | 41 | Funcionalidad core estable |
| **❌ Casos Fallidos (Fail)** | 1 | Fallo crítico en validación |
| **📈 Tasa de Éxito (Pass Rate)**| 97.6% | El sistema es funcional en su mayoría |

## 2. Análisis de Defectos (Root Cause Analysis)

### 🐞 Defecto DEF-001: Peso Negativo
* **Descripción:** El sistema permite ingresar `-5.0 kg`.
* **Impacto:** Alto. Afecta la integridad de los datos y los cálculos de envío.
* **Causa Raíz:** Falta de validación en la capa de entrada de datos (`input` en Python). El código confía ciegamente en el usuario.
* **Tendencia:** Se observa que las pruebas funcionales complejas (lógica de negocio) pasaron bien, pero las pruebas de robustez básica (validación de inputs) fallaron.

## 3. Retrospectiva de la Fase DO (Review Meeting)
* **¿Qué salió bien?**
    * Las pruebas de estrés (NFR) demostraron que el sistema es rápido (<1s).
    * La base de datos mantuvo la integridad relacional (Foreign Keys).
* **¿Qué salió mal / Bloqueos?**
    * Tuvimos un conflicto de fusión en Git al trabajar en el mismo archivo de Log (ya resuelto).
    * El sistema no tiene manejo de errores para textos ingresados en campos numéricos (se detectó en NFR2).

## 4. Recomendación para la Fase ACT
Se autoriza proceder a la fase ACT con las siguientes tareas:
1.  Implementar un parche (Hotfix) en `distribution_center.py` para validar `weight > 0`.
2.  Agregar una prueba de regresión específica para verificar el arreglo.