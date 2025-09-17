from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import psutil
import warnings

class BaseLLM:
    def __init__(self, model_name=None):
        # Check available memory
        available_ram_gb = psutil.virtual_memory().available / (1024**3)
        print(f"Available RAM: {available_ram_gb:.1f} GB")
        
        # Choose appropriate model based on available memory
        if model_name is None:
            if available_ram_gb < 8:
                model_name = "microsoft/DialoGPT-small"  # ~250MB
                print("Using small model due to limited memory")
            elif available_ram_gb < 12:
                model_name = "distilgpt2"  # ~350MB, good for code generation
                print("Using medium model")
            else:
                model_name = "codellama/CodeLlama-7b-Instruct-hf"
                print("Using CodeLlama model")
        
        print(f"Loading model: {model_name}... please wait")
        self.model_name = model_name
        
        try:
            # Load tokenizer first (lightweight)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Configure model loading options for memory efficiency
            model_kwargs = {
                "torch_dtype": torch.float32,  # Use float32 for CPU compatibility
                "low_cpu_mem_usage": True,
            }
            
            # Load the model
            self.model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
            
            # Explicitly move to CPU (safer than relying on defaults)
            self.model = self.model.to('cpu')
            
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model {model_name}: {str(e)}")
            if "out of memory" in str(e).lower() or "memory" in str(e).lower() or "size" in str(e).lower():
                print("\nTrying with a smaller model due to memory constraints...")
                # Fallback to a much smaller model
                fallback_model = "microsoft/DialoGPT-small"
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained(fallback_model)
                    if self.tokenizer.pad_token is None:
                        self.tokenizer.pad_token = self.tokenizer.eos_token
                    self.model = AutoModelForCausalLM.from_pretrained(
                        fallback_model,
                        torch_dtype=torch.float32,
                        low_cpu_mem_usage=True
                    ).to('cpu')
                    self.model_name = fallback_model
                    print(f"Loaded fallback model: {fallback_model}")
                except Exception as fallback_error:
                    print(f"Even fallback model failed: {fallback_error}")
                    # Try the smallest possible model
                    tiny_model = "distilgpt2"
                    print(f"Trying minimal model: {tiny_model}")
                    self.tokenizer = AutoTokenizer.from_pretrained(tiny_model)
                    if self.tokenizer.pad_token is None:
                        self.tokenizer.pad_token = self.tokenizer.eos_token
                    self.model = AutoModelForCausalLM.from_pretrained(
                        tiny_model,
                        torch_dtype=torch.float32
                    ).to('cpu')
                    self.model_name = tiny_model
                    print(f"Loaded minimal model: {tiny_model}")
            else:
                raise e

        def generate(self, prompt, max_tokens=200):
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
            text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
            # Clean output
            if "```" in text:
                text = text.split("```")[1]  # extract code between ```
            return text.strip()

    
    def get_model_info(self):
        """Return information about the loaded model."""
        return {
            'model_name': self.model_name,
            'parameters': sum(p.numel() for p in self.model.parameters()),
            'device': next(self.model.parameters()).device
        }

# Test the model
if __name__ == "__main__":
    llm = BaseLLM()
    result = llm.generate("Write a Python function to compute factorial")
    print(result)