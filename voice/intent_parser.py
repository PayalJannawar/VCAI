from faster_whisper import WhisperModel
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import requests

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
# Local LLM for fallback
# ---------------------------
class LocalLLM:
    def __init__(self, model_name=None):
        if model_name is None:
            model_name = "distilgpt2"  # lightweight model
        print(f"Loading local model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)
        self.model = self.model.to('cpu')
        print("Local model loaded!")

    def generate(self, prompt, max_tokens=200):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text.strip()

# Initialize local LLM
local_llm = LocalLLM()

# ---------------------------
# Main parser
# ---------------------------
def parse_intent(text):
    result = rule_based_parser(text)
    if result["intent"] == "unknown":
        # Use local LLM to generate a possible intent
        llm_response = local_llm.generate(f"Classify this request into one intent (create_function, run_tests, edit_function, explain_code): {text}")
        # Simple parsing: take first intent keyword found
        for intent in ["create_function", "run_tests", "edit_function", "explain_code"]:
            if intent in llm_response.lower():
                return {"intent": intent, "query": text}
        # If nothing matches, default
        return {"intent": "unknown", "query": text}
    return result

# ---------------------------
# Send intent to backend (optional)
# ---------------------------
def send_to_backend(intent_obj):
    url = "http://127.0.0.1:8000/code-assistant"
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
    engine.setProperty('voice', voices[0].id)
    print("🎧 Speaking response...")
    engine.say(text)
    engine.runAndWait()

# ---------------------------
# ASR with Whisper
# ---------------------------
def main():
    model = WhisperModel("small")
    segments, info = model.transcribe("user_input.wav", beam_size=5)
    spoken_text = "".join(segment.text for segment in segments)

    parsed = parse_intent(spoken_text)
    print("User said:", spoken_text)
    print("Intent:", parsed)

    backend_response = send_to_backend(parsed)
    print("Backend says:", backend_response["message"])

    speak_text(backend_response["message"])

# ---------------------------
# Run main
# ---------------------------
if __name__ == "__main__":
    main()
