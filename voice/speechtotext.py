import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import librosa
import noisereduce as nr
import soundfile as sf
from faster_whisper import WhisperModel

# -----------------------------
# Parameters
# -----------------------------
fs = 16000              # Sampling rate
duration = 5            # seconds to record
filename = "question.wav"
clean_filename = "clean.wav"

# -----------------------------
# List available audio devices
# -----------------------------
print("Available audio devices:")
print(sd.query_devices())

# -----------------------------
# Record audio safely
# -----------------------------
try:
    print("\nSpeak your question now...")
    # You can add device=DEVICE_ID if needed
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    write(filename, fs, audio)
    print(f"Recording saved as {filename}")
except Exception as e:
    print("Error recording audio:", e)
    exit()

# -----------------------------
# Noise Reduction
# -----------------------------
try:
    audio_data, sr = librosa.load(filename, sr=fs)
    clean_audio = nr.reduce_noise(y=audio_data, sr=sr)
    sf.write(clean_filename, clean_audio, sr)
    print(f"Noise-reduced file saved as {clean_filename}")
except Exception as e:
    print("Error during noise reduction:", e)
    exit()

# -----------------------------
# Load Whisper Model (GPU, float16 for speed)
# -----------------------------
print("Loading Whisper model (medium, GPU)...")
try:
    model = WhisperModel("medium", device="cuda", compute_type="float16")  # faster and more accurate
    print("Model loaded.")
except Exception as e:
    print("Error loading Whisper model:", e)
    exit()

# -----------------------------
# Transcribe audio
# -----------------------------
print("Transcribing...")
try:
    segments, info = model.transcribe(
        clean_filename,
        beam_size=5,        # improves accuracy
        best_of=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=300)
    )
    text = " ".join([seg.text for seg in segments])
    print("\nDetected Text:\n", text)
except Exception as e:
    print("Error during transcription:", e)
    exit()

# -----------------------------
# Function to get detected text
# -----------------------------
def get_detected_text():
    return text

