#!/usr/bin/env python3
import mido
from evdev import UInput, ecodes as e
import time
import sys

WHITE = [
    e.KEY_1, e.KEY_2, e.KEY_3, e.KEY_4, e.KEY_5, e.KEY_6, e.KEY_7,
    e.KEY_8, e.KEY_9, e.KEY_0, e.KEY_Q, e.KEY_W, e.KEY_E, e.KEY_R,
    e.KEY_T, e.KEY_Y, e.KEY_U,
    e.KEY_I, e.KEY_O, e.KEY_P, e.KEY_A, e.KEY_S, e.KEY_D, e.KEY_F,
    e.KEY_G, e.KEY_H, e.KEY_J, e.KEY_K, e.KEY_L, e.KEY_Z, e.KEY_X,
    e.KEY_C, e.KEY_V, e.KEY_B, e.KEY_N, e.KEY_M,
]

WHITE_NOTES = [
    36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59,
    60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83,
    84, 86, 88, 89, 91, 93, 95,
]

NOTE_MAP = dict(zip(WHITE_NOTES, WHITE[:len(WHITE_NOTES)]))

BLACK_MAP = {
    37: e.KEY_1, 39: e.KEY_2,
    42: e.KEY_4, 44: e.KEY_5, 46: e.KEY_6,
    49: e.KEY_8, 51: e.KEY_9,
    54: e.KEY_Q, 56: e.KEY_W, 58: e.KEY_E,
    61: e.KEY_T, 63: e.KEY_Y,
    66: e.KEY_I, 68: e.KEY_O, 70: e.KEY_P,
    73: e.KEY_S, 75: e.KEY_D,
    78: e.KEY_G, 80: e.KEY_H, 82: e.KEY_J,
    85: e.KEY_L, 87: e.KEY_Z,
    90: e.KEY_C, 92: e.KEY_V, 94: e.KEY_B,
}

def create_uinput():
    keys = list(set(NOTE_MAP.values()) | set(BLACK_MAP.values())) + [e.KEY_LEFTSHIFT]
    return UInput({e.EV_KEY: keys}, name="midi-piano-bridge")

def main():
    print("MIDI → Sober bridge")
    print("Looking for MIDI piano input...")

    names = mido.get_input_names()
    if not names:
        print("No MIDI inputs found. Connect your piano and try again.")
        sys.exit(1)

    port_name = names[0]
    print(f"Using: {port_name}")
    print("Switch to Sober, use the piano, and play.\n")
    print("Ctrl+C to exit.\n")

    ui = create_uinput()
    pressed = {}

    def on_note_on(note, velocity):
        if velocity == 0:
            on_note_off(note)
            return
        shift = False
        if note in NOTE_MAP:
            key = NOTE_MAP[note]
        elif note in BLACK_MAP:
            key = BLACK_MAP[note]
            shift = True
        else:
            return
        if note in pressed:
            return

        released = []
        if shift:
            for n, k in list(pressed.items()):
                if n in NOTE_MAP:
                    ui.write(e.EV_KEY, k, 0)
                    released.append((n, k))
            if released:
                ui.syn()
                time.sleep(0.008)

        if shift:
            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
            ui.syn()
            time.sleep(0.01)
        ui.write(e.EV_KEY, key, 1)
        ui.syn()
        if shift:
            time.sleep(0.01)
            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
            ui.syn()

        for n, k in released:
            ui.write(e.EV_KEY, k, 1)
        if released:
            ui.syn()

        pressed[note] = key

    def on_note_off(note):
        if note not in pressed:
            return
        key = pressed.pop(note)
        ui.write(e.EV_KEY, key, 0)
        ui.syn()

    try:
        with mido.open_input(port_name) as port:
            for msg in port:
                if msg.type == "note_on":
                    on_note_on(msg.note, msg.velocity)
                elif msg.type == "note_off":
                    on_note_off(msg.note)
    except KeyboardInterrupt:
        print("\nExiting...")
        for note in list(pressed):
            on_note_off(note)
    finally:
        ui.close()

if __name__ == "__main__":
    main()
