# TMAQT v15 — Síntesis completa

## Qué es

Sistema que **convierte gestos táctiles en sonido continuo y expresivo**:

- **Sensor:** MPR121 (24 zonas, 2 chips).
- **Gesto:** se resume en un vector de 20 números (`gesto_20d`).
- **Reducción:** 20D → 3D (`z_wav`) con `HybridReducer`.
- **Sonido:** 27 WAVs mezclados según `z_wav` (`LatentSonifier`).
- **Volumen:** `gate` sube al tocar, baja al soltar.
- **Aprendizaje:** `GrowingNeuralGas` (GNG) refina el gesto con el uso.

---

## Por qué se redujo 20D → 3D (breve)

Se redujo **a propósito**, por tres razones:

1. **Redundancia en las 20D:** muchas dimensiones miden lo mismo (duplicados de posición, derivadas). No aportan información nueva.
2. **PCA busca lo importante:** el `HybridReducer` usa PCA, que encuentra las **direcciones de mayor varianza**. Si las 3 primeras explican >80%, se pierde poco.
3. **Compatibilidad con el sistema:** el `SonicNavigator`, el `LatentSonifier` y el GNG trabajan en **3D**. Reducir a 3D es lo que permite que todo encaje.

**No es una pérdida arbitraria:** es una **compresión inteligente** que mantiene la riqueza útil y descarta ruido/redundancia.

---

## Arquitectura

### Flujo general del sistema

La arquitectura de TMAQT v15 organiza el procesamiento en una cadena que transforma el contacto físico en una 
representación gestual y, posteriormente, en una respuesta sonora.

**Contacto táctil → Captura sensora → Representación del gesto → Espacio latente 3D → Navegación y mezcla 
sonora → Salida de audio**

El sistema se compone de las siguientes etapas:

1. **Captura táctil:** dos controladores MPR121 registran el contacto en 24 zonas capacitivas distribuidas en la 
superficie textil.

2. **Representación gestual:** las señales capturadas se procesan para construir un vector de 20 dimensiones 
(`gesto_20d`), que resume características del gesto.

3. **Reducción dimensional:** `HybridReducer` transforma la representación de 20 dimensiones en un espacio de tres 
dimensiones (`z_wav`).

4. **Navegación sonora:** `SonicNavigator` y `LatentSonifier` utilizan la representación tridimensional para 
relacionar la trayectoria gestual con 27 archivos WAV y generar mezclas sonoras.

5. **Control de respuesta:** el parámetro `gate` regula la intensidad sonora en relación con el contacto, 
aumentando al tocar y disminuyendo al soltar.

6. **Adaptación:** `GrowingNeuralGas` (GNG) actualiza la organización de las representaciones gestuales a partir 
del uso, explorando relaciones que pueden modificarse con la experiencia.


## Proyección: retroalimentación y coadaptación humano–IA

A partir de la arquitectura de TMAQT v15, la investigación doctoral pretende explorar un sistema de interacción 
humano–IA basado en retroalimentación recíproca, aprendizaje no supervisado en línea (*online unsupervised 
learning*) y generación sonora. Se busca que la persona no solo produzca gestos táctiles que el sistema transforma 
en sonido, sino que también pueda intervenir en las propuestas sonoras generadas por la IA. A su vez, el sistema 
podrá incorporar nuevas experiencias táctiles, modificar progresivamente su organización interna y generar nuevas 
respuestas. Se propone así investigar un proceso de coadaptación en el que la persona y el sistema puedan 
influirse mutuamente, manteniendo la persona el control sobre los materiales de partida y las condiciones y 
límites del aprendizaje y la generación.

### Referente: jam_bot — MIT Media Lab

El proyecto *Jordan Rudess + jam_bot: A Human-AI Musical Dialogue*, desarrollado por el grupo Responsive 
Environments del MIT Media Lab, constituye un referente para esta proyección. jam_bot es un sistema de IA 
generativa diseñado para improvisar musicalmente junto a un intérprete. Escucha la interpretación humana, genera 
respuestas musicales en tiempo real y puede asumir distintos roles dentro de la improvisación, alternando entre 
acompañar al músico y proponer material propio.

Su interés para TmaqT reside en explorar la IA como un agente creativo que no solo responde a la persona, sino que 
también propone e interviene en un proceso sonoro compartido. TmaqT busca ampliar esta perspectiva incorporando el 
tacto como medio de interacción y el aprendizaje incremental no supervisado como una dimensión adicional de 
adaptación del sistema. A diferencia de jam_bot, la propuesta contempla que las nuevas experiencias táctiles 
puedan modificar progresivamente la organización interna del modelo y afectar sus futuras respuestas sonoras.

### Dos precisiones para mantener rigurosa la síntesis

- **jam_bot es un referente de generación, improvisación y retroalimentación interactiva**, no una demostración de 
aprendizaje no supervisado continuo durante la actuación. Sus modelos se preentrenan y ajustan (*fine-tuning*) con 
interpretaciones de Jordan Rudess.

- **La coadaptación que propones para TmaqT va un paso más allá:** no solo cambiaría la respuesta del sistema ante 
cada intervención; investigarías si las experiencias táctiles pueden modificar progresivamente su organización 
interna y, a través de ella, sus propuestas sonoras.

### Referencias

Blanchard, L., Naseck, P., Brade, S., Lecamwasam, K., Rudess, J., Huang, C.-Z. A., & Paradiso, J. (2025). *The 
jam_bot, a Real-Time System for Collaborative Free Improvisation with Music Language Models*. Proceedings of the 
26th International Society for Music Information Retrieval Conference, 755–762. 
https://doi.org/10.5281/zenodo.17811478

Blanchard, L., Naseck, P., Liang, K., Tan, J., Lei, H., Huang, C.-Z. A., & Paradiso, J. (2026). *Enhancing 
Expressive Musical Conversation in the jam_bot*. Proceedings of the International Conference on New Interfaces for 
Musical Expression, 621–626. https://doi.org/10.5281/zenodo.20784228

MIT Media Lab. *Jordan Rudess + jam_bot: A Human-AI Musical Dialogue*. 
https://www.media.mit.edu/projects/jordan-rudess-genai/overview/
