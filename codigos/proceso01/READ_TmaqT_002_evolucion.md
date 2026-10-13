## La búsqueda — de reglas a navegación entre espacios

Este documento resume el arco de investigación de TmaqT: cómo el sistema pasó de reglas fijas a aprendizaje, adaptación y, finalmente, navegación entre espacios de representación.

## El desplazamiento general

```text
REGLAS  →  APRENDIZAJE  →  ADAPTACIÓN  →  NAVEGACIÓN ENTRE ESPACIOS
La síntesis FM permanece como motor sonoro. Lo que cambia es cómo se representa la interacción antes de llegar al sonido.

Etapa 001 — main05.py
SOM + reglas + FM

El tejido se vuelve territorio táctil-sonoro. La relación tacto → sonido está definida por reglas explícitas.


TACTO → REPRESENTACIÓN → REGLAS → SÍNTESIS
Pregunta: ¿qué regla produce este sonido?

Etapa 002 — TmaqT_00_ML.py
SOM + MLP + FM

Aparece el aprendizaje automático. Un MLP pre-entrenado aprende la transformación X_ML → Y_ML.


TACTO → REPRESENTACIÓN → MLP → SÍNTESIS
El MLP queda congelado durante la interacción.

Pregunta: ¿qué relación puede aprender el sistema?

Etapa 003 — TmaqT_01_adaptativo.py
SOM adaptativo + MLP congelado + FM + WAV

La representación táctil se adapta durante el uso. El SOM se actualiza; el MLP no.

SOM adaptativo → MLP fijo → FM + WAV
Pregunta: ¿cómo puede el sistema adaptarse a la interacción?

Etapa actual — Navegación entre espacios
El sistema ya no produce una correspondencia única. Articula cuatro espacios:

Espacio	Origen	Qué representa
Topológico táctil	SOM	organización de estados táctiles
Paramétrico sonoro	MLP	6 parámetros de síntesis
Acústico FM	PCA sobre 600 sonidos FM	relaciones acústicas FM
Acústico WAV	PCA sobre 3 WAVs	relaciones acústicas WAV

TACTO
  ↓
SOM ADAPTATIVO
  ↓
ESPACIO TÁCTIL
  ↓
MLP
  ↓
ESPACIO PARAMÉTRICO
  ↓
FM + WAV
  ↓
ESPACIOS ACÚSTICOS
Pregunta: ¿cómo puede el usuario navegar entre diferentes espacios de representación a través del tacto?

Lo que se aprendió en el camino
El espacio acústico FM es estable. Se construyó con 600 sonidos FM y se validó con otros 600. La correlación de densidad entre ambos fue 0.9828. La correlación de distancias entre el espacio original y su proyección 2D fue 0.9067. Eso permite usarlo como referencia territorial.

Los WAV se pueden localizar dentro del territorio FM. Aunque los dos espacios se construyeron por separado, se pueden comparar usando una referencia común:


01.wav → FM[481]  (distancia 0.0077)
03.wav → FM[16]   (distancia 0.0780)
06.wav → FM[32]   (distancia 0.0207)

Eso abre la posibilidad de tratar FM y WAV como territorios conectados, sin asumir que son un único espacio matemático.

FM_Z complementa a Y_ML. El MLP produce parámetros sonoros. FM_Z localiza ese resultado dentro del territorio acústico FM. No lo reemplaza: le añade una posición.

Sobre la noción de "espacio latente"
No todos los espacios que usa TmaqT son latentes en sentido estricto. Es más preciso hablar de:

espacios de representación conectados — táctiles, paramétricos y acústicos — articulados mediante aprendizaje automático.

El término "latente" se reserva para representaciones aprendidas por un modelo generativo.

Arquitectura actual

                    TEJIDO
                      │
                      ▼
                24 ZONAS TÁCTILES
                      │
                      ▼
                MEMORIA TEMPORAL
                      │
                      ▼
                 SOM ADAPTATIVO
                      │
                      ▼
                 ESPACIO TÁCTIL 2D
                      │
                      ▼
                     X_ML
                      │
                      ▼
                MLP PRE-ENTRENADO
                      │
                      ▼
                     Y_ML
         ┌────────────┴────────────┐
         ▼                         ▼
    SÍNTESIS FM                FM_Z
     4 VOCES                     │
         │                       ▼
         │                ESPACIO FM 2D
         │
         └─────────────┐
                       │
        POSICIÓN SOM   │
               │       │
               ▼       │
        MEZCLA WAV     │
        01 / 03 / 06   │
               │       │
               ▼       │
           AUDIO ◄─────┘


Estado actual

🟢 24 zonas táctiles
🟢 2 × MPR121
🟢 memoria temporal
🟢 SOM adaptativo
🟢 MLP pre-entrenado
🟢 6 parámetros sonoros
🟢 4 voces FM
🟢 mezcla WAV 01/03/06
🟢 espacio acústico FM
🟢 espacio acústico WAV
🟢 proyección Y_ML → FM_Z
🟢 relación WAV → vecinos FM
🔜 integración experimental entre territorios
🔜 3 sensores Doppler
Próxima evolución
Corto plazo — Sonificación de los espacios.

Los espacios ya están construidos y caracterizados. Falta hacerlos audibles: transformar posición y desplazamiento dentro de cada espacio en parámetros sonoros.

ESPACIO → posición / trayectoria → mapeo → SONIDO
Se sonificarán primero el espacio táctil, el acústico WAV y el acústico FM.

Mediano plazo — Navegación en tiempo real.

El gesto corporal permitirá recorrer estos espacios y producir transformación sonora continua.


SONIFICACIÓN → NAVEGACIÓN → INTERACCIÓN EN TIEMPO REAL
Largo plazo — Multimodalidad.

Incorporación de 3 sensores Doppler como segunda modalidad perceptiva.

text
TACTO + DOPPLER → ESTADO MULTIMODAL → SOM → ML → SONIDO
El objetivo es estudiar cómo distintas modalidades convergen en una representación común y cómo esa representación se usa para navegar espacios sonoros.

Las cuatro preguntas del arco
text
ETAPA 001     ¿Qué regla produce este sonido?
ETAPA 002     ¿Qué relación puede aprender el sistema?
ETAPA 003     ¿Cómo puede el sistema adaptarse a la interacción?
ETAPA ACTUAL  ¿Cómo puede el usuario navegar entre diferentes
              espacios de representación a través del tacto?
Síntesis conceptual
El proyecto evoluciona desde un sistema basado en reglas hacia uno que combina:


PERCEPCIÓN → REPRESENTACIÓN → APRENDIZAJE → ADAPTACIÓN
           → TRANSFORMACIÓN → NAVEGACIÓN → SONIDO
La FM no desaparece. Permanece como mecanismo estable sobre el cual se experimentan nuevas relaciones entre tacto, aprendizaje automático, espacios de representación y comportamiento sonoro.




Si lo pones como `README.md` dentro de `proceso01/`, aparecerá como portada de esa carpeta.
