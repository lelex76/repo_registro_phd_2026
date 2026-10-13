Baseline 01 — Acoplamiento gestual-sonoro en espacio latente
Este baseline implementa Edge AI local en Raspberry Pi 4: gesto → espacio latente → sonido. Sin clasificación, sin presets, sin nube.

Flujo
text
24 zonas táctiles (MPR121)
        ↓
   Gesture Encoder (TFLite)
        ↓
        zG  (3D → 10D → 20D según versión)
        ↓
  Perturbación del estado latente
        ↓
   ┌────────────┴────────────┐
  zFM                       zWAV
   ↓                          ↓
FM Decoder              15 WAVs
   ↓                          ↓
 sonido                  sonido continuo
Tres espacios latentes
Espacio	Aprendido de	Dimensión
zG	gesto táctil	3D / 10D / 20D
zFM	representación sonora FM	3D
zWAV	audio WAV directo	3D
No son equivalentes. Eso es lo interesante: poner en relación representaciones de distinta naturaleza.

Estado persistente
El gesto no selecciona un sonido. Perturba un estado latente que persiste.

text
TOUCH    → el estado se desplaza
TOUCH    → sigue desplazándose
NO TOUCH → el estado queda donde llegó
TOUCH    → nueva perturbación desde ahí
Lo que todavía no es aprendido
Los tres espacios son aprendidos. Pero la relación entre ellos está definida a mano: ganancias, posición, velocidad, suavizado, límites.

text
zG ──[regla paramétrica]──→ zFM
 │
 └──[regla paramétrica]──→ zWAV
El acoplamiento gesto → sonido todavía no emerge de los datos.

Pregunta abierta
¿Qué cambia cuando la relación entre zG y los espacios sonoros deja de definirse explícitamente y pasa a aprenderse de la relación temporal continua?

Edge AI
Todo corre local en la Raspberry Pi 4. Sin dependencia remota durante la interacción. El textil funciona como sistema autónomo.

Versiones:

main_v12.py — 20D, 15 WAVs, co-adaptación (--rehearse)

main_v12_10d.py — 10D, misma lógica

main_v12_3d.py — 3D, versión base

Modos:

--perform — matrices congeladas

--rehearse — W_map se adapta durante el uso
