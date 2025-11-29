# integrate.py

from speechtotext import get_detected_text  # Your STT function
import requests

# -----------------------------
# Send text to backend
# -----------------------------
def send_text_to_backend(user_text: str, intent="generate_code", language="Python"):
    """
    Sends the detected text to your FastAPI backend.
    """
    API_URL = "http://127.0.0.1:8000/code-assistant"
    payload = {
        "intent": intent,
        "language": language,
        "task": user_text
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("response", "No response from backend")
        else:
            return f"Backend returned error {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"Backend not available: {e}"

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    # Step 1: Get detected text from speech
    detected_text = get_detected_text()
    print("Detected Text:\n", detected_text)

    # Step 2: Send text to backend and get response
    backend_response = send_text_to_backend(detected_text)
    print("\nBackend Output:\n", backend_response)
