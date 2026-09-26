# Voice Profile — NOT YET CALIBRATED

This file is a legacy location. The calibrated profile now lives outside the
skill package, at `~/workspace/writing-quality/voice-profile.md`, so that
updating the skill never overwrites it.

Run `python3 bin/voice_state.py status` to find the active profile. If an older
install left a calibrated profile here, `python3 bin/voice_state.py migrate`
copies it to the state path and leaves this file untouched.

Do not write new profiles here.
