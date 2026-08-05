# Registro de proceso experimental

## Desarrollo evolutivo desde TTT2 hacia TmaqT

Este documento registra el proceso de desarrollo experimental, las decisiones metodológicas, las pruebas de hardware y software, y las transformaciones conceptuales que llevaron desde la primera implementación de TTT2 hacia las exploraciones actuales de TmaqT.

A diferencia del README principal, que presenta la arquitectura general del proyecto, este documento funciona como una bitácora de investigación donde se documentan las diferentes versiones de código, sus objetivos, resultados, limitaciones y las razones que llevaron a nuevas etapas de desarrollo.

---

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
- aprendizaje computacional

---

# Código 01 — [Nombre pendiente]

## Objetivo

## Arquitectura

## Implementación

## Resultados

## Limitaciones

## Aprendizajes obtenidos

---

# Código 02 — [Nombre pendiente]

## Objetivo

## Cambios respecto al código anterior

## Arquitectura

## Implementación

## Resultados

## Limitaciones

## Decisión metodológica posterior

---

# Exploración paralela — Campo electromagnético (RF)

Durante el desarrollo se exploró la incorporación de información electromagnética ambiental mediante:

- detector RF AD8318
- conversión analógica-digital mediante MCP3008
- integración con Raspberry Pi

El objetivo era investigar la posibilidad de incorporar una modalidad adicional de interacción relacionada con el entorno electromagnético.

Aunque esta exploración permitió construir una arquitectura experimental funcional, posteriormente se decidió no continuar esta línea como eje principal de desarrollo.

La investigación retornó al problema central:

> la relación entre gesto corporal, síntesis sonora y organización de espacios generativos.

Esta exploración permanece documentada como una perturbación metodológica dentro del proceso, pero no define la arquitectura actual de TmaqT.

---

# Código 03 — [Nombre pendiente]

## Transición hacia síntesis sonora

## Objetivo

## Cambios conceptuales

Esta etapa marca el desplazamiento desde sistemas basados principalmente en reproducción de muestras hacia procesos donde el gesto comienza a modificar parámetros de generación sonora.

## Implementación

## Resultados

## Limitaciones

---

# Código 04 — [Nombre pendiente]

## Exploraciones con espacios latentes

## Objetivo

## SOM / aprendizaje no supervisado

## Representación del gesto

## Relación gesto → espacio sonoro

## Resultados

---

# Prototipo 0 — main10.py

## Primera arquitectura estable

## Descripción

## Componentes principales

## Resultados experimentales

## Estado actual

---

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

