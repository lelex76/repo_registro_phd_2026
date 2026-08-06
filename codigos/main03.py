#!/usr/bin/env python3
# ============================================================
# TmaqT v3 — TEXTIL HÍBRIDO (Etapa 03 del pipeline)
#
# Evolución de main02.py:
# - memoria tímbrica real por zona
# - modulación de capas WAV (morfología simple)
# - dinámica tímbrica dependiente del gesto
# - transición hacia FM (sin FM aún)
# - arquitectura híbrida textil + motor tímbrico
# ============================================================

import os
import time
import math
import random
import pygame
import busio
import board
import adafruit_mpr121

# ============================================================
# CONFIG
# ============================================================

WIDTH = 1024
HEIGHT = 768
FPS = 50

AUDIO_PATH = os.path.expanduser("~/proyecto/codigo/audios")
BASE_VOL = 0.35
MOD_DEPTH = 0.25   # profundidad de modulación tímbrica
MEM_DECAY = 0.97   # decaimiento de memoria tímbrica

pygame.init()
pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=512)
pygame.mixer.set_num_channels(72)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TmaqT v3 — Textile Hybrid Engine")

clock = pygame.time.Clock()

# ============================================================
# AUDIO FILES (9 capas WAV)
# ============================================================

files = [
    "01.wav", "02.wav", "03.wav", "04ok.wav", "05.wav",
    "06.wav", "07.wav", "08.wav", "09.wav"
]

sounds = []
for f in files:
    path = os.path.join(AUDIO_PATH, f)
    if os.path.exists(path):
        snd = pygame.mixer.Sound(path)
        snd.set_volume(BASE_VOL)
        sounds.append(snd)
        print("Audio OK:", f)
    else:
        print("FALTA AUDIO:", f)

# ============================================================
# PERFIL SONORO + MEMORIA TÍMBRICA
# ============================================================

zone_profiles = []
zone_memory = [0.0 for _ in range(24)]  # memoria tímbrica real

for zone in range(24):
    x = zone % 12
    y = zone // 12

    layer1 = zone % 9
    layer2 = (zone + 2 + y) % 9
    layer3 = (zone + 4 + x) % 9

    profile = {
        "layers": [layer1, layer2, layer3],
        "pan": x / 11.0,
        "base": BASE_VOL + (y * 0.05),
        "mod": MOD_DEPTH + (x * 0.01)
    }

    zone_profiles.append(profile)

# ============================================================
# MPR121
# ============================================================

addresses = [0x5A, 0x5C]

def init_mpr121():
    sensors = []
    i2c = busio.I2C(board.SCL, board.SDA)
    for addr in addresses:
        try:
            sensor = adafruit_mpr121.MPR121(i2c, address=addr)
            sensors.append(sensor)
            print("MPR121 OK", hex(addr))
        except Exception as e:
            print("MPR ERROR", e)
    return sensors

sensors = init_mpr121()

touch_state = [False for _ in range(24)]

# ============================================================
# CURVAS TEXTILES (más tímbricas)
# ============================================================

def bezier(p0, p1, p2, p3, steps=40):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = ((1 - t)**3 * p0[0] +
             3 * (1 - t)**2 * t * p1[0] +
             3 * (1 - t) * t**2 * p2[0] +
             t**3 * p3[0])
        y = ((1 - t)**3 * p0[1] +
             3 * (1 - t)**2 * t * p1[1] +
             3 * (1 - t) * t**2 * p2[1] +
             t**3 * p3[1])
        pts.append((x, y))
    return pts

class HybridCurve:
    def __init__(self, zone, memory):
        self.zone = zone
        self.birth = time.time()
        self.life = 4.0 + memory * 2.0
        self.points = self.make_curve(memory)

    def make_curve(self, memory):
        x0 = 60 + (self.zone % 12) * 80
        y0 = HEIGHT // 2
        spread = 60 + memory * 120

        return bezier(
            (x0, y0),
            (x0 + random.uniform(-spread, spread),
             y0 + random.uniform(-spread, spread)),
            (x0 + random.uniform(-spread, spread),
             y0 + random.uniform(-spread, spread)),
            (random.randint(100, WIDTH - 100),
             random.randint(100, HEIGHT - 100))
        )

    def draw(self, surface, frame):
        age = time.time() - self.birth
        if age > self.life:
            return False

        animated = []
        for i, (x, y) in enumerate(self.points):
            dx = math.sin(frame * 0.04 + i * 0.2) * 5
            dy = math.cos(frame * 0.03 + i * 0.15) * 5
            animated.append((x + dx, y + dy))

        pygame.draw.lines(surface, (0, 0, 0), False, animated, 2)
        return True

curves = []
frame = 0

# ============================================================
# MOTOR HÍBRIDO (WAV + memoria tímbrica)
# ============================================================

def trigger_hybrid(zone):
    profile = zone_profiles[zone]
    memory = zone_memory[zone]

    layers = profile["layers"]
    base = profile["base"]
    mod = profile["mod"]

    for i, layer_id in enumerate(layers):
        ch = pygame.mixer.Channel(zone * 3 + i)
        snd = sounds[layer_id]

        vol = base + (memory * mod * (0.5 - i * 0.15))
        vol = max(0.0, min(1.0, vol))

        ch.set_volume(vol)
        ch.play(snd, loops=-1)

# ============================================================
# LOOP PRINCIPAL
# ============================================================

running = True

while running:
    screen.fill((255, 255, 255))

    raw = [0] * 24
    for s_idx, sensor in enumerate(sensors):
        for i in range(12):
            idx = s_idx * 12 + i
            if sensor[i].value:
                raw[idx] = 1

    for zone in range(24):
        if raw[zone] == 1:
            if not touch_state[zone]:
                touch_state[zone] = True
                zone_memory[zone] = min(1.0, zone_memory[zone] + 0.15)
                curves.append(HybridCurve(zone, zone_memory[zone]))
                trigger_hybrid(zone)
        else:
            touch_state[zone] = False
            zone_memory[zone] *= MEM_DECAY

    curves[:] = [c for c in curves if c.draw(screen, frame)]

    pygame.display.flip()
    frame += 1
    clock.tick(FPS)

pygame.quit()

