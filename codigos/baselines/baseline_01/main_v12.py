!/usr/bin/env python3
# ============================================================
# TMAQT — PERFORM v6
#
# Cambios respecto a v3:
#   - WAVs en LOOP continuo con fade-in/out
#   - Volumen compensado por RMS (todos parejos)
#   - Paneo estéreo REAL (L, R) con constant-power
#   - FM expresivo: pitch por posición, brillo por presión,
#     modulación por velocidad
#   - Gate con histéresis (sin parpadeo)
#   - Volumen global subido
# ============================================================

import os
import sys
import glob
import time
import signal
import wave
import argparse
from collections import deque

import warnings
warnings.filterwarnings("ignore")
import numpy as np
import sys
sys.path.insert(0, '.')
from bayes_touch import BayesTouch
from gesture_features import GestureFeatures
from pca_online import PCAOnline
from latent_gng import GrowingNeuralGas
from gesture_features import GestureFeatures
from pca_online import PCAOnline
from latent_gng import GrowingNeuralGas
from latent_sonifier import LatentSonifier
from sonic_navigator import SonicNavigator
from scipy.io import wavfile
import board
import busio
import adafruit_mpr121

from tflite_runtime.interpreter import Interpreter
from scipy.signal import stft, istft


# ============================================================
# CONFIGURACIÓN
# ============================================================

N_ZONES            = 24
N_CONTACT_FEATS    = 6
N_GLOBAL_FEATS     = 6
N_SONIC_PARAMS     = 6
N_WAV_PROFILE      = 4

MAX_CONTACTS       = 4
N_VOICES           = MAX_CONTACTS
MAX_WAV_VOICES     = 4

WINDOW             = 32
LATENT_DIM         = 3

LOOP_DT            = 0.02
SAMPLE_RATE        = 48000
AUDIO_CHUNK        = 1024

GESTURE_MODEL      = "TMAQT_Gesture_Encoder.tflite"
FM_MODEL           = "modelos_fm/TMAQT_FM_Decoder.tflite"
FM_LATENT_NPZ      = "modelos_fm/TMAQT_FM_Latent.npz"
WAV_DECODER_MODEL  = "TMAQT_Sonic_Decoder_Spectral.tflite"
WAV_LATENT_NPZ     = "TMAQT_Sonic_Latent_NEW.npz"
WAV_DECODER_CONFIG = "TMAQT_Sonic_Decoder_Config.npz"
WAV_SR             = 48000
WAV_N_FFT          = 2048
WAV_HOP            = 512
WAV_GL_ITERS       = 8
WAV_GAIN           = 0.20

WAV_DIR            = "audios_pcm"
WAV_GLOB           = "*.wav"

MAPPING_FILE       = "TMAQT_Mapping_v2.npz"

GESTURE_MEAN = np.array([-3.5539024, 6.653916, -6.702165], dtype=np.float32)
GESTURE_STD  = np.array([ 8.123118,  5.57736,   6.830759], dtype=np.float32)

POSITION_GAIN      = 0.15
PRESSURE_GAIN      = 0.20
DURATION_GAIN      = 0.15
MOVEMENT_GAIN      = 0.45
VELOCITY_GAIN      = 0.15
FM_GAIN            = 1.0
STATE_DAMPING      = 0.00005
PARAM_SMOOTHING    = 0.18
MAX_PERTURBATION   = 1.20

LR_WC              = 0.003
LR_WG              = 0.002
LR_PC              = 0.001
COADAPT_DECAY      = 0.9995
COADAPT_INTERVAL   = 0.2

WAV_MEMORY_PEN     = 0.35
WAV_MEMORY_DECAY   = 0.98
WAV_TRIGGER_ENERGY = 0.15

HYBRID_SMOOTHING   = 0.10
FM_WEIGHT_MIN      = 0.30
FM_WEIGHT_MAX      = 0.75

# Gate con histéresis
GATE_RISE          = 0.85
GATE_FALL          = 0.40
GATE_THRESHOLD     = 0.002
GATE_OPEN_FRAMES   = 2
GATE_CLOSE_FRAMES  = 3

# WAV disparo (one-shot)
WAV_FADE_MS        = 30
WAV_FADEOUT_MS     = 80
WAV_VOL_MIN        = 0.70
WAV_VOL_MAX        = 1.20

# Volumen global
FM_GAIN_OUT        = 3.0
WAV_GAIN_OUT       = 2.5
MASTER_GAIN        = 3.5


# ============================================================
# MANEJO DE SIGTERM (systemd)
# ============================================================

def _handle_sigterm(signum, frame):
    raise KeyboardInterrupt()

signal.signal(signal.SIGTERM, _handle_sigterm)


# ============================================================
# ARGUMENTOS
# ============================================================

parser = argparse.ArgumentParser()
parser.add_argument("--rehearse", action="store_true")
parser.add_argument("--perform",  action="store_true")
parser.add_argument("--inspect",  action="store_true")
parser.add_argument("--no-audio", action="store_true")
parser.add_argument("--verbose",  action="store_true")
args = parser.parse_args()

if not (args.rehearse or args.perform or args.inspect):
    print("Uso: python3 TMAQT_Perform_v4.py --rehearse | --perform | --inspect [--verbose] [--no-audio]")
    sys.exit(1)
if args.rehearse and args.perform:
    print("Elige solo un modo.")
    sys.exit(1)


# ============================================================
# START
# ============================================================

print()
print("====================================================")
print("TMAQT — PERFORM v6  (cinta 24 zonas)")
if   args.rehearse: print("  MODO: REHEARSE")
elif args.perform:  print("  MODO: PERFORM")
else:               print("  MODO: INSPECT")
print("====================================================")
print()


# ============================================================
# INSPECT
# ============================================================

def inspect_mapping():
    if not os.path.exists(MAPPING_FILE):
        print("No existe TMAQT_Mapping_v2.npz. Corre --rehearse primero.")
        sys.exit(0)
    d = np.load(MAPPING_FILE)
    W_c = d["W_c"]; W_g = d["W_g"]; P_c = d["P_c"]
    c_labels = ["pos ", "wdth", "vel ", "dur ", "pres", "shpe"]
    g_labels = ["nC  ", "dens", "span", "cent", "symm", "alt "]

    print("W_c  (features de contacto → params FM):")
    print("        p0     p1     p2     p3     p4     p5")
    for i, lab in enumerate(c_labels):
        print(f"  {lab}  " + "  ".join(f"{v:+.3f}" for v in W_c[i]))
    print()
    print("W_g  (features globales → params FM):")
    print("        p0     p1     p2     p3     p4     p5")
    for i, lab in enumerate(g_labels):
        print(f"  {lab}  " + "  ".join(f"{v:+.3f}" for v in W_g[i]))
    print()
    print("P_c  (features de contacto → perfil acústico):")
    print("        rms    ctr    atk    dur")
    for i, lab in enumerate(c_labels):
        print(f"  {lab}  " + "  ".join(f"{v:+.3f}" for v in P_c[i]))
    sys.exit(0)

if args.inspect:
    inspect_mapping()


# ============================================================
# I2C / MPR121
# ============================================================

i2c_left  = busio.I2C(board.SCL, board.SDA)
i2c_right = busio.I2C(board.SCL, board.SDA)


def connect_mpr(i2c_bus, addr, label, retries=10, delay=0.5):
    last_err = None
    for attempt in range(retries):
        try:
            m = adafruit_mpr121.MPR121(i2c_bus, address=addr)
            print(f"MPR121 0x{addr:02X} : OK  ({label})")
            return m
        except OSError as e:
            last_err = e
            print(f"MPR121 0x{addr:02X} : intento {attempt+1}/{retries} falló ({e})")
            time.sleep(delay)
    raise RuntimeError(f"No se pudo conectar MPR121 0x{addr:02X}: {last_err}")


mpr_left  = connect_mpr(i2c_left,  0x5A, "zonas 0..11")
time.sleep(0.5)
mpr_right = connect_mpr(i2c_right, 0x5C, "zonas 12..23")


# ============================================================
# MODELOS
# ============================================================

def load_interpreter(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Modelo no encontrado: {path}")
    it = Interpreter(model_path=path)
    it.allocate_tensors()
    return it

gesture_interpreter = load_interpreter(GESTURE_MODEL)
fm_interpreter      = load_interpreter(FM_MODEL)
wav_interpreter     = load_interpreter(WAV_DECODER_MODEL)

gesture_input  = gesture_interpreter.get_input_details()[0]
gesture_output = gesture_interpreter.get_output_details()[0]
fm_input       = fm_interpreter.get_input_details()[0]
fm_output      = fm_interpreter.get_output_details()[0]
wav_input      = wav_interpreter.get_input_details()[0]
wav_output     = wav_interpreter.get_output_details()[0]

print()
print("Gesture  IN/OUT:", gesture_input["shape"], "->", gesture_output["shape"])
print("FM       IN/OUT:", fm_input["shape"],      "->", fm_output["shape"])

_fm_npz = np.load(FM_LATENT_NPZ)
fm_Z = None
for k in _fm_npz.files:
    arr = np.asarray(_fm_npz[k])
    if arr.ndim == 2 and arr.shape[1] == LATENT_DIM:
        fm_Z = arr.astype(np.float32)
        break
if fm_Z is None:
    raise RuntimeError("No se encontró latente FM (N,3)")
fm_min, fm_max, fm_center = fm_Z.min(0), fm_Z.max(0), fm_Z.mean(0)
print("FM center:", np.round(fm_center, 4))

_wav_npz = np.load(WAV_LATENT_NPZ)
wav_Z = np.asarray(_wav_npz["Z"], dtype=np.float32)

wav_min = wav_Z.min(0)
wav_max = wav_Z.max(0)
wav_center = wav_Z.mean(0)

_wav_cfg = np.load(WAV_DECODER_CONFIG)
wav_z_mean = np.asarray(_wav_cfg["zWAV_mean"], dtype=np.float32)
wav_z_std = np.asarray(_wav_cfg["zWAV_std"], dtype=np.float32)

WAV_SR = int(_wav_cfg["sr"])
WAV_N_FFT = int(_wav_cfg["n_fft"])
WAV_HOP = int(_wav_cfg["hop_length"])

print("WAV latent:", wav_Z.shape)
print("WAV center:", np.round(wav_center, 4))
print("WAV decoder:", wav_input["shape"], "->", wav_output["shape"])


# ============================================================
# WAVs (con recorte y perfil RMS)
# ============================================================

WAV_MAX_DURATION = 30.0

def load_wav_smart(path, max_dur=WAV_MAX_DURATION):
    with wave.open(path, "rb") as w:
        n  = w.getnframes()
        sr = w.getframerate()
        ch = w.getnchannels()
        sw = w.getsampwidth()
        raw = w.readframes(n)

    if sw == 2:
        a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    elif sw == 1:
        a = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
    elif sw == 4:
        a = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
    else:
        raise ValueError(f"Sample width no soportado: {sw}")

    if ch == 2:
        a = a.reshape(-1, 2).mean(axis=1)

    dur = len(a) / sr
    if dur > max_dur:
        target_n = int(max_dur * sr)
        start = (len(a) - target_n) // 2
        a = a[start:start + target_n]
        dur = len(a) / sr

    return a, sr, dur


def wav_profile(audio, sr):
    rms = float(np.sqrt(np.mean(audio**2) + 1e-9))
    duration = float(np.clip(len(audio) / sr / 30.0, 0.0, 1.0))
    n_fft = min(4096, len(audio))
    spec  = np.abs(np.fft.rfft(audio[:n_fft]))
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sr)
    centroid = float(np.sum(freqs * spec) / (np.sum(spec) + 1e-9))
    centroid_n = float(np.clip(centroid / (sr / 2.0), 0.0, 1.0))
    env = np.abs(audio)
    peak_idx = int(np.argmax(env))
    attack = float(np.clip(peak_idx / sr / 30.0, 0.0, 1.0))
    return np.array([rms, centroid_n, attack, duration], dtype=np.float32)


wav_paths = sorted(glob.glob(os.path.join(WAV_DIR, WAV_GLOB)))
if not wav_paths:
    raise RuntimeError(f"No hay WAVs en {WAV_DIR}/")

wav_profiles = []
wav_audio_loaded = []

for p in wav_paths:
    a, sr, dur = load_wav_smart(p)
    prof = wav_profile(a, sr)
    wav_profiles.append(prof)
    wav_audio_loaded.append((a, sr))
    print(f"  {os.path.basename(p):10s} dur={dur:6.2f}s  "
          f"prof=[rms={prof[0]:.2f} ctr={prof[1]:.2f} atk={prof[2]:.2f} dur={prof[3]:.2f}]")

wav_profiles = np.stack(wav_profiles)
N_WAVS = len(wav_paths)

# === v12: cargar WAVs para sonificacion continua ===
wav_arrays = []
for p in wav_paths:
    sr_file, data = wavfile.read(p)
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32767.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483647.0
    elif data.dtype == np.float32:
        pass
    else:
        data = data.astype(np.float32)
    wav_arrays.append(data)
print(f"v12: {len(wav_arrays)} WAVs cargados para sonificacion continua")

# === v12: SonicNavigator ===
sonic_nav = SonicNavigator('TMAQT_Sonic_Latent_NEW.npz')

# === v12: LatentSonifier ===
sonifier = LatentSonifier(
    sonic_nav=sonic_nav,
    wav_arrays=wav_arrays,
    sample_rate=48000,
    blocksize=1024,
    device=None,  # None = default (pulse → HifiBerry)
    k=3,
)
print(f"\n{N_WAVS} WAVs cargados.")


# ============================================================
# MATRICES
# ============================================================

def init_Wc():
    W = np.zeros((N_CONTACT_FEATS, N_SONIC_PARAMS), dtype=np.float32)
    W[0, 0] = 0.30; W[1, 3] = 0.10
    W[2, 0] = 0.20; W[2, 4] = 0.20
    W[3, 5] = 0.15; W[4, 2] = 0.25
    W[5, 4] = 0.10
    W += np.random.uniform(-0.02, 0.02, size=W.shape).astype(np.float32)
    return W

def init_Wg():
    W = np.zeros((N_GLOBAL_FEATS, N_SONIC_PARAMS), dtype=np.float32)
    W[0, 3] = 0.15; W[1, 4] = 0.20
    W[2, 1] = 0.15; W[3, 0] = 0.10
    W[4, 5] = 0.10; W[5, 4] = 0.10
    W += np.random.uniform(-0.02, 0.02, size=W.shape).astype(np.float32)
    return W

def init_Pc():
    P = np.zeros((N_CONTACT_FEATS, N_WAV_PROFILE), dtype=np.float32)
    P[0, 1] = 0.20; P[1, 0] = 0.25
    P[2, 1] = 0.20; P[3, 3] = 0.25
    P[4, 2] = 0.30
    P += np.random.uniform(-0.02, 0.02, size=P.shape).astype(np.float32)
    return P

def load_or_init():
    if os.path.exists(MAPPING_FILE):
        d = np.load(MAPPING_FILE)
        print(f"Matrices cargadas desde {MAPPING_FILE}")
        return d["W_c"].astype(np.float32), d["W_g"].astype(np.float32), d["P_c"].astype(np.float32)
    print("Inicializando matrices nuevas.")
    return init_Wc(), init_Wg(), init_Pc()

def save_mapping(W_c, W_g, P_c):
    np.savez(MAPPING_FILE, W_c=W_c, W_g=W_g, P_c=P_c)
    print(f"Matrices guardadas en {MAPPING_FILE}")

W_c, W_g, P_c = load_or_init()
print("W_c:", W_c.shape, "| W_g:", W_g.shape, "| P_c:", P_c.shape)


# ============================================================
# TEXTIL
# ============================================================

def read_textile():
    vector = np.zeros(N_ZONES, dtype=np.float32)
    try:
        left  = mpr_left.touched()
        right = mpr_right.touched()
    except OSError:
        return vector
    for ch in range(12):
        if left & (1 << ch):
            vector[ch] = 1.0
    for ch in range(12):
        if right & (1 << ch):
            vector[ch + 12] = 1.0
    return vector


# ============================================================
# CONTACTOS
# ============================================================

def detect_contacts(tactile):
    """Agrupa zonas contiguas. Fusiona grupos cercanos si el previo es angosto."""
    raw = []
    i = 0
    while i < N_ZONES:
        if tactile[i] > 0.5:
            j = i
            while j + 1 < N_ZONES and tactile[j+1] > 0.5:
                j += 1
            raw.append([i, j])
            i = j + 1
        else:
            i += 1

    if len(raw) <= 1:
        return [{"start": c[0], "end": c[1],
                 "pos": (c[0]+c[1])/2.0, "width": c[1]-c[0]+1}
                for c in raw]

    merged = [raw[0][:]]
    for c in raw[1:]:
        gap = c[0] - merged[-1][1]
        prev_width = merged[-1][1] - merged[-1][0] + 1
        # fusionar solo si gap < 3 Y el contacto previo es angosto (<=2)
        if gap < 3 and prev_width <= 2:
            merged[-1][1] = c[1]
        else:
            merged.append(c[:])

    return [{"start": c[0], "end": c[1],
             "pos": (c[0]+c[1])/2.0, "width": c[1]-c[0]+1}
            for c in merged]


class ContactTracker:
    def __init__(self):
        self.prev = []
        self.history = deque(maxlen=20)

    def match(self, contacts):
        out = []
        used = set()
        for c in contacts:
            # buscar TODOS los previos que se solapen espacialmente con c
            c_start, c_end = c["start"], c["end"]
            overlapping = []
            for i, p in enumerate(self.prev):
                if i in used: continue
                p_start, p_end = p["start"], p["end"]
                # se solapan si los rangos [start, end] se intersectan
                if not (c_end < p_start - 1 or c_start > p_end + 1):
                    overlapping.append(i)
            if overlapping:
                # tomar el de mayor dur_frames (corrección 4)
                durs = [self.prev[i]["dur_frames"] for i in overlapping]
                best_i = overlapping[int(np.argmax(durs))]
                dur = self.prev[best_i]["dur_frames"] + 1
                onset = self.prev[best_i].get("onset", 0.0)
                for i in overlapping:
                    used.add(i)
            else:
                dur = 1
                onset = 1.0
            c2 = dict(c)
            c2["dur_frames"] = dur
            c2["onset"] = max(onset * 0.9, 0.0) if dur > 1 else 1.0
            out.append(c2)

        self.history.append(len(out))

        self.prev = [{"start": c["start"], "end": c["end"],
                      "pos": c["pos"], "width": c["width"],
                      "dur_frames": c["dur_frames"],
                      "onset": c["onset"]} for c in out]
        return out

    def activity_var(self):
        if len(self.history) < 3:
            return 0.0
        return float(np.clip(np.std(list(self.history)) / 2.0, 0.0, 1.0))

contact_tracker = ContactTracker()


def contact_features(contacts, dt):
    if not contacts:
        return [], np.zeros(N_GLOBAL_FEATS, dtype=np.float32), np.zeros((0, 3), dtype=np.float32)
    feats_list = []
    positions = []
    a_var = contact_tracker.activity_var()
    for c in contacts:
        pos_n = c["pos"] / (N_ZONES - 1)
        width_n = c["width"] / N_ZONES
        dur_n = float(np.clip(c["dur_frames"] / 100.0, 0.0, 1.0))
        vel = 0.0
        if contact_tracker.prev:
            best_d = 1e9
            for p in contact_tracker.prev:
                d = abs(c["pos"] - p["pos"])
                if d < best_d: best_d = d
            vel = best_d / max(dt, 1e-6) / (N_ZONES - 1)
        vel = float(np.clip(vel, 0.0, 1.0))
        pressure = float(np.clip(width_n * min(vel * 8.0, 1.0), 0.0, 1.0))
        shape = 1.0
        feats_list.append(np.array([pos_n, width_n, vel, dur_n, pressure, shape],
                                   dtype=np.float32))
        positions.append(pos_n)
    n_contacts = len(contacts) / MAX_CONTACTS
    density = float(np.sum([c["width"] for c in contacts]) / N_ZONES)
    span = (max(positions) - min(positions)) if len(positions) > 1 else 0.0
    centroid = float(np.mean(positions))
    symmetry = 0.0
    if len(positions) == 2:
        symmetry = 1.0 - abs(positions[0] + positions[1] - 1.0)
    # info extra por contacto (onset, stability, activity_var)
    extra = []
    for c in contacts:
        onset = float(c.get("onset", 0.5))
        dur_f = c["dur_frames"]
        stability = float(np.clip(dur_f / 200.0, 0.0, 1.0))
        extra.append(np.array([onset, stability, a_var], dtype=np.float32))
    extra = np.stack(extra)

    g = np.array([n_contacts, density, span, centroid,
                  float(np.clip(symmetry, 0.0, 1.0)), 0.0], dtype=np.float32)
    return feats_list, g, extra


# ============================================================
# ENCODER / DECODER
# ============================================================

def encode_gesture(window):
    x = np.asarray(window, dtype=np.float32).reshape(1, WINDOW, N_ZONES)
    gesture_interpreter.set_tensor(gesture_input["index"], x)
    gesture_interpreter.invoke()
    return gesture_interpreter.get_tensor(gesture_output["index"])[0].astype(np.float32)

def normalize_gesture(z):
    return (z - GESTURE_MEAN) / (GESTURE_STD + 1e-6)

def decode_fm(z):
    x = np.asarray(z, dtype=np.float32).reshape(1, LATENT_DIM)
    fm_interpreter.set_tensor(fm_input["index"], x)
    fm_interpreter.invoke()
    return fm_interpreter.get_tensor(fm_output["index"])[0].astype(np.float32)


def decode_wav(z):
    # The spectral decoder was trained directly on RAW zWAV.
    z = np.asarray(z, dtype=np.float32)

    x = z.reshape(1, LATENT_DIM)
    wav_interpreter.set_tensor(wav_input["index"], x)
    wav_interpreter.invoke()
    return wav_interpreter.get_tensor(wav_output["index"])[0].astype(np.float32)


def synthesize_wav(z):
    decoded = decode_wav(z)
    decoded = np.asarray(decoded, dtype=np.float32).squeeze()

    # Undo training normalization
    log_mag = (
        decoded * _wav_cfg["spec_std"]
        + _wav_cfg["spec_mean"]
    )

    log_mag = np.maximum(log_mag, 0.0)

    magnitude = np.exp(log_mag) - 1.0
    magnitude = np.maximum(magnitude, 0.0)

    rng_local = np.random.default_rng(42)

    phase = np.exp(
        2j * np.pi
        * rng_local.random(magnitude.shape)
    )

    complex_spec = magnitude * phase

    # Griffin-Lim
    for _ in range(WAV_GL_ITERS):
        _, audio = istft(
            complex_spec,
            fs=WAV_SR,
            window="hann",
            nperseg=WAV_N_FFT,
            noverlap=WAV_N_FFT - WAV_HOP,
            input_onesided=True,
            freq_axis=0,
            time_axis=1
        )

        _, _, updated_spec = stft(
            audio,
            fs=WAV_SR,
            window="hann",
            nperseg=WAV_N_FFT,
            noverlap=WAV_N_FFT - WAV_HOP,
            nfft=WAV_N_FFT,
            return_onesided=True
        )

        h = min(updated_spec.shape[0], magnitude.shape[0])
        w = min(updated_spec.shape[1], magnitude.shape[1])

        phase = updated_spec[:h, :w]
        phase = phase / (np.abs(phase) + 1e-8)

        complex_spec = magnitude[:h, :w] * phase

    _, audio = istft(
        complex_spec,
        fs=WAV_SR,
        window="hann",
        nperseg=WAV_N_FFT,
        noverlap=WAV_N_FFT - WAV_HOP,
        input_onesided=True,
        freq_axis=0,
        time_axis=1
    )

    audio = np.asarray(audio, dtype=np.float32)

    peak = np.max(np.abs(audio)) + 1e-8
    audio = audio / peak

    return audio


# ============================================================
# WAV MATCHING
# ============================================================

wav_memory = np.zeros(N_WAVS, dtype=np.float32)
WAV_MEMORY_PEN_STRONG = 2.0     # penalización fuerte
WAV_TOP_K = 5                    # elegir entre los 5 mejores

def choose_wav(feats_c, extra=None):
    """Elige WAV según gesto. Diferencia golpe/sostener/deslizar."""
    global wav_memory
    pos      = feats_c[0]
    width    = feats_c[1]
    velocity = feats_c[2]
    duration = feats_c[3]
    pressure = feats_c[4]

    if extra is not None and len(extra) >= 3:
        onset = float(extra[0]); stab = float(extra[1]); a_var = float(extra[2])
    else:
        onset, stab, a_var = 0.5, 0.5, 0.0

    # === Clasificación suave del gesto ===
    is_golpe    = onset > 0.6 and stab < 0.3
    is_sostener = stab > 0.6 and onset < 0.3
    is_deslizar = velocity > 0.3

    target = np.zeros(4, dtype=np.float32)
    if is_golpe:
        target[0] = 0.5 + 0.4 * pressure    # rms alto
        target[1] = 0.5 + 0.4 * velocity    # brillante
        target[2] = 0.15                    # ataque rápido
        target[3] = 0.2                     # sample corto
    elif is_sostener:
        target[0] = 0.3 + 0.4 * pressure    # rms medio
        target[1] = 0.15                    # oscuro
        target[2] = 0.7                     # ataque lento
        target[3] = 0.9                     # sample largo
    elif is_deslizar:
        target[0] = 0.3
        target[1] = 0.6 + 0.3 * velocity    # brillante
        target[2] = 0.4
        target[3] = 0.6
    else:
        target[0] = 0.3 + 0.4 * pressure
        target[1] = 0.2 + 0.5 * velocity
        target[2] = 0.5
        target[3] = 0.5 + 0.3 * duration

    dists = np.linalg.norm(wav_profiles - target, axis=1)
    dists = dists + WAV_MEMORY_PEN_STRONG * wav_memory
    k = min(WAV_TOP_K, N_WAVS)
    topk_idx = np.argsort(dists)[:k]
    topk_d = dists[topk_idx] + 1e-6
    weights = 1.0 / topk_d
    weights /= weights.sum()
    idx = int(np.random.choice(topk_idx, p=weights))
    wav_memory[idx] = 1.0
    wav_memory *= 0.85
    return idx


# ============================================================
# AUDIO INIT (v12: sin pygame, sounddevice en sonifier)
# ============================================================

if args.no_audio:
    print("\nAUDIO DESACTIVADO")
else:
    print("\nAUDIO: sounddevice (LatentSonifier)")

# v12: no usamos pygame. Los WAVs ya estan en wav_arrays.
wav_sounds = []
wav_rms_gain = []
for prof in wav_profiles:
    rms = float(prof[0])
    gain = 0.10 / max(rms, 0.015)
    wav_rms_gain.append(float(np.clip(gain, 1.0, 5.0)))

FM_CHANNEL_INDEX = 0
WAV_CHANNEL_BASE = 1
fm_channel = None
wav_channels = []
SONIC_LEARNED_CHANNEL_INDEX = 0
sonic_learned_channel = None
sonic_learned_sound = None


# Estado de loop WAV por canal
wav_ch_playing   = np.full(MAX_WAV_VOICES, -1, dtype=int)
wav_ch_vol       = np.zeros(MAX_WAV_VOICES, dtype=np.float32)
wav_ch_cooldown  = np.zeros(MAX_WAV_VOICES, dtype=np.float32)   # frames restantes de bloqueo
WAV_COOLDOWN_FRAMES = 15   # ~300 ms a 50 Hz



# ============================================================
# AUDIO DEL ESTADO SONICO APRENDIDO
# ============================================================

# ============================================================
# ESTADO SONICO APRENDIDO
# ============================================================

# Estado continuo en un espacio sónico de 3 dimensiones.
# Todavía no reemplaza los WAV físicos ni modifica el FM.
z_sonic_state = np.zeros(LATENT_DIM, dtype=np.float32)

# v12: co-adaptacion del mapeo gesto -> latente
LR_MAP = 0.005
DECAY_MAP = 0.9995

SONIC_STATE_GAIN = 0.12
SONIC_STATE_SCALE = 1.5
SONIC_STATE_CLIP = 2.5

# One-shot del sonido aprendido.
SONIC_LEARNED_COOLDOWN = 18
sonic_learned_cooldown = 0


# ============================================================
# FM SYNTH POR VOZ
# ============================================================

class FMVoice:
    def __init__(self):
        self.phase_c = 0.0
        self.phase_m = 0.0
        self.params  = np.array([0.1]*6, dtype=np.float32)
        self.fm_w    = 0.7

    def synth(self, n_samples, pos_n=0.5, pressure=0.0, velocity=0.0, t_global=0.0):
        p = np.clip(self.params, 0.0, 1.0)

        # === FM expresivo ===
        # Posición → pitch (±1 octava)
        octave_shift = (pos_n - 0.5) * 2.0
        carrier_freq = 120.0 * (2.0 ** octave_shift)

        # Modulación por velocidad (vibrato/LFO)
        n = np.arange(n_samples, dtype=np.float32)
        t = t_global + n / SAMPLE_RATE
        if velocity > 0.15:
            lfo_depth = 0.02 + 0.08 * velocity
            lfo_rate  = 5.0 + 8.0 * velocity
            vibrato = 1.0 + lfo_depth * np.sin(2*np.pi*lfo_rate*t)
            carrier_freq = carrier_freq * vibrato

        # Brillo por presión
        base_mod_idx = 0.5 + p[2] * 4.0
        mod_index = base_mod_idx * (1.0 + 1.5 * pressure)

        mod_ratio = 0.5 + p[1] * 3.0
        mod_freq  = carrier_freq * mod_ratio

        # Amplitud
        amplitude = 0.15 + p[3] * 0.30
        amplitude *= (1.0 + 0.5 * pressure)

        spectral    = 0.3 + p[4] * 1.5
        output_gain = 0.3 + p[5] * 0.5

        cp = self.phase_c + 2*np.pi*carrier_freq*n/SAMPLE_RATE
        mp = self.phase_m + 2*np.pi*mod_freq*n/SAMPLE_RATE
        mod = mod_index * np.sin(mp)
        sig = np.sin(cp + mod)
        sig += 0.20 * spectral * np.sin(2*cp + mod*0.5)
        sig *= amplitude * output_gain
        sig = np.tanh(sig * 1.5)

        self.phase_c = (cp[-1] + 2*np.pi*carrier_freq/SAMPLE_RATE) % (2*np.pi)
        self.phase_m = (mp[-1] + 2*np.pi*mod_freq    /SAMPLE_RATE) % (2*np.pi)
        return sig

    def update_params(self, target):
        self.params += 0.5 * (target - self.params)

fm_voices = [FMVoice() for _ in range(N_VOICES)]

# Módulos del espacio latente
bayes = BayesTouch(N_ZONES)
gf = GestureFeatures(N_ZONES)
pca = PCAOnline(n_in=20, n_out=3, lr=0.005)
gng = GrowingNeuralGas(dim=3, params_dim=8, max_nodes=2000,
                       learning_rate=0.05, neighbor_lr=0.005,
                       max_age=50, new_node_every=150)
gf = GestureFeatures(N_ZONES)
pca = PCAOnline(n_in=20, n_out=3, lr=0.005)
gng = GrowingNeuralGas(dim=3, params_dim=8, max_nodes=2000,
                       learning_rate=0.05, neighbor_lr=0.005,
                       max_age=50, new_node_every=150)
prev_gng_node = -1


# ============================================================
# ESTADO GLOBAL
# ============================================================

z_fm_state = fm_center.copy()
z_gesture_previous = None
gesture_buffer = deque(maxlen=WINDOW)

fm_weight = 0.5
last_coadapt_time = 0.0
frame = 0
last_print = 0.0
alternation_hist = deque(maxlen=50)

master_gain = 0.0
t_global = 0.0

# Gate con histéresis
contact_count_hist = deque(maxlen=10)
last_contact_count = 0


# ============================================================
# LOOP
# ============================================================

print()
if args.rehearse:
    print("REHEARSE — explora la cinta. Las matrices se refinan con el uso.")
else:
    print("PERFORM — matrices congeladas. El gesto altera el sonido.")
print("CTRL+C para salir.")
print()

# === v12: iniciar sonificador continuo ===
sonifier.start()

try:
    while True:
        loop_start = time.perf_counter()

        tactile = read_textile()
        gesture_buffer.append(tactile.copy())

        # === BAYES: 24 probabilidades continuas ===
        p_touch = bayes.update(tactile)

        # === 20 PROPIEDADES del gesto ===
        features = gf.compute(p_touch)

        # === PCA: 20D -> 3D ===
        pca.update(features)
        z_gesto = pca.transform(features)
        z_gesto = np.tanh(z_gesto).astype(np.float32)

        # === GNG: espacio latente navegable ===
        area = float(features[0])
        touching = area > 0.03
        if touching:
            gng_params = np.array([
                0.3 + 0.4 * area,
                0.2 + 0.6 * min(1.0, float(features[2]) * 4),
                0.3 + 0.5 * min(1.0, area * 2),
                0.3 + 0.5 * area,
                0.2 + 0.6 * min(1.0, float(features[9])),
                0.5,
                float(features[1]),
                min(1.0, area * 1.5),
            ], dtype=np.float32)
            gng.add_or_update(z_gesto, gng_params)

            # Nodo más cercano
            node_dists = []
            for ni, node in enumerate(gng.nodes):
                d = float(np.linalg.norm(node.pos - z_gesto))
                node_dists.append((d, ni, node))
            node_dists.sort(key=lambda x: x[0])
            gng_current_node = node_dists[0] if node_dists else None
        else:
            gng_current_node = None

        raw_contacts = detect_contacts(tactile)
        contacts = contact_tracker.match(raw_contacts)
        feats_list, g, extra_feats = contact_features(contacts, LOOP_DT)

        n_c = len(contacts)
        alternation_hist.append(1.0 if n_c != last_contact_count else 0.0)
        last_contact_count = n_c
        g[5] = float(np.mean(alternation_hist)) if alternation_hist else 0.0

        # === GATE con histéresis ===
        contact_count_hist.append(n_c)
        recent = list(contact_count_hist)
        if n_c > 0 and all(x > 0 for x in recent[-GATE_OPEN_FRAMES:]):
            master_gain += GATE_RISE * (1.0 - master_gain)
        elif n_c == 0 and all(x == 0 for x in recent[-GATE_CLOSE_FRAMES:]):
            master_gain += GATE_FALL * (0.0 - master_gain)
        master_gain = float(np.clip(master_gain, 0.0, 1.0))

        if len(gesture_buffer) < WINDOW:
            time.sleep(LOOP_DT)
            frame += 1
            continue

        # === Latente FM base ===
        z_gesture = encode_gesture(gesture_buffer)
        zg = normalize_gesture(z_gesture)

        if z_gesture_previous is None:
            delta = np.zeros(LATENT_DIM, dtype=np.float32)
        else:
            delta = z_gesture - z_gesture_previous
        z_gesture_previous = z_gesture.copy()

        velocity = delta / max(LOOP_DT, 1e-6)
        delta_norm    = np.tanh(delta / 2.0)
        velocity_norm = np.tanh(velocity / 20.0)

        touching = n_c > 0

        # === Estado sonico aprendido ===
        # El gesto navega suavemente por un espacio sonico continuo.
        if touching:
            sonic_target = np.tanh(zg).astype(np.float32)

            z_sonic_state += SONIC_STATE_GAIN * (
                sonic_target - z_sonic_state
            )

            z_sonic_state = np.clip(
                z_sonic_state,
                -SONIC_STATE_CLIP,
                SONIC_STATE_CLIP
            )

        # === v12: MAPEO APRENDIDO gesto -> z_wav_state ===
        if touching and feats_list:
            pos_avg = float(np.mean([f[0] for f in feats_list]))   # 0..1
            width_avg = float(np.mean([f[1] for f in feats_list]))  # 0..1
            dur_avg = float(np.mean([f[3] for f in feats_list]))    # 0..1

            gx = 2.0 * pos_avg - 1.0
            gy = 2.0 * width_avg - 1.0
            gz = 2.0 * dur_avg - 1.0

            gesto_3d = np.array([gx, gy, gz], dtype=np.float32)

            global _z_gesto_prev
            if '_z_gesto_prev' not in globals():
                _z_gesto_prev = gesto_3d.copy()
            alpha = 0.15
            _z_gesto_prev = (1.0 - alpha) * _z_gesto_prev + alpha * gesto_3d
            gesto_suave = _z_gesto_prev

            # v12: mapeo aprendido W_map (3x3)
            global W_map
            if 'W_map' not in globals():
                scale = 0.5 * (wav_max - wav_min)
                W_map = np.diag(scale).astype(np.float32)

            z_wav_target = wav_center + W_map @ gesto_suave
            z_wav_state = z_wav_target
            z_wav_state = np.clip(z_wav_state, wav_min, wav_max)

            # Co-adaptacion del mapeo
            if args.rehearse:
                delta = z_wav_state - wav_center
                W_map += LR_MAP * np.outer(delta, gesto_suave)
                W_map *= DECAY_MAP
                # Limitar para evitar divergencia
                W_map = np.clip(W_map, -2.0 * scale.max(), 2.0 * scale.max())
        else:
            z_wav_state = wav_center.copy()

        # === v12: enviar al sonificador continuo ===
        sonifier.set_gesture(z_wav_state, gate=master_gain)

        if touching:
            # Medias de los features de contacto
            if feats_list:
                pressure_avg = float(np.mean([f[4] for f in feats_list]))
                duration_avg = float(np.mean([f[3] for f in feats_list]))
                velocity_avg = float(np.mean([f[2] for f in feats_list]))
            else:
                pressure_avg = duration_avg = velocity_avg = 0.0

            # La perturbación suma 4 contribuciones:
            #   posición  → mueve el estado según dónde tocas
            #   movimiento → mueve el estado según cómo te mueves
            #   velocidad  → mueve el estado según la rapidez
            #   presión    → mueve el estado según el área
            #   duración   → mueve el estado según cuánto llevas tocando
            perturbation = (POSITION_GAIN * np.tanh(zg)
                            + MOVEMENT_GAIN * delta_norm
                            + VELOCITY_GAIN * velocity_norm
                            + PRESSURE_GAIN * pressure_avg * np.ones(3, dtype=np.float32)
                            + DURATION_GAIN * duration_avg * np.ones(3, dtype=np.float32))
            perturbation = np.clip(perturbation, -MAX_PERTURBATION, MAX_PERTURBATION)
            z_fm_state += FM_GAIN * perturbation
        z_fm_state += STATE_DAMPING * (fm_center - z_fm_state)
        z_fm_state = np.clip(z_fm_state, fm_min, fm_max)

        base_params = decode_fm(z_fm_state)
        learned_global = g @ W_g if touching else np.zeros(N_SONIC_PARAMS, dtype=np.float32)

        # === Cooldown del sonido aprendido ===
        if sonic_learned_cooldown > 0:
            sonic_learned_cooldown -= 1

        # === Voces ===
        energies = [float(np.mean(f[:3])) for f in feats_list]
        order = np.argsort(energies)[::-1][:MAX_CONTACTS] if energies else np.array([], dtype=int)

        audio_L = np.zeros(AUDIO_CHUNK, dtype=np.float32)
        audio_R = np.zeros(AUDIO_CHUNK, dtype=np.float32)

        # Decrementar cooldown de todos los canales WAV
        for s in range(MAX_WAV_VOICES):
            if wav_ch_cooldown[s] > 0:
                wav_ch_cooldown[s] -= 1

        # Reset targets de WAV
        wav_ch_target = np.zeros(MAX_WAV_VOICES, dtype=np.float32)

        for slot, ci in enumerate(order):
            feats_c = feats_list[ci]
            contact = contacts[ci]
            energy = energies[ci]

            learned_c = feats_c @ W_c
            # FM 100% desde el nodo del GNG (IML radical)
            if gng_current_node is not None:
                _, ni_gng, node_gng = gng_current_node
                target = np.clip(node_gng.params[:6], 0.0, 1.0)
            else:
                target = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5], dtype=np.float32)
            fm_voices[slot].update_params(target)

            pos_n     = feats_c[0]
            pressure  = feats_c[4]
            vel_c     = feats_c[2]

            # GATE: solo sintetizar si hay contacto
            if n_c > 0:
                sig = fm_voices[slot].synth(AUDIO_CHUNK,
                                            pos_n=pos_n,
                                            pressure=pressure,
                                            velocity=vel_c,
                                            t_global=t_global)
            else:
                sig = np.zeros(AUDIO_CHUNK, dtype=np.float32)

            # === PANEO constant-power (arreglado) ===
            # Paneo por z_gesto (IML)
            pan = 0.5 + 0.5 * float(np.tanh(z_gesto[0]))
            pan = float(np.clip(pan, 0.0, 1.0))
            pan = 0.05 + 0.90 * pan
            angle = pan * (np.pi / 2.0)
            gain_L = np.cos(angle)
            gain_R = np.sin(angle)

            # FM APAGADO (solo WAVs)
            # audio_L += sig * gain_L * FM_GAIN_OUT
            # audio_R += sig * gain_R * FM_GAIN_OUT

            target_fm_w = float(np.clip(
                FM_WEIGHT_MAX - (FM_WEIGHT_MAX - FM_WEIGHT_MIN) * energy,
                FM_WEIGHT_MIN, FM_WEIGHT_MAX
            ))
            fm_voices[slot].fm_w += HYBRID_SMOOTHING * (target_fm_w - fm_voices[slot].fm_w)

        # === Balance híbrido global ===
        if touching and order.size:
            avg_energy = float(np.mean(energies[:len(order)]))
            target_fm_w = float(np.clip(
                FM_WEIGHT_MAX - (FM_WEIGHT_MAX - FM_WEIGHT_MIN) * avg_energy,
                FM_WEIGHT_MIN, FM_WEIGHT_MAX
            ))
        else:
            target_fm_w = 1.0
        fm_weight += HYBRID_SMOOTHING * (target_fm_w - fm_weight)
        fm_weight = float(np.clip(fm_weight, FM_WEIGHT_MIN, 1.0))

        # === Audio out ===
        # GATE DURO: silencio absoluto si no hay contacto
        if n_c == 0:
            audio_L *= 0.0
            audio_R *= 0.0

        # v12: el audio lo maneja LatentSonifier (sounddevice)
        # No hay pygame mixer aqui.

        # === Co-adaptación ===
        now = time.perf_counter()
        if args.rehearse and touching:
            if now - last_coadapt_time > COADAPT_INTERVAL:
                if order.size:
                    feats_avg = np.mean([feats_list[i] for i in order], axis=0)
                    sonic_resp = np.clip(base_params - 0.5, -0.5, 0.5)
                    W_c += LR_WC * np.outer(feats_avg, sonic_resp)
                    W_c *= COADAPT_DECAY

                    W_g += LR_WG * np.outer(g, sonic_resp)
                    W_g *= COADAPT_DECAY

                last_coadapt_time = now

        # === Diagnóstico ===
        if args.verbose and (now - last_print > 0.5):
            active = np.where(tactile > 0.5)[0].tolist()
            stats = gng.stats()
            print(f"FRAME {frame:05d} | ZONAS {active} | nC={n_c} | "
                  f"gate={master_gain:.2f} | fm_w={fm_weight:.2f} | "
                  f"gng_nodes={stats['nodes']} | "
                  f"area={features[0]:.2f} cen={features[1]:.2f}")
            for k, ci in enumerate(order):
                print(f"  voz{k}: pos={contacts[ci]['pos']:.1f} "
                      f"w={contacts[ci]['width']} "
                      f"E={energies[ci]:.2f}")
            print()
            last_print = now

        frame += 1
        t_global += AUDIO_CHUNK / SAMPLE_RATE

        elapsed   = time.perf_counter() - loop_start
        remaining = LOOP_DT - elapsed
        if remaining > 0:
            time.sleep(remaining)


except KeyboardInterrupt:
    print()
    print("Stopping TMAQT v6...")

finally:
    if args.rehearse:
        try:
            save_mapping(W_c, W_g, P_c)
        except Exception as e:
            print("WARN save_mapping:", e)
    if not args.no_audio:
        try:
            sonifier.set_gesture(z_wav_state, gate=0.0)
            time.sleep(0.1)
            sonifier.stop()
        except Exception as e:
            print("WARN sonifier stop:", e)
    print("Done.")
