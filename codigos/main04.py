#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ==========================================================
# TmaqT — Etapa 00 (main04.py)
# Propuesta doctoral transdisciplinaria 2027
#
# Sistema FM + SOM inicial
# - síntesis FM básica
# - mapa SOM 2D
# - memoria tímbrica
# - gesto textil → morfología sonora
#
# Esta es la primera versión del sistema autónomo.
# ==========================================================

import os
import time
import math
import random
import numpy as np

# ==========================================================
# AUDIO SYSTEM FIX
# ==========================================================
os.environ["SDL_AUDIODRIVER"] = "alsa"

# ==========================================================
# HARDWARE
# ==========================================================
import board
import busio
import adafruit_mpr121

# ==========================================================
# AUDIO ENGINE
# ==========================================================
import pygame

# ==========================================================
# CONFIGURACIÓN AUDIO AVANZADA
# ==========================================================
SAMPLE_RATE = 48000
BUFFER = 256

pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, BUFFER)
pygame.init()
pygame.mixer.set_num_channels(8)

audio_channel = pygame.mixer.Channel(0)
fx_channel = pygame.mixer.Channel(1)

# ==========================================================
# MEMORIA DE FASE
# ==========================================================
carrier_phase = 0.0
mod_phase = 0.0
fx_phase = 0.0

# ==========================================================
# MEMORIA SONORA TMAQT
# ==========================================================
sound_memory = 0.0

# ==========================================================
# PARÁMETROS GLOBALES
# ==========================================================
FX_FREQ = 55
FX_AMP = 0.025
DECAY_SOUND_MEMORY = 0.985

# ==========================================================
# CAMPO AMBIENTE CONTINUO
# ==========================================================
def fx_buffer():
    global fx_phase
    t = np.arange(BUFFER) / SAMPLE_RATE

    wave = np.sin(2*np.pi*FX_FREQ*t + fx_phase)
    fx_phase += 2*np.pi*FX_FREQ*BUFFER/SAMPLE_RATE
    fx_phase %= 2*np.pi

    noise = np.random.randn(BUFFER) * 0.08
    signal = 0.85*wave + 0.15*noise
    signal *= FX_AMP
    signal = np.clip(signal, -1.0, 1.0)

    stereo = np.column_stack((signal, signal))
    return (stereo * 32767).astype(np.int16)

# ==========================================================
# SÍNTESIS FM TMAQT
# ==========================================================
def fm_buffer(fc, fm, index, amp):
    global carrier_phase, mod_phase

    t = np.arange(BUFFER) / SAMPLE_RATE

    modulator = np.sin(2*np.pi*fm*t + mod_phase)
    carrier = np.sin(2*np.pi*fc*t + index*modulator + carrier_phase)

    carrier_phase += 2*np.pi*fc*BUFFER/SAMPLE_RATE
    mod_phase += 2*np.pi*fm*BUFFER/SAMPLE_RATE

    carrier_phase %= 2*np.pi
    mod_phase %= 2*np.pi

    sub = np.sin(2*np.pi*(fc*0.5)*t)
    body = carrier
    bright = (
        0.65*np.sin(2*np.pi*(fc*2.0)*t + modulator*0.25)
        + 0.35*np.sin(2*np.pi*(fc*4.0)*t)
    )

    signal = 0.42*sub + 0.43*body + 0.15*bright
    signal = np.tanh(signal * 1.15)
    signal *= amp
    signal = np.clip(signal, -1.0, 1.0)

    stereo = np.column_stack((signal, signal))
    return (stereo * 32767).astype(np.int16)

# ==========================================================
# REPRODUCCIÓN FM
# ==========================================================
def play_synth(fc, fm, index, amp):
    global audio_channel

    amp = float(np.clip(amp, 0.0, 1.0))
    if amp < 0.01:
        audio_channel.set_volume(0)
        return

    data = fm_buffer(fc, fm, index, amp)
    sound = pygame.mixer.Sound(buffer=data)
    audio_channel.play(sound, loops=-1)
    audio_channel.set_volume(amp)

# ==========================================================
# FX CONTINUO
# ==========================================================
def play_fx_base():
    global fx_channel
    data = fx_buffer()
    sound = pygame.mixer.Sound(buffer=data)

    if not fx_channel.get_busy():
        fx_channel.play(sound, loops=-1)

    fx_channel.set_volume(FX_AMP)

# ==========================================================
# STOP
# ==========================================================
def stop_sound():
    audio_channel.set_volume(0)
    fx_channel.set_volume(0)

# ==========================================================
# MPR121 TEXTILE SENSOR SYSTEM
# ==========================================================
i2c = busio.I2C(board.SCL, board.SDA)
mpr_left = adafruit_mpr121.MPR121(i2c, address=0x5A)
mpr_right = adafruit_mpr121.MPR121(i2c, address=0x5C)

print("--------------------------------")
print("MPR121 TEXTILE READY")
print("LEFT 0x5A")
print("RIGHT 0x5C")
print("--------------------------------")

# ==========================================================
# LECTURA VECTOR 24D
# ==========================================================
def read_textile():
    vector = np.zeros(24, dtype=np.float32)
    try:
        left = mpr_left.touched()
        right = mpr_right.touched()
    except Exception as e:
        print("I2C SENSOR RECOVER", e)
        time.sleep(0.05)
        return vector

    for ch in range(12):
        if left & (1 << ch):
            vector[ch] = 1.0
    for ch in range(12):
        if right & (1 << ch):
            vector[ch+12] = 1.0

    return vector

# ==========================================================
# SUAVIZADO TEMPORAL
# ==========================================================
touch_memory = np.zeros(24, dtype=np.float32)

def smooth_touch(raw):
    global touch_memory
    touch_memory = 0.80*touch_memory + 0.20*raw
    return touch_memory.copy()

# ==========================================================
# SOM KOHONEN
# ==========================================================
class SOM:
    def __init__(self, rows=6, cols=4, input_dim=24):
        self.rows = rows
        self.cols = cols
        self.input_dim = input_dim

        self.learning_rate = 0.35
        self.radius = 2.5
        self.step = 0

        self.weights = (np.random.random((rows, cols, input_dim)) * 0.1).astype(np.float32)

        grid = []
        for x in range(rows):
            for y in range(cols):
                grid.append([x, y])
        self.grid = np.array(grid, dtype=np.float32)

        print("--------------------------------")
        print("SOM KOHONEN READY")
        print("MAP:", rows, "x", cols)
        print("INPUT:", input_dim)
        print("--------------------------------")

    def winner(self, x):
        distances = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                distances[i,j] = np.linalg.norm(self.weights[i,j] - x)

        idx = np.unravel_index(np.argmin(distances), distances.shape)
        bmu = idx[0]*self.cols + idx[1]
        error = distances[idx]
        return (bmu, float(error))

    def update(self, x):
        bmu,_ = self.winner(x)
        bx = bmu // self.cols
        by = bmu % self.cols

        lr = self.learning_rate * np.exp(-self.step/5000)
        radius = max(0.5, self.radius * np.exp(-self.step/5000))

        for i in range(self.rows):
            for j in range(self.cols):
                distance_grid = math.sqrt((i-bx)**2 + (j-by)**2)
                influence = np.exp(-(distance_grid**2) / (2*radius*radius))
                self.weights[i,j] += lr * influence * (x - self.weights[i,j])

        self.step += 1

# ==========================================================
# CREACIÓN DEL MAPA LATENTE
# ==========================================================
som = SOM()

print("--------------------------------")
print("TmaqT FM SYNTH READY")
print("LATENT SPACE ENGINE")
print("--------------------------------")

# ==========================================================
# MEMORIA DEL GESTO
# ==========================================================
gesture_memory = np.zeros(24, dtype=np.float32)
DECAY = 0.985
FEEDBACK = 0.35
sound_memory = 0.0

# ==========================================================
# MOTOR PRINCIPAL
# ==========================================================
def main():
    global gesture_memory, sound_memory

    print("--------------------------------")
    print("TmaqT LATENT FM ENGINE START")
    print("GESTURE → MORPHOLOGY → SOUND")
    print("--------------------------------")

    smooth = np.zeros(24, dtype=np.float32)
    play_fx_base()

    while True:
        raw = read_textile()
        smooth = 0.8*smooth + 0.2*raw
        latent_input = np.clip(smooth, 0, 1)
        active = np.where(raw > 0)[0]

        if len(active) == 0:
            gesture_memory *= DECAY
            sound_memory *= 0.995
            time.sleep(0.01)
            continue

        gesture_memory *= DECAY
        gesture_memory += latent_input

        memory_energy = np.sum(gesture_memory)
        energy = memory_energy * FEEDBACK

        amp = np.clip((energy/12.0)**2.8, 0.0, 1.0)

        bmu, error = som.winner(latent_input)
        som.update(latent_input)

        coord = som.grid[bmu]
        x_latent = coord[0]
        y_latent = coord[1]

        fc = 120 + x_latent*140 + y_latent*80
        fm = 20 + y_latent*250

        sound_memory *= 0.98
        sound_memory += memory_energy

        index = np.clip(sound_memory/10.0, 0.3, 8.0)
        pan = x_latent / 5.0

        print(
            "TOUCH", active.tolist(),
            "BMU", bmu,
            "LATENT", (round(float(x_latent),2), round(float(y_latent),2)),
            "FC", int(fc),
            "FM", int(fm),
            "INDEX", round(float(index),2),
            "AMP", round(float(amp),2)
        )

        play_synth(fc, fm, index, amp)
        time.sleep(0.01)

# ==========================================================
# EJECUCIÓN FINAL
# ==========================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("--------------------------------")
        print("TmaqT STOP")
        print("CLOSING AUDIO ENGINE")
        print("--------------------------------")
        stop_sound()
        pygame.quit()

