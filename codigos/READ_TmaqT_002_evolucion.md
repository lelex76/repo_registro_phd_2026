# Evolución de TmaQT — de reglas a aprendizaje, adaptación y espacios acústicos

La evolución de **TmaQT** puede entenderse como un desplazamiento progresivo desde relaciones diseñadas explícitamente hacia relaciones aprendidas y, posteriormente, hacia una representación adaptable de la interacción.

La transición general es:

```text
REGLAS
  ↓
APRENDIZAJE
  ↓
ADAPTACIÓN
  ↓
NAVEGACIÓN ENTRE ESPACIOS
```

La síntesis FM permanece como uno de los principales mecanismos de generación sonora. Lo que evoluciona es la manera en que la interacción táctil se representa y se transforma antes de llegar al sonido.

---

# Etapa 001 — `main05.py`

## SOM + reglas + síntesis FM

La primera arquitectura establece el tejido como un territorio táctil-sonoro.

De manera general:

```text
24 zonas táctiles
        ↓
memoria / estado gestual
        ↓
SOM 6×4
        ↓
posición / estado táctil
        ↓
reglas de mapeo
        ↓
parámetros FM
        ↓
FM × 4 voces
        ↓
SONIDO
```

En esta etapa, la relación entre la representación de la interacción y los parámetros sonoros está principalmente definida mediante **reglas explícitas**.

El SOM organiza diferentes configuraciones táctiles en un espacio bidimensional, mientras que la lógica de mapeo determina cómo esas posiciones se convierten en parámetros del sintetizador.

La síntesis FM actúa como motor de generación sonora.

La arquitectura puede resumirse como:

```text
TACTO
  ↓
REPRESENTACIÓN
  ↓
REGLAS
  ↓
SÍNTESIS
```

---

# Etapa 002 — `TmaqT_00_ML.py`

## SOM + MLP + FM

La segunda etapa introduce **aprendizaje automático en la transformación entre interacción y sonido**.

La arquitectura pasa a ser:

```text
24 zonas táctiles
        ↓
memoria / representación
        ↓
SOM
        ↓
X_ML
        ↓
MLP
        ↓
Y_ML
        ↓
parámetros sonoros
        ↓
FM × 4 voces
        ↓
SONIDO
```

La diferencia fundamental respecto de la etapa anterior es que parte de la relación entre entrada y salida deja de estar especificada únicamente mediante reglas.

El MLP aprende previamente una transformación:

```text
X_ML → Y_ML
```

donde `X_ML` representa el estado utilizado como entrada del modelo y `Y_ML` representa los parámetros sonoros deseados.

El modelo se entrena previamente y posteriormente se utiliza para inferencia en la Raspberry Pi.

### Inferencia congelada

Durante la interacción:

```text
TACTO
  ↓
REPRESENTACIÓN
  ↓
X_ML
  ↓
MLP
  ↓
Y_ML
  ↓
FM
```

El MLP no se modifica durante la ejecución.

Por tanto, en esta etapa:

```text
REPRESENTACIÓN → MODELO APRENDIDO → SÍNTESIS
```

---

# Etapa 003 — `TmaqT_01_adaptativo.py`

## SOM adaptativo + MLP + FM + WAV

La tercera etapa introduce una diferencia conceptual importante: **la representación táctil puede adaptarse durante la interacción**.

La arquitectura actual es:

```text
24 zonas táctiles
        ↓
memoria temporal
        ↓
SOM adaptativo
        ↓
espacio topológico táctil
        ↓
X_ML
        ↓
MLP
        ↓
Y_ML
        ↓
parámetros sonoros
        ↓
FM × 4 voces
```

El MLP permanece congelado durante la interacción.

La adaptación se concentra en el SOM:

```text
SOM
→ representación aprendida
→ actualización durante la interacción
```

mientras:

```text
MLP
→ aprendido previamente
→ congelado durante la ejecución
```

Por tanto:

```text
TmaqT_00_ML

SOM fijo → MLP fijo → FM


TmaqT_01_adaptativo

SOM adaptativo → MLP fijo → FM
```

La adaptación no implica volver a entrenar todo el sistema. Implica permitir que la organización del espacio táctil se modifique progresivamente a partir de la interacción.

---

# 1. Del espacio táctil al espacio sonoro

La versión `TmaqT_01_adaptativo` introduce además una separación entre distintos tipos de representación.

El flujo puede entenderse como:

```text
TACTO
  ↓
MEMORIA TEMPORAL
  ↓
SOM ADAPTATIVO
  ↓
ESPACIO TOPOLÓGICO TÁCTIL
  ↓
MLP
  ↓
ESPACIO PARAMÉTRICO SONORO
  ↓
SÍNTESIS
```

Esto significa que el SOM no es todavía un espacio sonoro.

Es principalmente una representación de la **organización de los estados táctiles**.

El MLP establece entonces la transformación entre esa representación y los parámetros utilizados por la síntesis.

---

# 2. Espacio acústico FM

Además de la síntesis en tiempo real, TmaQT incorpora un territorio acústico construido previamente a partir de **600 sonidos FM sintéticos**.

Cada sonido fue representado mediante características acústicas y posteriormente proyectado a dos dimensiones mediante PCA.

```text
600 sonidos FM
      ↓
características acústicas
      ↓
normalización
      ↓
PCA
      ↓
ESPACIO ACÚSTICO FM 2D
```

Este espacio se almacena en:

```text
TmaqT_FM_latente.npz
```

La representación contiene:

```text
Z            → coordenadas 2D
parameters   → parámetros FM
features     → características acústicas
```

### Estabilidad

Se realizó una segunda prueba independiente con otros 600 sonidos FM y se proyectó sobre la misma base PCA.

La correlación de densidad entre ambas distribuciones fue:

```text
0.9828
```

Esto indica una alta estabilidad de la organización espacial frente al muestreo.

La correlación de distancias entre el espacio acústico original y la representación 2D fue:

```text
0.9067
```

Estos resultados permiten utilizar este espacio como una **referencia territorial para interpretar los sonidos FM producidos por el sistema**.

---

# 3. `FM_Z` — posición del resultado sonoro

Cuando el MLP produce un conjunto de parámetros sonoros:

```text
Y_ML
  ↓
parámetros FM
```

TmaQT puede localizar ese resultado aproximadamente dentro del territorio acústico FM:

```text
Y_ML
  ↓
búsqueda de referencia acústica
  ↓
FM_Z
  ↓
posición 2D
```

Por ejemplo:

```text
Y_ML
→ frecuencia
→ modulación
→ índice
→ timbre
→ panorama
→ amplitud

        ↓

      FM_Z
       X Y
```

`FM_Z` no reemplaza a `Y_ML`.

Es una **representación espacial complementaria** que permite interpretar dónde se encuentra el resultado sonoro dentro del territorio acústico FM.

---

# 4. Espacio acústico de los WAV

Los materiales WAV utilizados por TmaQT también fueron analizados acústicamente.

Actualmente se consideran tres materiales:

```text
01.wav
03.wav
06.wav
```

Cada uno se representa mediante características acústicas y una proyección 2D:

```text
WAV
 ↓
características acústicas
 ↓
normalización
 ↓
PCA
 ↓
ESPACIO ACÚSTICO WAV 2D
```

Resultado actual:

```text
01.wav → (-2.056,  2.018)
03.wav → (-1.707, -2.146)
06.wav → ( 3.763,  0.129)
```

Este espacio contiene actualmente tres puntos y funciona como una primera representación acústica de los materiales WAV.

El resultado se almacena en:

```text
TmaqT_WAV_latente.npz
```

---

# 5. Relación entre WAV y FM

Los dos espacios acústicos se construyeron por separado:

```text
ESPACIO WAV
3 materiales
     ↓
PCA 2D


ESPACIO FM
600 sonidos
     ↓
PCA 2D
```

Por lo tanto, **no son matemáticamente el mismo espacio**.

Sin embargo, pueden compararse utilizando una referencia común.

En esa comparación se localizaron los WAV respecto del territorio FM.

Los vecinos FM más cercanos fueron:

```text
01.wav → FM[481] → distancia 0.0077
03.wav → FM[16]  → distancia 0.0780
06.wav → FM[32]  → distancia 0.0207
```

Esto permite establecer una relación experimental entre los materiales WAV y regiones concretas del territorio acústico FM.

Conceptualmente:

```text
01.wav ─────→ FM[481]
03.wav ─────→ FM[16]
06.wav ─────→ FM[32]
```

Esta relación abre la posibilidad de estudiar los materiales WAV y la síntesis FM como **territorios acústicos conectados**, sin asumir que constituyen un único espacio matemático.

---

# 6. FM + WAV

La salida sonora actual combina dos mecanismos:

```text
                    TACTO
                      │
                      ▼
                SOM ADAPTATIVO
                 /          \
                /            \
               ▼              ▼
             MLP           POSICIÓN SOM
              │                │
              ▼                ▼
        PARÁMETROS FM       MEZCLA WAV
              │             01 / 03 / 06
              ▼                │
        SÍNTESIS FM             │
          4 voces                │
               \                /
                \              /
                 └──────┬─────┘
                        ▼
                      AUDIO
```

La síntesis FM responde a los parámetros producidos por el MLP.

Los materiales WAV se mezclan espacialmente según la posición del estado táctil dentro del SOM.

Así, el sistema mantiene simultáneamente:

```text
ESPACIO TÁCTIL
        +
ESPACIO PARAMÉTRICO
        +
ESPACIO ACÚSTICO FM
        +
ESPACIO ACÚSTICO WAV
```

---

# 7. De un mapeo a una navegación entre espacios

La evolución de TmaQT puede resumirse ahora como:

```text
ETAPA 001
REGLAS

TACTO
 ↓
REPRESENTACIÓN
 ↓
REGLAS
 ↓
SONIDO


ETAPA 002
APRENDIZAJE

TACTO
 ↓
REPRESENTACIÓN
 ↓
MLP
 ↓
SONIDO


ETAPA 003
ADAPTACIÓN

TACTO
 ↓
SOM ADAPTATIVO
 ↓
REPRESENTACIÓN
 ↓
MLP
 ↓
SONIDO


ETAPA ACTUAL
NAVEGACIÓN ENTRE ESPACIOS

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
```

La transición conceptual puede expresarse como:

> **de definir correspondencias entre tacto y sonido, a aprenderlas, adaptarlas y explorar las relaciones entre diferentes espacios de representación.**

---

# 8. ¿Son “espacios latentes”?

TmaQT actualmente utiliza varios espacios, pero no todos son equivalentes.

### Espacio topológico táctil

Producido por:

```text
SOM
```

Representa la organización de los estados táctiles.

### Espacio paramétrico sonoro

Producido por:

```text
MLP
```

Representa los seis parámetros que controlan la síntesis.

### Espacio acústico FM

Producido por:

```text
características acústicas
→ PCA
```

Representa relaciones acústicas entre sonidos FM sintéticos.

### Espacio acústico WAV

Producido por:

```text
características acústicas
→ PCA
```

Representa relaciones acústicas entre materiales WAV.

Por esta razón, es más preciso hablar de:

> **espacios de representación conectados**

o:

> **espacios táctiles, paramétricos y acústicos articulados mediante aprendizaje automático.**

El término **“espacio latente”** puede utilizarse en contextos específicos donde la representación corresponda efectivamente a un modelo generativo o a una representación latente aprendida.

---

# 9. Arquitectura actual

La arquitectura experimental actual puede resumirse así:

```text
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
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
         SÍNTESIS FM                FM_Z
          4 VOCES                     │
              │                       ▼
              │                ESPACIO FM 2D
              │
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
```

---

# 10. Estado actual

```text
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
```

---

# 11. Próxima evolución: multimodalidad

La siguiente etapa prevista incorpora **3 sensores Doppler** como una segunda modalidad perceptiva.

La arquitectura futura será:

```text
                 TACTO                  DOPPLER
              24 zonas                    3
                   │                       │
                   └──────────┬────────────┘
                              ▼
                       ESTADO MULTIMODAL
                              │
                              ▼
                       SOM / ESPACIO
                         DE REPRESENTACIÓN
                              │
                              ▼
                             ML
                              │
                              ▼
                      PARÁMETROS SONOROS
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                   FM              OTROS MATERIALES
                    │                   │
                    └─────────┬─────────┘
                              ▼
                            AUDIO
```

La incorporación del Doppler permitirá estudiar cómo diferentes modalidades perceptivas pueden converger en una representación común y cómo esa representación puede utilizarse para navegar espacios sonoros.

La síntesis FM permanece como parte central del sistema.

---

# Síntesis conceptual

La evolución de TmaQT puede resumirse en tres preguntas:

```text
ETAPA 001
¿Qué regla produce este sonido?


ETAPA 002
¿Qué relación puede aprender el sistema?


ETAPA 003
¿Cómo puede el sistema adaptarse a la interacción?


ETAPA ACTUAL
¿Cómo puede el usuario navegar entre
diferentes espacios de representación
a través del tacto?
```

El proyecto evoluciona así desde un sistema basado principalmente en **reglas**, hacia un sistema que combina:

```text
PERCEPCIÓN
   ↓
REPRESENTACIÓN
   ↓
APRENDIZAJE
   ↓
ADAPTACIÓN
   ↓
TRANSFORMACIÓN
   ↓
NAVEGACIÓN
   ↓
SONIDO
```

La síntesis FM no desaparece en esta evolución. Por el contrario, permanece como un mecanismo estable sobre el cual se experimentan nuevas relaciones entre **tacto, aprendizaje automático, espacios de representación y comportamiento sonoro**.

---------------------------------------


## Próxima etapa — Sonificación de los espacios de representación

Una vez construidos y caracterizados los diferentes espacios de representación, la siguiente etapa consiste en estudiar su **sonificación directa**.

El objetivo es transformar la **posición y el desplazamiento dentro de cada espacio** en parámetros sonoros.

```text
ESPACIO
   ↓
posición / trayectoria
   ↓
mapeo sonoro
   ↓
parámetros
   ↓
SONIDO
```

Esta etapa permitirá explorar los espacios no solamente mediante visualización, sino también mediante **escucha**.

Se estudiarán inicialmente:

```text
ESPACIO TOPOLÓGICO TÁCTIL
          ↓
     sonificación


ESPACIO ACÚSTICO WAV
          ↓
     sonificación


ESPACIO ACÚSTICO FM
          ↓
     sonificación
```

La etapa posterior será la **navegación en tiempo real**, donde el gesto corporal permitirá recorrer estos espacios y producir una transformación sonora continua.

```text
SONIFICACIÓN
      ↓
NAVEGACIÓN
      ↓
INTERACCIÓN EN TIEMPO REAL
```

Esta progresión permitirá avanzar desde la **construcción y representación de los espacios** hacia su **exploración perceptiva mediante sonido**.
