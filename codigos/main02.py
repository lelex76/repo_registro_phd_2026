#!/usr/bin/env python3
# ============================================================
# TmaqT v2 — TEXTIL WAV (Etapa 02 del pipeline)
#
# Evolución directa del código original TTT2:
# - 24 zonas
# - 3 capas WAV por zona (72 canales)
# - perfiles sonoros por zona
# - curvas textiles más complejas
# - fade orgánico
# - sin RF, sin FM, sin SOM
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
TOUCH_VOL = 0.8

pygame.init()
pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=512)
pygame.mixer.set_num_channels(72)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TmaqT v2 — Textile WAV Engine")

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
        snd.set_volume(TOUCH_VOL)
        sounds.append(snd)
        print("Audio OK:", f)
    else:
        print("FALTA AUDIO:", f)

if len(sounds) < 9:
    print("ERROR: faltan WAV")

# ============================================================
# PERFIL SONORO POR ZONA
# ============================================================

zone_profiles = []

for zone in range(24):
    x = zone % 12
    y = zone // 12

    layer1 = zone % 9
    layer2 = (zone + 1 + y) % 9
    layer3 = (zone + 3 + x) % 9

    profile = {
        "layers": [layer1, layer2, layer3],
        "volume": 0.45 + (zone % 6) * 0.03,
        "fade": 2500 + y * 700,
        "pan": x / 11.0
    }

    zone_profiles.append(profile)

# ============================================================
# ESTADO TÁCTIL
# ============================================================

touch_state = [False for _ in range(24)]
touch_memory = [0.0 for _ in range(24)]
curves = []
frame = 0

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
            for i in range(12):
                sensor[i].threshold = 18
                sensor[i].release_threshold = 12
            sensors.append(sensor)
            print("MPR121 OK", hex(addr))
        except Exception as e:
            print("MPR ERROR", e)

    return sensors

sensors = init_mpr121()

# ============================================================
# BEZIER CURVES
# ============================================================

def bezier(p0, p1, p2, p3, steps=40):
    points = []
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
        points.append((x, y))
    return points

class TextileCurve:
    def __init__(self, zone, intensity=1.0):
        self.zone = zone
        self.birth = time.time()
        self.life = 4.0
        self.intensity = intensity
        self.points = self.create_curve()

    def create_curve(self):
        x0 = 60 + (self.zone % 12) * 80
        y0 = HEIGHT // 2
        spread = 80 * self.intensity

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
            dx = math.sin(frame * 0.05 + i * 0.2) * 4
            dy = math.cos(frame * 0.04 + i * 0.15) * 4
            animated.append((x + dx, y + dy))

        pygame.draw.lines(surface, (0, 0, 0), False, animated, 2)
        return True

# ============================================================
# EVENTO TEXTIL
# ============================================================

def create_textile_event(zone):
    intensity = 1.0 + touch_memory[zone]
    curves.append(TextileCurve(zone, intensity))

# ============================================================
# AUDIO ENGINE (72 canales)
# ============================================================

def trigger_sound(zone):
    if not sounds:
        return

    profile = zone_profiles[zone]
    base_volume = profile["volume"]
    energy = touch_memory[zone]
    layers = profile["layers"]

    print("TEXTILE MIX ZONE:", zone, "LAYERS:", layers)

    base_channel = zone * 3

    for i, layer_id in enumerate(layers):
        channel = pygame.mixer.Channel(base_channel + i)
        sound = sounds[layer_id]

        if i == 0:
            volume = base_volume + energy * 0.40
        elif i == 1:
            volume = base_volume + energy * 0.25
        else:
            volume = base_volume + energy * 0.15

        channel.set_volume(volume)
        channel.play(sound, loops=-1)

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
                create_textile_event(zone)
                trigger_sound(zone)
            touch_memory[zone] = min(1.0, touch_memory[zone] + 0.05)
        else:
            touch_state[zone] = False
            touch_memory[zone] *= 0.95

    curves[:] = [c for c in curves if c.draw(screen, frame)]

    pygame.display.flip()
    frame += 1
    clock.tick(FPS)

pygame.quit()

