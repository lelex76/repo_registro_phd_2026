## La búsqueda — NOTAS ACERCA de reglas a navegación entre espacios

TmaqT pasó de reglas fijas a aprendizaje, (cierta) adaptación y navegación entre espacios de representación.
REGLAS → APRENDIZAJE → ADAPTACIÓN → NAVEGACIÓN



La síntesis FM permanece. Lo que cambia es cómo se representa la interacción.


## Etapa 001 — `main05.py`

**SOM + reglas + FM**
TACTO → REPRESENTACIÓN → REGLAS → SÍNTESIS



*¿Qué regla produce este sonido?*

---

## Etapa 002 — `TmaqT_00_ML.py`

**SOM + MLP + FM**
TACTO → REPRESENTACIÓN → MLP → SÍNTESIS



MLP congelado durante la interacción.

*¿Qué relación puede aprender el sistema?*

---

## Etapa 003 — `TmaqT_01_adaptativo.py`

**SOM adaptativo + MLP congelado + FM + WAV**
SOM adaptativo → MLP fijo → FM + WAV



El SOM se actualiza, el MLP no.

*¿Cómo puede el sistema adaptarse a la interacción?*

---

## Etapa actual — Navegación entre espacios

Cuatro espacios articulados:

| Espacio | Origen | Representa |
|---|---|---|
| Táctil | SOM | estados táctiles |
| Paramétrico | MLP | 6 parámetros de síntesis |
| Acústico FM | PCA 600 FM | relaciones acústicas FM |
| Acústico WAV | PCA 3 WAVs | relaciones acústicas WAV |

TACTO → SOM → MLP → FM + WAV → ESPACIOS ACÚSTICOS


*¿Cómo navegar entre espacios de representación a través del tacto?*

---

## Hallazgos

- **Espacio FM estable.** 600 FM + 600 de validación. Correlación de densidad **0.9828**. Correlación de distancias **0.9067**.
- **WAV localizados en el territorio FM:**
  - `01.wav → FM[481]` (0.0077)
  - `03.wav → FM[16]` (0.0780)
  - `06.wav → FM[32]` (0.0207)
- **FM_Z complementa a Y_ML.** No lo reemplaza: le añade una posición.

---

## Sobre "espacio latente"

No todos los espacios son latentes en sentido estricto. Es más preciso hablar de **espacios de representación conectados**, articulados mediante aprendizaje automático. "Latente" se reserva para representaciones aprendidas por un modelo generativo.

---

## Estado
🟢 24 zonas táctiles
🟢 2 × MPR121
🟢 SOM adaptativo
🟢 MLP pre-entrenado
🟢 6 parámetros sonoros
🟢 4 voces FM
🟢 mezcla WAV 01/03/06
🟢 espacio acústico FM
🟢 espacio acústico WAV
🟢 proyección Y_ML → FM_Z
🔜 sonificación de espacios
🔜 3 sensores Doppler


## Próximos pasos

sonificar los espacios. Posición y trayectoria → parámetros sonoros.
ESPACIO → posición → mapeo → SONIDO

navegación en tiempo real.
SONIFICACIÓN → NAVEGACIÓN → INTERACCIÓN


## Las cuatro preguntas
001 ¿Qué regla produce este sonido?
002 ¿Qué relación puede aprender el sistema?
003 ¿Cómo puede el sistema adaptarse?
ACTUAL ¿Cómo navegar entre espacios de representación?


## Síntesis
PERCEPCIÓN → REPRESENTACIÓN → APRENDIZAJE → ADAPTACIÓN
→ TRANSFORMACIÓN → NAVEGACIÓN → SONIDO



La FM no desaparece. Permanece como mecanismo estable sobre el cual se experimentan nuevas relaciones entre tacto, aprendizaje automático, espacios de representación y sonido.
