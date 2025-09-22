from openai import OpenAI
from faster_whisper import WhisperModel
import requests
import pyttsx3

# ---------------------------
# Rule-based intent parser
# ---------------------------
def rule_based_parser(text):
    text = text.lower()

    if "make" in text or "create function" in text or "write code" in text:
        return {"intent": "create_function", "query": text}

    elif "test" in text or "run pytest" in text or "check" in text:
        return {"intent": "run_tests", "query": text}

    elif "modify" in text or "update" in text or "change" in text:
        return {"intent": "edit_function", "query": text}

    elif "explain" in text or "describe" in text:
        return {"intent": "explain_code", "query": text}

    else:
        return {"intent": "unknown", "query": text}

# ---------------------------
# LLM fallback parser (OpenAI)
# ---------------------------
client = OpenAI(api_key="YOUR_API_KEY")  # replace with your OpenAI key

def llm_fallback_parser(text):
    prompt = f"""
Classify the following request into one intent:
- create_function
- run_tests
- edit_function
- explain_code

Request: "{text}"
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )
    intent = response.choices[0].message.content.strip()
    return {"intent": intent, "query": text}

# ---------------------------
# Main parser
# ---------------------------
def parse_intent(text):
    result = rule_based_parser(text)
    if result["intent"] == "unknown":
        return llm_fallback_parser(text)
    return result

# ---------------------------
# Send intent to backend (real API)
# ---------------------------
def send_to_backend(intent_obj):
    url = "http://127.0.0.1:8000/code-assistant"  # Person A's backend endpoint
    try:
        response = requests.post(url, json=intent_obj)
        return response.json()
    except Exception as e:
        return {"message": f"⚠️ Backend not available: {e}"}

# ---------------------------
# TTS with pyttsx3
# ---------------------------
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # male voice (voices[1] for female)
    
    print("🎧 Speaking response...")
    engine.say(text)
    engine.runAndWait()

# ---------------------------
# ASR with Whisper
# ---------------------------
def main():
    # Load Whisper model
    model = WhisperModel("small")

    # Transcribe audio
    segments, info = model.transcribe("user_input.wav", beam_size=5)
    spoken_text = "".join(segment.text for segment in segments)

    # Parse intent
    parsed = parse_intent(spoken_text)

    print("User said:", spoken_text)
    print("Intent:", parsed)

    # Send to backend
    backend_response = send_to_backend(parsed)
    print("Backend says:", backend_response["message"])

    # Speak back result
    speak_text(backend_response["message"])

# ---------------------------
# Run main
# ---------------------------
if __name__ == "__main__":
    main()
