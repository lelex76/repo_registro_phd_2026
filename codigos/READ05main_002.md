### Etapa 002 — `TmaqT_00_ML.py`

**SOM + MLP + FM con modelos de aprendizaje congelados**

Esta etapa parte de la arquitectura desarrollada en `main05.py` y añade una nueva capa de aprendizaje.

La diferencia principal es que el sistema deja de utilizar únicamente reglas definidas manualmente para relacionar el espacio táctil con los parámetros sonoros.

En `TmaqT_00_ML.py`, el flujo pasa a ser:

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

El **SOM continúa organizando las configuraciones táctiles**, pero ahora su salida alimenta un **MLP (Multi-Layer Perceptron)** que ha aprendido previamente relaciones entre las características de entrada y los parámetros de síntesis.

### ¿Qué cambia respecto a `main05.py`?

En `main05.py`, la relación entre interacción y síntesis se construye principalmente mediante reglas:

```text
GESTO
  ↓
SOM
  ↓
posición
  +
zona
  +
memoria
  ↓
parámetros FM
  ↓
sonido
```

En `TmaqT_00_ML.py`, parte de estas relaciones son aprendidas:

```text
GESTO
  ↓
SOM
  ↓
características
  ↓
MLP aprendido
  ↓
parámetros sonoros
  ↓
FM
  ↓
sonido
```

Esto permite que la correspondencia entre interacción y sonido no tenga que estar definida completamente mediante reglas explícitas.

### Modelos congelados

Los modelos se entrenan previamente y posteriormente se exportan a la Raspberry Pi.

Durante la interacción no se realiza aprendizaje.

Se utilizan tres archivos:

```text
TmaqT_SOM.npz
TmaqT_ML_model.npz
TmaqT_ML_parameters.npz
```

El SOM tiene una estructura:

```text
6 × 4 × 24
```

y el MLP:

```text
7 → 16 → 16 → 6
```

Los parámetros de normalización utilizados durante el entrenamiento también se almacenan para garantizar que la inferencia en la Raspberry utilice la misma escala de datos.

### Diferencia fundamental

La evolución puede resumirse así:

```text
main05
────────────────────────────────

24 zonas
   ↓
memoria
   ↓
SOM
   ↓
reglas de mapeo
   ↓
zona + gesto + posición
   ↓
FM × 4
   ↓
SONIDO


TmaqT_00_ML
────────────────────────────────

24 zonas
   ↓
memoria
   ↓
SOM
   ↓
representación
   ↓
MLP aprendido
   ↓
parámetros sonoros
   ↓
FM × 4
   ↓
SONIDO
```

### Qué permanece

La incorporación de ML **no elimina la arquitectura sonora anterior**.

Se mantienen:

* 24 zonas táctiles.
* Dos MPR121.
* Memoria temporal del gesto.
* SOM como organización espacial.
* Polifonía.
* Hasta 4 voces FM.
* Diferenciación espacial de las zonas.
* Ataque y release de las voces.
* Síntesis FM.
* Ejecución local en Raspberry Pi.

El cambio se produce principalmente en la **capa de mapeo**.

```text
ANTES

interacción
    ↓
reglas
    ↓
síntesis


AHORA

interacción
    ↓
representación
    ↓
modelo aprendido
    ↓
síntesis
```

### Cambio conceptual

Con `main05.py`, el sistema comienza a tratar el tejido como un **territorio sonoro distribuido**, donde múltiples contactos pueden coexistir y generar voces independientes.

Con `TmaqT_00_ML.py`, este territorio incorpora además una relación aprendida entre la interacción y la síntesis.

Por tanto, la evolución no consiste simplemente en **añadir ML**.

Consiste en pasar de:

> **un sistema de mapeo definido mediante reglas**

a:

> **un sistema donde parte de la relación entre gesto, representación y sonido es aprendida a partir de datos.**

La síntesis FM continúa siendo el mecanismo que produce el sonido. El ML funciona como una capa intermedia que transforma la representación de la interacción en parámetros para ese motor sonoro.

### Estado de la arquitectura

La arquitectura final de esta etapa puede resumirse como:

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
                       SOM 6×4
                          │
                          ▼
                  REPRESENTACIÓN
                          │
                          ▼
                  MLP 7→16→16→6
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

Esta etapa establece una arquitectura compacta de **tacto → representación → aprendizaje → síntesis**, ejecutada localmente en Raspberry Pi y preparada para futuras extensiones de la capa perceptiva.

### Etapa 002 — `TmaqT_00_ML.py`

**SOM + MLP + FM con modelos de aprendizaje congelados**

Esta etapa parte de la arquitectura desarrollada en `main05.py` y añade una nueva capa de aprendizaje.

La diferencia principal es que el sistema deja de utilizar únicamente reglas definidas manualmente para relacionar el espacio táctil con los parámetros sonoros.

En `TmaqT_00_ML.py`, el flujo pasa a ser:

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

El **SOM continúa organizando las configuraciones táctiles**, pero ahora su salida alimenta un **MLP (Multi-Layer Perceptron)** que ha aprendido previamente relaciones entre las características de entrada y los parámetros de síntesis.

### ¿Qué cambia respecto a `main05.py`?

En `main05.py`, la relación entre interacción y síntesis se construye principalmente mediante reglas:

```text
GESTO
  ↓
SOM
  ↓
posición
  +
zona
  +
memoria
  ↓
parámetros FM
  ↓
sonido
```

En `TmaqT_00_ML.py`, parte de estas relaciones son aprendidas:

```text
GESTO
  ↓
SOM
  ↓
características
  ↓
MLP aprendido
  ↓
parámetros sonoros
  ↓
FM
  ↓
sonido
```

Esto permite que la correspondencia entre interacción y sonido no tenga que estar definida completamente mediante reglas explícitas.

### Modelos congelados

Los modelos se entrenan previamente y posteriormente se exportan a la Raspberry Pi.

Durante la interacción no se realiza aprendizaje.

Se utilizan tres archivos:

```text
TmaqT_SOM.npz
TmaqT_ML_model.npz
TmaqT_ML_parameters.npz
```

El SOM tiene una estructura:

```text
6 × 4 × 24
```

y el MLP:

```text
7 → 16 → 16 → 6
```

Los parámetros de normalización utilizados durante el entrenamiento también se almacenan para garantizar que la inferencia en la Raspberry utilice la misma escala de datos.

### Diferencia fundamental

La evolución puede resumirse así:

```text
main05
────────────────────────────────

24 zonas
   ↓
memoria
   ↓
SOM
   ↓
reglas de mapeo
   ↓
zona + gesto + posición
   ↓
FM × 4
   ↓
SONIDO


TmaqT_00_ML
────────────────────────────────

24 zonas
   ↓
memoria
   ↓
SOM
   ↓
representación
   ↓
MLP aprendido
   ↓
parámetros sonoros
   ↓
FM × 4
   ↓
SONIDO
```

### Qué permanece

La incorporación de ML **no elimina la arquitectura sonora anterior**.

Se mantienen:

* 24 zonas táctiles.
* Dos MPR121.
* Memoria temporal del gesto.
* SOM como organización espacial.
* Polifonía.
* Hasta 4 voces FM.
* Diferenciación espacial de las zonas.
* Ataque y release de las voces.
* Síntesis FM.
* Ejecución local en Raspberry Pi.

El cambio se produce principalmente en la **capa de mapeo**.

```text
ANTES

interacción
    ↓
reglas
    ↓
síntesis


AHORA

interacción
    ↓
representación
    ↓
modelo aprendido
    ↓
síntesis
```

### Cambio conceptual

Con `main05.py`, el sistema comienza a tratar el tejido como un **territorio sonoro distribuido**, donde múltiples contactos pueden coexistir y generar voces independientes.

Con `TmaqT_00_ML.py`, este territorio incorpora además una relación aprendida entre la interacción y la síntesis.

Por tanto, la evolución no consiste simplemente en **añadir ML**.

Consiste en pasar de:

> **un sistema de mapeo definido mediante reglas**

a:

> **un sistema donde parte de la relación entre gesto, representación y sonido es aprendida a partir de datos.**

La síntesis FM continúa siendo el mecanismo que produce el sonido. El ML funciona como una capa intermedia que transforma la representación de la interacción en parámetros para ese motor sonoro.

### Estado de la arquitectura

La arquitectura final de esta etapa puede resumirse como:

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
                       SOM 6×4
                          │
                          ▼
                  REPRESENTACIÓN
                          │
                          ▼
                  MLP 7→16→16→6
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

Esta etapa establece una arquitectura compacta de **tacto → representación → aprendizaje → síntesis**, ejecutada localmente en Raspberry Pi y preparada para futuras extensiones de la capa perceptiva.

------------

## Código — `TmaqT_00_ML.py`

El programa principal integra en un único flujo la lectura táctil, el procesamiento temporal, la inferencia mediante los modelos congelados y la síntesis FM.

La estructura general del código es:

```text
TmaqT_00_ML.py
│
├── 1. Inicialización hardware
│      └── MPR121 × 2
│
├── 2. Configuración
│      ├── 24 zonas
│      ├── 4 voces
│      ├── attack / release
│      └── decay
│
├── 3. Carga de modelos
│      ├── SOM
│      ├── MLP
│      └── parámetros
│
├── 4. Lectura textil
│      └── 24 valores
│
├── 5. Procesamiento temporal
│      ├── smoothing
│      └── gesture_memory
│
├── 6. SOM
│      └── búsqueda del BMU
│
├── 7. MLP
│      └── predicción de parámetros
│
├── 8. Gestión de voces
│      ├── asignación por zona
│      ├── attack
│      └── release
│
├── 9. Síntesis FM
│      └── generación de audio
│
└── 10. Mezcla y salida
       ├── estéreo
       └── delay
```

### 1. Inicialización de los sensores

Los dos MPR121 proporcionan las 24 zonas táctiles:

```python
mpr_left = adafruit_mpr121.MPR121(
    i2c,
    address=0x5A
)

mpr_right = adafruit_mpr121.MPR121(
    i2c,
    address=0x5C
)
```

La superficie se interpreta como un único vector:

```text
24 zonas → vector táctil 24D
```

---

### 2. Configuración de la interacción

El sistema utiliza:

```python
NUM_ZONES = 24
NUM_VOICES = 4
```

También se definen los parámetros temporales de las voces:

```python
ATTACK_SPEED = 0.08
RELEASE_SPEED = 0.015
DECAY = 0.90
```

El `DECAY` controla la pérdida progresiva de la memoria del gesto.

La detección de contacto utiliza un umbral:

```python
active = set(
    np.where(
        raw > 0.05
    )[0].tolist()
)
```

Esto evita que pequeñas variaciones o ruido del sensor sean interpretados como contactos activos.

---

### 3. Carga del SOM

El SOM se carga desde un archivo previamente entrenado:

```text
TmaqT_SOM.npz
```

Su estructura es:

```text
6 × 4 × 24
```

El modelo no se modifica durante la ejecución.

Por cada estado táctil se busca la **BMU (Best Matching Unit)**:

```text
vector táctil
      ↓
comparación con SOM
      ↓
BMU
      ↓
posición (x, y)
```

---

### 4. Memoria temporal

La actividad táctil se acumula mediante:

```python
gesture_memory *= DECAY
gesture_memory += latent_input
```

Por tanto, el sistema no depende únicamente del contacto instantáneo.

La dinámica puede representarse como:

```text
contacto
   ↓
acumulación
   ↓
persistencia
   ↓
decaimiento
   ↓
liberación
```

Esto introduce una dimensión temporal en la representación del gesto.

---

### 5. Entrada del MLP

El MLP recibe un vector de características de 7 dimensiones.

La arquitectura es:

```text
7
↓
16
↓
16
↓
6
```

Los pesos se cargan desde:

```text
TmaqT_ML_model.npz
```

y los parámetros de normalización desde:

```text
TmaqT_ML_parameters.npz
```

El modelo realiza únicamente inferencia:

```text
X
↓
normalización
↓
MLP
↓
Y
↓
desnormalización
```

---

### 6. Predicción de parámetros sonoros

Las seis salidas del MLP se convierten en parámetros utilizados por el sistema de síntesis.

Conceptualmente:

```text
representación táctil
        ↓
       MLP
        ↓
┌──────────────────┐
│ parámetros       │
│ sonoros          │
└────────┬─────────┘
         ↓
       FM
```

Esto permite que una misma interacción pueda producir diferentes combinaciones de frecuencia, modulación, índice FM, espacialización y otros parámetros.

---

### 7. Gestión de voces

El sistema dispone de:

```python
NUM_VOICES = 4
```

Las voces se asignan dinámicamente a las zonas mediante:

```python
zone_voice
```

Esto mantiene la relación:

```text
zona → voz
```

mientras el contacto permanece activo.

Cuando una zona deja de estar activa:

```python
voices[voice_index].target_amp = 0.0
```

La voz entra entonces en `release`.

---

### 8. Ataque y release

La amplitud no cambia instantáneamente.

Para el release:

```python
voice.amp = max(
    voice.target_amp,
    voice.amp - RELEASE_SPEED
)
```

Para el ataque:

```python
voice.amp = min(
    voice.target_amp,
    voice.amp + ATTACK_SPEED
)
```

Esto genera una transición progresiva:

```text
CONTACTO
   ↓
ATTACK
   ↓
SOSTENIMIENTO
   ↓
RELEASE
   ↓
SILENCIO
```

---

### 9. Síntesis FM

Una vez obtenidos los parámetros, `generate_voice()` genera cada voz.

La síntesis continúa siendo FM:

```text
frecuencia portadora
        +
frecuencia de modulación
        +
índice FM
        ↓
      FM
        ↓
      audio
```

El modelo ML, por tanto, **no genera directamente la onda de audio**.

Genera los parámetros que controlan el sintetizador.

---

### 10. Mezcla de voces

Cada voz genera sus canales izquierdo y derecho:

```python
left_mix += l * voice.amp
right_mix += r * voice.amp
```

Las cuatro voces pueden coexistir:

```text
zona 9  → voz 1
zona 10 → voz 2
zona 15 → voz 3
zona 16 → voz 4
```

La salida final se mezcla como señal estéreo.

---

## Flujo completo del código

La lógica principal puede resumirse en:

```text
while running:

    leer MPR121
          ↓
    suavizar
          ↓
    detectar zonas
          ↓
    actualizar memoria
          ↓
    calcular representación
          ↓
    encontrar BMU en SOM
          ↓
    construir entrada ML
          ↓
    MLP predict()
          ↓
    obtener parámetros
          ↓
    asignar voces
          ↓
    generar FM
          ↓
    aplicar attack / release
          ↓
    mezclar
          ↓
    salida de audio
```

### Resultado

El código integra tres niveles:

```text
┌─────────────────────────────┐
│ INTERACCIÓN                 │
│ 24 zonas + memoria temporal │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ REPRESENTACIÓN              │
│ SOM 6×4                     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ APRENDIZAJE                 │
│ MLP 7→16→16→6               │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ SÍNTESIS                    │
│ FM × 4 voces                │
└─────────────────────────────┘
```

La implementación mantiene así una separación clara entre **percepción táctil, representación, aprendizaje y síntesis sonora**.


