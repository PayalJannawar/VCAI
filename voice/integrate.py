# integrate.py

from speechtotext import get_detected_text  # Get voice as text
from intent_recognizer import predict_intent  # Predict user intent
import requests

# -----------------------------
# Send request to backend LLM
# -----------------------------
def send_to_backend(task_type, language, task):
    """
    Sends a structured command to the backend AI.
    task_type: Intent detected (e.g., create_function, run_code)
    language: Programming language (default: Python)
    task: Original user command
    """
    API_URL = "http://127.0.0.1:8000/code-assistant"
    payload = {"task_type": task_type, "language": language, "task": task}
    try:
        resp = requests.post(API_URL, json=payload, timeout=5)
        return resp.json().get("response", "No response from backend")
    except Exception as e:
        return f" Backend not available: {e}"

# -----------------------------
# Process user text
# -----------------------------
def process_text(user_text):
    """
    Process the detected text:
    1. Predict the intent
    2. Send structured command to backend
    """
    print(f" User Text: {user_text}")

    # Step 1: Predict intent
    parsed_intent = predict_intent(user_text)
    print(f" Parsed Intent: {parsed_intent}")

    # Step 2: Send structured intent to backend
    return send_to_backend(
        task_type=parsed_intent["intent"],  # e.g., create_function, run_code
        language="Python",                 # default language
        task=user_text                      # original user command
    )

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    # Step 1: Get detected text from speech
    detected_text = get_detected_text()
    print(" Detected Text:\n", detected_text)

    # Step 2: Process text (predict intent + send to backend)
    output = process_text(detected_text)
    print("\n Backend Output:\n", output)

