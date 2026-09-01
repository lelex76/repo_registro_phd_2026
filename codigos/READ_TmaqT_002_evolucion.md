# Evolución de TmaqT — de reglas a aprendizaje y adaptación

La evolución de TmaqT se desarrolla en tres etapas. En todas ellas se mantiene la misma base material y sonora —24 zonas táctiles, memoria temporal, SOM y síntesis FM—, mientras que progresivamente cambia la forma en que el sistema relaciona la interacción táctil con el sonido.

La transición fundamental es:

```text
REGLAS
  ↓
APRENDIZAJE
  ↓
ADAPTACIÓN
```

---

## Etapa 001 — `main05.py`

### SOM + reglas + FM

La primera arquitectura establece el tejido como un territorio táctil-sonoro distribuido.

```text
24 zonas táctiles
        ↓
memoria gestual
        ↓
SOM 6×4
        ↓
posición / zona / memoria
        ↓
reglas de mapeo
        ↓
parámetros FM
        ↓
FM × 4 voces
        ↓
SONIDO
```

El SOM organiza las configuraciones táctiles en un espacio topológico de 6×4. La relación entre esa representación y los parámetros sonoros se define mediante reglas explícitas.

La síntesis FM constituye el motor sonoro y permite mantener hasta cuatro voces simultáneas, con diferenciación espacial, ataque, release y dinámica temporal.

En esta etapa, por tanto, la correspondencia entre interacción y sonido está principalmente **diseñada manualmente**.

---

# Etapa 002 — `TmaqT_00_ML.py`

### SOM + MLP + FM con modelos aprendidos congelados

La segunda etapa incorpora aprendizaje automático en la capa de mapeo.

La arquitectura pasa a ser:

```text
24 zonas táctiles
        ↓
memoria gestual
        ↓
SOM 6×4
        ↓
representación
        ↓
MLP
        ↓
parámetros sonoros
        ↓
FM × 4 voces
        ↓
SONIDO
```

La diferencia principal respecto de `main05.py` es que la relación entre la representación de la interacción y los parámetros sonoros ya no está completamente definida mediante reglas.

El MLP aprende previamente una relación:

```text
X_ML → Y_ML
```

donde `X_ML` corresponde a las características utilizadas para representar la interacción y `Y_ML` a los parámetros sonoros deseados.

El modelo se entrena fuera de la Raspberry Pi y posteriormente se exporta para su ejecución local.

### Inferencia congelada

Durante la interacción:

```text
TACTO
  ↓
SOM
  ↓
X_ML
  ↓
MLP entrenado
  ↓
Y_ML
  ↓
FM
```

No se realiza entrenamiento del MLP durante la ejecución.

El modelo funciona como una capa de inferencia que transforma la representación táctil en parámetros para el sintetizador.

La síntesis FM continúa siendo la responsable de producir el audio. El ML no genera directamente la señal sonora.

La arquitectura puede resumirse como:

```text
INTERACCIÓN
     ↓
REPRESENTACIÓN
     ↓
APRENDIZAJE
     ↓
SÍNTESIS
```

---

# Etapa 003 — `TmaqT_01_adaptativo`

### SOM adaptativo + MLP + FM

La tercera etapa introduce una diferencia conceptual importante: el sistema deja de ser completamente estático durante la interacción.

La arquitectura mantiene el flujo general:

```text
24 zonas táctiles
        ↓
memoria gestual
        ↓
SOM
        ↓
representación
        ↓
MLP
        ↓
parámetros sonoros
        ↓
FM × 4 voces
        ↓
SONIDO
```

pero ahora el **SOM incorpora una actualización adaptativa durante la interacción**.

El objetivo no es volver a entrenar continuamente todo el modelo ni modificar el MLP en tiempo real. La adaptación se concentra en la organización de la representación táctil.

Conceptualmente:

```text
                 ┌───────────────┐
                 │   INTERACCIÓN │
                 └───────┬───────┘
                         ↓
                  memoria temporal
                         ↓
                     SOM 6×4
                         ↕
                  actualización
                   adaptativa
                         ↓
                  representación
                         ↓
                     MLP fijo
                         ↓
               parámetros sonoros
                         ↓
                      FM × 4
                         ↓
                       AUDIO
```

De esta manera, el sistema conserva un **MLP aprendido previamente, cuyos parámetros permanecen congelados durante la interacción**, mientras permite que la organización de la información táctil se modifique progresivamente a partir de la interacción.

### ¿Qué significa aquí “adaptativo”?

No significa que todo el sistema esté aprendiendo de nuevo.

La distinción es:

```text
MLP
→ aprendido previamente
→ permanece congelado


SOM
→ aprendido inicialmente
→ puede actualizarse durante la interacción
```

Por tanto:

```text
TmaqT_00_ML

SOM fijo → MLP fijo → FM


TmaqT_01_adaptativo

SOM adaptativo → MLP fijo → FM
```

Esta diferencia permite introducir una primera forma de **adaptación del sistema sin convertirlo en un sistema de aprendizaje online completo**.

---

# Evolución conceptual

Las tres etapas pueden entenderse como una progresión:

```text
ETAPA 001
main05.py

TACTO
  ↓
REPRESENTACIÓN
  ↓
REGLAS
  ↓
SONIDO


ETAPA 002
TmaqT_00_ML.py

TACTO
  ↓
REPRESENTACIÓN
  ↓
MODELO APRENDIDO
  ↓
SONIDO


ETAPA 003
TmaqT_01_adaptativo

TACTO
  ↓
REPRESENTACIÓN
  ↕
ADAPTACIÓN
  ↓
MODELO APRENDIDO
  ↓
SONIDO
```

La incorporación progresiva de aprendizaje no reemplaza la lógica sonora existente. El sistema mantiene la síntesis FM como mecanismo de generación de sonido y utiliza el aprendizaje automático como una capa intermedia entre la interacción y la síntesis.

---

# Qué permanece constante

A lo largo de las tres etapas se mantiene una misma infraestructura:

* 24 zonas táctiles textiles.
* Dos sensores MPR121.
* Procesamiento temporal de la interacción.
* Memoria gestual.
* SOM de 6×4.
* Hasta cuatro voces simultáneas.
* Diferenciación espacial.
* Ataque y release.
* Síntesis FM.
* Ejecución local en Raspberry Pi.

Lo que cambia es principalmente la **relación entre la interacción y el sonido**:

```text
main05
REGLAS


        ↓


TmaqT_00_ML
APRENDIZAJE


        ↓


TmaqT_01_adaptativo
ADAPTACIÓN
```

---

# Estado de la arquitectura actual

La arquitectura de TmaqT puede resumirse actualmente como:

```text
                    TEJIDO TEXTIL
                          │
                          ▼
                    24 ZONAS
                          │
                          ▼
                    MPR121 × 2
                          │
                          ▼
                 MEMORIA GESTUAL
                          │
                          ▼
                    SOM 6 × 4
                          ↕
                 ADAPTACIÓN ONLINE
                          │
                          ▼
                  REPRESENTACIÓN
                          │
                          ▼
                  MLP PRE-ENTRENADO
                          │
                          ▼
                PARÁMETROS SONOROS
                          │
                          ▼
                     FM × 4
                          │
                          ▼
                       AUDIO
```

Esta etapa establece una arquitectura compacta de:

> **tacto → memoria → representación adaptativa → inferencia aprendida → síntesis**

La adaptación permanece deliberadamente acotada: el MLP no se modifica durante la ejecución y la síntesis FM se conserva como motor sonoro.

Esto permite estudiar una primera forma de relación entre **interacción táctil, representación computacional y comportamiento adaptativo**, antes de incorporar nuevas modalidades perceptivas.

---

# Perspectiva de investigación

La progresión de TmaqT no consiste simplemente en añadir capas de machine learning.

El desplazamiento conceptual es:

```text
¿QUÉ REGLA DEBE PRODUCIR ESTE SONIDO?
                 ↓
¿QUÉ RELACIÓN PUEDE APRENDER EL SISTEMA?
                 ↓
¿CÓMO PUEDE EL SISTEMA ADAPTARSE A LA INTERACCIÓN?
```

Así, el prototipo pasa de ser un instrumento cuyo comportamiento está principalmente especificado por reglas, a un sistema en el que parte de la relación entre tacto y sonido es aprendida y, posteriormente, una parte de su representación puede adaptarse durante la interacción.

La **síntesis FM permanece estable a lo largo de esta evolución**: lo que evoluciona es la capa que determina cómo la interacción táctil llega hasta sus parámetros.

