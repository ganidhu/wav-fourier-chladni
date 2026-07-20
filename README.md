# WAV → Fourier → Chladni Pattern

An interactive tool to analyze WAV audio files, perform discrete Fourier analysis to extract dominant peak frequencies, and map those peaks to physical resonant modes on a square Chladni vibrating plate.

This repository is a fork of [Fourier-from-WAV-file](https://github.com/KyleSmith19091/Fourier-from-WAV-file), extended to support interactive TUI workflows, macOS native file dialogs, SVG design exports, and WebGL-powered interactive HTML dashboards.

For the mathematical background of plate vibration models, see [this paper on Chladni Plates](https://ddonle.com/docs/Chladni_Plate.pdf).

## Project Structure

* [voca-spectral.py](voca-spectral.py) — The main interactive Python pipeline script (3-step TUI: input selection, Fourier peak analysis, and visualizer exporting).
* [fourier_analysis.html](fourier_analysis.html) — Dynamic HTML report template displaying audio waveform and FFT spectrum charts (Chart.js).
* [chladni_simulator.html](chladni_simulator.html) — Interactive 2D vibrating plate simulator displaying nodal sand patterns corresponding to the wave equation.
* [fourier_transform_analysis.md](fourier_transform_analysis.md) — Document summarizing Fourier transform calculations and eigenvalue mapping.

## Features

* **WAV Audio Analysis** — Parse 16-bit PCM mono WAV waveforms and compute dominant peak frequencies using discrete Fourier analysis.
* **Mac-Native UI Dialogs** — Native macOS file picker window dialogs (`osascript`) for importing audio and selecting export folders, with terminal fallback prompts for Windows/Linux.
* **Immediate Validation** — Immediate WAV format parsing and corruption checks during step 1 before starting computation.
* **Vector SVG Exports** — Generate resolution-independent SVG designs of the resulting nodal sand patterns for graphic/branding usage.
* **Portable Web Visualizers** — Export standalone HTML dashboards to inspect audio waveforms, FFT spectra, and simulated 2D plate nodal lines.
* **Zero External Python Dependencies** — Built entirely on the standard Python library (no numpy/scipy/matplotlib required to run the core script).

## Advanced Wave Mechanics

This project models Chladni sand patterns using Cartesian standing wave solutions of the multi-dimensional wave equation.

### The Cartesian Wave Equation
For a square vibrating plate $\Omega = \{(x,y) \in \mathbb{R}^2 \mid -L \le x, y \le L\}$, the displacement $u(x, y, t)$ is modeled by:

$$u_{tt} = c^2\nabla^2u = c^2\left(\frac{\partial^2u}{\partial x^2} + \frac{\partial^2u}{\partial y^2}\right)$$

Assuming clamped boundary conditions at the edges, the standing wave solutions (eigenmodes) can be approximated by:

$$u(x, y, t) = \sum_{n=1}^{\infty}\sum_{m=1}^{\infty} w_{nm} \cdot \left(\sin\left(\frac{n\pi x}{L}\right)\sin\left(\frac{m\pi y}{L}\right) + \beta\sin\left(\frac{m\pi x}{L}\right)\sin\left(\frac{n\pi y}{L}\right)\right)\cos(\omega_{nm} t)$$

Where:
* $n, m$ are the integer mode parameters (eigenvalues).
* $w_{nm}$ is the weight of each mode, mapped directly from the dominant audio frequency amplitudes computed via Fourier analysis.
* $\beta$ is the symmetry factor (typically $\pm 1$ for square plates).
* The sand particles accumulate at the **nodal lines** where the plate displacement is zero, i.e., $u(x,y,t) \approx 0$.

---

## Installation & Running

### Prerequisites
To run the core analysis, you only need **Python 3**.

If you wish to use the microphone recording feature:
* **macOS**: `brew install sox` or ensure `ffmpeg` is installed.
* **Linux**: `sudo apt install alsa-utils` (for `arecord`) or `sox`.

### Usage
Start the interactive terminal program:

```bash
python3 voca-spectral.py
```

The script will guide you through:
1. **Audio Selection**: Pick a WAV file using a native macOS window picker or record live from the microphone.
2. **Analysis**: Performs the discrete Fourier calculations.
3. **Resonant Signatures**: Renders an ASCII art preview of the pattern in the terminal, and lets you choose to export SVG files or HTML dashboards.
