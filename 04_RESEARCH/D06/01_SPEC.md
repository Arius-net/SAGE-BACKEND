# Especificación `D06` — Criterios de Empaquetado y Defensa Académica

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Fecha:** `2026-11-23`

---

## Componentes del Paquete Final

1. **Reproducibilidad limpia en 2 comandos:** instalación de dependencias (`requirements.txt`), verificación automatizada (`pytest 09_VALIDATION -v`) y regeneración íntegra de la campaña experimental (`python -m sage.cli campaign`).
2. **Informe académico autocontenido (`10_DOCUMENTATION/SAGE_FINAL_REPORT.md`):** cubre planteamiento prescriptivo, 4 VD, 4 VO, función *Fitness*, arquitectura modular, resultados experimentales `EXP-001`–`EXP-003`, análisis comparativo Línea Base vs. Top-3, límites y supuestos explícitos.
3. **Auditoría documental y de memoria:** todos los entregables `D01`–`D06` en estado `completed_pending_owner_review` / `approved` según trazabilidad, `DECISION_LOG.md` estrictamente inmutable (*append-only*), y puntos de decisión asumidos listados en `02_CONTEXT/OPEN_QUESTIONS.md`.
