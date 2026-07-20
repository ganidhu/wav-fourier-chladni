#!/bin/bash
set -e

# Colors for terminal styling
GREEN='\033[32m'
CYAN='\033[36m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'
BOLD='\033[1m'

echo -e "${BOLD}${GREEN}┌────────────────────────────────────────────────────────┐${RESET}"
echo -e "${BOLD}${GREEN}│        WAV → Fourier → Chladni Installer               │${RESET}"
echo -e "${BOLD}${GREEN}└────────────────────────────────────────────────────────┘${RESET}"
echo

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "  ${RED}Error: Python 3 is required but could not be found.${RESET}"
    echo -e "  Please install Python 3 and try again."
    exit 1
fi

# 2. Determine installation method (pipx or system pip)
if command -v pipx &> /dev/null; then
    echo -e "  ${CYAN}Installing via pipx (recommended isolated environment)...${RESET}"
    pipx install wav-fourier-chladni --force
elif command -v pip3 &> /dev/null; then
    echo -e "  ${CYAN}Installing via pip3...${RESET}"
    pip3 install wav-fourier-chladni --break-system-packages
elif command -v pip &> /dev/null; then
    echo -e "  ${CYAN}Installing via pip...${RESET}"
    pip install wav-fourier-chladni --break-system-packages
else
    echo -e "  ${RED}Error: Neither pipx nor pip could be found.${RESET}"
    echo -e "  Please install pip or pipx and try again."
    exit 1
fi

# 3. Verification
echo
if command -v wav-fourier-chladni &> /dev/null; then
    echo -e "  ${BOLD}${GREEN}✓ Installation complete!${RESET}"
    echo -e "  Run the tool from any directory using:"
    echo -e "  ${BOLD}${YELLOW}wav-fourier-chladni${RESET}"
else
    echo -e "  ${YELLOW}Warning: Installation completed but the command was not found in your PATH.${RESET}"
    echo -e "  Make sure Python's global script installation folder is in your PATH."
fi
echo

# 4. Check and install optional audio recording packages
OS_TYPE=$(uname)
HAS_REC=false

if command -v rec &> /dev/null || command -v sox &> /dev/null || command -v arecord &> /dev/null || command -v ffmpeg &> /dev/null; then
    HAS_REC=true
fi

if [ "$HAS_REC" = false ]; then
    echo -e "  ${YELLOW}Note: Optional microphone recording dependencies (sox/ffmpeg) are missing.${RESET}"
    read -p "  Do you want to install them now for live audio recording? (y/N): " choice
    case "$choice" in 
        [yY][eE][sS]|[yY]) 
            echo
            if [ "$OS_TYPE" = "Darwin" ]; then
                if command -v brew &> /dev/null; then
                    echo -e "  ${CYAN}Installing sox via Homebrew...${RESET}"
                    brew install sox
                else
                    echo -e "  ${RED}Error: Homebrew (brew) is not installed. Please install Homebrew or run: brew install sox${RESET}"
                fi
            elif [ "$OS_TYPE" = "Linux" ]; then
                if command -v apt-get &> /dev/null; then
                    echo -e "  ${CYAN}Installing sox and alsa-utils via apt...${RESET}"
                    sudo apt-get update && sudo apt-get install -y sox alsa-utils
                elif command -v yum &> /dev/null; then
                    echo -e "  ${CYAN}Installing sox via yum...${RESET}"
                    sudo yum install -y sox
                else
                    echo -e "  ${YELLOW}Unsupported package manager. Please install 'sox' or 'alsa-utils' manually.${RESET}"
                fi
            else
                echo -e "  ${YELLOW}Unsupported OS. Please install 'sox' or 'ffmpeg' manually.${RESET}"
            fi
            ;;
        *)
            echo -e "  ${CYAN}Skipping audio recording setup. You can still import WAV files!${RESET}"
            ;;
    esac
else
    echo -e "  ${GREEN}✓ Microphone recording dependencies are already installed.${RESET}"
fi
echo
