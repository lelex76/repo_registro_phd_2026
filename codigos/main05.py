
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TmaQT MAIN12

24 zonas textiles
↓
2 x MPR121
↓
suavizado temporal
↓
SOM 24D → 2D
↓
4 voces FM independientes
↓
diferenciación por zona
↓
polifonía
↓
interacción entre voces
↓
release individual
↓
delay corto

PRIORIDAD:
SONIDO > VISUAL
"""

import os
import time
import math
import threading
import numpy as np

# ==========================================================
# AUDIO
# ==========================================================

os.environ["SDL_AUDIODRIVER"] = "alsa"

import pygame

SAMPLE_RATE = 48000
BUFFER = 256

pygame.mixer.pre_init(
    SAMPLE_RATE,
    -16,
    2,
    BUFFER
)

pygame.init()

pygame.mixer.set_num_channels(8)

audio_channel = pygame.mixer.Channel(0)

# ==========================================================
# HARDWARE
# ==========================================================

import board
import busio
import adafruit_mpr121

i2c = busio.I2C(
    board.SCL,
    board.SDA
)

mpr_left = adafruit_mpr121.MPR121(
    i2c,
    address=0x5A
)

mpr_right = adafruit_mpr121.MPR121(
    i2c,
    address=0x5C
)

print("--------------------------------")
print("MPR121 TEXTILE READY")
print("LEFT  0x5A")
print("RIGHT 0x5C")
print("--------------------------------")

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

NUM_ZONES = 24
NUM_VOICES = 4

VOICE_VOLUME = 0.48

ATTACK_SPEED = 0.08
RELEASE_SPEED = 0.035

DECAY = 0.985

# Diferenciación física entre zonas
ZONE_SPREAD = 0.18

# Interacción entre voces
POLY_INTERACTION = 0.20

# ==========================================================
# DELAY CORTO
# ==========================================================

DELAY_TIME = 0.16
DELAY_FEEDBACK = 0.28
DELAY_MIX = 0.20

delay_samples = int(
    SAMPLE_RATE * DELAY_TIME
)

delay_buffer_left = np.zeros(
    delay_samples,
    dtype=np.float32
)

delay_buffer_right = np.zeros(
    delay_samples,
    dtype=np.float32
)

delay_position = 0

# ==========================================================
# FASES
# ==========================================================

carrier_phase = np.zeros(
    NUM_VOICES,
    dtype=np.float64
)

mod_phase = np.zeros(
    NUM_VOICES,
    dtype=np.float64
)

# ==========================================================
# MEMORIA TÁCTIL
# ==========================================================

touch_memory = np.zeros(
    NUM_ZONES,
    dtype=np.float32
)

gesture_memory = np.zeros(
    NUM_ZONES,
    dtype=np.float32
)

# ==========================================================
# VOZ
# ==========================================================

class Voice:

    def __init__(self):

        self.active = False

        self.zone = -1

        self.amp = 0.0
        self.target_amp = 0.0

        self.fc = 220.0
        self.fm = 80.0
        self.index = 1.0

        self.pan = 0.0

        self.zone_bias = 0.0

        self.last_touch = 0.0


voices = [
    Voice()
    for _ in range(NUM_VOICES)
]

zone_voice = {}

# ==========================================================
# LECTURA TEXTIL
# ==========================================================

def read_textile():

    vector = np.zeros(
        NUM_ZONES,
        dtype=np.float32
    )

    try:

        left = mpr_left.touched()
        right = mpr_right.touched()

    except Exception as e:

        print(
            "I2C SENSOR RECOVER:",
            e
        )

        return vector

    for ch in range(12):

        if left & (1 << ch):
            vector[ch] = 1.0

    for ch in range(12):

        if right & (1 << ch):
            vector[ch + 12] = 1.0

    return vector


# ==========================================================
# SUAVIZADO
# ==========================================================

def smooth_touch(raw):

    global touch_memory

    touch_memory = (
        0.80 * touch_memory
        +
        0.20 * raw
    )

    return touch_memory.copy()


# ==========================================================
# SOM
# ==========================================================

class SOM:

    def __init__(
        self,
        rows=6,
        cols=4,
        input_dim=24
    ):

        self.rows = rows
        self.cols = cols
        self.input_dim = input_dim

        self.learning_rate = 0.35
        self.radius = 2.5
        self.step = 0

        self.weights = (
            np.random.random(
                (
                    rows,
                    cols,
                    input_dim
                )
            )
            * 0.1
        ).astype(
            np.float32
        )

        grid = []

        for x in range(rows):

            for y in range(cols):

                grid.append(
                    [
                        x,
                        y
                    ]
                )

        self.grid = np.array(
            grid,
            dtype=np.float32
        )

        print("--------------------------------")
        print("SOM KOHONEN READY")
        print("MAP:", rows, "x", cols)
        print("INPUT:", input_dim)
        print("--------------------------------")

    def winner(self, x):

        distances = np.zeros(
            (
                self.rows,
                self.cols
            )
        )

        for i in range(self.rows):

            for j in range(self.cols):

                distances[i, j] = np.linalg.norm(
                    self.weights[i, j]
                    -
                    x
                )

        idx = np.unravel_index(
            np.argmin(distances),
            distances.shape
        )

        bmu = (
            idx[0] * self.cols
            +
            idx[1]
        )

        error = distances[idx]

        return (
            bmu,
            float(error)
        )

    def update(self, x):

        bmu, _ = self.winner(x)

        bx = bmu // self.cols
        by = bmu % self.cols

        lr = (
            self.learning_rate
            *
            np.exp(
                -self.step / 5000
            )
        )

        radius = max(
            0.5,
            self.radius
            *
            np.exp(
                -self.step / 5000
            )
        )

        for i in range(self.rows):

            for j in range(self.cols):

                distance_grid = math.sqrt(
                    (i - bx) ** 2
                    +
                    (j - by) ** 2
                )

                influence = np.exp(
                    -(
                        distance_grid ** 2
                    )
                    /
                    (
                        2 *
                        radius *
                        radius
                    )
                )

                self.weights[i, j] += (
                    lr
                    *
                    influence
                    *
                    (
                        x
                        -
                        self.weights[i, j]
                    )
                )

        self.step += 1


som = SOM()

# ==========================================================
# ASIGNACIÓN DE VOCES
# ==========================================================

def find_voice_for_zone(zone):

    # Mantener la voz mientras la zona siga activa

    if zone in zone_voice:

        return zone_voice[zone]

    # Buscar voz libre

    for i, voice in enumerate(voices):

        if not voice.active:

            zone_voice[zone] = i

            return i

    # Si no hay voces libres,
    # reutilizar la voz con menor amplitud

    amplitudes = [
        v.amp
        for v in voices
    ]

    idx = int(
        np.argmin(amplitudes)
    )

    old_zone = voices[idx].zone

    if old_zone in zone_voice:

        del zone_voice[old_zone]

    zone_voice[zone] = idx

    return idx


# ==========================================================
# CONFIGURAR VOZ
# ==========================================================

def configure_voice(
    voice_index,
    zone,
    x_latent,
    y_latent,
    gesture_energy,
    active_count
):

    voice = voices[voice_index]

    # ------------------------------------------------------
    # IDENTIDAD DE LA ZONA
    #
    # La zona no determina una nota fija.
    # Introduce una diferencia dentro del espacio latente.
    # ------------------------------------------------------

    zone_position = zone / (NUM_ZONES - 1)

    zone_bias = (
        zone_position - 0.5
    )

    voice.zone_bias = zone_bias

    # ------------------------------------------------------
    # POLIFONÍA
    # ------------------------------------------------------

    polyphonic_spread = min(
        active_count,
        NUM_VOICES
    )

    # ------------------------------------------------------
    # FRECUENCIA
    # ------------------------------------------------------

    fc = (
        100.0
        +
        x_latent * 150.0
        +
        y_latent * 85.0
        +
        zone_bias * 90.0
        +
        polyphonic_spread * zone_bias * 20.0
    )

    # ------------------------------------------------------
    # MODULACIÓN
    # ------------------------------------------------------

    fm = (
        25.0
        +
        y_latent * 230.0
        +
        abs(zone_bias) * 90.0
    )

    # ------------------------------------------------------
    # ÍNDICE FM
    # ------------------------------------------------------

    index = np.clip(
        0.5
        +
        gesture_energy * 3.0
        +
        y_latent * 0.7
        +
        abs(zone_bias) * 1.5,
        0.3,
        8.0
    )

    # ------------------------------------------------------
    # PANORAMA
    # ------------------------------------------------------

    pan = np.clip(
        (
            x_latent / 5.0
        ) * 2.0
        - 1.0
        +
        zone_bias * 0.35,
        -1.0,
        1.0
    )

    # ------------------------------------------------------
    # CONFIGURAR VOZ
    # ------------------------------------------------------

    voice.zone = zone

    voice.fc = fc
    voice.fm = fm
    voice.index = index
    voice.pan = pan

    voice.target_amp = VOICE_VOLUME

    voice.active = True

    voice.last_touch = time.time()

# ==========================================================
# GENERAR FM
# ==========================================================

def generate_voice(
    voice_index,
    voice
):

    t = (
        np.arange(BUFFER)
        /
        SAMPLE_RATE
    )

    # ------------------------------------------------------
    # MODULADOR
    # ------------------------------------------------------

    modulator = np.sin(
        2 *
        np.pi *
        voice.fm *
        t
        +
        mod_phase[voice_index]
    )

    # ------------------------------------------------------
    # PORTADORA
    # ------------------------------------------------------

    carrier = np.sin(
        2 *
        np.pi *
        voice.fc *
        t
        +
        (
            voice.index *
            modulator
        )
        +
        carrier_phase[voice_index]
    )

    # ------------------------------------------------------
    # SUBGRAVE
    # ------------------------------------------------------

    sub = np.sin(
        2 *
        np.pi *
        (
            voice.fc * 0.5
        )
        *
        t
    )

    # ------------------------------------------------------
    # ARMÓNICOS
    # ------------------------------------------------------

    bright = (
        0.65 *
        np.sin(
            2 *
            np.pi *
            (
                voice.fc * 2.0
            )
            *
            t
            +
            modulator * 0.25
        )
        +
        0.35 *
        np.sin(
            2 *
            np.pi *
            (
                voice.fc * 4.0
            )
            *
            t
        )
    )

    # ------------------------------------------------------
    # DIFERENCIA TÍMBRICA POR ZONA
    # ------------------------------------------------------

    zone_amount = abs(
        voice.zone_bias
    )

    body_level = (
        0.45
        -
        zone_amount * 0.12
    )

    bright_level = (
        0.15
        +
        zone_amount * 0.15
    )

    sub_level = (
        0.40
        -
        zone_amount * 0.10
    )

    signal = (
        sub_level * sub
        +
        body_level * carrier
        +
        bright_level * bright
    )

    signal = np.tanh(
        signal * 1.15
    )

    signal *= voice.amp

    # ------------------------------------------------------
    # PAN
    # ------------------------------------------------------

    pan = np.clip(
        voice.pan,
        -1.0,
        1.0
    )

    left_gain = math.sqrt(
        (1.0 - pan) * 0.5
    )

    right_gain = math.sqrt(
        (1.0 + pan) * 0.5
    )

    left = (
        signal *
        left_gain
    )

    right = (
        signal *
        right_gain
    )

    # ------------------------------------------------------
    # FASE
    # ------------------------------------------------------

    carrier_phase[voice_index] += (
        2 *
        np.pi *
        voice.fc *
        BUFFER
        /
        SAMPLE_RATE
    )

    mod_phase[voice_index] += (
        2 *
        np.pi *
        voice.fm *
        BUFFER
        /
        SAMPLE_RATE
    )

    carrier_phase[voice_index] %= (
        2 * np.pi
    )

    mod_phase[voice_index] %= (
        2 * np.pi
    )

    return (
        left,
        right
    )


# ==========================================================
# DELAY
# ==========================================================

def apply_delay(
    left,
    right
):

    global delay_position

    output_left = np.zeros_like(
        left
    )

    output_right = np.zeros_like(
        right
    )

    for i in range(
        len(left)
    ):

        delayed_left = (
            delay_buffer_left[
                delay_position
            ]
        )

        delayed_right = (
            delay_buffer_right[
                delay_position
            ]
        )

        output_left[i] = (
            left[i]
            +
            delayed_left *
            DELAY_MIX
        )

        output_right[i] = (
            right[i]
            +
            delayed_right *
            DELAY_MIX
        )

        delay_buffer_left[
            delay_position
        ] = (
            left[i]
            +
            delayed_left *
            DELAY_FEEDBACK
        )

        delay_buffer_right[
            delay_position
        ] = (
            right[i]
            +
            delayed_right *
            DELAY_FEEDBACK
        )

        delay_position += 1

        if (
            delay_position
            >=
            delay_samples
        ):

            delay_position = 0

    return (
        output_left,
        output_right
    )


# ==========================================================
# AUDIO CALLBACK
# ==========================================================

def audio_callback():

    left_mix = np.zeros(
        BUFFER,
        dtype=np.float32
    )

    right_mix = np.zeros(
        BUFFER,
        dtype=np.float32
    )

    active_count = 0

    # ------------------------------------------------------
    # VOCES
    # ------------------------------------------------------

    for i, voice in enumerate(
        voices
    ):

        # RELEASE

        if (
            voice.amp
            >
            voice.target_amp
        ):

            voice.amp = max(
                voice.target_amp,
                voice.amp -
                RELEASE_SPEED
            )

        # ATAQUE

        elif (
            voice.amp
            <
            voice.target_amp
        ):

            voice.amp = min(
                voice.target_amp,
                voice.amp +
                ATTACK_SPEED
            )

        if voice.amp > 0.001:

            l, r = generate_voice(
                i,
                voice
            )

            left_mix += l
            right_mix += r

            active_count += 1

        else:

            voice.active = False

    # ------------------------------------------------------
    # MEZCLA POLIFÓNICA
    # ------------------------------------------------------

    if active_count > 0:

        scale = max(
            1.0,
            active_count * 0.62
        )

        left_mix /= scale
        right_mix /= scale

    # ------------------------------------------------------
    # DELAY
    # ------------------------------------------------------

    left_mix, right_mix = apply_delay(
        left_mix,
        right_mix
    )

    # ------------------------------------------------------
    # LIMITADOR
    # ------------------------------------------------------

    left_mix = np.tanh(
        left_mix
    )

    right_mix = np.tanh(
        right_mix
    )

    stereo = np.column_stack(
        (
            left_mix,
            right_mix
        )
    )

    return (
        stereo * 32767
    ).astype(
        np.int16
    )


# ==========================================================
# AUDIO LOOP
# ==========================================================

audio_running = False


def audio_loop():

    global audio_running

    audio_running = True

    while audio_running:

        data = audio_callback()

        sound = pygame.mixer.Sound(
            buffer=data
        )

        if not audio_channel.get_busy():

            audio_channel.play(
                sound
            )

        else:

            audio_channel.queue(
                sound
            )

        time.sleep(
            BUFFER /
            SAMPLE_RATE *
            0.70
        )

# ==========================================================
# MAIN
# ==========================================================

def main():

    global gesture_memory
    global running

    print("--------------------------------")
    print("TMAQT MAIN12")
    print("--------------------------------")
    print("24 ZONES")
    print("4 FM VOICES")
    print("ZONE DIFFERENTIATION")
    print("POLYPHONIC INTERACTION")
    print("INDIVIDUAL RELEASE")
    print("SHORT DELAY")
    print("SOM 6x4")
    print("--------------------------------")

    smooth = np.zeros(
        NUM_ZONES,
        dtype=np.float32
    )

    previous_active = set()

    # ------------------------------------------------------
    # AUDIO
    # ------------------------------------------------------

    audio_thread = threading.Thread(
        target=audio_loop,
        daemon=True
    )

    audio_thread.start()

    # ------------------------------------------------------
    # LOOP
    # ------------------------------------------------------

    while True:

        raw = read_textile()

        smooth = (
            0.80 * smooth
            +
            0.20 * raw
        )

        latent_input = np.clip(
            smooth,
            0,
            1
        )

        active = set(
            np.where(
                raw > 0
            )[0].tolist()
        )

        # --------------------------------------------------
        # MEMORIA DEL GESTO
        # --------------------------------------------------

        gesture_memory *= DECAY

        gesture_memory += (
            latent_input
        )

        # --------------------------------------------------
        # SIN CONTACTO
        # --------------------------------------------------

        if len(active) == 0:

            for voice in voices:

                voice.target_amp = 0.0

            previous_active = set()

            time.sleep(0.01)

            continue

        # --------------------------------------------------
        # SOM
        # --------------------------------------------------

        bmu, error = som.winner(
            latent_input
        )

        som.update(
            latent_input
        )

        coord = som.grid[
            bmu
        ]

        x_latent = float(
            coord[0]
        )

        y_latent = float(
            coord[1]
        )

        # --------------------------------------------------
        # CONFIGURAR VOCES
        # --------------------------------------------------

        for zone in sorted(active):

            voice_index = find_voice_for_zone(
                zone
            )

            gesture_energy = float(
                gesture_memory[zone]
            )

            configure_voice(
                voice_index,
                zone,
                x_latent,
                y_latent,
                gesture_energy,
                len(active)
            )

        # --------------------------------------------------
        # RELEASE DE ZONAS SOLTADAS
        # --------------------------------------------------

        for zone in list(
            zone_voice.keys()
        ):

            if zone not in active:

                voice_index = zone_voice[
                    zone
                ]

                voices[
                    voice_index
                ].target_amp = 0.0

                del zone_voice[
                    zone
                ]

        # --------------------------------------------------
        # MONITOR
        # --------------------------------------------------

        print(
            "TOUCH",
            sorted(active),
            "| BMU",
            bmu,
            "| LATENT",
            (
                round(x_latent, 2),
                round(y_latent, 2)
            ),
            "| VOICES",
            [
                (
                    v.zone,
                    round(v.amp, 2),
                    int(v.fc),
                    int(v.fm),
                    round(v.index, 2)
                )
                for v in voices
                if v.amp > 0.01
            ]
        )

        previous_active = active

        time.sleep(
            0.01
        )


# ==========================================================
# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print("--------------------------------")
        print("TMAQT MAIN13 STOP")
        print("--------------------------------")

    finally:

        print("--------------------------------")
        print("TMAQT CLEAN SHUTDOWN")
        print("--------------------------------")

        audio_running = False

        for voice in voices:

            voice.target_amp = 0.0
            voice.amp = 0.0

        audio_channel.stop()

        pygame.quit()

