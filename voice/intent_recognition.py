"""
Improved rule-based + similarity intent recognizer.

Usage:
    from intent_recognizer import predict_intent
    print(predict_intent("Create a function called add_numbers that takes two numbers a and b"))
"""

import csv
import re
from pathlib import Path

# Path to your intents CSV (adjust if needed)
INTENTS_CSV = Path("/mnt/data/day3_outputs/intents.csv")

# Load example utterances from intents.csv (if present)
examples_by_intent = {}
if INTENTS_CSV.exists():
    with INTENTS_CSV.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            intent = row["intent"].strip()
            utt = row["utterance"].strip().lower()
            examples_by_intent.setdefault(intent, []).append(utt)
else:
    # minimal fallback examples
    examples_by_intent = {
        "create_function": ["write a function called add_numbers", "create a function named factorial"],
        "run_code": ["run main.py", "execute this python file"],
        "create_class": ["create a class called student", "write a python class bankaccount"],
        "add_loop": ["add a for loop from 1 to 10", "create a while loop that runs until x equals 5"],
        "write_file": ["write results to output.txt", "save this file as main.py"],
    }

# Utility tokenization
def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s\.]", " ", text)       # keep dots for filenames
    return text.split()

def jaccard(a, b):
    sa = set(a); sb = set(b)
    if not sa and not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

# Phrase-based high-priority rules (check these first)
def phrase_rules(text):
    t = text.lower()

    # filenames present?
    if re.search(r"\b[\w\-\_]+\.(py|txt|json|csv)\b", t):
        # ambiguous: if also contains 'function' prefer create_function
        if "function" in t or "def " in t or "method" in t:
            return {"intent": "create_function", "method": "phrase_rule", "score": 1.0}
        # if contains run/execute -> run_code
        if any(w in t for w in ("run ", "execute ", "start ")):
            return {"intent": "run_code", "method": "phrase_rule", "score": 1.0}
        # save / write phrases
        if any(w in t for w in ("save ", "write ", "store ")):
            return {"intent": "write_file", "method": "phrase_rule", "score": 1.0}

    # Create function/class rules
    if ("function" in t or "def " in t or "method" in t):
        if any(w in t for w in ("create ", "make ", "define ", "build ", "add ")):
            return {"intent": "create_function", "method": "phrase_rule", "score": 1.0}
        # user might say "write a function" — treat as create_function not write_file
        if "write a function" in t or "write function" in t:
            return {"intent": "create_function", "method": "phrase_rule", "score": 1.0}

    if "class" in t:
        if any(w in t for w in ("create ", "make ", "define ", "add ")):
            return {"intent": "create_class", "method": "phrase_rule", "score": 1.0}

    # Run / execute
    if any(w in t for w in ("run ", "execute ", "start ")):
        # "run tests" -> run_tests
        if "test" in t or "pytest" in t:
            return {"intent": "run_tests", "method": "phrase_rule", "score": 1.0}
        return {"intent": "run_code", "method": "phrase_rule", "score": 1.0}

    # Debug / find errors
    if any(w in t for w in ("error", "bug", "debug", "fix", "traceback", "exception")):
        # more specific: "how to fix IndexError" -> suggest_fix
        if "how" in t and ("fix" in t or "solve" in t):
            return {"intent": "suggest_fix", "method": "phrase_rule", "score": 1.0}
        if any(w in t for w in ("fix", "suggest", "how to")):
            return {"intent": "suggest_fix", "method": "phrase_rule", "score": 1.0}
        return {"intent": "find_errors", "method": "phrase_rule", "score": 1.0}

    # Formatting / linting
    if any(w in t for w in ("format", "formatting", "pep8", "black", "autopep8", "indent")):
        return {"intent": "format_code", "method": "phrase_rule", "score": 1.0}

    # Save / write file
    if any(w in t for w in ("save as", "save this file", "save file", "write to", "store as")):
        return {"intent": "save_file", "method": "phrase_rule", "score": 1.0}

    # stop execution
    if any(w in t for w in ("stop execution", "terminate", "stop running", "cancel execution", "kill script")):
        return {"intent": "stop_execution", "method": "phrase_rule", "score": 1.0}

    return None

# Keyword mapping lower-priority (single tokens)
keyword_map = {
    "function": "create_function",
    "def": "create_function",
    "class": "create_class",
    "loop": "add_loop",
    "for": "add_loop",
    "while": "add_loop",
    "run": "run_code",
    "execute": "run_code",
    "error": "find_errors",
    "bug": "find_errors",
    "debug": "find_errors",
    "format": "format_code",
    "indent": "format_code",
    "save": "save_file",
    "write": "write_file",
    "test": "run_tests",
    "refactor": "refactor_function",
    "explain": "explain_code",
    "rename": "rename_identifier",
    "delete": "delete_code",
    "comment": "add_comment",
    "try": "add_try_except",
    "stop": "stop_execution",
    "duplicate": "duplicate_block",
    "run_tests": "run_tests"
}

def predict_intent(text, threshold=0.2):
    """
    Predict intent for an input text.
    Returns: {"intent": str, "method": "phrase_rule"|"keyword"|"similarity"|"fallback", "score": float}
    """
    if not text or not text.strip():
        return {"intent": "none", "method": "fallback", "score": 0.0}

    text_clean = text.strip()
    t = text_clean.lower()
    tokens = tokenize(t)

    # 1) Phrase rules (highest priority)
    pr = phrase_rules(t)
    if pr:
        return pr

    # 2) Token-level keywords (choose first confident token)
    for tok in tokens:
        if tok in keyword_map:
            # special-case ambiguous 'write' - prefer create_function if function present
            if tok == "write":
                if "function" in tokens or "def" in tokens:
                    return {"intent": "create_function", "method": "keyword", "score": 1.0}
                # otherwise if filename present -> write_file
                if re.search(r"\b[\w\-\_]+\.(py|txt|json|csv)\b", t):
                    return {"intent": "write_file", "method": "keyword", "score": 1.0}
            return {"intent": keyword_map[tok], "method": "keyword", "score": 1.0}

    # 3) Similarity against example utterances (Jaccard)
    best_intent = None
    best_score = 0.0
    for intent, examples in examples_by_intent.items():
        for ex in examples:
            score = jaccard(tokens, tokenize(ex))
            if score > best_score:
                best_score = score
                best_intent = intent
    if best_score >= threshold:
        return {"intent": best_intent, "method": "similarity", "score": round(best_score, 3)}

    # 4) fallback: guess based on presence of high-value nouns
    if "function" in tokens:
        return {"intent": "create_function", "method": "fallback", "score": 0.5}
    if "class" in tokens:
        return {"intent": "create_class", "method": "fallback", "score": 0.5}
    if re.search(r"\b[\w\-\_]+\.(py|txt|json|csv)\b", t):
        # if action word present
        if any(w in tokens for w in ("run","execute","start")):
            return {"intent": "run_code", "method": "fallback", "score": 0.5}
        return {"intent": "read_file", "method": "fallback", "score": 0.5}

    return {"intent": "none", "method": "fallback", "score": 0.0}


# Quick CLI test when run directly
if __name__ == "__main__":
    tests = [
        "Create a function called add_numbers that takes two numbers a and b",
        "Write a bubble sort function",
        "Write this file to utils.py",
        "Run main.py now",
        "How do I fix IndexError in line 12?",
        "Create a class called Student with name and grade",
        "Format my code to PEP8"
    ]
    for t in tests:
        print(t, "->", predict_intent(t))
