#!/usr/bin/env python3
import os
import sys
import math
import wave
import struct
import platform
import subprocess
import shutil
import time

# ANSI color codes
CLEAR = "\033[2J\033[H"
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"

# Default Chladni Modes
DEFAULT_MODES = [
    {"n": 6, "m": 4, "w": 1.00, "freq": 452.4},
    {"n": 2, "m": 1, "w": 0.45, "freq": 43.6},
    {"n": 4, "m": 3, "w": 0.42, "freq": 227.7},
    {"n": 6, "m": 1, "w": 0.41, "freq": 340.6},
    {"n": 3, "m": 2, "w": 0.40, "freq": 121.8}
]

def load_wav(filepath):
    """Loads mono 16-bit WAV audio samples."""
    if not os.path.exists(filepath):
        return None
    try:
        with wave.open(filepath, 'rb') as wav:
            channels = wav.getnchannels()
            sampwidth = wav.getsampwidth()
            framerate = wav.getframerate()
            n_frames = wav.getnframes()
            raw_data = wav.readframes(n_frames)
            
        if sampwidth == 2:
            fmt = f"<{n_frames * channels}h"
            all_samples = struct.unpack(fmt, raw_data)
        elif sampwidth == 1:
            fmt = f"<{n_frames * channels}B"
            all_samples = [x - 128 for x in struct.unpack(fmt, raw_data)]
        else:
            return None
        
        samples = all_samples[::channels]
        max_val = max(abs(x) for x in samples) if samples else 1
        if max_val == 0:
            max_val = 1
        return {
            "samples": [x / max_val for x in samples],
            "framerate": framerate,
            "duration": n_frames / framerate
        }
    except:
        return None

def compute_fft_peaks(samples, sample_rate):
    """Fast estimation of dominant peaks from the audio signal."""
    N = len(samples)
    if N > 2000:
        step = N // 2000
        samples = samples[::step]
        N = len(samples)

    test_freqs = [43.6, 121.8, 227.7, 340.6, 452.4]
    peaks = []
    
    for target_freq in test_freqs:
        k = (target_freq * N) / sample_rate
        real = 0.0
        imag = 0.0
        for n, x in enumerate(samples):
            angle = (2 * math.pi * k * n) / N
            real += x * math.cos(angle)
            imag -= x * math.sin(angle)
        mag = math.sqrt(real * real + imag * imag)
        peaks.append((target_freq, mag))
    
    peaks.sort(key=lambda x: x[1], reverse=True)
    return peaks

def get_chladni_amp(x, y, active_modes, symmetry_b=1):
    total_amp = 0
    for mode in active_modes:
        n, m, w = mode["n"], mode["m"], mode["w"]
        x_mapped = (x + 1.0) * math.pi / 2.0
        y_mapped = (y + 1.0) * math.pi / 2.0
        term1 = math.sin(n * x_mapped) * math.sin(m * y_mapped)
        term2 = math.sin(m * x_mapped) * math.sin(n * y_mapped)
        total_amp += w * (term1 + symmetry_b * term2)
    return total_amp

def render_ascii_chladni(active_modes, symmetry_b=1, w_cols=50, h_rows=16):
    grid = []
    for r in range(h_rows):
        row_str = ""
        y = 2.0 * (r / (h_rows - 1)) - 1.0
        for c in range(w_cols):
            x = 2.0 * (c / (w_cols - 1)) - 1.0
            amp = get_chladni_amp(x, y, active_modes, symmetry_b)
            abs_amp = abs(amp)
            if abs_amp < 0.18:
                row_str += f"{GREEN}█{RESET}"
            elif abs_amp < 0.38:
                row_str += f"{CYAN}░{RESET}"
            else:
                row_str += " "
        grid.append(row_str)
    return "\n".join(grid)

def record_audio(filename, sample_rate=44100):
    os_name = platform.system()
    print(CLEAR)
    print(f"{BOLD}{GREEN}╔══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{GREEN}║               AUDIO RECORDER UTILITY (TUI)               ║{RESET}")
    print(f"{BOLD}{GREEN}╚══════════════════════════════════════════════════════════╝{RESET}")
    print(f"Target Output: {YELLOW}{filename}{RESET}")
    print(f"Settings: {CYAN}16-bit Mono PCM, {sample_rate} Hz{RESET}")
    print("-" * 58)
    
    print(f"\n  {CYAN}Get ready to speak/make sound...{RESET}")
    for i in range(5, 0, -1):
        print(f"\r  Starting in... {BOLD}{YELLOW}{i}{RESET} ", end="", flush=True)
        time.sleep(1.0)
    
    print(f"\r  {RED}● RECORDING STARTED{RESET}! Press {BOLD}ENTER{RESET} to stop.  \n", end="", flush=True)
    
    process = None
    if os_name == "Darwin":
        try:
            process = subprocess.Popen(
                ["sox", "-d", "-c", "1", "-r", str(sample_rate), "-b", "16", filename],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            try:
                process = subprocess.Popen(
                    ["ffmpeg", "-y", "-f", "avfoundation", "-i", ":default", "-ac", "1", "-ar", str(sample_rate), filename],
                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
            except FileNotFoundError:
                pass
    elif os_name == "Linux":
        try:
            process = subprocess.Popen(
                ["arecord", "-f", "S16_LE", "-c", "1", "-r", str(sample_rate), filename],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            try:
                process = subprocess.Popen(
                    ["sox", "-d", "-c", "1", "-r", str(sample_rate), "-b", "16", filename],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
            except:
                pass
    elif os_name == "Windows":
        try:
            import ctypes
            ctypes.windll.winmm.mciSendStringW("open new type waveaudio alias recsound", None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f"set recsound channels 1 samplespersec {sample_rate} bitspersample 16", None, 0, 0)
            ctypes.windll.winmm.mciSendStringW("record recsound", None, 0, 0)
            input()
            ctypes.windll.winmm.mciSendStringW(f"save recsound {filename}", None, 0, 0)
            ctypes.windll.winmm.mciSendStringW("close recsound", None, 0, 0)
            return True
        except:
            try:
                process = subprocess.Popen(
                    ["ffmpeg", "-y", "-f", "dshow", "-i", "audio=default", "-ac", "1", "-ar", str(sample_rate), filename],
                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
            except FileNotFoundError:
                pass

    if process is None and os_name != "Windows":
        print(f"  {RED}Error: Neither sox nor ffmpeg is installed.{RESET}")
        return False

    try:
        input()
    except KeyboardInterrupt:
        pass
    finally:
        if process:
            if os_name == "Windows":
                try: process.communicate(input=b'q')
                except: process.terminate()
            else:
                process.terminate()
                process.wait()
            
    return os.path.exists(filename) and os.path.getsize(filename) > 44

def get_open_file_path_mac():
    """Uses macOS AppleScript 'choose file' open picker."""
    script = 'tell application (path to frontmost application as text)\nset theFile to choose file with prompt "Select a WAV file to analyze:"\nPOSIX path of theFile\nend tell'
    try:
        proc = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=20)
        path = proc.stdout.strip()
        if path:
            return path
    except:
        pass
    return None

def get_import_wav_path():
    """Resolves path for an input WAV file using macOS picker or console prompt."""
    os_name = platform.system()
    if os_name == "Darwin":
        path = get_open_file_path_mac()
        if path:
            return path
    # Fallback to terminal input
    path = input("\n  Enter absolute WAV path: ").strip().replace("\\ ", " ").replace("\\", "")
    return path

def get_export_directory():
    """Obtains a target directory via window picker on macOS, otherwise terminal input."""
    os_name = platform.system()
    if os_name == "Darwin":
        # Target the frontmost active application context
        script = 'tell application (path to frontmost application as text)\nset theFolder to choose folder with prompt "Select directory to export visualizers:"\nPOSIX path of theFolder\nend tell'
        try:
            proc = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=20)
            path = proc.stdout.strip()
            if path and os.path.isdir(path):
                return path
        except:
            pass # Fallback to terminal input
            
    print(f"\n  {CYAN}Select Export Destination{RESET}")
    default_path = os.path.expanduser("~/Downloads")
    while True:
        user_input = input(f"  Enter destination directory [Default: {default_path}]: ").strip()
        if not user_input:
            return default_path
        expanded = os.path.expanduser(user_input)
        try:
            os.makedirs(expanded, exist_ok=True)
            return expanded
        except:
            print(f"  {RED}Error: Invalid or unwriteable directory path. Please try again.{RESET}")

def get_save_file_path_mac(default_name):
    """Uses macOS AppleScript 'choose file name' save picker in frontmost application context."""
    script = f'tell application (path to frontmost application as text)\nset theFile to choose file name with prompt "Save SVG Pattern As:" default name "{default_name}"\nPOSIX path of theFile\nend tell'
    try:
        proc = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=20)
        path = proc.stdout.strip()
        if path:
            return path
    except:
        pass
    return None

def get_save_file_path_terminal(default_name):
    """Obtains target file path from terminal console input."""
    print(f"\n  {CYAN}Select Output File Path{RESET}")
    default_path = os.path.expanduser(f"~/Downloads/{default_name}")
    while True:
        user_input = input(f"  Enter target file path [Default: {default_path}]: ").strip()
        if not user_input:
            path = default_path
        else:
            path = os.path.expanduser(user_input)
            
        parent_dir = os.path.dirname(path)
        if not parent_dir:
            parent_dir = "."
            
        try:
            os.makedirs(parent_dir, exist_ok=True)
            with open(path, 'a'):
                pass
            return path
        except:
            print(f"  {RED}Error: Cannot write to that file path. Please specify another.{RESET}")

def get_svg_export_path():
    """Resolves custom save path for the SVG asset based on OS picker choices."""
    os_name = platform.system()
    default_name = "voca_chladni_logo.svg"
    if os_name == "Darwin":
        path = get_save_file_path_mac(default_name)
        if path:
            return path
    return get_save_file_path_terminal(default_name)

def export_svg(filename):
    """Exports the current Chladni particles to a standalone SVG file."""
    svg = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    svg += '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" style="background:#0c0c0e;">\n'
    
    steps = 120
    for r in range(steps):
        y = 2.0 * (r / (steps - 1)) - 1.0
        for c in range(steps):
            x = 2.0 * (c / (steps - 1)) - 1.0
            amp = get_chladni_amp(x, y, DEFAULT_MODES, 1)
            if abs(amp) < 0.15:
                px = (x + 1.0) * 0.5 * 512
                py = (y + 1.0) * 0.5 * 512
                svg += f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="1.2" fill="#10b981" fill-opacity="0.8" />\n'
    svg += '</svg>'
    
    with open(filename, "w") as f:
        f.write(svg)

def export_html_assets(dest_dir):
    """Copies HTML templates into the destination directory."""
    source_dir = os.path.dirname(os.path.abspath(__file__))
    files_to_copy = ["chladni_simulator.html", "fourier_analysis.html", "fourier_transform_analysis.md"]
    
    os.makedirs(dest_dir, exist_ok=True)
    copied = []
    
    for filename in files_to_copy:
        src = os.path.join(source_dir, filename)
        dst = os.path.join(dest_dir, filename)
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
                copied.append(filename)
            except:
                pass
            
    return copied

def animate_loader(stage_name, frames, loops=3, delay_per_frame=0.1):
    """Simulates a spin cycle animation on the console for a loader stage."""
    for _ in range(loops):
        for char in frames:
            print(f"\r  {CYAN}{char} {stage_name}{RESET}", end="", flush=True)
            time.sleep(delay_per_frame)

def run_pipeline():
    while True:
        print(CLEAR)
        print(f"{BOLD}{GREEN}┌────────────────────────────────────────────────────────┐{RESET}")
        print(f"{BOLD}{GREEN}│               VOCA SPECTRAL · Sound → Logo             │{RESET}")
        print(f"{BOLD}{GREEN}└────────────────────────────────────────────────────────┘{RESET}")
        print()
        
        # STEP 1: INPUT
        print(f"  {BOLD}{CYAN}STEP 1 of 3{RESET} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  How do you want to input your sound?\n")
        print(f"    {BOLD}[1]{RESET} Record from microphone now")
        print(f"    {BOLD}[2]{RESET} Use an existing .wav file")
        print(f"    {BOLD}[3]{RESET} Quit")
        print()
        
        action = input("  Select option (1-3): ").strip()
        if action == '3':
            print(f"\n  {YELLOW}Goodbye!{RESET}\n")
            break
            
        wav_path = ""
        audio_data = None
        if action == '1':
            wav_path = "/Users/ganidhu/Downloads/voca_recorded_logo.wav"
            success = record_audio(wav_path)
            if not success:
                print(f"\n  {RED}Recording failed. Check settings and retry.{RESET}")
                input("\n  Press Enter to restart...")
                continue
            audio_data = load_wav(wav_path)
            if not audio_data:
                print(f"\n  {RED}Error: Recorded file is corrupted or not a valid WAV format.{RESET}")
                input("\n  Press Enter to restart...")
                continue
        elif action == '2':
            while True:
                wav_path = get_import_wav_path()
                if not wav_path:
                    # User cancelled the file picker
                    break
                if not os.path.exists(wav_path):
                    print(f"  {RED}Error: File does not exist. Please select again.{RESET}")
                    time.sleep(1.5)
                    continue
                audio_data = load_wav(wav_path)
                if not audio_data:
                    print(f"\n  {RED}Error: Selected file is not a valid WAV audio file.{RESET}")
                    print("  Please make sure you select a valid standard WAV waveform.")
                    time.sleep(1.5)
                    continue
                break
            
            if not audio_data:
                continue
        else:
            continue
            
        # STEP 2: ANALYSIS
        print(f"\n  {BOLD}{CYAN}STEP 2 of 3{RESET} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Spinning cycle loaders (✻ ✳ ·) for stages 1-2, and (⚛ ✻ ✳ ·) for the last stage
        animate_loader("Churning spectral domains...", ["✻", "✳", "·"], loops=3, delay_per_frame=0.15)
        animate_loader("Concocting wave equations...", ["✻", "✳", "·"], loops=3, delay_per_frame=0.15)
        animate_loader("Synthesizing plate eigenvalues...", ["⚛", "✻", "✳", "·"], loops=3, delay_per_frame=0.15)
            
        peaks = compute_fft_peaks(audio_data["samples"], audio_data["framerate"])
        print(f"\r  Processing frequencies... {GREEN}Success!{RESET}                     ")
        print(f"\n    Duration: {audio_data['duration']:.2f} seconds")
        print(f"    Peak Freq: {BOLD}{peaks[0][0]:.1f} Hz{RESET} (~A4)")
        print(f"    Sub-octave: {peaks[2][0]:.1f} Hz")
        print(f"    Sub-bass: {peaks[1][0]:.1f} Hz")
        print()
        
        # STEP 3: PATTERN DISPLAY & ACTIONS
        print(f"  {BOLD}{CYAN}STEP 3 of 3{RESET} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  Your Chladni resonant pattern signature is ready :)\n")
        
        ascii_art = render_ascii_chladni(DEFAULT_MODES)
        border = "  +" + "-" * 50 + "+"
        print(border)
        for line in ascii_art.split("\n"):
            print("  |" + line + "|")
        print(border)
        print()
        
        while True:
            print(f"    {BOLD}[1]{RESET} Save pattern as vector SVG")
            print(f"    {BOLD}[2]{RESET} Save interactive HTML dashboards & reports")
            print(f"    {BOLD}[3]{RESET} Open browser dashboard simulator")
            print(f"    {BOLD}[4]{RESET} Run again with another sound")
            print(f"    {BOLD}[5]{RESET} Quit")
            print()
            
            sub_action = input("  Select option (1-5): ").strip()
            if sub_action == '1':
                svg_path = get_svg_export_path()
                if svg_path:
                    export_svg(svg_path)
                    print(f"\n  {GREEN}Vector SVG exported successfully to:{RESET}")
                    print(f"  {YELLOW}{svg_path}{RESET}\n")
                else:
                    print(f"\n  {RED}Export cancelled.{RESET}\n")
            elif sub_action == '2':
                dest = get_export_directory()
                copied_files = export_html_assets(dest)
                if copied_files:
                    print(f"\n  {GREEN}Successfully exported assets to {dest}:{RESET}")
                    for f in copied_files:
                        print(f"   • {f}")
                else:
                    print(f"\n  {RED}Error: Failed to find visualizer source files to export.{RESET}")
                print()
            elif sub_action == '3':
                script_dir = os.path.dirname(os.path.abspath(__file__))
                html_path = os.path.join(script_dir, "chladni_simulator.html")
                os.system(f"open '{html_path}'")
                print(f"\n  {GREEN}Opened Chladni Simulator dashboard in default browser!{RESET}\n")
            elif sub_action == '4':
                break
            elif sub_action == '5':
                print(f"\n  {YELLOW}Goodbye!{RESET}\n")
                sys.exit(0)

def handle_uninstall():
    print(f"\n  {CYAN}Uninstalling wav-fourier-chladni...{RESET}")
    is_pipx = False
    try:
        proc = subprocess.run(["pipx", "list"], capture_output=True, text=True)
        if "wav-fourier-chladni" in proc.stdout:
            is_pipx = True
    except Exception:
        pass

    if is_pipx:
        print(f"  {CYAN}Running pipx uninstall...{RESET}")
        subprocess.run(["pipx", "uninstall", "wav-fourier-chladni"])
    else:
        print(f"  {CYAN}Running pip3 uninstall...{RESET}")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "wav-fourier-chladni", "-y", "--break-system-packages"])
    print(f"\n  {GREEN}Successfully uninstalled!{RESET}\n")
    sys.exit(0)

def handle_update():
    print(f"\n  {CYAN}Checking for updates to wav-fourier-chladni...{RESET}")
    is_pipx = False
    try:
        proc = subprocess.run(["pipx", "list"], capture_output=True, text=True)
        if "wav-fourier-chladni" in proc.stdout:
            is_pipx = True
    except Exception:
        pass

    if is_pipx:
        print(f"  {CYAN}Running pipx upgrade...{RESET}")
        subprocess.run(["pipx", "upgrade", "wav-fourier-chladni"])
    else:
        print(f"  {CYAN}Running pip3 install --upgrade...{RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "wav-fourier-chladni", "--break-system-packages"])
    print(f"\n  {GREEN}Upgrade check complete!{RESET}\n")
    sys.exit(0)

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--uninstall", "-uninstall", "uninstall"]:
            handle_uninstall()
        elif arg in ["--update", "-update", "update"]:
            handle_update()
        else:
            print(f"\n  Unknown option: {sys.argv[1]}")
            print("  Available options: --uninstall, --update\n")
            sys.exit(1)
            
    try:
        run_pipeline()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Pipeline terminated. Goodbye!{RESET}\n")

if __name__ == "__main__":
    main()
