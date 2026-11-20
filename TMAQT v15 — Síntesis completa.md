# TMAQT v15 — Síntesis completa

## Qué es

Sistema que **convierte gestos táctiles en sonido continuo y expresivo**:

- **Sensor:** MPR121 (24 zonas, 2 chips).
- **Gesto:** se resume en un vector de 20 números (`gesto_20d`).
- **Reducción:** 20D → 3D (`z_wav`) con `HybridReducer`.
- **Sonido:** 27 WAVs mezclados según `z_wav` (`LatentSonifier`).
- **Volumen:** `gate` sube al tocar, baja al soltar.
- **Aprendizaje:** `GrowingNeuralGas` (GNG) refina el gesto con el uso.

---

## Por qué se redujo 20D → 3D (breve)

Se redujo **a propósito**, por tres razones:

1. **Redundancia en las 20D:** muchas dimensiones miden lo mismo (duplicados de posición, derivadas). No aportan información nueva.
2. **PCA busca lo importante:** el `HybridReducer` usa PCA, que encuentra las **direcciones de mayor varianza**. Si las 3 primeras explican >80%, se pierde poco.
3. **Compatibilidad con el sistema:** el `SonicNavigator`, el `LatentSonifier` y el GNG trabajan en **3D**. Reducir a 3D es lo que permite que todo encaje.

**No es una pérdida arbitraria:** es una **compresión inteligente** que mantiene la riqueza útil y descarta ruido/redundancia.

---

## Arquitectura
