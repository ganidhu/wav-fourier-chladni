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
