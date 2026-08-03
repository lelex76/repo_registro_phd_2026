# TTT2 — La Piel Tejida
## Repositorio de desarrollo experimental

<p align="center">
  <img src="../02_img_orig/Diagrama_caja.png" width="700">
</p>

<p align="center">
  <sub>
  Figura 1. Arquitectura experimental TTT2: superficie textil interactiva,
  adquisición gestual mediante sensores capacitivos y generación audiovisual en tiempo real.
  </sub>
</p>


---

## Descripción

Este repositorio documenta el desarrollo experimental de **TTT2 (La Piel Tejida)** y las primeras 
exploraciones técnicas que dieron origen a la propuesta doctoral:

**TmaqT — Arquitectura Topológica Multimodal para el Modelado Adaptativo del Gesto en Interfaces 
Háptico-Táctiles. (textil)**

El proyecto explorará la relación entre:

- superficies textiles sensibles
- interacción corporal
- sonido generativo
- modelos adaptativos

El repositorio funciona como un registro de laboratorio experimental donde se documentan códigos, pruebas de hardware y exploraciones audiovisuales.

Se encuentra en una etapa inicial de desarrollo, tomando como punto de partida **TTT2 (La Piel Tejida)** y sus primeras experimentaciones de interacción táctil ( gesto ) y sonido. Esta evolución plantea una pregunta central de investigación:

**¿Cómo pasar de una correspondencia fija gesto-respuesta a un sistema capaz de aprender relaciones nuevas entre interacción corporal, espacio latente y generación sonora?**

La investigación explora tanto nuevas posibilidades de creación artística mediante sistemas generativos como el desarrollo de arquitecturas computacionales adaptativas aplicables a diferentes interfaces multimodales, más allá de una única tecnología textil.


---

# TTT2 — La Piel Tejida

TTT2 es un prototipo de interfaz textil interactiva desarrollado dentro del proyecto:

*La Piel Tejida: Codificar y Significar mediante una Proto-Escritura desde una Constelación de 
Lenguajes.*

La superficie textil conductiva funciona como una interfaz donde el gesto corporal genera respuestas 
audiovisuales.

## Arquitectura inicial
GESTO
|

TEXTIL CONDUCTIVO
|

MPR121
24 zonas capacitivas
|

RASPBERRY PI
|
+-------------+
| |

SONIDO VISUAL
WAV Pygame


---

# Tecnologías

## Hardware

- Raspberry Pi
- 2 x MPR121
- 24 zonas capacitivas
- Superficie textil conductiva

## Software

- Python
- Pygame
- NumPy

---

# Evolución experimental

## Etapa 1 — Prototipo inicial

Implementación del sistema interactivo:

- lectura capacitiva
- activación sonora
- visualización generativa
- interacción en tiempo real


## Etapa 2 — Exploraciones audiovisuales

Pruebas con:

- capas sonoras
- mezcla dinámica
- variación temporal
- nuevas relaciones gesto-sonido


## Etapa 3 — Hacia sistemas más adaptativos y generativos

Primeras exploraciones hacia:

- representación del gesto
- espacios latentes
- Self-Organizing Maps (SOM)
- modelos generativos de sonido

---

# Relación con TmaqT ( TTT2)

TTT2 constituye el punto de partida experimental desde el cual surge la propuesta doctoral TmaqT. TTT2 es una interfaz textil reactiva con mapeos definidos, que corresponde a la Tesis de Magíster en Artes Mediales de la U. de Chile, 2025. https://www.academia.edu/144409160/TTT2_La_Piel_Tejida_Codificar_y_Significar_mediante_una_proto_Escritura_Desde_una_constelaci%C3%B3n_de_lenguaje_s_ 

TmaqT = evolución hacia una arquitectura adaptativa con aprendizaje automático no supervisado. Doctorado 2027:

"Pasar de una correspondencia fija gesto-respuesta a un sistema capaz de aprender relaciones nuevas entre interacción corporal, espacio latente y generación sonora, tanto como herramienta de exploración artística para la creación de nuevas formas de expresión audiovisual, como una arquitectura computacional implementable para interfaces multimodales adaptativas, aplicable no solo a superficies textiles, sino también a otros dispositivos sensibles, entornos interactivos y sistemas basados en la captura e interpretación del gesto humano."
