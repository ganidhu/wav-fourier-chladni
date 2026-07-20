# ⚛️ wav-fourier-chladni

> Generate Chladni plate resonant pattern signatures from WAV audio waveforms using Fourier peak frequency estimation.

Built for **Voca** to capture the visual aesthetic of sound. 😉

This tool parses standard mono PCM WAV files, computes dominant resonant peaks via Fourier analysis, and projects them into physical Chladni plate math patterns. The resulting resonance signatures can be rendered as terminal ASCII art, exported as vector SVGs, or saved as interactive HTML visualizer dashboards.

---

## ✨ Features

- **Direct WAV Analysis** — Extracts frequency peaks using discrete Fourier estimation across target resonant ranges.
- **Mac-Native UI Pickers** — Uses native macOS dialog windows for file imports and exports, falling back to safe console prompts on Linux & Windows.
- **WAV Validation Safety** — Immediately checks file integrity and WAV headers upon import to catch incorrect files before animating the pipeline.
- **Vector SVG Export** — Generates clean, resolution-independent SVG designs based on plate plate-eigenvalue equations.
- **Interactive HTML Dashboards** — Exports portable WebGL-powered visualizers and Fourier analytics documents.
- **Zero-Dependency Core** — Built purely on the Python standard library.

---

## 📐 Mathematical Background

This project simulates Chladni patterns using square wave resonance models derived from the multi-dimensional wave equation.

### The Wave Equation on Cartesian Coordinates
For a vibrating plate $\Omega = \{(x,y) \in \mathbb{R}^2 \mid -L \le x, y \le L\}$, the displacement $u(x, y, t)$ is modeled by:

$$u_{tt} = c^2\nabla^2u = c^2\left(\frac{\partial^2u}{\partial x^2} + \frac{\partial^2u}{\partial y^2}\right)$$

Assuming clamped boundary conditions at the edges, the standing wave solutions (eigenmodes) can be approximated by combinations of sinusoidal functions:

$$u(x, y, t) = \sum_{n=1}^{\infty}\sum_{m=1}^{\infty} w_{nm} \cdot \left(\sin\left(\frac{n\pi x}{L}\right)\sin\left(\frac{m\pi y}{L}\right) + \beta\sin\left(\frac{m\pi x}{L}\right)\sin\left(\frac{n\pi y}{L}\right)\right)\cos(\omega_{nm} t)$$

Where:
- $n, m$ are the integer mode parameters (eigenvalues/eigenmodes).
- $w_{nm}$ is the weight/amplitude of each mode (extracted from the audio peaks).
- $\beta$ is the symmetry factor ($\pm 1$ for square plates).
- The sand particles accumulate at the **nodal lines** where the displacement is zero, i.e., $u(x,y,t) \approx 0$.

For a deeper dive into the physics of plate resonance, check out [this paper on Chladni Plates](https://ddonle.com/docs/Chladni_Plate.pdf).

---

## 🚀 Prerequisites

To run the core analysis and file workflows, all you need is **Python 3**.

If you wish to use the **live microphone recording** feature:
- **macOS**: `brew install sox` or ensure `ffmpeg` is in your system path.
- **Linux**: `sudo apt install alsa-utils` (for `arecord`) or `sox`.

---

## 🕹 Usage

Launch the pipeline tool:

```bash
python3 voca-spectral.py
```

The interactive TUI walks you through 3 simple steps:

1. **Input Sound** — Record live from your mic or select an existing `.wav` file using a macOS window dialog.
2. **Fourier Analysis** — Computes spectral resonance loops.
3. **Resonant Signatures** — Displays a terminal preview, exports SVGs, generates WebGL HTML dashboards, or runs a local browser simulator.
