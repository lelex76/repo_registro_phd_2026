import time
from collections import deque

import numpy as np
import pygame
import board
import busio
import adafruit_mpr121

from tflite_runtime.interpreter import Interpreter


# ============================================================
# TMAQT — HYBRID LATENT FM AUDIO
#
# Gesture latent → stateful sonic perturbation → FM latent
# → FM decoder → real-time FM synthesis
#
# WAV latent is maintained in parallel but not yet audible.
# ============================================================

WINDOW = 32
N_ZONES = 24
LATENT_DIM = 3

LOOP_DT = 0.02          # 50 Hz tactile loop
SAMPLE_RATE = 48000
AUDIO_CHUNK = 512

GESTURE_MODEL = "TMAQT_Gesture_Encoder.tflite"
FM_MODEL = "modelos_fm/TMAQT_FM_Decoder.tflite"
WAV_MODEL = "TMAQT_Sonic_Decoder_STANDARD.tflite"

# ------------------------------------------------------------
# Gesture latent statistics
# ------------------------------------------------------------

GESTURE_MEAN = np.array(
    [-3.5539024, 6.653916, -6.702165],
    dtype=np.float32
)

GESTURE_STD = np.array(
    [8.123118, 5.57736, 6.830759],
    dtype=np.float32
)

# ------------------------------------------------------------
# Stateful coupling parameters
# ------------------------------------------------------------

POSITION_GAIN = 0.035
MOVEMENT_GAIN = 0.18
VELOCITY_GAIN = 0.035

FM_GAIN = 1.0
WAV_GAIN = 0.65

STATE_DAMPING = 0.002
PARAM_SMOOTHING = 0.18

MAX_PERTURBATION = 0.35


# ============================================================
# START
# ============================================================

print()
print("================================================")
print("TMAQT — HYBRID LATENT FM AUDIO")
print("================================================")
print()
print("Gesture latent → stateful FM latent → audio")
print()


# ============================================================
# I2C / MPR121
# ============================================================

i2c = busio.I2C(board.SCL, board.SDA)

mpr_left = adafruit_mpr121.MPR121(
    i2c,
    address=0x5A
)

mpr_right = adafruit_mpr121.MPR121(
    i2c,
    address=0x5C
)

print("MPR121 0x5A : OK")
print("MPR121 0x5C : OK")


# ============================================================
# MODELS
# ============================================================

gesture_interpreter = Interpreter(
    model_path=GESTURE_MODEL
)

fm_interpreter = Interpreter(
    model_path=FM_MODEL
)

wav_interpreter = Interpreter(
    model_path=WAV_MODEL
)

gesture_interpreter.allocate_tensors()
fm_interpreter.allocate_tensors()
wav_interpreter.allocate_tensors()

gesture_input = gesture_interpreter.get_input_details()[0]
gesture_output = gesture_interpreter.get_output_details()[0]

fm_input = fm_interpreter.get_input_details()[0]
fm_output = fm_interpreter.get_output_details()[0]

wav_input = wav_interpreter.get_input_details()[0]
wav_output = wav_interpreter.get_output_details()[0]

print()
print("Gesture input :", gesture_input["shape"])
print("Gesture output:", gesture_output["shape"])
print("FM input      :", fm_input["shape"])
print("FM output     :", fm_output["shape"])
print("WAV input     :", wav_input["shape"])
print("WAV output    :", wav_output["shape"])


# ============================================================
# LOAD LATENT RANGES
# ============================================================

fm_latent = np.load("modelos_fm/TMAQT_FM_Latent.npz")
wav_latent = np.load("TMAQT_Sonic_Latent.npz")

print()
print("FM latent keys :", fm_latent.files)
print("WAV latent keys:", wav_latent.files)


def find_latent_array(data):
    """
    Find the 2D latent matrix inside an NPZ.
    """
    for key in data.files:
        arr = np.asarray(data[key])

        if arr.ndim == 2 and arr.shape[1] == LATENT_DIM:
            return arr.astype(np.float32)

    raise RuntimeError(
        "No 3D latent matrix found in NPZ."
    )


fm_Z = find_latent_array(fm_latent)
wav_Z = find_latent_array(wav_latent)

fm_min = fm_Z.min(axis=0)
fm_max = fm_Z.max(axis=0)
fm_center = fm_Z.mean(axis=0)

wav_min = wav_Z.min(axis=0)
wav_max = wav_Z.max(axis=0)
wav_center = wav_Z.mean(axis=0)

print()
print("FM latent min    :", fm_min)
print("FM latent max    :", fm_max)
print("FM latent center :", fm_center)

print()
print("WAV latent min    :", wav_min)
print("WAV latent max    :", wav_max)
print("WAV latent center :", wav_center)


# ============================================================
# TEXTILE
# ============================================================

def read_textile():

    vector = np.zeros(
        N_ZONES,
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


# ============================================================
# GESTURE ENCODER
# ============================================================

def encode_gesture(window):

    x = np.asarray(
        window,
        dtype=np.float32
    ).reshape(
        1,
        WINDOW,
        N_ZONES
    )

    gesture_interpreter.set_tensor(
        gesture_input["index"],
        x
    )

    gesture_interpreter.invoke()

    z = gesture_interpreter.get_tensor(
        gesture_output["index"]
    )

    return z[0].astype(np.float32)


# ============================================================
# NORMALIZE GESTURE
# ============================================================

def normalize_gesture(z):

    return (
        z - GESTURE_MEAN
    ) / (
        GESTURE_STD + 1e-6
    )


# ============================================================
# FM DECODER
# ============================================================

def decode_fm(z):

    x = np.asarray(
        z,
        dtype=np.float32
    ).reshape(
        1,
        LATENT_DIM
    )

    fm_interpreter.set_tensor(
        fm_input["index"],
        x
    )

    fm_interpreter.invoke()

    params = fm_interpreter.get_tensor(
        fm_output["index"]
    )

    return params[0].astype(np.float32)


# ============================================================
# WAV DECODER
# ============================================================

def decode_wav(z):

    x = np.asarray(
        z,
        dtype=np.float32
    ).reshape(
        1,
        LATENT_DIM
    )

    wav_interpreter.set_tensor(
        wav_input["index"],
        x
    )

    wav_interpreter.invoke()

    representation = wav_interpreter.get_tensor(
        wav_output["index"]
    )

    return representation[0].astype(np.float32)


# ============================================================
# AUDIO
# ============================================================

pygame.mixer.pre_init(
    frequency=SAMPLE_RATE,
    size=-16,
    channels=2,
    buffer=AUDIO_CHUNK
)

pygame.init()

pygame.mixer.init(
    frequency=SAMPLE_RATE,
    size=-16,
    channels=2,
    buffer=AUDIO_CHUNK
)

print()
print("AUDIO:", pygame.mixer.get_init())
print("Mixer channels:", pygame.mixer.get_num_channels())


# ============================================================
# FM SYNTHESIS
#
# IMPORTANT:
# The exact semantic meaning of the six decoder outputs has
# not yet been confirmed. We therefore use a provisional
# interpretation:
#
# p0 = carrier frequency control
# p1 = modulation frequency ratio
# p2 = modulation index
# p3 = amplitude
# p4 = second spectral control
# p5 = output level
#
# These mappings can be changed after inspecting the original
# FM training code.
# ============================================================

phase_carrier = 0.0
phase_modulator = 0.0

current_params = np.array(
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    dtype=np.float32
)


def synthesize_fm(params):

    global phase_carrier
    global phase_modulator

    p = np.clip(
        np.asarray(params, dtype=np.float32),
        0.0,
        1.0
    )

    # --------------------------------------------
    # Provisional parameter mapping
    # --------------------------------------------

    carrier_freq = (
        70.0
        + p[0] * 900.0
    )

    mod_ratio = (
        0.25
        + p[1] * 5.0
    )

    mod_freq = carrier_freq * mod_ratio

    mod_index = (
        0.2
        + p[2] * 12.0
    )

    amplitude = (
        0.03
        + p[3] * 0.22
    )

    spectral = (
        0.2
        + p[4] * 2.0
    )

    output_gain = (
        0.15
        + p[5] * 0.45
    )

    n = np.arange(
        AUDIO_CHUNK,
        dtype=np.float32
    )

    carrier_phase = (
        phase_carrier
        + 2.0
        * np.pi
        * carrier_freq
        * n
        / SAMPLE_RATE
    )

    mod_phase = (
        phase_modulator
        + 2.0
        * np.pi
        * mod_freq
        * n
        / SAMPLE_RATE
    )

    modulation = (
        mod_index
        * np.sin(mod_phase)
    )

    signal = np.sin(
        carrier_phase
        + modulation
    )

    # Small secondary component controlled by p4
    signal += (
        0.18
        * spectral
        * np.sin(
            2.0
            * carrier_phase
            + modulation * 0.5
        )
    )

    signal *= (
        amplitude
        * output_gain
    )

    # Soft limiting
    signal = np.tanh(
        signal * 1.5
    )

    # Update phases
    phase_carrier = (
        carrier_phase[-1]
        + 2.0
        * np.pi
        * carrier_freq
        / SAMPLE_RATE
    ) % (2.0 * np.pi)

    phase_modulator = (
        mod_phase[-1]
        + 2.0
        * np.pi
        * mod_freq
        / SAMPLE_RATE
    ) % (2.0 * np.pi)

    stereo = np.column_stack(
        (signal, signal)
    )

    audio = (
        stereo
        * 32767.0
    ).astype(
        np.int16
    )

    return audio.tobytes()


# ============================================================
# STATEFUL LATENT VARIABLES
# ============================================================

z_fm_state = fm_center.copy()
z_wav_state = wav_center.copy()

z_gesture_previous = None


# ============================================================
# AUDIO CHANNEL
# ============================================================

audio_channel = pygame.mixer.Channel(0)

print()
print("Audio channel ready.")
print()
print("Toca la superficie para comenzar.")
print("Mueve, desliza y cambia el contacto.")
print("CTRL+C para salir.")
print()


# ============================================================
# MAIN LOOP
# ============================================================

gesture_buffer = deque(
    maxlen=WINDOW
)

frame = 0

last_print = 0.0

try:

    while True:

        loop_start = time.perf_counter()

        tactile = read_textile()

        gesture_buffer.append(
            tactile.copy()
        )

        # ----------------------------------------
        # Wait for complete temporal window
        # ----------------------------------------

        if len(gesture_buffer) < WINDOW:

            time.sleep(LOOP_DT)

            frame += 1

            continue

        # ----------------------------------------
        # Gesture latent
        # ----------------------------------------

        z_gesture = encode_gesture(
            gesture_buffer
        )

        g = normalize_gesture(
            z_gesture
        )

        # ----------------------------------------
        # Gesture temporal variation
        # ----------------------------------------

        if z_gesture_previous is None:

            delta = np.zeros(
                LATENT_DIM,
                dtype=np.float32
            )

        else:

            delta = (
                z_gesture
                - z_gesture_previous
            )

        z_gesture_previous = (
            z_gesture.copy()
        )

        velocity = (
            delta / max(LOOP_DT, 1e-6)
        )

        # ----------------------------------------
        # Normalize dynamic terms
        # ----------------------------------------

        delta_norm = np.tanh(
            delta / 2.0
        )

        velocity_norm = np.tanh(
            velocity / 20.0
        )

        # ----------------------------------------
        # Stateful sonic perturbation
        # ----------------------------------------

        if not np.any(tactile > 0.5):
            perturbation = np.zeros(3, dtype=np.float32)
        else:
            perturbation = (
                POSITION_GAIN * np.tanh(g)
                +
                MOVEMENT_GAIN * delta_norm
                +
                VELOCITY_GAIN * velocity_norm
            )

            perturbation = np.clip(
                perturbation,
                -MAX_PERTURBATION,
                MAX_PERTURBATION
            )

        # ----------------------------------------
        # FM latent state
        # ----------------------------------------

        z_fm_before = z_fm_state.copy()

        if np.any(tactile > 0.5):
            z_fm_state += (
                FM_GAIN
                * perturbation
            )

            z_fm_state += (
                STATE_DAMPING
                * (fm_center - z_fm_state)
            )

        z_fm_state = np.clip(
            z_fm_state,
            fm_min,
            fm_max
        )

        if not np.any(tactile > 0.5):
            if not np.array_equal(z_fm_before, z_fm_state):
                print(
                    "!!! ERROR: zFM cambió sin tacto !!!",
                    z_fm_before,
                    "->",
                    z_fm_state
                )

        # ----------------------------------------
        # WAV latent state
        # ----------------------------------------

        if np.any(tactile > 0.5):
            z_wav_state += (
                WAV_GAIN
                * perturbation
            )

            z_wav_state += (
                STATE_DAMPING
                * (wav_center - z_wav_state)
            )

        z_wav_state = np.clip(
            z_wav_state,
            wav_min,
            wav_max
        )

        # ----------------------------------------
        # Decode FM
        # ----------------------------------------

        target_params = decode_fm(
            z_fm_state
        )

        # ----------------------------------------
        # Smooth FM parameters
        # ----------------------------------------

        current_params += (
            PARAM_SMOOTHING
            * (
                target_params
                - current_params
            )
        )

        # ----------------------------------------
        # Generate audio
        # ----------------------------------------

        audio_bytes = synthesize_fm(
            current_params
        )

        sound = pygame.mixer.Sound(
            buffer=audio_bytes
        )

        audio_channel.queue(
            sound
        )

        # ----------------------------------------
        # Diagnostic output
        # ----------------------------------------

        now = time.perf_counter()

        if (
            now - last_print
            > 0.25
        ):

            active = np.where(
                tactile > 0.5
            )[0].tolist()

            print(
                f"FRAME {frame:05d} | "
                f"TOUCH {active} | "
                f"zG {np.round(z_gesture, 3)} | "
                f"dG {np.round(delta, 3)}"
            )

            print(
                f"  perturbation "
                f"{np.round(perturbation, 4)}"
            )

            print(
                f"  zFM "
                f"{np.round(z_fm_state, 4)}"
            )

            print(
                f"  FM "
                f"{np.round(current_params, 4)}"
            )

            print(
                f"  zWAV "
                f"{np.round(z_wav_state, 4)}"
            )

            print()

            last_print = now

        frame += 1

        # ----------------------------------------
        # Maintain 50 Hz tactile loop
        # ----------------------------------------

        elapsed = (
            time.perf_counter()
            - loop_start
        )

        remaining = (
            LOOP_DT
            - elapsed
        )

        if remaining > 0:
            time.sleep(
                remaining
            )


except KeyboardInterrupt:

    print()
    print("Stopping TMAQT...")

finally:

    pygame.mixer.stop()
    pygame.mixer.quit()
    pygame.quit()

    print("Audio stopped.")
