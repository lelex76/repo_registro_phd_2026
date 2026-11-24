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

### Flujo general del sistema

La arquitectura de TMAQT v15 organiza el procesamiento en una cadena que transforma el contacto físico en una 
representación gestual y, posteriormente, en una respuesta sonora.

**Contacto táctil → Captura sensora → Representación del gesto → Espacio latente 3D → Navegación y mezcla 
sonora → Salida de audio**

El sistema se compone de las siguientes etapas:

1. **Captura táctil:** dos controladores MPR121 registran el contacto en 24 zonas capacitivas distribuidas en la 
superficie textil.

2. **Representación gestual:** las señales capturadas se procesan para construir un vector de 20 dimensiones 
(`gesto_20d`), que resume características del gesto.

3. **Reducción dimensional:** `HybridReducer` transforma la representación de 20 dimensiones en un espacio de tres 
dimensiones (`z_wav`).

4. **Navegación sonora:** `SonicNavigator` y `LatentSonifier` utilizan la representación tridimensional para 
relacionar la trayectoria gestual con 27 archivos WAV y generar mezclas sonoras.

5. **Control de respuesta:** el parámetro `gate` regula la intensidad sonora en relación con el contacto, 
aumentando al tocar y disminuyendo al soltar.

6. **Adaptación:** `GrowingNeuralGas` (GNG) actualiza la organización de las representaciones gestuales a partir 
del uso, explorando relaciones que pueden modificarse con la experiencia.
