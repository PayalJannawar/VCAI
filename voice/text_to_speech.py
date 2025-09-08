# tts_coqui.py
from TTS.api import TTS
import simpleaudio as sa

def speak_text(text, filename="output_coqui.wav"):
    """
    Offline TTS using Coqui TTS.
    """
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
    tts.tts_to_file(text=text, file_path=filename)
    print(f"✅ Speech saved as {filename}")

    # Play immediately
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()

if __name__ == "__main__":
    user_text = input("📝 Enter text to convert into speech (Coqui XTTS): ")
    speak_text(user_text)
