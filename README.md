# WAV → Fourier → Chladni Pattern

> An interactive tool to analyze WAV audio files, perform discrete Fourier analysis to extract dominant peak frequencies, and map those peaks to physical resonant modes on a square Chladni vibrating plate.

```bash
curl -fsSL https://raw.githubusercontent.com/ganidhu/wav-fourier-chladni/master/install.sh | bash
```

For the mathematical background of plate vibration models, see [this paper](https://ddonle.com/docs/Chladni_Plate.pdf) on Chladni Plates.

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

Since the core pipeline runs entirely on the Python standard library, there are **no third-party Python libraries** to install.

### 1. One-Line Installer (macOS & Linux)
You can install and verify the tool globally in one line using `curl`:
```bash
curl -fsSL https://raw.githubusercontent.com/ganidhu/wav-fourier-chladni/master/install.sh | bash
```

### 2. Manual Global Installation
You can also install the tool manually from PyPI using one of the following methods:

#### Option A: Standard pip
```bash
pip install wav-fourier-chladni --break-system-packages
```
*(Note: The `--break-system-packages` flag is required on macOS Homebrew Python installations to allow global CLI scripts).*

#### Option B: Using pipx (Recommended for macOS/Linux)
`pipx` automatically manages isolated virtual environments for CLI tools:
```bash
# Install pipx (if not already installed)
brew install pipx

# Install the package
pipx install wav-fourier-chladni
```

Once installed via either option, launch the program globally from any directory:
```bash
wav-fourier-chladni
```

### 2. Alternative: Run the source script directly
If you do not want to install it globally, you can clone the repository and run the script directly:
```bash
python3 wav_fourier_chladni/cli.py
```

### 3. Prerequisites (Optional)
To run the core analysis and visualizers, you only need **Python 3** installed.

* **macOS**: `brew install sox` or ensure `ffmpeg` is in your system path.
* **Linux**: `sudo apt install alsa-utils` (for `arecord`) or `sox`.

### 4. Uninstallation
To remove the package from your system:

* If installed via **pipx**:
  ```bash
  pipx uninstall wav-fourier-chladni
  ```
* If installed via **pip**:
  ```bash
  pip3 uninstall wav-fourier-chladni --break-system-packages
  ```

---

The script will guide you through:
1. **Audio Selection**: Pick a WAV file using a native macOS window picker or record live from the microphone.
2. **Analysis**: Performs the discrete Fourier calculations.
3. **Resonant Signatures**: Renders an ASCII art preview of the pattern in the terminal, and lets you choose to export SVG files or HTML dashboards.


## 🤝 Contributing

Got ideas? Found a bug?

PRs and issues are very welcome! This is a community tool and it gets better when more people chip in. Even small improvements — better selectors, new step actions, docs fixes — make a real difference.

[Open an issue](https://github.com/ganidhu/wav-fourier-chladni/issues) or just submit a PR. Let's build it together. 🙌

---

## 📄 License

MIT

---

<p align="center">
  <sub>Built by Ganidhu and Baymax</sub>
</p>
