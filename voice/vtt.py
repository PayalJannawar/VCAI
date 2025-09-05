import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

# Step 1: Record audio
def record_audio(filename="input.wav", duration=5, fs=16000):
    print("Recording... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()  # Wait until recording is finished
    write(filename, fs, recording)  # Save as WAV file
    print(f" Recording saved as {filename}")

# Step 2: Transcribe with Whisper
def transcribe_audio(filename="input.wav"):
    print("Transcribing...")
    model = WhisperModel("base")  # You can try "tiny", "small", "medium"
    segments, info = model.transcribe(filename)
    
    text = ""
    for segment in segments:
        text += segment.text + " "
    print(" Transcription:", text.strip())
    return text.strip()

if __name__ == "__main__":
    record_audio("input.wav", duration=5)   # record for 5 seconds
    transcribe_audio("input.wav")
