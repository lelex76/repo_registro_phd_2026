CODIGO OROIG
#!/usr/bin/env python3

import pygame
import math
import random
import time
import os
import busio
import board
import adafruit_mpr121

# ==== CONFIGURACIÓN PYGAME ====
pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

# Pantalla principal (blanca)
WIDTH, HEIGHT = 1024, 768
screen_white = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Pantalla Blanca - Sonificación + Visual")

# Pantalla secundaria (negra)
screen_black = pygame.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# ==== SONIDOS CAPAS ====
audio_folder = os.path.expanduser("~/proyecto/codigo/audios")
BASE_VOL = 0.35
CAPA_VOL = 0.9
FADE_SPEED = 0.02
EXTRA_BLEND = 0.2

base       = pygame.mixer.Sound(os.path.join(audio_folder, "01.wav"))
grave      = pygame.mixer.Sound(os.path.join(audio_folder, "02.wav"))
media      = pygame.mixer.Sound(os.path.join(audio_folder, "03.wav"))
media_alta = pygame.mixer.Sound(os.path.join(audio_folder, "04ok.wav"))
aguda      = pygame.mixer.Sound(os.path.join(audio_folder, "05.wav"))
extra      = pygame.mixer.Sound(os.path.join(audio_folder, "06.wav"))

ch_base       = pygame.mixer.Channel(0)
ch_grave      = pygame.mixer.Channel(1)
ch_media      = pygame.mixer.Channel(2)
ch_media_alta = pygame.mixer.Channel(3)
ch_aguda      = pygame.mixer.Channel(4)
ch_extra      = pygame.mixer.Channel(5)

ch_base.play(base, loops=-1)
ch_base.set_volume(BASE_VOL)

for ch, snd in [(ch_grave, grave),(ch_media, media),
                (ch_media_alta, media_alta),(ch_aguda, aguda),
                (ch_extra, extra)]:
    ch.play(snd, loops=-1)
    ch.set_volume(0.0)

canales = {
    "grave": ch_grave,
    "media": ch_media,
    "media_alta": ch_media_alta,
    "aguda": ch_aguda,
    "extra": ch_extra
}

ZONAS = {
    "grave": range(0,6),
    "media": range(6,12),
    "media_alta": range(12,18),
    "aguda": range(18,24),
    "extra": range(24,30)
}

# ==== SENSORES ====
i2c_addresses = [0x5A, 0x5C]
electrodes_per_sensor = 12

def initialize_sensors(addresses):
    sensors = []
    i2c = busio.I2C(board.SCL, board.SDA)
    for addr in addresses:
        try:
            sensors.append(adafruit_mpr121.MPR121(i2c, address=addr))
        except Exception as e:
            print(f"Warning: Failed to init sensor {hex(addr)}: {e}")
    return sensors

sensors = initialize_sensors(i2c_addresses)
toques_anteriores = [False]*24
last_touch_time = [0]*24
debounce_time = 0.05

# ==== FUNCIONES VISUALES ====
def bezier(p0, p1, p2, p3, steps=30):
    return [(
        (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + 
t**3*p3[0],
        (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + 
t**3*p3[1]
    ) for t in [i/steps for i in range(steps+1)]]

class Curva:
    def __init__(self, index, duracion=2.0, intensidad=1.0):
        self.index = index
        self.duracion = duracion
        self.tiempo_inicio = time.time()
        self.intensidad = intensidad
        self.points = self.generar_puntos()
    
    def generar_puntos(self):
        base_y = HEIGHT//2
        base_x = 50 + (self.index % 12) * 90
        ampl = 80 * self.intensidad  # amplitud aumenta al tocar
        p0 = (base_x, base_y)
        p1 = (base_x + random.randint(-ampl, ampl), base_y + 
random.randint(-ampl, ampl))
        p2 = (base_x + random.randint(-ampl, ampl), base_y + 
random.randint(-ampl, ampl))
        p3 = (base_x + random.randint(-ampl, ampl), base_y + 
random.randint(-ampl, ampl))
        return bezier(p0, p1, p2, p3)
    
    def dibujar(self, frame, surface):
        elapsed = time.time() - self.tiempo_inicio
        if elapsed > self.duracion:
            return False
        animated_points = []
        for j, (x, y) in enumerate(self.points):
            dx = 5 * math.sin(math.radians(frame*5 + j*10))
            dy = 5 * math.cos(math.radians(frame*7 + j*12))
            animated_points.append((x+dx, y+dy))
        color = (0,0,0)  # negro
        pygame.draw.lines(surface, color, False, animated_points, 3)
        return True

curvas_activas = []
frame_count = 0

# ==== LOOP PRINCIPAL ====
running = True
while running:
    screen_white.fill((255,255,255))
    screen_black.fill((0,0,0))
    now = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for sensor_idx, sensor in enumerate(sensors):
        for i in range(electrodes_per_sensor):
            global_idx = sensor_idx*12 + i
            if global_idx >= len(toques_anteriores):
                continue
            if sensor[i].value:
                if not toques_anteriores[global_idx] and now - 
last_touch_time[global_idx] > debounce_time:
                    last_touch_time[global_idx] = now
                    toques_anteriores[global_idx] = True
                    for zona, indices in ZONAS.items():
                        if global_idx in indices:
                            intensidad = 1.5 if zona != "extra" else 1.0
                            if zona == "extra":
                                ch_extra.set_volume(CAPA_VOL)
                                ch_base.set_volume(BASE_VOL + EXTRA_BLEND)
                            else:
                                canales[zona].set_volume(CAPA_VOL)
                            curvas_activas.append(Curva(global_idx, 
intensidad=intensidad))
            else:
                toques_anteriores[global_idx] = False
    
    for zona, ch in canales.items():
        indices = ZONAS.get(zona, [])
        active = any(
            sensors[sensor_idx][i % 12].value
            for sensor_idx in range(len(sensors))
            for i in indices if i < len(toques_anteriores)
        )
        if not active:
            v = ch.get_volume()
            ch.set_volume(max(0.0, v - FADE_SPEED))
            if zona == "extra":
                ch_base.set_volume(max(BASE_VOL, ch_base.get_volume() - 
FADE_SPEED/2))
    
    curvas_activas = [c for c in curvas_activas if c.dibujar(frame_count, 
screen_white)]
    curvas_activas = [c for c in curvas_activas if c.dibujar(frame_count, 
screen_black)]
    
    pygame.display.flip()
    frame_count += 1
    time.sleep(0.01)

pygame.quit()
