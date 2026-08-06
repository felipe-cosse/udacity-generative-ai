In this exercise, you'll explore how different inference parameters affect LLM output quality, creativity, and consistency. You'll perform experiments with temperature, top_p, max_tokens, frequency_penalty, and logprobs to understand when and how to use each parameter.

Starter Code Instructions
Step 1: Initialize the InferenceExplorer Class
Open exercises/starter/inference_parameters.py and locate the __init__ method.

Your task:

def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
    # TODO: Initialize the OpenAI client
    self.client = OpenAI(api_key=api_key)

    # TODO: Store the model name
    self.model = model
Step 2: Implement generate_with_temperature()
Complete the method that generates text with a specific temperature:

def generate_with_temperature(self, prompt: str, temperature: float) -> str:
    # Make API call with temperature parameter
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=100
    )
    return response.choices[0].message.content
Test it:

explorer = InferenceExplorer(api_key)
response = explorer.generate_with_temperature("Write a creative story opener", 0.9)
print(response)
Step 3: Implement compare_temperatures()
This method compares outputs at different temperatures:

def compare_temperatures(self, prompt: str, temperatures: List[float]) -> Dict[float, str]:
    results = {}
    for temp in temperatures:
        results[temp] = self.generate_with_temperature(prompt, temp)
    return results
Step 4: Implement generate_with_top_p()
Add nucleus sampling support:

def generate_with_top_p(self, prompt: str, top_p: float, temperature: float = 1.0) -> str:
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=100
    )
    return response.choices[0].message.content
Step 5: Implement generate_with_max_tokens()
Control response length:

def generate_with_max_tokens(self, prompt: str, max_tokens: int) -> str:
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].message.content
Step 6: Implement generate_with_frequency_penalty()
Reduce repetition:

def generate_with_frequency_penalty(self, prompt: str, frequency_penalty: float) -> str:
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": prompt}],
        frequency_penalty=frequency_penalty,
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content
Step 7: Implement analyze_logprobs()
Analyze token probabilities:

def analyze_logprobs(self, prompt: str, top_logprobs: int = 5) -> Dict:
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=50,
        logprobs=True,
        top_logprobs=top_logprobs
    )

    return {
        'text': response.choices[0].message.content,
        'logprobs': response.choices[0].logprobs
    }
Step 8: Implement the Experiments
For each experiment function, uncomment and complete the TODOs:

Experiment 1 - Temperature Effects:

def experiment_1_temperature_effects():
    api_key = os.getenv("OPENAI_API_KEY")
    explorer = InferenceExplorer(api_key)

    prompt = "Write a creative opening sentence for a science fiction story about time travel."
    temperatures = [0.0, 0.5, 1.0, 1.5]

    results = explorer.compare_temperatures(prompt, temperatures)

    for temp, response in results.items():
        print(f"\n🌡️  Temperature: {temp}")
        print(f"Response: {response}")
Repeat similar patterns for experiments 2-5.

Step 9: Run the Complete Program
Uncomment all experiment calls in main() and run:

export OPENAI_API_KEY="your-api-key"
python exercises/starter/inference_parameters.py



