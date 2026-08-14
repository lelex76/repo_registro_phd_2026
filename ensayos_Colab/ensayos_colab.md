# Progresión de los experimentos 001 → 004B

## Del espacio diseñado al territorio sonoro aprendido

### Pregunta inicial

> **¿Cómo pasar de decirle a una máquina exactamente qué hacer, a construir un sistema capaz de aprender relaciones nuevas entre sonido, espacio e interacción?**

Los primeros experimentos fueron diseñados como una progresión. Cada uno introduce una idea necesaria para llegar al siguiente.

La progresión general es:

```text
001
espacio diseñado manualmente
        ↓
002
Autoencoder
        ↓
espacio aprendido
        ↓
003
VAE
        ↓
espacio continuo y generativo
        ↓
004
espectrogramas
        ↓
estructura tiempo–frecuencia
        ↓
004B
dataset más rico
        ↓
espacio latente 2D aprendido
        ↓
005
exploración mediante interacción
        ↓
TmaqT
navegación del territorio mediante el gesto
```

---

# PARTE I — CONCEPTOS FUNDAMENTALES

Antes de comprender los experimentos, necesito entender algunos conceptos básicos de Machine Learning y de procesamiento de sonido.

---

## 1. Red neuronal

Una **red neuronal** es un sistema que aprende relaciones a partir de ejemplos.

En vez de decirle directamente:

```text
si ocurre A → haz B
```

le damos muchos ejemplos:

```text
datos
 ↓
red neuronal
 ↓
aprende relaciones
 ↓
resultado
```

La red contiene muchos **pesos internos**. Durante el entrenamiento, estos pesos se van ajustando para producir mejores resultados.

Una forma simple de pensarlo:

> **Una red neuronal aprende ajustando muchos números internos a partir de ejemplos.**

En nuestro caso:

```text
sonidos / espectrogramas
        ↓
   red neuronal
        ↓
representación aprendida
```

### Conceptos que necesito aprender

* neurona
* capa
* pesos
* bias
* función de activación
* entrada
* salida
* forward pass
* error / loss
* backpropagation
* gradiente
* optimizador
* learning rate
* epoch
* batch
* entrenamiento
* validación

### Función fundamental

```text
entrada
 ↓
forward pass
 ↓
predicción
 ↓
loss
 ↓
backpropagation
 ↓
actualización de pesos
```

---

# 2. Autoencoder

Un **Autoencoder** es una arquitectura de red neuronal diseñada para aprender a **comprimir y reconstruir datos**.

La estructura básica es:

```text
entrada
  ↓
Encoder
  ↓
representación pequeña
  ↓
Decoder
  ↓
reconstrucción
```

Por ejemplo:

```text
sonido
  ↓
Encoder
  ↓
representación pequeña
  ↓
Decoder
  ↓
sonido reconstruido
```

### ¿Qué aprende?

No le decimos exactamente qué características debe buscar.

Le damos muchos ejemplos y la red intenta encontrar una representación pequeña que conserve información suficiente para reconstruirlos.

Por eso:

> **Autoencoder = una red neuronal que aprende una representación comprimida de los datos.**

### Sus tres elementos principales

#### Encoder

```text
datos grandes
    ↓
representación pequeña
```

Comprime la información.

#### Latent Space

```text
representación pequeña
```

Es el espacio donde queda codificada la información aprendida.

#### Decoder

```text
representación pequeña
    ↓
datos reconstruidos
```

Intenta reconstruir la entrada original.

### Conceptos que necesito aprender

* Encoder
* Decoder
* bottleneck
* latent representation
* latent space
* reconstruction
* reconstruction loss
* dimensionality reduction

---

# 3. VAE — Variational Autoencoder

El **VAE** parte de la idea del Autoencoder, pero agrega algo fundamental:

> **intenta construir un espacio latente continuo y organizado.**

La estructura sigue siendo:

```text
entrada
   ↓
Encoder
   ↓
espacio latente
   ↓
Decoder
   ↓
reconstrucción
```

Pero el VAE introduce una representación probabilística del espacio latente.

En nuestro experimento:

```text
espectrograma
     ↓
  Encoder
     ↓
   z1, z2
     ↓
  Decoder
     ↓
nuevo espectrograma
```

Como tenemos solamente dos dimensiones:

```text
z1
↑
│       •
│   •       •
│       X
│  •   •
└────────────→ z2
```

podemos visualizar y recorrer el espacio.

### Diferencia fundamental

Autoencoder:

```text
entrada
 ↓
comprimir
 ↓
reconstruir
```

VAE:

```text
entrada
 ↓
comprimir
 ↓
organizar espacio continuo
 ↓
explorar / muestrear
 ↓
generar
```

Por eso:

> **Autoencoder:** aprende una representación comprimida.

> **VAE:** aprende una representación comprimida y organiza un espacio latente continuo que podemos explorar.

### Conceptos que necesito aprender

* variational
* distribución
* media (`μ`)
* desviación estándar (`σ`)
* muestreo
* reparameterization trick
* KL divergence
* KL loss
* reconstruction loss
* latent distribution
* sampling

---

# 4. Latent Space — Espacio latente

El **espacio latente** es la representación interna que la red aprende para describir los datos de una manera más pequeña.

En nuestro caso:

```text
muchos espectrogramas
        ↓
      Encoder
        ↓
   espacio latente
        ↓
      (z1, z2)
```

Cada sonido termina asociado a una posición dentro de ese espacio.

Por ejemplo:

```text
        z2
         ↑
         │       sonido B
         │          •
         │
         │   • sonido A
         │
         └────────────────→ z1
```

Lo importante es:

> **nosotros no dibujamos manualmente este mapa.**

La red aprende una organización a partir de los datos.

### Conceptos que necesito aprender

* latent vector
* latent dimensions
* coordinates
* interpolation
* latent traversal
* latent manifold
* clustering
* neighbourhood
* continuity

---

# 5. Decoder

El **Decoder** toma una posición del espacio latente e intenta convertirla nuevamente en una representación del sonido.

```text
(z1, z2)
    ↓
Decoder
    ↓
espectrograma
    ↓
audio
```

En nuestro experimento:

```text
posición
   ↓
(z1,z2)
   ↓
Decoder
   ↓
espectrograma generado
   ↓
Griffin-Lim
   ↓
audio
```

### Conceptos que necesito aprender

* decoding
* reconstruction
* generation
* latent traversal
* interpolation

---

# 6. Reconstruction Loss

Es el error entre lo que entró al modelo y lo que el Decoder reconstruyó.

```text
entrada
   ↕
reconstrucción
```

Si son muy diferentes:

```text
error grande
```

Si son parecidos:

```text
error pequeño
```

El entrenamiento intenta reducir este error.

### Conceptos

* loss
* MSE
* MAE
* reconstruction error

---

# 7. KL Loss

La **KL loss** es una parte específica del VAE.

Ayuda a mantener el espacio latente organizado y cercano a una distribución conocida.

Simplificando:

```text
reconstrucción
      +
organización del espacio latente
      ↓
     VAE
```

Sin esta parte, el modelo se parecería mucho más a un Autoencoder convencional.

### Conceptos

* KL divergence
* probability distribution
* prior
* posterior
* latent regularization

---

# 8. Sampling

El VAE introduce variación alrededor de la representación aprendida.

Simplificando:

```text
z_mean
   +
variación
   ↓
punto latente
   ↓
Decoder
```

Esto permite que el modelo trabaje con **regiones de posibilidades** y no solamente con puntos rígidos.

### Conceptos

* random sampling
* Gaussian distribution
* mean
* variance
* standard deviation
* reparameterization trick

---

# 9. Espectrograma

Antes de 004, el sonido se trabajaba principalmente como señal de audio.

En 004 hacemos:

```text
audio
 ↓
espectrograma
 ↓
VAE
```

Un espectrograma representa cómo se distribuye la energía del sonido en función del:

```text
tiempo
   ×
frecuencia
```

Podemos visualizarlo como:

```text
frecuencia
↑
│ ███
│ █████
│   █████
│      ███
│
└────────────────→ tiempo
```

### Conceptos que necesito aprender

* waveform
* sample rate
* frequency
* amplitude
* Fourier Transform
* STFT
* spectrogram
* FFT
* window
* hop length
* frequency bins
* time frames
* magnitude
* phase
* log scale / dB

---

# 10. Griffin-Lim

El VAE trabaja con espectrogramas, pero para volver a escuchar el resultado necesitamos convertir el espectrograma nuevamente en audio.

Una posibilidad es:

```text
espectrograma
      ↓
Griffin-Lim
      ↓
waveform
      ↓
audio
```

Griffin-Lim estima la información de fase necesaria para reconstruir una señal de audio.

### Conceptos

* phase
* magnitude
* inverse STFT
* Griffin-Lim
* reconstruction artifacts

---

# PARTE II — PROGRESIÓN EXPERIMENTAL

---

# 001 — Crear un espacio latente manualmente

El primer experimento parte de un espacio diseñado por nosotros.

La relación es explícita:

```text
punto del mapa
      ↓
    sonido
```

Es decir:

> "Si estoy aquí, suena esto. Si me muevo allá, cambia aquello."

El espacio no es aprendido por la máquina.

Nosotros diseñamos las relaciones.

### Objetivo

Comprender experimentalmente:

* qué significa explorar un espacio sonoro;
* cómo una posición puede relacionarse con un sonido;
* cómo interpolar entre sonidos;
* cómo una coordenada puede controlar parámetros sonoros.

### Conceptos / funciones a aprender

```text
x, y
 ↓
mapping
 ↓
frequency / amplitude / timbre
 ↓
sound
```

Necesito aprender:

* coordenadas
* normalización
* mapping
* interpolación
* escalamiento
* funciones matemáticas
* generación de ondas
* síntesis básica
* visualización 2D

### Pregunta experimental

> ¿Qué significa diseñar manualmente un territorio sonoro?

---

# 002 — Autoencoder: la máquina comienza a encontrar relaciones

En el segundo experimento dejamos de definir manualmente dónde debe estar cada sonido.

Presentamos múltiples sonidos a una red neuronal:

```text
muchos sonidos
     ↓
   Encoder
     ↓
espacio reducido
     ↓
   Decoder
     ↓
sonido reconstruido
```

Aquí aparece un cambio importante:

> **La organización del espacio ya no es completamente diseñada por nosotros.**

La máquina comienza a construir una representación propia de los datos.

### Objetivo

Comprender:

* compresión;
* representación latente;
* reconstrucción;
* aprendizaje de características;
* diferencia entre espacio diseñado y espacio aprendido.

### Conceptos / funciones

```text
Dataset
 ↓
normalización
 ↓
Encoder
 ↓
latent space
 ↓
Decoder
 ↓
reconstruction
 ↓
loss
```

Necesito aprender:

* dataset
* batch
* epoch
* train / validation
* neural network
* encoder
* decoder
* bottleneck
* latent vector
* loss
* optimizer
* Adam
* training loop

---

# 003 — Primer VAE

El siguiente paso es pasar del Autoencoder al Variational Autoencoder.

El VAE introduce una representación probabilística y continua del espacio latente.

En lugar de pensar solamente:

```text
sonido A
sonido B
sonido C
```

podemos pensar:

```text
sonido A ───────── sonido B
             ↑
       zona intermedia
             ↑
       nuevos puntos
```

### Cambio conceptual

El espacio deja de ser solamente una colección de representaciones comprimidas y comienza a convertirse en:

> **un espacio continuo y generativo.**

### Objetivo

Comprender:

* distribución latente;
* continuidad;
* sampling;
* generación;
* interpolación.

### Conceptos / funciones

```text
Encoder
 ↓
μ
σ
 ↓
sampling
 ↓
z
 ↓
Decoder
```

Y la función de pérdida:

```text
VAE Loss
=
Reconstruction Loss
+
KL Loss
```

### Pregunta experimental

> ¿Qué ocurre cuando podemos movernos entre representaciones aprendidas?

---

# 004 — Trabajar con espectrogramas

En este experimento hacemos otro cambio fundamental.

En lugar de entregar directamente la onda de audio al VAE:

```text
onda de audio
 ↓
VAE
```

transformamos primero el sonido:

```text
audio
 ↓
STFT
 ↓
espectrograma
 ↓
VAE
```

El espectrograma representa la estructura:

```text
tiempo × frecuencia
```

### Cambio conceptual

Pasamos de:

> aprender directamente la forma de una señal

a:

> aprender una representación de sus características tiempo–frecuencia.

### Conceptos / funciones

Necesito aprender:

```text
audio
 ↓
STFT
 ↓
magnitude
 ↓
spectrogram
 ↓
normalization
 ↓
VAE
```

Y después:

```text
latent
 ↓
Decoder
 ↓
spectrogram
 ↓
Griffin-Lim
 ↓
audio
```

---

# 004B — Dataset más grande y eventos sonoros más ricos

El 004B amplía considerablemente el experimento.

En lugar de trabajar con sonidos simples, construimos:

* 3000 sonidos sintéticos;
* 3 segundos de duración;
* diferentes frecuencias;
* armónicos;
* modulación FM;
* ruido;
* evolución temporal mediante envolventes.

El cambio puede resumirse así:

```text
004

un tono
↓
onda simple
```

hacia:

```text
004B

frecuencia
+
armónicos
+
FM
+
ruido
+
evolución temporal
↓
evento sonoro
```

---

## Dataset

Los 3000 sonidos son transformados en espectrogramas.

Resultado:

```text
(3000, 257, 345)
```

Esto significa:

```text
3000 → número de sonidos
257  → componentes de frecuencia
345  → posiciones temporales
```

Tenemos, por tanto:

> **3000 representaciones tiempo–frecuencia de eventos sonoros diferentes.**

### Conceptos / funciones

Necesito aprender:

* dataset generation
* synthetic dataset
* NumPy
* random distributions
* waveform synthesis
* harmonic synthesis
* FM synthesis
* envelopes
* noise
* STFT
* spectrogram
* normalization
* tensor shape
* batch dimensions

---

# Construcción del VAE

El modelo sigue esta estructura:

```text
Espectrograma
      ↓
    Encoder
      ↓
Espacio latente
   (z1, z2)
      ↓
    Decoder
      ↓
Nuevo espectrograma
```

El espacio latente tiene 2 dimensiones para permitir:

* visualizarlo;
* compararlo;
* recorrerlo;
* interpolarlo;
* comenzar a estudiarlo como territorio.

Durante el entrenamiento, el VAE intenta simultáneamente:

1. reconstruir los espectrogramas originales;
2. mantener una organización continua del espacio latente.

El resultado observado fue aproximadamente:

```text
loss ≈ 0.0016
```

La reconstrucción funciona y el modelo consigue aprender una representación latente de los sonidos.

---

# ¿Qué aprendimos del espacio?

Al visualizar el espacio latente observamos que determinadas características sonoras tienden a ocupar regiones diferenciadas.

Es importante formularlo con precisión:

> **Sin haber definido explícitamente categorías como grave, agudo, armónico o complejo, observamos que determinadas características sonoras tienden a ocupar regiones diferenciadas del espacio latente.**

No significa que el VAE haya recibido esas categorías ni que las "comprenda" como conceptos humanos.

Significa que:

> **la organización de los datos aprendida por la red presenta correlaciones con características sonoras observables.**

Esto convierte el espacio latente en algo que podemos comenzar a estudiar como:

> **un territorio sonoro aprendido.**

---

# PARTE III — LO QUE NECESITO APRENDER PARA LEER EL CÓDIGO

A medida que avanzo en los experimentos, hay una serie de funciones y elementos de Python / ML que necesito reconocer.

## NumPy

```python
np.array()
np.random.normal()
np.random.uniform()
np.linspace()
np.sin()
np.mean()
np.std()
np.min()
np.max()
```

Necesito comprender:

> **qué hacen matemáticamente y qué forma tienen los datos que producen.**

---

## Shapes

Una de las cosas más importantes para entender ML es saber:

> **qué forma tiene el dato en cada momento.**

Por ejemplo:

```text
audio
(3000, samples)

espectrograma
(3000, 257, 345)

batch
(batch_size, 257, 345)

latent
(batch_size, 2)
```

Necesito aprender:

* shape
* axis
* reshape
* flatten
* batch dimension
* channels

---

## Keras / TensorFlow

Necesito reconocer:

```python
Model
Input
Dense
Flatten
Reshape
compile()
fit()
predict()
```

Y entender qué ocurre en:

```python
model.compile()
```

```text
define cómo aprenderá
```

y:

```python
model.fit()
```

```text
entrena la red
```

y:

```python
model.predict()
```

```text
utiliza lo aprendido
```

---

# Adam

Adam es el **optimizador** utilizado para ajustar los pesos de la red durante el entrenamiento.

Simplificando:

```text
predicción
 ↓
loss
 ↓
gradiente
 ↓
Adam
 ↓
nuevos pesos
```

No es un tipo de red neuronal.

Es un mecanismo que ayuda a decidir:

> **cómo modificar los números internos de la red para reducir el error.**

---

# PARTE IV — DEL 004B AL SIGUIENTE EXPERIMENTO

El 004B construye y permite observar el territorio sonoro aprendido.

Ahora aparece el siguiente problema:

> **Si ya tenemos un territorio sonoro aprendido, ¿cómo podemos recorrerlo mediante una interacción física?**

El 005 puede comenzar de manera sencilla:

```text
teclado / mouse
      ↓
posición (z1, z2)
      ↓
espacio latente
      ↓
Decoder
      ↓
sonido
```

Primero necesitamos comprobar que podemos navegar el espacio sin introducir todavía la complejidad del textil.

---

# 005 — Explorar el territorio

El objetivo del 005 no sería todavía construir TmaqT completo.

Sería responder una pregunta más sencilla:

> **¿Podemos recorrer intencionalmente el espacio latente y escuchar cómo cambia el sonido?**

Por ejemplo:

```text
mouse
 ↓
x,y
 ↓
z1,z2
 ↓
Decoder
 ↓
espectrograma
 ↓
audio
```

Podemos experimentar con:

* navegación;
* interpolación;
* puntos;
* líneas;
* trayectorias;
* velocidad;
* dirección;
* regiones;
* vecinos.

### Conceptos nuevos

* latent traversal
* interpolation
* trajectory
* navigation
* continuous control
* temporal movement
* mapping
* sonification

---

# PARTE V — HACIA UN ESPACIO SINTÉTICO ESTRUCTURADO

La experimentación plantea otra pregunta:

> **¿Qué tipo de sonido debería habitar este territorio?**

No es necesario abandonar la síntesis pura.

Al contrario, un dataset completamente sintético puede ofrecer una ventaja conceptual y técnica:

> **cada evento sonoro puede construirse a partir de parámetros conocidos y controlables.**

En lugar de producir miles de sonidos completamente aleatorios, podemos construir un:

> **espacio sintético estructurado.**

---

## Parámetros posibles

```text
SÍNTESIS
│
├── frecuencia
│
├── timbre
│   ├── armónicos
│   ├── FM
│   ├── AM
│   ├── ruido
│   └── distorsión
│
└── dinámica
    ├── attack
    ├── decay
    ├── sustain
    └── release
```

Parámetros:

```text
frequency
harmonics
fm_ratio
fm_index
am_depth
noise_amount
filter_cutoff
resonance
attack
decay
sustain
release
duration
amplitude
```

De esta manera el dataset deja de ser simplemente:

```text
3000 sonidos
```

y pasa a ser:

```text
3000 configuraciones diferentes
de un sistema de síntesis
```

Esto permite estudiar:

```text
parámetros
    ↕
sonido
    ↕
espectrograma
    ↕
espacio latente
```

---

# De "tono" a "evento sonoro"

Podemos ampliar progresivamente la complejidad:

```text
tono
 ↓
tono + armónicos
 ↓
FM
 ↓
FM + envolvente
 ↓
FM + ruido
 ↓
FM + ruido + modulación
 ↓
evento sonoro complejo
```

Así, el territorio latente no estaría compuesto solamente por variaciones de altura.

Podría contener diferencias de:

* frecuencia;
* densidad armónica;
* modulación;
* ruido;
* dinámica;
* duración;
* textura;
* complejidad temporal.

Esto permitiría que la navegación del espacio tenga mayor riqueza perceptual.

---

# PARTE VI — DOS FORMAS DE RELACIONAR SÍNTESIS Y VAE

A partir de aquí aparecen dos posibilidades experimentales.

## A. El VAE aprende solamente del audio

```text
parámetros de síntesis
        ↓
   sintetizador
        ↓
       audio
        ↓
   espectrograma
        ↓
       VAE
        ↓
  espacio latente
```

El VAE **no recibe información sobre los parámetros** utilizados para generar cada sonido.

Después podemos preguntar:

> **¿Qué relaciones aparecen espontáneamente en el espacio aprendido?**

Esta opción permite estudiar qué organización emerge exclusivamente a partir de las características presentes en el audio.

---

## B. Conservar también los parámetros de síntesis

Además del audio, guardamos los parámetros:

```text
audio_001.wav

frequency = 220
fm_index = 0.4
noise = 0.1
attack = 0.2
...
```

Entonces podemos comparar:

```text
espacio latente
      ↕
parámetros de síntesis
```

Y formular una nueva pregunta:

> **¿El espacio latente aprendido mantiene relaciones con el espacio paramétrico original del sintetizador?**

Esta relación puede convertirse en una línea de análisis importante para los siguientes experimentos.

---

# PARTE VII — MPR121 + SUPERFICIE TEXTIL

El MPR121 introduce otra dimensión en el problema.

No se trataría necesariamente de:

```text
sensor 1 → sonido A
sensor 2 → sonido B
sensor 3 → sonido C
```

porque esto volvería a establecer correspondencias fijas entre gesto y sonido.

La alternativa sería:

```text
textil
 ↓
24 zonas capacitivas
 ↓
valores de contacto
 ↓
gesto
 ↓
posición / trayectoria
 ↓
espacio latente
 ↓
síntesis
```

La superficie textil no seleccionaría directamente un sonido.

> **El textil navegaría un espacio de posibilidades sonoras.**

---

# Una posible arquitectura futura

```text
TEXTIL
   │
   ├── contacto
   │
   └── movimiento
        ↓
   24 sensores
        ↓
representación del gesto
        ↓
espacio latente
     (z1,z2)
        ↓
parámetros de síntesis
        ↓
osciladores + FM + filtros
        ↓
     sonido
```

En este escenario, el Decoder no necesariamente tiene que producir directamente el audio.

El espacio latente podría utilizarse para controlar parámetros de un sintetizador:

```text
gesto textil
     ↓
espacio latente
   (z1,z2)
     ↓
parámetros de síntesis
     ↓
osciladores
+ FM
+ filtros
+ envolventes
     ↓
sonido
```

Esto mantiene abierta la posibilidad de trabajar con **síntesis sonora explícita**, en lugar de convertir todo el sistema en una caja negra de generación de audio.

---

# PARTE VIII — CAMBIO CONCEPTUAL HACIA TmaqT

La pregunta inicial era:

> **¿Cómo pasar de decirle a una máquina exactamente qué hacer, a construir un sistema capaz de aprender relaciones nuevas entre sonido, espacio e interacción?**

Después de los experimentos 001–004B, la pregunta comienza a desplazarse.

Ya no se trata solamente de:

```text
gesto → sonido
```

sino de:

```text
gesto
 ↓
trayectoria
 ↓
espacio latente aprendido
 ↓
región sonora
 ↓
síntesis / sonido
```

La interacción no selecciona necesariamente un objeto sonoro previamente definido.

Puede convertirse en:

> **una forma de navegación.**

---

# PARTE IX — SÍNTESIS DEL PROCESO

## 001–004B

### CONSTRUIR Y COMPRENDER EL TERRITORIO

```text
001
espacio diseñado manualmente
        ↓
002
Autoencoder
        ↓
espacio aprendido
        ↓
003
VAE
        ↓
espacio continuo y generativo
        ↓
004
espectrogramas
        ↓
estructura tiempo–frecuencia
        ↓
004B
dataset más rico
        ↓
3000 eventos sintéticos
        ↓
VAE
        ↓
espacio latente 2D
        ↓
territorio sonoro aprendido
```

## 005

### EXPLORAR EL TERRITORIO

```text
teclado / mouse
        ↓
posición
        ↓
espacio latente
        ↓
Decoder
        ↓
sonido
```

## TmaqT

### NAVEGAR EL TERRITORIO MEDIANTE EL GESTO

```text
MPR121
 ↓
gesto textil
 ↓
trayectoria
 ↓
espacio latente
 ↓
parámetros de síntesis
 ↓
sonido
```

---

# Mapa general de aprendizaje

Esta es probablemente la parte más importante para continuar los ensayos:

```text
01. RED NEURONAL
    ↓
    pesos / capas / activaciones
    ↓

02. ENTRENAMIENTO
    ↓
    loss / gradiente / backpropagation / Adam
    ↓

03. AUTOENCODER
    ↓
    Encoder / latent space / Decoder
    ↓

04. VAE
    ↓
    μ / σ / sampling / KL loss
    ↓

05. ESPACIO LATENTE
    ↓
    coordenadas / continuidad / interpolación
    ↓

06. AUDIO
    ↓
    waveform / frecuencia / amplitud
    ↓

07. ESPECTROGRAMA
    ↓
    FFT / STFT / tiempo / frecuencia
    ↓

08. RECONSTRUCCIÓN
    ↓
    Decoder / Griffin-Lim / audio
    ↓

09. DATASET SINTÉTICO
    ↓
    frecuencia / armónicos / FM / ruido / envolventes
    ↓

10. NAVEGACIÓN
    ↓
    z1 / z2 / trayectoria / interpolación
    ↓

11. INTERACCIÓN
    ↓
    teclado / mouse
    ↓

12. MPR121
    ↓
    24 zonas capacitivas
    ↓

13. GESTO
    ↓
    contacto / presión / trayectoria temporal
    ↓

14. TmaqT
    ↓
    gesto → espacio latente → territorio sonoro
```

---

# La idea que debo recordar

La progresión completa puede resumirse en cinco verbos:

```text
001
DISEÑAR
el espacio

↓

002
APRENDER
una organización

↓

003
GENERAR
dentro del espacio

↓

004–004B
OBSERVAR
el territorio sonoro aprendido

↓

005
EXPLORAR
el territorio

↓

TmaqT
NAVEGAR
el territorio mediante el gesto
```

Y la distinción metodológica queda:

```text
001–004B
CONSTRUIR Y COMPRENDER
EL TERRITORIO

005
EXPLORAR EL TERRITORIO

TmaqT
NAVEGAR EL TERRITORIO
MEDIANTE EL GESTO
```

La hipótesis de trabajo comienza entonces a formularse de otra manera:

> **No partimos de una relación fija gesto → sonido. Partimos de un territorio sonoro aprendido que puede ser explorado mediante la interacción.**

La síntesis sonora puede permanecer en el centro del sistema.

El aprendizaje automático no tiene necesariamente que reemplazar al sintetizador.

Puede funcionar como una estructura que:

```text
ORGANIZA
   ↓
RELACIONA
   ↓
GENERA UN ESPACIO
   ↓
HACE NAVEGABLE
   ↓
LAS POSIBILIDADES SONORAS
```

En este sentido:

```text
004B
APRENDER EL TERRITORIO
        ↓
005
EXPLORAR EL TERRITORIO
        ↓
TmaqT
NAVEGAR EL TERRITORIO
MEDIANTE EL GESTO
```
