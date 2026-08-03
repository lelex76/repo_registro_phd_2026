# TTT2 Original Code — La Piel Tejida

Este código corresponde a la primera implementación funcional del 
prototipo **TTT2 (La Piel Tejida)** desarrollado durante la investigación 
de tesis.

El sistema implementa una interfaz textil interactiva basada en una 
superficie conductiva conectada a una Raspberry Pi mediante sensores 
capacitivos **MPR121** (24 zonas táctiles).

La arquitectura integra:

- Raspberry Pi 4B
- Dos sensores capacitivos MPR121
- Interfaz textil conductiva
- Python
- Pygame
- Reproducción y mezcla de capas sonoras
- Generación visual en tiempo real

Cada interacción táctil sobre el tejido activa comportamientos 
audiovisuales predefinidos mediante una correspondencia determinista entre 
gesto, sonido e imagen.

El código implementa:

- Lectura de sensores capacitivos mediante I2C
- Activación de capas sonoras independientes
- Control dinámico de volumen y transiciones (*fade*)
- Generación de curvas visuales mediante geometrías Bézier
- Relación entre gesto corporal, superficie textil y respuesta 


Además de la superficie textil, el sistema incorpora dos pedales mono como 
elementos de control complementarios, ampliando la interacción desde el 
gesto manual hacia una experiencia corporal distribuida.

La combinación entre el contacto táctil con el tejido y la activación 
mediante pedales permite explorar relaciones entre movimiento corporal, 
producción sonora y respuesta visual, configurando una interfaz 
audiovisual interactiva donde diferentes acciones del cuerpo generan 
comportamientos computacionales.

Esta versión representa la etapa inicial del proyecto, basada en reglas 
fijas de interacción. Posteriormente, estas exploraciones dieron origen a 
la investigación TmaqT, orientada hacia arquitecturas adaptativas mediante 
aprendizaje automático, representación latente y organización topológica 
del gesto, iniciando una nueva etapa de experimentación.





