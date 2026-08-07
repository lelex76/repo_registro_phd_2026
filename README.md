
# TTT2 — La Piel Tejida

## Repositorio de desarrollo experimental
<p align="center">

<img src="imgs/Diagrama_caja.png" width="600">

<p align="center">
<sub>Figura 1. Arquitectura experimental TTT2: superficie textil interactiva, adquisición gestual mediante 
sensores capacitivos y generación audiovisual en tiempo real.</sub>
</p>

---

# Descripción

Este repositorio documenta el desarrollo experimental de **TTT2 — La Piel Tejida**, un prototipo de interfaz 
textil interactiva desarrollado dentro del proyecto:

**La Piel Tejida: Codificar y Significar mediante una Proto-Escritura desde una Constelación de Lenguajes.**

TTT2 explora la superficie textil conductiva como una interfaz sensible donde el gesto corporal genera respuestas 
audiovisuales mediante la relación entre:

* superficie textil sensible
* interacción corporal
* adquisición gestual: primeras aproximaciones
* sonido ( preseteado aun no generativo)
* representación visual

El repositorio funciona como un registro de laboratorio experimental donde se documentan códigos, pruebas de 
hardware, configuraciones electrónicas y exploraciones audiovisuales.

Video de la obra completa:

### https://photos.app.goo.gl/cZkKCfsx2pKV977p8 
---

# De TTT2 hacia TmaqT

TTT2 constituye el punto de partida experimental desde el cual surge la propuesta doctoral:

**TmaqT — Arquitectura Topológica Multimodal para el Modelado Adaptativo del Gesto en Interfaces 
Háptico-Táctiles abordando lo textil.**

Mientras TTT2 implementa una relación definida entre gesto, sonido e imagen mediante reglas de interacción 
preestablecidas, TmaqT explora la transición hacia sistemas capaces de aprender nuevas relaciones entre:

* interacción corporal
* espacio latente
* generación sonora
* comportamiento emergente

La pregunta central que articula esta evolución es:

> ¿Cómo pasar de una correspondencia fija gesto-respuesta a un sistema capaz de aprender relaciones nuevas entre 
interacción corporal, espacio latente y generación sonora?

La motivación principal de TmaqT no es utilizar inteligencia artificial para generar sonido, sino investigar cómo 
el gesto corporal puede convertirse en una condición generativa del sonido. Desde esta perspectiva, la IA deja de 
operar como un sistema externo de producción y se convierte en un componente relacional dentro de una arquitectura 
donde cuerpo, materia, datos efímeros provenientes de la experiencia táctil-háptica y síntesis sonora co-emergen.

Esta relación plantea la posibilidad de desarrollar interfaces adaptativas capaces de modificar su comportamiento 
a partir de la interacción continua con el cuerpo. En lugar de funcionar como superficies pasivas de entrada o 
dispositivos basados en correspondencias predeterminadas, estas interfaces podrían aprender progresivamente las 
particularidades del gesto, la presión, la trayectoria y las formas de contacto, construyendo representaciones 
dinámicas de la interacción corporal.

Desde esta perspectiva, el textil deja de ser únicamente un medio de captura y se transforma en una 
superficie capaz de adaptarse a diferentes modos de interacción, generando nuevas posibilidades para 
instrumentos musicales aumentados, interfaces hápticas expresivas, sistemas de rehabilitación sensorial, 
dispositivos de comunicación corporal y otras arquitecturas multimodales donde la relación entre humano y 
tecnología se construya de manera situada y evolutiva.

 ---

# TTT2 — Arquitectura experimental

La primera implementación consiste en una superficie textil conductiva conectada a un sistema computacional capaz 
de interpretar interacciones táctiles y transformarlas en comportamientos audiovisuales.

```text
Arquitectura:

GESTO CORPORAL
        |
        |
TEXTIL CONDUCTIVO
        |
        |
SENSORES CAPACITIVOS MPR121
(24 zonas táctiles)
        |
        |
RASPBERRY PI
        |
        |
PYTHON
        |
        |
+----------------------+
| Librerías principales|
+----------------------+
| Adafruit_MPR121      |
| BusIO / I2C          |
| Pygame               |
| Math                 |
| Random               |
| Time                 |
| OS                   |
+----------------------+
        |
        |
SONIDO + VISUALIZACIÓN
(Pygame Mixer + Pygame Drawing)
```

---

# Tecnologías

## Hardware

* Raspberry Pi 4B
* 2 sensores capacitivos MPR121
* 24 zonas táctiles
* superficie textil conductiva
* pedales de control complementarios

## Software

* Python
* Pygame
* NumPy
* comunicación I2C para adquisición sensorial

---

# Implementación experimental

La primera versión funcional del sistema integra:

* lectura de sensores capacitivos
* detección de interacción táctil
* activación y mezcla de capas sonoras
* control dinámico de volumen y transiciones
* generación visual en tiempo real
* relación entre gesto corporal, superficie textil y respuesta computacional

El sistema utiliza una correspondencia determinista entre interacción y respuesta audiovisual, permitiendo 
investigar cómo una superficie material puede transformarse en una interfaz expresiva basada en el gesto.

La incorporación de pedales como elementos de control complementarios amplía la interacción desde el contacto 
manual hacia una experiencia corporal distribuida, donde diferentes acciones del cuerpo generan variaciones dentro 
del comportamiento audiovisual.

---

# Evolución experimental

## Etapa 1 — Prototipo inicial

Implementación de:

* adquisición capacitiva
* interacción textil
* activación sonora
* visualización generativa

## Etapa 2 — Exploraciones audiovisuales

Investigación de:

* capas sonoras
* mezcla dinámica
* variación temporal
* relaciones gesto-sonido

## Etapa 3 — Hacia sistemas adaptativos

Primeras exploraciones hacia:

* representación del gesto
* espacios latentes
* Self-Organizing Maps (SOM)
* modelos generativos de sonido
* aprendizaje automático no supervisado

---

# Referencia

TTT2 — La Piel Tejida corresponde a la investigación de tesis de Magíster en Artes Mediales, Universidad de Chile, 
2025.

https://www.academia.edu/144409160/TTT2_La_Piel_Tejida_Codificar_y_Significar_mediante_una_proto_Escritura_Desde_una_constelaci%C3%B3n_de_lenguaje_s_

