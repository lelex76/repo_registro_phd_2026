# Registro de proceso experimental

## Desarrollo evolutivo desde TTT2 hacia TmaqT

Este documento registra el proceso de desarrollo experimental, las decisiones metodológicas, las pruebas de hardware y software, y las transformaciones conceptuales que llevaron desde la primera implementación de TTT2 hacia las exploraciones actuales de TmaqT.

A diferencia del README principal, que presenta la arquitectura general del proyecto, este documento funciona como una bitácora de investigación donde se documentan las diferentes versiones de código, sus objetivos, resultados, limitaciones y las razones que llevaron a nuevas etapas de desarrollo.
---


Este proceso experimental constituye la transición desde TTT2 hacia TmaqT, una evolución desde una interfaz textil 
reactiva hacia una arquitectura adaptativa basada en aprendizaje automático, representación latente y organización 
topológica del gesto.

Mi investigación explora cómo una superficie textil sensible puede transformarse en un sistema relacional capaz de 
establecer nuevas conexiones entre cuerpo, materia, datos y sonido. En este recorrido, el textil deja de funcionar 
únicamente como una superficie de entrada táctil y comienza a comprenderse como una piel informante: una interfaz 
capaz de recibir, organizar y transformar información mediante la interacción corporal.

La incorporación de modelos de inteligencia artificial en el borde (Edge AI), TinyML y modelos generativos 
pequeños abre la posibilidad de desarrollar sistemas donde la relación entre gesto y sonido no esté determinada 
por correspondencias predefinidas, sino que emerja progresivamente mediante procesos de aprendizaje, adaptación y 
exploración de espacios latentes.

TmaqT se plantea entonces como una arquitectura experimental para investigar nuevas formas de interacción 
audiovisual, donde el contacto háptico con la materia textil participa en la generación sonora a través de modelos 
computacionales capaces de aprender relaciones dinámicas entre gesto, comportamiento y síntesis.

Esta investigación busca desarrollar herramientas artísticas para nuevas formas de expresión audiovisual, pero 
también explorar arquitecturas computacionales aplicables a interfaces multimodales sensibles, superficies 
deformables y otros sistemas basados en la captura e interpretación del gesto humano.

--- ---

# 1. Punto de partida: TTT2 — La Piel Tejida

## Pregunta inicial

¿Cómo puede una superficie textil conductiva transformarse en una interfaz sensible capaz de relacionar gesto corporal, sonido y representación visual?

## Arquitectura inicial

```text
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
| NumPy                |
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


## Características iniciales

- interacción táctil sobre superficie textil
- adquisición gestual mediante sensores capacitivos
- correspondencias deterministas entre gesto y respuesta audiovisual
- generación visual en tiempo real
- utilización de capas sonoras predefinidas

## Limitación identificada

El sistema permitía una interacción corporal expresiva, pero la relación entre gesto y respuesta permanecía definida previamente.

La pregunta que emerge desde esta primera etapa es:

> ¿Cómo pasar de una correspondencia fija gesto-respuesta hacia un sistema capaz de aprender nuevas relaciones entre interacción corporal, espacio latente y generación sonora?

---

# 2. Desarrollo experimental de códigos

Los siguientes códigos representan diferentes hipótesis experimentales dentro del proceso de investigación.

Cada versión no corresponde solamente a una mejora técnica, sino a una transformación en la manera de comprender la relación entre:

- cuerpo
- gesto
- materia textil
- datos
- síntesis sonora
- Aprendizaje automático

---

### Etapa 02 — `main02.py` (instrumento textil v2)

**Versión evolucionada del instrumento textil original TTT2.**  
Introduce estructura modular, perfiles por zona y mezcla de capas WAV.

---

### Objetivo
Crear una **versión 2.0 del instrumento textil**, más robusta y modular, mejorando:

- arquitectura sonora  
- organización del código  
- expresividad del tejido  
- escalabilidad hacia versiones posteriores (03, 09, 10)

Funciona como **puente** entre el código original y las etapas híbridas/FM.

---

### Arquitectura

#### 1. Sistema táctil (MPR121 dual)
- 24 electrodos (zonas conductivas independientes)  
- lectura touch/no-touch  
- memoria táctil simple  
- suavizado básico  

#### 2. Perfiles sonoros por zona
- 3 capas WAV por zona  
- selección según posición (x,y)  
- volumen base + energía táctil  
- fade orgánico  
- paneo estéreo  
- **72 canales de audio**

#### 3. Curvas textiles
- curvas Bezier animadas  
- intensidad según memoria táctil  
- movimiento orgánico  
- vida limitada  
- representación visual del gesto (similar al original)

#### 4. Motor WAV
- activación por contacto  
- reproducción continua  
- fade-out sin contacto  
- arquitectura modular

---

### Implementación
- **Lectura táctil:** 24 electrodos, actualización de estado y memoria  
- **Audio:** 9 WAV, mezcla por zona, 72 canales, volumen dinámico  
- **Visualización:** curvas Bezier animadas por frame  
- **Loop principal:** lectura táctil, memoria, sonido, curvas, FPS

---

### Resultados
- Instrumento textil más expresivo que el original  
- Zonas con identidad sonora propia  
- Texturas más complejas  
- Curvas visuales más coherentes con el gesto  
- Sistema estable, modular y escalable  

---

### Limitaciones
- Sin RF (AD8318, MCP3008)  
- Sin síntesis FM  
- Sin SOM  
- Mezcla WAV estática  
- Memoria táctil simple  
- Paneo estéreo básico  
- Control tímbrico limitado al volumen  

---

### Aprendizajes obtenidos
- Importancia de modularizar para futuras expansiones  
- Valor de los perfiles por zona  
- Curvas textiles como representación del gesto (aunque se exploró más lo sonoro)  
- Cómo manejar 72 canales sin saturar CPU  
- Base para integrar memoria tímbrica, SOM, FM y RF  
- Etapa intermedia esencial hacia TmaqT  
---
### Etapa 03 — `main03.py` (instrumento textil híbrido)

**Versión híbrida del instrumento textil.**  
Introduce memoria tímbrica real, modulación de capas WAV y dinámica tímbrica dependiente del gesto.  
Es el puente entre la etapa textil pura (02) y las etapas RF/FM/SOM (09 y 10).

---

### Objetivo
Crear una **versión híbrida** del instrumento textil que combine:

- interacción táctil (MPR121)
- perfiles sonoros por zona
- **memoria tímbrica real**
- **modulación de capas WAV**
- dinámica tímbrica dependiente del gesto

Esta etapa prepara la transición hacia RF (main09) y FM + SOM (main10).

---

### Arquitectura

#### 1. Sistema táctil (MPR121 dual)
- 24 electrodos  
- lectura touch/no-touch  
- memoria táctil + memoria tímbrica  
- suavizado básico  

#### 2. Perfiles sonoros híbridos
- 3 capas WAV por zona  
- volumen dinámico según memoria tímbrica  
- modulación tímbrica simple  
- paneo estéreo  
- 72 canales de audio  

#### 3. Curvas textiles híbridas
- curvas Bezier animadas  
- vida dependiente de memoria tímbrica  
- movimiento orgánico  
- representación del gesto + estado tímbrico  

#### 4. Motor híbrido WAV
- activación por contacto  
- reproducción continua  
- volumen modulado por memoria tímbrica  
- fade-out sin contacto  
- arquitectura modular para FM/RF

---

### Implementación
- **Lectura táctil:** 24 electrodos, estado + memoria tímbrica  
- **Audio:** 9 WAV, mezcla por zona, modulación tímbrica  
- **Visualización:** curvas Bezier híbridas  
- **Loop:** lectura táctil, memoria, sonido, curvas, FPS

---

### Resultados
- Instrumento textil con **mayor expresividad tímbrica**  
- Zonas con evolución sonora dependiente del gesto  
- Curvas textiles más vivas y coherentes con la energía táctil  
- Sistema estable y preparado para RF/FM/SOM  

---

### Limitaciones
- Sin RF (AD8318, MCP3008)  
- Sin FM real (solo modulación WAV)  
- Sin SOM ni mapa latente  
- Memoria tímbrica aún simple  
- Modulación tímbrica limitada  

---

### Aprendizajes obtenidos
- Cómo integrar memoria tímbrica en un sistema textil  
- Cómo modular capas WAV sin saturar CPU  
- Cómo vincular gesto táctil con evolución tímbrica  
- Base conceptual para RF, FM y SOM  
- Etapa clave para pasar de textil puro a instrumento híbrido TmaqT

---

### Etapa 03 — `main03.py` (instrumento textil híbrido)

Versión híbrida del instrumento textil.
Introduce memoria tímbrica real, modulación de capas WAV y dinámica tímbrica dependiente del gesto.  
Es el puente entre la etapa textil pura (02) y las etapas RF/FM/SOM (09 y 10).

---

### Objetivo
Crear una **versión híbrida** del instrumento textil que combine:

- interacción táctil (MPR121)
- perfiles sonoros por zona
- memoria tímbrica real
- modulación de capas WAV
- dinámica tímbrica dependiente del gesto

Esta etapa prepara la transición hacia RF (main09) y FM + SOM (main10).

---

### Arquitectura

#### 1. Sistema táctil (MPR121 dual)
- 24 electrodos  
- lectura touch/no-touch  
- memoria táctil + memoria tímbrica  
- suavizado básico  

#### 2. Perfiles sonoros híbridos
- 3 capas WAV por zona  
- volumen dinámico según memoria tímbrica  
- modulación tímbrica simple  
- paneo estéreo  
- 72 canales de audio  

#### 3. Curvas textiles híbridas
- curvas Bezier animadas  
- vida dependiente de memoria tímbrica  
- movimiento orgánico  
- representación del gesto + estado tímbrico  

#### 4. Motor híbrido WAV
- activación por contacto  
- reproducción continua  
- volumen modulado por memoria tímbrica  
- fade-out sin contacto  
- arquitectura modular para FM/RF

---

### Implementación
- Lectura táctil: 24 zonas, estado + memoria tímbrica  
- Audio: 9 WAV, mezcla por zona, modulación tímbrica  
- Visualización:curvas Bezier híbridas  
- Loop: lectura táctil, memoria, sonido, curvas, FPS

---

### Resultados
- Instrumento textil con **mayor expresividad tímbrica**  
- Zonas con evolución sonora dependiente del gesto  
- Curvas textiles más vivas y coherentes con la energía táctil  
- Sistema estable y preparado para RF/FM/SOM  

---

### Limitaciones
- Sin RF (AD8318, MCP3008)  
- Sin FM real (solo modulación WAV)  
- Sin SOM ni mapa latente  
- Memoria tímbrica aún simple  
- Modulación tímbrica limitada  

---

### Aprendizajes obtenidos
- Cómo integrar memoria tímbrica en un sistema textil  
- Cómo modular capas WAV sin saturar CPU  
- Cómo vincular gesto táctil con evolución tímbrica  
- Base conceptual para RF, FM y SOM  
- Etapa clave para pasar de textil puro a instrumento híbrido TmaqT
---


### Etapa 00 — `main04.py`  
**Sistema FM + SOM inicial (versión base del ciclo doctoral 2027)**

Esta etapa inaugura el nuevo paradigma del instrumento TmaqT:  
un sistema autónomo donde el gesto textil se transforma en morfología sonora a través de un mapa SOM y síntesis FM.  
Es la primera versión del **motor latente**, y constituye la base conceptual del doctorado transdisciplinario 2027.

---

### Objetivo
Construir la **primera versión del sistema autónomo TmaqT**, donde:

- el gesto textil (24D) se convierte en un vector latente 2D mediante un SOM,
- ese vector latente controla parámetros de síntesis FM,
- el sistema desarrolla **memoria tímbrica** y **memoria gestual**,
- el sonido emerge de la interacción prolongada con el tejido.

Esta etapa define el **inicio del ciclo doctoral**:  
la arquitectura FM + SOM como fundamento del comportamiento emergente.

---

### Arquitectura del sistema

#### 1. Entrada táctil (MPR121 dual)
- 24 electrodos (12 izquierda + 12 derecha).  
- Lectura binaria → vector 24D.  
- Suavizado temporal para convertir contacto en trayectoria.  
- Memoria gestual acumulativa.

#### 2. SOM (Self‑Organizing Map)
- Mapa 2D de tamaño 6×4.  
- Cada neurona contiene un vector de pesos 24D.  
- Aprendizaje continuo: el mapa se adapta a la experiencia táctil.  
- BMU (Best Matching Unit) determina la posición latente del gesto.

#### 3. Espacio latente
- Coordenadas (x_latent, y_latent) definen:
  - frecuencia portadora (fc),
  - frecuencia moduladora (fm),
  - índice FM (index),
  - amplitud (amp),
  - futura espacialización (pan).

#### 4. Síntesis FM
- Oscilador modulador + portadora.  
- Tres capas espectrales:
  - subgrave,  
  - cuerpo FM,  
  - armónicos altos.  
- Mezcla espectral + saturación suave.  
- Motor estéreo preparado para paneo.

#### 5. Memoria tímbrica
- Acumula energía del gesto.  
- Controla la complejidad del índice FM.  
- Produce evolución tímbrica dependiente de exploración.

#### 6. Campo ambiental continuo
- Oscilador + ruido.  
- Fondo resonante del tejido.  
- Funciona como “atmósfera” del instrumento.

---

### Implementación técnica

- **Audio:** pygame mixer, 48 kHz, buffer 256.  
- **FM:** cálculo por bloque, actualización de fase, mezcla espectral.  
- **SOM:** distancia euclidiana, BMU, influencia radial, aprendizaje exponencial.  
- **Memoria:** dos memorias:
  - gestual (24D),
  - tímbrica (escalar).  
- **Latente → FM:** mapeo directo de coordenadas SOM a parámetros FM.  
- **Loop principal:** lectura → suavizado → SOM → latente → FM → reproducción.

---

### Resultados
- Primer instrumento textil con **síntesis FM controlada por un mapa SOM**.  
- El gesto produce **morfología sonora**, no solo activación.  
- El sistema desarrolla **memoria tímbrica** y responde de forma no lineal.  
- El sonido evoluciona según la historia del gesto.  
- Se establece la base del **comportamiento emergente**.

---

### Limitaciones
- SOM pequeño (6×4).  
- FM de 2 operadores (versión inicial).  
- Sin integración RF (queda en experimento aparte).  
- Sin mapa latente avanzado (eso será `main10`).  
- Sin paneo espacial real (solo preparado).  
- Sin aprendizaje multimodal (solo tacto).

---

### Aprendizajes obtenidos
- Cómo mapear un gesto textil 24D a un espacio latente 2D.  
- Cómo usar SOM como interfaz sonora.  
- Cómo generar timbre emergente mediante memoria tímbrica.  
- Cómo vincular materialidad textil con síntesis FM.  
- Cómo construir un motor autónomo que evoluciona con la interacción.  
- Base conceptual para la versión avanzada (`main10`) del doctorado 2027.

-----


# Reflexiones metodológicas

El desarrollo de TTT2 hacia TmaqT representa una transición:

Desde:

```text

GESTO

  |

REGLA FIJA

  |

SONIDO


Hacia:


GESTO

  |

REPRESENTACIÓN

  |

ESPACIO LATENTE

  |

SÍNTESIS SONORA

  |

COMPORTAMIENTO EMERGENTE

```

