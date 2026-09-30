"""Original 15s electronic track, synthesized from scratch (no samples, no licensing).
120 BPM -> 1 beat = 0.5s, 1 bar = 2s. Drop at 2.0s, end-card impact at 12.0s."""
import numpy as np, wave

SR = 44100
DUR = 15.0
BPM = 120
BEAT = 60 / BPM
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

def place(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= N: return
    j = min(N, i + len(sig))
    buf[i:j] += sig[: j - i] * gain

def both(sig, t, g=1.0, pan=0.0):
    place(L, sig, t, g * (1 - max(0, pan)))
    place(R, sig, t, g * (1 + min(0, pan)))

def env_exp(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))

def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env_exp(n, 0.16)
    s[:200] += rng.standard_normal(200) * np.linspace(0.5, 0, 200)  # click
    return np.tanh(s * 1.8)

def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    s = rng.standard_normal(n)
    s = s - np.convolve(s, np.ones(4) / 4, 'same')  # crude highpass
    return s * env_exp(n, 0.06 if open_ else 0.012) * 0.5

def clap():
    n = int(0.25 * SR)
    s = rng.standard_normal(n)
    s = s - np.convolve(s, np.ones(8) / 8, 'same')
    e = env_exp(n, 0.07)
    for d in (0.0, 0.011, 0.022):  # layered flams
        k = int(d * SR); e[k:k + 300] += np.linspace(0.8, 0, 300)
    return s * e * 0.6

def saw(freq, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in (-detune, 0, detune):
        out += 2 * ((t * freq * (1 + d)) % 1) - 1
    return out / 3

def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * np.asarray(cutoff) / SR)
    y = np.zeros_like(x); prev = 0.0
    a = np.broadcast_to(a, x.shape)
    for i in range(len(x)):
        prev = (1 - a[i]) * x[i] + a[i] * prev
        y[i] = prev
    return y

def note(midi): return 440 * 2 ** ((midi - 69) / 12)

# A minor: Am - F - C - G, one chord per bar
prog = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [60, 64, 67]), (43, [59, 62, 67])]

# --- Intro impact + riser (0-2s)
n = int(1.2 * SR); t = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t / 0.08)) / SR) * env_exp(n, 0.4)
both(np.tanh(boom * 2), 0.0, 0.9)
n = int(2.0 * SR); t = np.arange(n) / SR
noise = rng.standard_normal(n)
riser = lowpass(noise, 300 + 9000 * (t / 2.0) ** 2) * (t / 2.0) ** 1.5
both(riser, 0.0, 0.35)
# pad in the intro (filtered, swelling)
pad = sum(saw(note(m), n, 0.004) for m in prog[0][1]) / 3
both(lowpass(pad, 400 + 2500 * t / 2.0) * np.minimum(1, t / 0.3), 0.0, 0.25)
# 8th-note snare roll accelerating into the drop
for k, tt in enumerate(np.arange(1.0, 2.0, BEAT / 4)):
    both(clap(), tt, 0.15 + 0.35 * k / 8)

# --- Main groove (2-12s) and outro (12-15s)
kick_times = []
for b in range(int(2.0 / BEAT), int(DUR / BEAT)):
    tb = b * BEAT
    outro = tb >= 12.0
    if tb < 14.5:
        both(kick(), tb, 0.95); kick_times.append(tb)
    both(hat(), tb + BEAT / 2, 0.35 if not outro else 0.2, pan=0.3)
    if not outro: both(hat(), tb + BEAT / 4, 0.12, pan=-0.3); both(hat(), tb + 3 * BEAT / 4, 0.12, pan=-0.3)
    if b % 2 == 1 and not outro: both(clap(), tb, 0.55, pan=-0.1)
    if b % 8 == 7 and not outro: both(hat(True), tb + BEAT / 2, 0.3, pan=0.3)

# bass: offbeat pumping 8ths following the progression
for bar in range(1, 8):
    root = prog[(bar - 1) % 4][0]
    for e8 in range(8):
        tt = bar * 2.0 + e8 * BEAT / 2
        if tt >= 14.5: break
        n = int(BEAT / 2 * SR * 0.9)
        f = note(root + (12 if e8 in (3, 7) else 0))
        s = saw(f, n, 0.003)
        s = lowpass(s, 900 * env_exp(n, 0.05) + 150)
        s *= np.minimum(1, np.arange(n) / 200) * np.minimum(1, (n - np.arange(n)) / 400)
        both(np.tanh(s * 2.5), tt, 0.32)

# chord stabs on the off-beats (2-12s), long pad in outro
for bar in range(1, 6):
    notes = prog[(bar - 1) % 4][1]
    for off in (0.75, 1.75, 2.75, 3.75):
        tt = bar * 2.0 + off * BEAT
        n = int(0.18 * SR)
        s = sum(saw(note(m + 12), n, 0.006) for m in notes) / 3
        s = lowpass(s, 2500 * env_exp(n, 0.06) + 400) * env_exp(n, 0.08)
        both(s, tt, 0.28, pan=0.25 * (1 if off in (0.75, 2.75) else -1))

# riser into the end card 11-12s
n = int(1.0 * SR); t = np.arange(n) / SR
both(lowpass(rng.standard_normal(n), 500 + 8000 * t ** 2) * t ** 1.5, 11.0, 0.35)
# end-card impact at 12s + sustaining Am pad
n = int(1.5 * SR); t = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(36 + 70 * np.exp(-t / 0.07)) / SR) * env_exp(n, 0.5)
both(np.tanh(boom * 2), 12.0, 0.9)
n = int(3.0 * SR); t = np.arange(n) / SR
pad = sum(saw(note(m), n, 0.005) for m in prog[0][1] + [69]) / 4
both(lowpass(pad, 1800) * np.minimum(1, t / 0.05) * np.exp(-t / 2.5), 12.0, 0.35)

# sidechain pump: duck everything except kicks around each kick
duck = np.ones(N)
for kt in kick_times:
    i = int(kt * SR); n = int(0.3 * SR); j = min(N, i + n)
    duck[i:j] = np.minimum(duck[i:j], 0.45 + 0.55 * (np.arange(j - i) / n) ** 0.6)
k_only = np.zeros(N)
for kt in kick_times: place(k_only, kick(), kt, 0.95)
L = (L - k_only) * duck + k_only
R = (R - k_only) * duck + k_only

# master: fade out last 0.4s, soft clip, normalize
fade = np.ones(N); fn = int(0.4 * SR); fade[-fn:] = np.linspace(1, 0, fn)
st = np.stack([L, R], 1) * fade[:, None]
st = np.tanh(st * 1.2)
st = st / np.max(np.abs(st)) * 0.89
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok')
