import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

fs = 16000                 # sample rate
duration = 5               # seconds to record
filename = "question.wav"  # saved file name

# -----------------------------
# Record audio
# -----------------------------
print("🎙 Speak now...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
sd.wait()
write(filename, fs, audio)
print("✔ Recording saved as", filename)

# -----------------------------
# Load Whisper Model
# -----------------------------
model = WhisperModel("small")   # small = faster
print("✔ Model loaded")

# -----------------------------
# Transcribe
# -----------------------------
segments, info = model.transcribe(filename)
text = " ".join([seg.text for seg in segments])

print("\n📝 Detected Text:")
print(text)

# -----------------------------
# Function to return detected text
# -----------------------------
def get_detected_text():
    return text
