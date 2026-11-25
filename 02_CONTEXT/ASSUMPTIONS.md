# Registro de Supuestos — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Sincronización:** Alineado con la Sección 7 de `00_GOVERNANCE/DECISION_SPEC.md`

---

## Tabla de Supuestos Declarados

| ID | Supuesto | Fundamento | Estado | Dónde se valida |
| :--- | :--- | :--- | :--- | :--- |
| `ASM-01` | Los precios de semillas, insumos, agua y valor por tonelada cosechada en la `Base de Conocimiento` se mantienen constantes durante los 10 ciclos (5 años). | Delimitación prescriptiva aprobada en `D-0001`: SAGE no pronostica precios de mercado y usa parámetros económicos de referencia estáticos. | `ASSUMPTION` | `D01` (definición de parámetros de referencia) y `D05` (análisis de sensibilidad de precios en escenarios alternos). |
| `ASM-02` | La fertilidad edáfica relevante para la rotación de cultivos puede modelarse mediante un balance discreto de nitrógeno (`N`) por parcela y ciclo, con umbral crítico estricto `N > 0`. | Simplificación agronómica adecuada al alcance académico para capturar el contraste entre cultivos extractivos, fijadores (Frijol) y recuperación (Barbecho). | `ASSUMPTION` | `D01` (formulación agronómica), `D03` (ecuaciones de balance de `N`) y `D05` (revisión de trayectorias de `N` en el Top-3). |
| `ASM-03` | El requerimiento hídrico por cultivo y temporada (`PV` / `OI`) es determinista y conocido en el catálogo estático, sin modelar estocasticidad meteorológica diaria. | Consistente con la naturaleza no predictiva de SAGE y con el foco en minimizar desviación entre riego aplicado y demanda nominal (`VO-4`). | `ASSUMPTION` | `D01` (parámetros hídricos `PV`/`OI`), `D03` (función de penalización hídrica) y `D05` (pruebas en escenarios secos/normales). |
| `ASM-04` | Cada parcela del predio piloto (3 a 10 parcelas) puede planificarse con su propia secuencia de cultivos y riego sin restricciones ocultas de maquinaria compartida ni contagio fitosanitario espacial no declarado. | Permite mantener tratable la complejidad inicial del cromosoma y cerrar la rebanada vertical `DEC-01` antes de evaluar restricciones acopladas entre parcelas. | `ASSUMPTION` | `D01` (alcance de restricciones) y `D03` (decisión sobre restricciones globales opcionales de agua o presupuesto). |
| `ASM-05` | Tres individuos estructuralmente distintos son suficientes para exponer los *trade-offs* principales (financiero, edáfico e hídrico) al decisor humano en `DEC-02`. | Equilibra riqueza comparativa y carga cognitiva del administrador agrícola y del agrónomo conforme a las salidas obligatorias de `D-0001`. | `ASSUMPTION` | `D03` (criterio de diversidad estructural del Top-3) y `D05` (evaluación de diferenciación real entre los 3 planes reportados). |

---

## Política de Revisión

Cuando un supuesto se verifique con evidencia técnica (código, pruebas y experimentos), su estado deberá actualizarse explícitamente a `SUPPORTED` o `VERIFIED` (o a `CONTRADICTED` si falla en experimentación), registrando el hallazgo en `03_MEMORY/lessons_learned/LESSONS.md`.
