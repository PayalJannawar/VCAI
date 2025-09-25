import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import numpy as np

# -----------------------------
# Parameters
# -----------------------------
fs = 16000          # Sampling rate
duration = 5        # seconds to record (adjust as needed)
filename = "question.wav"

# -----------------------------
# Record audio
# -----------------------------
print("🎤 Speak your question now...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
sd.wait()
write(filename, fs, audio)
print(f"💾 Recording saved as {filename}")

# -----------------------------
# Transcribe audio
# -----------------------------
model = WhisperModel("small")  # or "medium" for better accuracy
segments, info = model.transcribe(filename)
text = " ".join([seg.text for seg in segments])
print("📝 Detected Text:\n", text)
