set -euo pipefail

echo "MIDI → Sober Bridge Installer"

if command -v pacman &>/dev/null; then
PKG="pacman"
elif command -v apt &>/dev/null; then
PKG="apt"
elif command -v dnf &>/dev/null; then
PKG="dnf"
else
echo "Unsupported distro. Install python3, python3-venv, and libasound2-dev manually."
exit 1
fi

echo "[1/5] Installing system packages..."
case $PKG in
pacman)
sudo pacman -Sy --noconfirm python python-pip python-virtualenv alsa-lib
;;
apt)
sudo apt update
sudo apt install -y python3 python3-pip python3-venv libasound2-dev
;;
dnf)
sudo dnf install -y python3 python3-pip python3-virtualenv alsa-lib-devel
;;
esac

echo "[2/5] Adding user to input group (for /dev/uinput)..."
sudo usermod -aG input "$USER" || true

echo "[3/5] Creating virtual environment..."
INSTALL_DIR="$HOME/.local/share/midi-sober-bridge"
mkdir -p "$INSTALL_DIR"
python3 -m venv "$INSTALL_DIR/venv"

echo "[4/5] Installing Python dependencies..."
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install mido python-rtmidi evdev

echo "[5/5] Installing script..."
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/midi_to_sober.py"
cp "$SCRIPT_PATH" "$INSTALL_DIR/midi_to_sober.py"
chmod +x "$INSTALL_DIR/midi_to_sober.py"

mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/midi-sober" << 'EOF'
#!/usr/bin/env bash
exec "$HOME/.local/share/midi-sober-bridge/venv/bin/python" \
     "$HOME/.local/share/midi-sober-bridge/midi_to_sober.py" "$@"
EOF
chmod +x "$HOME/.local/bin/midi-sober"

echo ""
echo "=== Installation complete ==="
echo ""
echo "IMPORTANT: Log out and log back in (or reboot) so the 'input' group takes effect."
echo ""
echo "Then run:"
echo "  midi-sober"
echo ""
echo "Make sure your MIDI keyboard is connected and Sober is focused on the piano."
