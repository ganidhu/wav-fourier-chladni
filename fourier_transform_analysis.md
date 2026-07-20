# Fourier Transform Analysis: input_audio.wav

We have successfully performed a Fast Fourier Transform (FFT) on the audio file `input_audio.wav` to analyze its frequency components. 

## Audio Metadata
* **Filename**: `input_audio.wav`
* **Format**: WAV PCM (Mono, 16-bit)
* **Sample Rate**: 44,100 Hz (44.1 kHz)
* **Duration**: 1.01 seconds
* **Total Samples**: 44,544 samples

---

## Dominant Spectral Peaks
Below are the top 5 dominant frequencies found in the audio signal, ordered by their spectral magnitude:

| Rank | Frequency (Hz) | Closest Note / Tone | Spectral Magnitude |
| :--- | :--- | :--- | :--- |
| **1** | **452.4 Hz** | ~A4 (440.0 Hz) / A#4 (466.2 Hz) | 1,018.35 |
| **2** | **43.6 Hz** | Sub-bass region (near F1/F#1) | 455.09 |
| **3** | **227.7 Hz** | ~A3 (220.0 Hz) - exact octave below peak | 427.53 |
| **4** | **340.6 Hz** | ~E4 (329.6 Hz) / F4 (349.2 Hz) | 418.01 |
| **5** | **121.8 Hz** | ~B2 (123.5 Hz) | 407.01 |

### Observations
1. **Octave Relationship**: The peak at **227.7 Hz** is approximately half of the primary frequency (**452.4 Hz**). This represents a strong sub-octave component, which gives the sound a rich, warm, and full timber.
2. **Sub-bass Component**: The frequency of **43.6 Hz** is very low and represents a deep bass frequency, common in high-quality sound designs, synth basses, or voice recordings with significant proximity effect or background rumble.

---

## Interactive Dashboard (shadcn-style)
The analysis dashboard has been fully rewritten using shadcn design guidelines to present a clean, content-first, and highly-functional interface. 

### Visual Features
- **App Shell & Theme Toggle**: Supports a fluid light/dark mode system switching theme tokens. Icons dynamically update using Lucide, and chart backgrounds and grids adjust automatically without reloading.
- **Metrics & Structure**: Spacing is configured on a strict 4px grid (using standard card padding and gutters). Grouped stats cards use clean borders and minimal styling.
- **Copy-to-Clipboard & Toasts**: Hitting the *Copy Report Markdown* button compiles the analysis metadata and copies it instantly, raising a centered, pill-style floating toast notification.

### Chart Interactivities
- **Waveform Plot**: A smooth spline chart displaying normalized amplitude over time (0.00s to 1.01s).
- **FFT Spectrum Plot**: Displays the magnitude of frequency bins from 0 Hz to 12,000 Hz. You can toggle between Linear and Logarithmic spacing to inspect micro-harmonics.

**👉 [Open Interactive Dashboard](fourier_analysis.html)**

---

## Chladni Pattern Simulator (Resonant Geometry)
The frequency signature of this wave has been mapped to physical resonant modes of a square plate to create a unique geometric signature.

- **Vibration Mechanics**: Runs a physics simulation of 15,000 sand particles on a virtual metal plate vibrating at the custom frequency chord.
- **Audio Synthesizer**: Connects your browser's Web Audio API to play the resonant chord corresponding to the FFT data.
- **Design Exporters**: Easily export the resulting nodal patterns as vector SVG files or high-res transparent PNGs for branding and logo design.

**👉 [Open Chladni Plate Simulator](chladni_simulator.html)**

---

## Command Line Interface (CLI) & Terminal User Interface (TUI)
We have added a cross-platform command-line tool `voca-spectral.py` to run analyses and simulations directly from your terminal.

* **ASCII DFT/FFT Plotting**: Generates color-coded frequency bars in your console.
* **ASCII Chladni Simulation**: Simulates sand alignment and draws the square plate geometry inside the terminal using characters (`█` and `░`).
* **Zero Dependencies**: Written purely in Python using only built-in modules (`wave`, `struct`, `math`, `argparse`).

### How to Run:
Run the TUI menu interactively:
```bash
python3 "voca-spectral.py"
```

Or analyze a specific audio file directly in CLI mode:
```bash
python3 "voca-spectral.py" --wav "/path/to/your/audio.wav"
```

**👉 [View CLI Script](voca-spectral.py)**

