# ESPLAT_01 — Espacio latente sonoro

## ¿Qué estamos haciendo?

Estamos construyendo un pequeño sistema experimental para explorar una pregunta:

> **¿Qué ocurre si podemos dibujar, navegar y escuchar un espacio latente?
**
La idea principal es:

**datos táctiles → modelo → espacio latente → navegación → sonido**

No se está diciendo qué significa cada zona del espacio.

Queremos **explorar qué aparece**.

---

# 1. Generación de datos

1. Se crean datos artificiales que representen estados de:

**24 zonas táctiles.**

Se obtienen:

- 5000 muestras
- 24 dimensiones por muestra

Por eso:

```text
X = (5000, 24)


Cada muestra puede imaginarse como:

zona 1
zona 2
zona 3
...
zona 24

**2. Tenemos 24 dimensiones**

Podemos explorar físicamente las 24 zonas conductivas del textil.

Cada zona produce un valor, por lo que en un instante tenemos:

24 zonas
↓
24 valores
↓
un estado de 24 dimensiones

El computador puede trabajar perfectamente con esos 24 valores.

La dificultad aparece cuando queremos visualizar y explorar
las relaciones entre muchos estados de 24 dimensiones.

Por eso utilizamos el Encoder para construir una representación
más pequeña y visualizable:

24 dimensiones
↓
Encoder
↓
2 dimensiones
(z₁, z₂)

Estas dos dimensiones forman el espacio latente.

**3. Construimos un Autoencoder
**
El Autoencoder aprende a:

ENTRADA
24 valores
   ↓
ENCODER
   ↓
ESPACIO LATENTE
2 valores
   ↓
DECODER
   ↓
RECONSTRUCCIÓN
24 valores

El modelo intenta aprender una representación comprimida de los datos.

**4. El Encoder comprime
**
El Encoder transforma:

24 dimensiones
      ↓
2 dimensiones

Estas dos dimensiones son:

z₁
z₂

Por ejemplo:

[-0.17, 3.18]

Ese punto representa un estado aprendido por el modelo.

**5. Aparece el espacio latente**

Ahora se puede visualizar los datos como puntos en un plano:

             z₂
              ↑
              |
       •      •
          •
    •
              •
              |
              +------------→ z₁

El espacio latente no fue dibujado manualmente.

Fue aprendido por el modelo.

**6.  Escoger un punto**

Por ejemplo:

Punto A
[-0.177, 3.182]

y otro:

Punto B
[-1.981, 5.779]

También se puede calcular puntos entre ellos.

Por ejemplo:

Punto intermedio
[-1.079, 4.480]

Así descubrimos que es posible moverse dentro del espacio latente.

**7. El Decoder permite volver**

Ahi se tiene:

z₁
z₂

y se puede enviarlos al Decoder.

El Decoder genera nuevamente:

24 valores

Por ejemplo:

z₁,z₂
 ↓
DECODER
 ↓
24 valores

Es decir:

 navegar por el espacio de 2 dimensiones y observar qué estados de 24 dimensiones produce el modelo.

**8. Reconstrucción**

Probamos un punto y se observa qué tan bien el Decoder reconstruye el estado original.

Obtuvimos, por ejemplo:

Error de reconstrucción:
0.066

No significa que el modelo sea perfecto.

Significa que el modelo está aprendiendo una relación entre:

24D ↔ 2D

**9. Construcción de una trayectoria**

En lugar de mirar solamente un punto:

A

podemos desplazarnos:

A → → → → → B

Creamos una trayectoria de puntos dentro del espacio latente.

Por ejemplo:

Forma:
(21, 2)

Eso significa:

21 posiciones
2 coordenadas por posición

El punto intermedio nos permite observar qué ocurre mientras nos desplazamos de un estado a otro.

No saltamos directamente de A a B.

El modelo genera un estado intermedio y podemos observar cómo cambia la representación de 24 dimensiones durante
ese recorrido.

Esto permite estudiar la trayectoria y no solamente
los estados inicial y final.

Esto calcula un punto entre A y B.

alpha = 0.5 significa 50% del camino.

A ●────────● B
      ↑
   punto intermedio

**10. Cada posición produce un estado
**
Cada punto de la trayectoria entra al Decoder.

Por eso se obtienen:

21 posiciones latentes
        ↓
21 estados de 24 dimensiones

Tenemos entonces:

espacio latente
      ↓
decoder
      ↓
secuencia de estados 24D

**11. Comparamos estados consecutivos**

Ahora pregunto:

**¿Cuánto cambia el estado cuando avanzamos un poco?**

Calculamos la diferencia entre estados consecutivos.

Se obtuvo, por ejemplo:

0.0479
0.0479
0.0479
...
0.0366

Esto nos permite observar cómo cambia el estado generado por el modelo.

**12. Aparece la idea de sensibilidad**

Podemos comparar:

cuánto me moví en el espacio latente

con:

cuánto cambió el estado de 24 dimensiones

Si un pequeño movimiento produce un gran cambio:

alta sensibilidad

Si un movimiento produce un cambio pequeño:

baja sensibilidad

**13. Campo de sensibilidad**

Esto me permite empezar a pensar el espacio latente no solamente como:

un plano con puntos

sino como:

***un territorio con comportamientos diferentes.***

Algunas regiones pueden ser estables.

Otras pueden cambiar rápidamente.

**14. Exploramos la sensibilidad**

Calculamos:

sensibilidad media
sensibilidad mínima
sensibilidad máxima

Por ejemplo:

Sensibilidad media:
0.261


Mínima:
0


Máxima:
0.319

Sin estar asignando nombres a las zonas.

No se dice:

zona = emoción
zona = gesto
zona = sonido

Simplemente se observa cómo se comporta el modelo.

**15. Comenzamos a operar el espacio**

Introducimos controles para poder movernos por el espacio latente.

La idea cambia de:

modelo que observamos

a:

espacio que podemos explorar

**16. Se elige una posición**

Al seleccionar una coordenada:

z₁ = -2.666
z₂ = 2.038

El Decoder genera:

24 valores

Es decir:

posición
   ↓
modelo
   ↓
estado 24D

**17. Visualizamos el estado generado**

Se Observan los 24 valores producidos.

Por ejemplo:

[0.68, 0.59, 0.47, ... , 0.77]

***Esto significa que una posición de solamente:
2 dimensiones***

puede producir un estado complejo de:

24 dimensiones.

**18. Creamos trayectorias más largas**

Ya no solamente vamos:

A → B

Se puede recorrer muchas posiciones:

A
 \
  \
   \____
        \
         \
          B

Por ejemplo:

240 posiciones

**19. Convertir la trayectoria en sonido**

Ahora se añade otra capa.

Los 24 valores pueden utilizarse para controlar síntesis sonora.

Entonces:

trayectoria
     ↓
espacio latente
     ↓
decoder
     ↓
24 valores
     ↓
síntesis sonora
     ↓
SONIDO

Ya no solamente vemos el espacio.

Podemos escucharlo.

**20. Aparece la idea de navegación sonora**

Ahora la trayectoria no es solamente:

dibujar una línea

Es:

moverse por un espacio

donde cada posición puede producir una configuración sonora diferente.

**21. Volvemos al Canvas**

Creamos un Canvas.

El Canvas representa el espacio latente:

              z₂
               ↑
               |
               |
               |
               +--------------→ z₁

Se puede colocar el cursor en diferentes lugares.

**22. Dibujamos sobre el espacio
**

Al mantener pulsado el mouse podemos dibujar:

       ●
      /
     /
    /____
         \
          ●

La trayectoria queda registrada como una serie de puntos.

**23. La trayectoria se convierte al espacio latente**

Los píxeles del Canvas:

x,y

se convierten en:

z₁,z₂

Por ejemplo:

Canvas
(300,400)
     ↓
Latente
(-1.2,4.3)

***Así el dibujo no es solamente una imagen.***

Es una navegación por el espacio aprendido.

**24. Dibujar → latente → 24D → sonido**

La cadena completa comienza a ser:

DIBUJO
  ↓
x,y
  ↓
z₁,z₂
  ↓
DECODER
  ↓
24D
  ↓
SÍNTESIS
  ↓
SONIDO

**25. Medimos la sensibilidad de la trayectoria**

Cuando se dibuja una trayectoria podemos calcular nuevamente:

distancia en el espacio latente

y:

cambio producido en 24D

para estimar:

sensibilidad

Así podemos comparar diferentes recorridos.

```text
24 zonas táctiles
       ↓
   Autoencoder
       ↓
espacio latente
       ↓
   tú te mueves
       ↓
¿cuánto cambia la salida del Decoder?
       ↓
   SENSIBILIDAD
   

**26. Encontramos zonas diferentes**

Por ejemplo:

Zona de menor sensibilidad
0.0

y:

Zona de mayor sensibilidad
0.319

Esto empieza a mostrar que el espacio aprendido no se comporta de manera uniforme.

En código, la idea es aproximadamente:
sensibilidad = cambio_24D / distancia_latente

**27. Sensibilidad → sonido**

Introducimos la sensibilidad en la síntesis.

Ahora se tienen:

posición
   ↓
estado 24D
   ↓
sensibilidad
   ↓
sonido

La sensibilidad no recibe una etiqueta como:

"esto es un sonido agudo"

Simplemente modifica la transformación sonora.

**28. Navegación interactiva**

Se crea una interfaz donde el cursor muestra:

z₁ = ...
z₂ = ...
sensibilidad = ...

Mientras se dibuja es posible observar dónde estamos.

La trayectoria queda guardada.

**29. Nuestra propia trayectoria produce sonido**

Tomo el dibujo que acabo de hacer:

267 puntos

y hago:

267 puntos
    ↓
267 posiciones latentes
    ↓
267 estados 24D
    ↓
sensibilidad
    ↓
sonido

Por ejemplo:

Inicio:
[-3.086, 4.334]


Final:
[4.159, 1.460]

Ya no se escucha una trayectoria inventada.

Estamos escuchando una trayectoria dibujada por nosotros.

**30. ESPLAT LIVE**

Finalmente hacemos que la navegación y el sonido ocurran simultáneamente.

Ahora podemos:

MOVER
  ↓
NAVEGAR
  ↓
DIBUJAR
  ↓
ESCUCHAR


El cursor controla en tiempo real:

z₁
z₂
sensibilidad

y estos parámetros modifican el sonido.

La interfaz se convierte en algo parecido a un instrumento:

                 CUERPO / GESTO
                       ↓
                    CURSOR
                       ↓
                ESPACIO LATENTE
                  ↙         ↘
             VISUAL          SONIDO
                ↓               ↓
             TRAYECTORIA    TRANSFORMACIÓN
             
             
¿Qué se ha construido realmente?

**No se ha construido aún un sistema que "entienda" qué significa un tacto.**

Se ha construido algo más experimental:

**un espacio aprendido que puede ser recorrido, visualizado y sonificado.**

El modelo aprende una relación entre los 24 valores de entrada y una representación de 2 dimensiones.

Después se intervinió ese espacio mediante el movimiento. (cursor que dibuja-se desplaza )

Por eso aparecen tres niveles:

1. DATOS
   24 dimensiones


        ↓


2. REPRESENTACIÓN
   espacio latente 2D


        ↓


3. EXPERIENCIA
   navegación + visualización + sonido

Y la pregunta interesante que queda abierta es:

**¿Qué propiedades del espacio aprendido pueden hacerse perceptibles mediante el movimiento, la imagen y el sonido?**

Importante:

ESPLAT_01 todavía es un experimento.

No estoy afirmando que:

z₁ = una cosa
z₂ = otra cosa

ni que una zona determinada tenga un significado psicológico o musical fijo.

El objetivo es explorar qué emerge cuando:

datos
+
modelo
+
espacio latente
+
movimiento
+
sonido

se ponen en relación.

**ESPLAT LIVE — estado actual**

Ya se consiguió:

5000 muestras
24 dimensiones
Autoencoder
espacio latente 2D
Decoder
reconstrucción
trayectorias
sensibilidad
visualización
dibujo libre
conversión dibujo → latente
sonificación
navegación interactiva
sonido durante la navegación

Y finalmente:

dibujar + navegar + escuchar simultáneamente.

El siguiente paso no es necesariamente agregar más cosas.

Es preguntarse:

¿Qué cambia si ahora el sonido deja de ser una simple síntesis controlada por z₁, z₂ y sensibilidad, y pasa a ser generado directamente por los 24 valores que produzca el Decoder?

**Ahí comienza una versión mucho más fuerte de ESPLAT.**
