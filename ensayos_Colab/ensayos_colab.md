# Progresión 001 → 004B — síntesis

## Pregunta inicial

> ¿Cómo pasar de decirle a una máquina qué hacer, a construir un sistema que aprenda relaciones entre sonido, espacio e interacción?

## Progresión

```text
001  espacio diseñado a mano
002  Autoencoder  →  espacio aprendido
003  VAE          →  espacio continuo y generativo
004  espectrogramas →  estructura tiempo–frecuencia
004B dataset rico  →  espacio latente 2D
005  exploración mediante interacción
001 — Espacio diseñado manualmente
Relación explícita: posición → sonido. Nosotros definimos el mapa.

Pregunta: ¿qué significa diseñar manualmente un territorio sonoro?

002 — Autoencoder
Dejamos de definir el mapa. La red aprende una representación comprimida.


sonidos → Encoder → latente → Decoder → reconstrucción
Pregunta: ¿qué organización emerge de los datos?

003 — VAE
El VAE añade una representación probabilística del latente. El espacio se vuelve continuo y explorable.


entrada → μ, σ → sampling → z → Decoder
Loss = Reconstruction + KL
Pregunta: ¿qué ocurre cuando podemos movernos entre representaciones?

004 — Espectrogramas
Pasamos de la onda al espectrograma.


audio → STFT → espectrograma → VAE → latent → Decoder → Griffin-Lim → audio
Pregunta: ¿qué aprende el modelo de la estructura tiempo–frecuencia?

004B — Dataset más rico
3000 sonidos sintéticos de 3 segundos: frecuencia, armónicos, FM, ruido, envolventes.

Espectrogramas: (3000, 257, 345).

VAE con latent 2D. Loss observado: ≈ 0.0016.

Hallazgo observado, formulado con cuidado:

Sin haber definido categorías, la organización aprendida presenta correlaciones con características sonoras observables.

El espacio se puede empezar a estudiar como territorio sonoro aprendido.

Aclaración importante sobre el VAE
Los experimentos con VAE se realizaron, pero no fueron el camino que continuó TmaqT.

Qué se hizo:

Se entrenó un VAE con 3000 espectrogramas.

Se obtuvo un espacio latente 2D.

Se observó organización correlacionada con características sonoras.

La reconstrucción funcionó (loss ≈ 0.0016).

Qué no se hizo:

No se navegó el espacio con gesto.

No se conectó a una superficie textil.

No se integró al instrumento.

No se usó para síntesis en tiempo real.

Por qué importa la distinción:

El VAE fue una fase de exploración conceptual: entender qué es un espacio aprendido, cómo se organiza, cómo se navega. Pero el sistema TmaqT que llegó a existir no usa VAE.

Lo que sí quedó de esa fase:

La noción de espacio latente navegable.

La idea de que la organización puede emerger de los datos.

La separación entre representación y síntesis.

El interés por territorios sonoros en lugar de mapeos fijos.

Esas ideas se trasladaron a TmaqT con otras herramientas: PCA, SOM, MLP, espacios acústicos construidos con características, no VAE.

005 — Explorar el territorio
Primero sin textil: teclado/mouse.

mouse → (z1, z2) → Decoder → sonido
Pregunta: ¿podemos recorrer intencionalmente el espacio y escuchar cómo cambia el sonido?

##TmaqT — Navegar el territorio con gesto

MPR121 → gesto textil → trayectoria → espacio → síntesis
El textil no selecciona sonidos. Navega un espacio de posibilidades.

001     DISEÑAR el espacio
002     APRENDER una organización
003     GENERAR dentro del espacio
004–B   OBSERVAR el territorio aprendido
005     EXPLORAR el territorio
TmaqT   NAVEGAR el territorio mediante el gesto

Hipótesis de trabajo
No parto de una relación fija gesto → sonido. Parto de un territorio sonoro aprendido que podría ser explorado mediante la interacción.

##El aprendizaje automático no reemplaza al sintetizador. Lo organiza, lo relaciona, lo hace navegable.

Mapa conceptual

red neuronal → entrenamiento → Autoencoder → VAE
    → espacio latente → audio → espectrograma
    → reconstrucción → dataset sintético → navegación
    → interacción → MPR121 → gesto → TmaqT
Idea final

004B    APRENDER el territorio
005     EXPLORAR el territorio
TmaqT   NAVEGAR el territorio mediante el gesto
