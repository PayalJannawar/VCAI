import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

# Parameters
fs = 16000           # Sampling frequency
threshold = 500      # Silence threshold (adjust as needed)
chunk_duration = 1   # Record in 1-second chunks

def record_until_silence(filename="input.wav"):
    print("Recording... Speak now! (Recording will stop when you stop talking)")
    recording = []
    
    while True:
        chunk = sd.rec(int(chunk_duration * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()
        recording.append(chunk)
        
        # Check if chunk is mostly silence
        if np.max(np.abs(chunk)) < threshold:
            print("Silence detected. Stopping recording.")
            break

    recording = np.concatenate(recording, axis=0)
    write(filename, fs, recording)
    print(f"Recording saved as {filename}")

def transcribe_audio(filename="input.wav"):
    print("Transcribing...")
    model = WhisperModel("base")  # tiny, small, medium also possible
    segments, info = model.transcribe(filename)
    
    text = ""
    for segment in segments:
        text += segment.text + " "
    print("Transcription:", text.strip())
    return text.strip()

if __name__ == "__main__":
    record_until_silence("input.wav")
    transcribe_audio("input.wav")
