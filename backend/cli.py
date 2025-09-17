import requests
import json

API_URL = "http://127.0.0.1:8000/code-assistant"

def ask_ai(task_type, language, task):
    payload = {
        "task_type": task_type,
        "language": language,
        "task": task
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # raises an error if status != 200
        data = response.json()
        return data.get("response", "No 'response' key in API reply")
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Welcome to Coding AI CLI!")
    while True:
        task_type = input("Enter task type (e.g., generate_code, explain_code): ")
        language = input("Enter language (e.g., Python, C++): ")
        task = input("Enter your task (e.g., reverse a string): ")

        answer = ask_ai(task_type, language, task)
        print(f"\nAI Response:\n{answer}\n")

        cont = input("Do you want to continue? (y/n): ")
        if cont.lower() != "y":
            break
