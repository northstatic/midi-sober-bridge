MIDI → Sober Bridge

Play your USB-MIDI keyboard directly into Roblox Visual Pianos running in Sober on Linux.

```bash
curl -sL https://raw.githubusercontent.com/northstatic/midi-sober-bridge/main/install.sh | bash
```

Or clone and run:

```bash
git clone https://github.com/northstatic/midi-sober-bridge.git
cd midi-sober-bridge
chmod +x install.sh
./install.sh
```

Log out and back in after install (so the `input` group applies), then:

```bash
midi-sober
```

Switch to Sober, click the piano, and play.

Requirements:

- Linux (Arch, Debian/Ubuntu, Fedora)(Must be working on these :>)
- USB-MIDI keyboard
- Sober
- User in `input` group (installer handles it)

Notes:

- Black keys use a Shift workaround. Chords mixing white + black keys may have minor artifacts - this is a limitation of how Visual Pianos handles input.
- Tested with Yamaha pianos and some Pianos experiences (to be exact - Meet People Around The World, Visual Pianos, Universal Piano Hub, Starving Pianists).

Manual run (without install):

```bash
python3 -m venv venv
source venv/bin/activate
pip install mido python-rtmidi evdev
python midi_to_sober.py
```

Thanks for attention
