Large language models can struggle with seemingly simple, structured tasks like sequential counting. They might skip numbers, count by twos, or fail to follow formatting instructions. This demo walks through how to use Group Relative Policy Optimization (GRPO)—a technique similar to reinforcement learning—to fine-tune a small LLM, teaching it to count accurately and consistently.

Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-18-reinforcement-fine-tuning-on-foundation-models/demo
Double-click the demo.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv2) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv2/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.

This walkthrough demonstrates how to teach a small Large Language Model (LLM) a new skill: counting sequentially. We'll use a technique called Group Relative Policy Optimization (GRPO). The process involves six main steps: setting up the environment, loading a base model, creating a dataset, evaluating the model's baseline performance, configuring LoRA and training with GRPO, and finally, re-evaluating the fine-tuned model.

First, we load the SmolLM2-135M-Instruct model from the Hugging Face Hub. This is a small, 135-million-parameter instruction-tuned model, which is lightweight and efficient for demonstrating fine-tuning concepts without requiring a high-end GPU.

# Model ID for SmolLM2-135M-Instruct
model_id = "HuggingFaceTB/SmolLM2-135M-Instruct"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Load the model
model = AutoModelForCausalLM.from_pretrained(
    model_id,
)

# Copy the model to the device (GPU, MPS, or CPU)
model = model.to(device)

print("Model parameters (total):", sum(p.numel() for p in model.parameters()))
Next, we create the dataset for training. Instead of using a static file, we generate our dataset programmatically. This function creates a series of prompts that ask the model to count from a starting number to an ending number. The dataset also includes the start and end values, which we'll use later in our reward functions.

def generate_records():
    for start in range(1, 5):
        for end in range(start + 5, start + 8):
            yield {
                # The prompt that is sent to the model
                "prompt": (
                    f"You are a counting assistant. Count from {start} to {end} by 1. Begin: "
                ),
                # Extra values sent to the reward functions
                "start": start,
                "end": end,
            }

ds = Dataset.from_generator(generate_records)
Before fine-tuning, we evaluate the base model to establish a clear baseline. We loop through our dataset and use a helper function to check the model's performance on each counting task.

# Evaluate the base model's counting ability
proportion_correct = 0.0

for example in ds:
    prompt = example["prompt"]
    start = example["start"]
    end = example["end"]
    result = check_counting(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        start=start,
        end=end,
    )
    proportion_correct += result

print(f"{proportion_correct}/{len(ds)} sequences correct")
The output shows the model gets some sequences right but often makes mistakes, such as counting by twos or starting from the wrong number. Its performance is inconsistent.

Now, we'll use GRPO to encourage the model to always count correctly by ones. We start by configuring LoRA (Low-Rank Adaptation), a parameter-efficient fine-tuning (PEFT) method. LoRA freezes the original model's weights and injects small, trainable adapter layers, drastically reducing the number of parameters that need to be updated.

# Print how many params are trainable at first
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(
    f"Trainable params BEFORE: {trainable:,} / {total:,} ({100 * trainable / total:.2f}%)"
)

lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)

# Print the number of trainable parameters after applying LoRA
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(
    f"Trainable params AFTER: {trainable:,} / {total:,} ({100 * trainable / total:.2f}%)"
)
Notice that after applying LoRA, only about 2.67% of the parameters are trainable.

GRPO improves the model's behavior using a set of reward functions that guide the training process. We'll create four:

Starts correctly: This function rewards the model if its generated sequence starts with the correct number.
def reward_starting_at_start(
    completions: list[str], start: list[int], **kwargs
) -> list[float]:
    """Reward function that rewards completions that start with the given start value."""
    start_list = start
    return [
        1.0 if completion.startswith(str(start)) else 0.0
        for completion, start in zip(completions, start_list)
    ]
Uses correct format: This rewards the model for using a comma and a space to separate numbers.
def reward_using_comma_separated_numbers(
    completions: list[str], **kwargs
) -> list[float]:
    """Reward function that rewards completions that use comma-separated numbers."""
    return [1.0 if ", " in completion else 0.0 for completion in completions]
Counts by one: This crucial function checks if the numbers in the sequence are actually incrementing by one.
def reward_counting_by_one(completions: list[str], **kwargs) -> list[float]:
    """Reward function that rewards completions that count by 1."""
    # ... function implementation ...
    # Check if the differences are all 1
    if all(d == 1 for d in differences):
        rewards.append(1.0)
    else:
        rewards.append(0.0)
    # ...
    return rewards
Ends correctly: Finally, this function checks if the sequence ends with the correct final number.
def reward_ending_at_end(
    completions: list[str], end: list[int], **kwargs
) -> list[float]:
    """Reward function that rewards completions that end with the given end value."""
    # ... function implementation ...
    return [
        1.0 if completion.endswith(str(end)) else 0.0
        for completion, end in zip(completions, end_list)
    ]
With our reward functions defined, we can set up and run the GRPOTrainer. We pass it our model, the list of reward functions, the training dataset, and configuration arguments like the learning rate and number of epochs.

from trl import GRPOConfig, GRPOTrainer

training_args = GRPOConfig(
    output_dir="data/counting-grpo",
    max_completion_length=30,  # The maximum number of tokens to generate
    learning_rate=5e-5,  # The learning rate for the optimizer
    num_train_epochs=10,  # We'll train just for a few epochs
    beta=0.0,  # beta=0.0 means no KL penalty
    # ... other arguments ...
)
trainer = GRPOTrainer(
    model=model,
    reward_funcs=[
        reward_starting_at_start,
        reward_using_comma_separated_numbers,
        reward_counting_by_one,
        reward_ending_at_end,
    ],
    args=training_args,
    train_dataset=ds,
)
trainer.train()
After training, we can visualize the total reward the model received over the training epochs. The upward trend in the graph indicates that the model was successfully learning to generate better responses that satisfied our reward functions.

import pandas as pd
import matplotlib.pyplot as plt

log_df = pd.DataFrame(trainer.state.log_history)
log_df["reward"].plot()

plt.legend(["reward"])
plt.show()
[IMAGE_PLACEHOLDER: Screengrab of the reward curve plot, showing an upward trend.]

Finally, we evaluate the fine-tuned model's performance one more time using the same evaluation loop as before.

# Evaluate the fine-tuned model on the same training examples
proportion_correct = 0.0

for example in ds:
    prompt = example["prompt"]
    start = example["start"]
    end = example["end"]
    result = check_counting(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        start=start,
        end=end,
    )
    proportion_correct += result

print(f"{proportion_correct}/{len(ds)} sequences correct")
The output shows the model is now much more accurate and correctly counts by one for most of the examples it failed on before.

By defining a set of simple reward functions, Group Relative Policy Optimization (GRPO) can effectively teach a large language model to perform structured tasks like sequential counting with high accuracy.

Concept: The purpose of reward functions in GRPO. Suggestion: A matching question. Note to author: Create two columns. Column A lists the function names (reward_starting_at_start, reward_using_comma_separated_numbers, reward_ending_at_end). Column B lists their descriptions ("Ensures the output uses a comma and space," "Checks if the first number is correct," "Verifies the last number is correct"). The learner matches the function to its purpose.






In this demo, we teach a large language model a new skill, how to account sequentially using a technique called group relative policy optimization, or GRPO. We'll walk through six main steps. First, we set up our environment. Then we load a base model and create a simple counting dataset. We'll evaluate the model's performance before any training. Next, we'll configure a technique called LoRA and fine tune the model using our dataset. Finally, we'll evaluate the model again to see how much it has improved. So let's begin with a setup. Here, we import all the necessary libraries, including PyTorch, hugging face, transformers, etc. We also detect and select the best available hardware to run on. Next, we loader base model. For this exercise, we're using a small, 135 million parameter instruction tune model called Small LM2. It's lightweight, which makes it perfect for demonstrating fine tuning concepts without needing a high NGP. In this cell, we load the tokenizer in the model itself from the hugging face hub. We then move the model to a selected device and print out the total number parameters, which is about 134 million. Next, we create a dataset that we'll be using for training. We're generating our dataset programmatically. This function creates a series of prompts that ask the model to count from a starting number to an ending number. The dataset also includes the start and end values which we'll use later in our reward functions. Now, let's evaluate the base model before we make any changes. This gives us a clear baseline to measure our progress against. To help with evaluation, we create a helper function called check counting. This function sends a prompt to the model, gets a generated text, and compares a model's answer to the correct counting sequence. And then print to whether the model's output was correct and returns a score. We now loop through our entire data set and use this function to evaluate the base model's performance. As you can see, it gets them right, but it often makes mistakes, like counting by twos or starting from the wrong number. The model's performance is inconsistent. Now, we'll use GRPO to encourage it to always count correctly by ones. It's time to configure LoRA and train the model. We'll use a technique called low rank adaptation or LoRA. This method freezes the original models weights and injects small trainable adapter layers. Here, we define a LoRA configuration and apply it to the model. Notice the output. Before applying it, 100% of the models parameters are trainable, and now only about 2% are. GRPO improves a model's behavior by using a set of reward functions. Let's create those now. Our first reward function, checks if the models generated sequence starts with the correct number. If it does, the model gets a reward of one, otherwise, zero. The second reward function rewards the model for using the correct format. We want the numbers to be separated by a comma in a space, so this function gives a reward if that pattern is present. This is a crucial reward function. It checks if the numbers in the sequence are actually counting up by one. It extracts all the numbers, calculates a difference, and then gives a reward only if all the differences are exactly one. Our final reward function is a counterpart to our first one. It checks to see if the model's response ends with a final correct number. With our reward functions defined, we can now set up the GRPO trainer. We pass in our model, the list of reward functions, the training dataset, and some configuration arguments like the learning rate and the number of epics. Then we simply call trainer.dottrain. After training, we can visualize the results. This cell plots the total reward the model received over the training epics. The upward trend in the graph indicates that the model was successfully learning to train better responses that satisfy the reward function. We also print the names of other available metrics that could be plotted. Now that we have fine tuned or model, let's evaluate its performance one more time. We've run the exact same evaluation loop as before, using our fine tune model. Looking at the output, we can see the model is much more accurate. It now correctly counts by one for most of the examples it failed on before. We've run the exact same evaluation loop as before, using our Fine Tune model. Looking at the output, we can see the model has improved. As we can see, the Fine Tune model now performs better on the data it has seen, and that concludes our demonstration of teaching an LLM to account using group relative policy optimization.