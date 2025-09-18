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
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No 'response' key in API reply")
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("🤖 Welcome to Coding AI CLI (Week 3 Version) 🤖")
    while True:
        print("\nChoose a task type:")
        print("1. Generate Code")
        print("2. Explain Code")
        print("3. Debug Code")
        print("4. Quit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "4":
            print("Goodbye! 👋")
            break

        # Map user choice to task_type
        task_types = {
            "1": "generate_code",
            "2": "explain_code",
            "3": "debug_code"
        }

        if choice not in task_types:
            print("⚠️ Invalid choice, try again.")
            continue

        task_type = task_types[choice]
        language = input("Enter language (e.g., Python, C++): ")

        if task_type == "generate_code":
            task = input("Describe the problem you want solved: ")
        elif task_type == "explain_code":
            print("Paste your code (end with a single line 'END'):")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            task = "\n".join(lines)
        elif task_type == "debug_code":
            print("Paste your buggy code (end with a single line 'END'):")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            code = "\n".join(lines)
            desc = input("Briefly describe the issue: ")
            task = f"Code:\n{code}\nIssue:\n{desc}"

        # Send to backend
        answer = ask_ai(task_type, language, task)

        # Format output
        print("\n===== AI Response =====")
        if isinstance(answer, str):
            print(answer)
        else:
            print(json.dumps(answer, indent=2))
        print("=======================\n")

if __name__ == "__main__":
    main()
