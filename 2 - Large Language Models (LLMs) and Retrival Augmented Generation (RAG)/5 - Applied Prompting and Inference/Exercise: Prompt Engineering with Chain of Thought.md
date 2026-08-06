This exercise explores how different prompt engineering techniques affect LLM reasoning quality, accuracy, and output format. You'll experiment with zero-shot, few-shot, and chain-of-thought prompting to understand when and how to use each technique.

Master zero-shot prompting for simple tasks
Apply few-shot learning to improve consistency
Use chain-of-thought (CoT) for complex reasoning
Generate structured outputs (JSON, tables, etc.)
Compare effectiveness of different approaches

Starter Code Instructions
Step 1: Initialize the PromptEngineer Class
Open exercises/starter/prompt_engineering.py and locate the __init__ method.

Your task:

def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
    # Initialize the OpenAI client
    self.client = OpenAI(api_key=api_key)

    # Store the model name
    self.model = model
Step 2: Implement zero_shot_prompt()
Create the simplest prompting approach:

def zero_shot_prompt(self, task: str) -> str:
    # Direct API call with just the task
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": task}],
        temperature=0
    )
    return response.choices[0].message.content
Test it:

engineer = PromptEngineer(api_key)
result = engineer.zero_shot_prompt("Classify sentiment: 'This is great!'")
print(result)
Step 3: Implement few_shot_prompt()
Add examples to guide the model:

def few_shot_prompt(self, task: str, examples: List[Dict[str, str]]) -> str:
    # Build prompt with examples
    prompt = "Here are some examples:\n\n"

    for i, example in enumerate(examples, 1):
        prompt += f"Example {i}:\n"
        prompt += f"Input: {example['input']}\n"
        prompt += f"Output: {example['output']}\n\n"

    prompt += f"Now, complete this task:\n{task}"

    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
Step 4: Implement chain_of_thought_prompt()
Add reasoning instructions:

def chain_of_thought_prompt(self, problem: str) -> str:
    # Add CoT instruction
    cot_prompt = f"{problem}\n\nLet's think step by step and show the reasoning:"

    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": cot_prompt}],
        temperature=0
    )
    return response.choices[0].message.content
Step 5: Implement structured_output_prompt()
Request specific output formats:

def structured_output_prompt(self, task: str, output_format: str) -> str:
    format_instructions = {
        "JSON": "Respond in valid JSON format. Use proper JSON syntax with quoted keys.",
        "markdown table": "Respond as a markdown table.",
        "YAML": "Respond in valid YAML format.",
        "CSV": "Respond in CSV format with headers."
    }

    instruction = format_instructions.get(output_format, f"Respond in {output_format} format.")

    prompt = f"{task}\n\n{instruction}"

    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
Step 6: Implement compare_approaches()
Compare all three techniques:

def compare_approaches(self, problem: str, examples: List[Dict[str, str]] = None) -> Dict[str, str]:
    results = {}

    # Zero-shot
    results['zero_shot'] = self.zero_shot_prompt(problem)

    # Few-shot (if examples provided)
    if examples:
        results['few_shot'] = self.few_shot_prompt(problem, examples)
    else:
        results['few_shot'] = "No examples provided"

    # Chain-of-thought
    results['chain_of_thought'] = self.chain_of_thought_prompt(problem)

    return results
Step 7: Implement the Experiments
Complete each experiment function by following the TODOs. Basic pattern:

def experiment_1_zero_shot_vs_few_shot():
    api_key = os.getenv("OPENAI_API_KEY")
    engineer = PromptEngineer(api_key)

    # Define task
    task = "Your task here"

    # Zero-shot
    zero_shot_result = engineer.zero_shot_prompt(task)
    print(f"Zero-shot: {zero_shot_result}")

    # Few-shot with examples
    examples = [{"input": "...", "output": "..."}]
    few_shot_result = engineer.few_shot_prompt(task, examples)
    print(f"Few-shot: {few_shot_result}")
Step 8: Run the Complete Program
Uncomment all experiment calls in main() and run:

export OPENAI_API_KEY="your-api-key"
python exercises/starter/prompt_engineering.py



