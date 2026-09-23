# Baseline 01 — Acoplamiento gestual-sonoro latente con estado

Este baseline establece la primera implementación de **Edge AI de TmaqT** ejecutándose localmente en una Raspberry Pi 4.

Demuestra la infraestructura fundamental para relacionar representaciones gestuales continuas con espacios latentes sonoros aprendidos:

* **Edge AI ejecutada localmente en una Raspberry Pi 4**
* **Gesture Encoder** ejecutado localmente mediante **TensorFlow Lite**
* representación gestual continua `zG`
* dos espacios latentes sonoros aprendidos: `zFM` y `zWAV`
* perturbación de los espacios latentes sonoros a partir del gesto
* estado latente persistente: **el gesto desplaza el sistema y el sistema conserva ese desplazamiento**
* ausencia de clasificación de gestos
* ejecución autónoma mediante `systemd`

## Arquitectura del sistema

```text
Sensores táctiles MPR121
          ↓
   Gesture Encoder
          ↓
         zG
          ↓
Perturbación latente paramétrica
          ↓
 ┌─────────────────┐
 │                 │
zFM               zWAV
 │                 │
FM Decoder       WAV Decoder
 │                 │
sonido          representación
                 sonora
```

## Comportamiento con estado

El sistema no convierte directamente las lecturas individuales de los sensores en parámetros de síntesis.

En cambio, la representación gestual actual produce una **perturbación de un estado sonoro persistente**.

```text
gesto
  ↓
zG
  ↓
perturbación
  ↓
desplazamiento del estado latente
  ↓
zFM / zWAV
```

El estado latente persiste en el tiempo:

```text
TOUCH
  ↓
el estado latente se desplaza
  ↓
TOUCH
  ↓
el estado continúa desplazándose
  ↓
NO TOUCH
  ↓
el estado permanece donde llegó
  ↓
TOUCH AGAIN
  ↓
nueva perturbación desde el estado actual
```

Esto establece un principio fundamental para TmaqT:

> **El gesto no selecciona un sonido; el gesto perturba un espacio latente sonoro.**

## Distinción importante

Este baseline **todavía no debe describirse como un acoplamiento gestual-sonoro aprendido**.

El `Gesture Encoder` y los decodificadores son modelos aprendidos. Sin embargo, la relación entre el espacio latente gestual y los espacios latentes sonoros está actualmente definida mediante una **regla de acoplamiento paramétrica y con estado**, que incluye ganancias, términos de perturbación y suavizado.

En otras palabras:

```text
representación aprendida
        +
acoplamiento paramétrico
        +
estado latente persistente
        =
Baseline 01
```

Por tanto, el acoplamiento propiamente tal todavía está **definido explícitamente**, y no aprendido a partir de datos gestuales y sonoros sincronizados.

## Pregunta de investigación

Este baseline establece el punto de partida para la siguiente etapa de la investigación:

> **¿Qué cambia cuando la relación entre el espacio latente gestual y los espacios latentes sonoros deja de estar definida explícitamente y pasa a ser aprendida a partir de su relación temporal continua?**

Los siguientes experimentos investigarán si el propio acoplamiento puede **emerger de los datos**, en lugar de estar definido mediante relaciones diseñadas manualmente.

## Contexto de Edge AI

Baseline 01 constituye el punto de partida para investigar **Edge AI encarnada** en TmaqT.

La Raspberry Pi realiza localmente la codificación del gesto y la interacción con los espacios latentes, permitiendo que el instrumento textil funcione como un sistema computacional autónomo, sin depender de una infraestructura remota durante la interacción.

Este baseline establece así la infraestructura sobre la cual se podrán investigar posteriormente:

* acoplamiento gestual-sonoro aprendido
* relaciones temporales entre espacios latentes
* comportamiento sonoro adaptativo
* interacción multimodal entre espacios latentes
* dinámicas continuas entre gesto y sonido
* aprendizaje de relaciones entre estados gestuales y estados sonoros
