
Sistema FM + SOM polifónico con diferenciación espacial de zonas.

## Qué hace

El textil deja de ser una superficie de entrada y se vuelve un **territorio sonoro distribuido**: varias zonas pueden estar activas a la vez, cada una sosteniendo una voz.

## Flujo

```text
24 zonas táctiles (MPR121)
        ↓
   Vector táctil 24D
        ↓
   Memoria gestual
        ↓
      SOM 6×4
        ↓
  Posición latente (x, y)
        ↓
 ┌──────┴──────┐
 ▼             ▼
Diferenciación  Parámetros
de zona         de síntesis
 └──────┬──────┘
        ↓
   Voces FM × 4
        ↓
   Mezcla estéreo
        ↓
      Delay
        ↓
      SONIDO
Polifonía
NUM_VOICES = 4

Cada voz mantiene:

zona de origen

amplitud

frecuencia portadora

frecuencia de modulación

índice FM

posición estéreo

identidad de zona

estado de release

Una zona puede producir una voz. Tres zonas simultáneas producen tres voces. La polifonía no es superposición: es coexistencia temporal de relaciones entre contacto, zona y espacio latente.

Diferenciación de zonas
Cada zona tiene una posición normalizada:

python
zone_position = zone / (NUM_ZONES - 1)
zone_bias = zone_position - 0.5
Ese valor desplaza ligeramente los parámetros de la voz.

La zona no determina una nota, pero tampoco desaparece dentro del latente.

Memoria
Dos formas de persistencia:

Memoria gestual — gesture_memory acumula actividad táctil y decae progresivamente.

Memoria de voz — cada voz conserva amplitud y parámetros durante su release.

Retirar un contacto no produce un corte abrupto.

text
contacto → acumulación → sonido → liberación → desaparición
El SOM como superficie de organización
El SOM no es un mapa físico de las 24 zonas. Aprende progresivamente las configuraciones táctiles que aparecen durante la interacción y las organiza por proximidad.

Una misma zona puede participar de diferentes posiciones del SOM según el estado global del tejido.

Síntesis
La frecuencia portadora combina:

text
posición SOM + diferenciación de zona
La modulación y el índice FM incorporan además:

text
gesto + posición latente + zona + polifonía
El timbre emerge de múltiples variables relacionadas, no de una correspondencia directa sensor → nota.

Cambio respecto a main04.py
text
main04
──────────────
24D → SOM → FM → sonido
(comportamiento global)

main05
──────────────────────────────
24D → memoria → SOM → latente
                         ├── zona
                         ├── gesto
                         ├── voz
                         └── tiempo
                         ↓
                    FM × 4 voces
                         ↓
                       sonido
No es solo agregar voces. Es pasar de un sistema donde el gesto produce un sonido a uno donde múltiples relaciones táctiles coexisten, persisten y desaparecen dentro de un espacio sonoro aprendido.

Estado de la arquitectura
main05.py es la transición entre:

espacio latente aprendido

territorio sonoro interactivo

El SOM funciona como estructura de organización relacional.
La polifonía permite experimentar varios contactos a la vez.

La pregunta deja de ser:

¿Qué sonido corresponde a este gesto?

Y pasa a ser:

¿Qué relaciones sonoras pueden emerger cuando múltiples gestos coexisten dentro de un espacio aprendido?
