#!/usr/bin/env python3
"""
Test script for the BaseLLM model to ensure it's working correctly.
"""

from base_llm import BaseLLM

def test_model():
    print("Testing BaseLLM model...")
    
    try:
        # Initialize the model
        llm = BaseLLM()
        
        # Display model information
        info = llm.get_model_info()
        print(f"\nModel Information:")
        print(f"- Name: {info['model_name']}")
        print(f"- Parameters: {info['parameters']:,}")
        print(f"- Device: {info['device']}")
        
        # Test different types of prompts
        test_prompts = [
            "def factorial(n):",
            "Hello, how are you?",
            "The capital of France is",
            "def fibonacci(n):"
        ]
        
        print("\nTesting text generation:")
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n{i}. Prompt: '{prompt}'")
            result = llm.generate(prompt, max_tokens=50)
            print(f"   Response: {result.strip()}")
        
        print("\n✅ Model testing completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Model testing failed: {e}")
        return False

if __name__ == "__main__":
    test_model()
