class PromptManager:
    def __init__(self):
        # We can expand this later with more prompt types
        self.templates = {
            "generate_code": "Write {language} code for the following task:\n{task}",
            "explain_code": "Explain in simple terms what this code does:\n{code}",
            "debug_code": "Find bugs and fix the following {language} code:\n{code}",
        }

    def build_prompt(self, task_type, **kwargs):
        if task_type not in self.templates:
            raise ValueError("Unknown task type")
        return self.templates[task_type].format(**kwargs)


# Test it
if __name__ == "__main__":
    pm = PromptManager()
    print(pm.build_prompt("generate_code", language="Python", task="sort a list"))