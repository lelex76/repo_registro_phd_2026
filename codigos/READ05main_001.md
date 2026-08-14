### Etapa 001 — `main05.py`

**Sistema FM + SOM polifónico con diferenciación espacial de zonas**

Esta etapa desarrolla el sistema TmaqT hacia una interacción textil **polifónica y espacialmente diferenciada**.

A diferencia de la versión inicial, donde el gesto global del tejido controlaba principalmente un único comportamiento sonoro, `main05.py` permite que **varias zonas táctiles permanezcan activas simultáneamente**, generando y manteniendo voces independientes.

El tejido comienza a comportarse no solamente como una superficie de entrada, sino como un **territorio sonoro distribuido**, donde cada zona participa de una configuración dinámica dentro del espacio latente.



puede producir una voz.

Pero una configuración como:

[ zona 3 ] + [ zona 14 ] + [ zona 21 ]

puede producir simultáneamente varias voces, cada una asociada a una zona diferente.

La polifonía, por tanto, no es solamente una superposición de sonidos: surge de la coexistencia temporal de diferentes relaciones entre contacto, zona y espacio latente.

Diferenciación de zonas

Aunque el SOM continúa siendo el principal mecanismo de organización del espacio táctil, main13.py introduce una segunda dimensión de diferenciación.

Cada zona posee una posición normalizada:

zone_position = zone / (NUM_ZONES - 1)

a partir de la cual se calcula:

zone_bias = zone_position - 0.5

Este valor desplaza ligeramente determinados parámetros de la voz.

De esta manera:

la zona no determina directamente una nota, pero tampoco desaparece completamente dentro de la representación latente.

La identidad sonora resulta de la combinación:

```
                    TEJIDO TEXTIL
                         │
                         ▼
                  24 zonas táctiles
                         │
                  ┌──────┴──────┐
                  │             │
               MPR121         MPR121
                0x5A           0x5C
                  │             │
                  └──────┬──────┘
                         │
                         ▼
                  Vector táctil 24D
                         │
                         ▼
                  Memoria gestual
                         │
                         ▼
                      SOM 6×4
                         │
                         ▼
                  Posición latente
                      (x, y)
                         │
                  ┌──────┴──────┐
                  │             │
                  ▼             ▼
          Diferenciación     Parámetros
             de zona         de síntesis
                  │             │
                  └──────┬──────┘
                         │
                         ▼
                    Voces FM × 4
                         │
                         ▼
                   Mezcla estéreo
                         │
                         ▼
                       Delay
                         │
                         ▼
                       SONIDO
```
El SOM funciona como una superficie de organización del gesto.

El vector de 24 sensores no se transforma simplemente en una coordenada fija. El mapa aprende progresivamente las configuraciones táctiles que aparecen durante la interacción y las organiza mediante relaciones de proximidad.

Por ello, una misma zona física puede participar de diferentes posiciones del SOM dependiendo del estado global del tejido.

El espacio latente es, entonces, una representación aprendida de las relaciones entre los contactos, y no un simple mapa físico de las 24 zonas.

Memoria

El sistema incorpora dos formas de persistencia:

Memoria gestual

gesture_memory

acumula temporalmente la actividad táctil y decae progresivamente.

Memoria de voz

Cada voz conserva su estado de amplitud y parámetros durante su release.

Esto permite que retirar un contacto no produzca necesariamente un corte abrupto del sonido.

La interacción adquiere así una dimensión temporal:

contacto → acumulación → sonido → liberación → desaparición
Polifonía

main05.py utiliza:

NUM_VOICES = 4

Cada voz mantiene:

zona de origen,
amplitud,
frecuencia portadora,
frecuencia de modulación,
índice FM,
posición estéreo,
identidad de zona,
estado de release.

La asignación dinámica mediante zone_voice permite mantener la relación entre una zona activa y una voz mientras esa interacción permanece vigente.

Síntesis sonora

La síntesis continúa basada en FM, pero sus parámetros ya no dependen exclusivamente de una coordenada.

La frecuencia portadora resulta de la combinación entre:

posición SOM
+
diferenciación de zona

Mientras que la modulación y el índice FM incorporan además información procedente de:

gesto
+
posición latente
+
zona
+
polifonía

El resultado es un sistema donde el timbre emerge de múltiples variables
relacionadas, en lugar de una correspondencia directa:

**sensor → nota**

### Cambio conceptual respecto a `main04.py`

```text
main04
────────────────────────────

24D
 │
 ▼
SOM
 │
 ▼
FM
 │
 ▼
sonido
 │
 └── comportamiento global


main05
────────────────────────────────────────

24D
 │
 ▼
memoria
 │
 ▼
SOM
 │
 ▼
espacio latente
 │
 ├── zona
 ├── gesto
 ├── voz
 └── tiempo
 │
 ▼
FM × 4 voces
 │
 ▼
sonido
```

La evolución principal no consiste solamente en agregar más voces.

Consiste en pasar de un sistema donde el gesto produce un comportamiento sonoro a uno donde múltiples relaciones táctiles pueden coexistir, persistir y desaparecer independientemente dentro de un espacio sonoro aprendido.

Estado de la arquitectura

main05.py constituye así una transición entre:

espacio latente aprendido

y

territorio sonoro interactivo.

El SOM comienza a funcionar como una estructura de organización relacional, mientras que la polifonía permite que diferentes contactos sean experimentados simultáneamente.

La arquitectura deja de responder únicamente a la pregunta:

¿Qué sonido corresponde a este gesto?

y comienza a explorar:

¿Qué relaciones sonoras pueden emerger cuando múltiples gestos coexisten dentro de un espacio aprendido?

---
