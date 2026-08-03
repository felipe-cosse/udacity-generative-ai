Large language models (LLMs) are notoriously bad at spelling. This is partly because tokenizers break words into smaller pieces, so the model learns about sub-word units rather than individual letters. In this exercise, you'll use Group Relative Policy Optimization (GRPO) and a technique called Parameter-Efficient Fine-Tuning (PEFT) with Low-Rank Adaptation (LoRA) to teach a small LLM how to spell words. This is a classic example of teaching a model a new skill that isn't well-represented in its pre-training data.

Prerequisites
Familiarity with the Hugging Face transformers library for loading models and tokenizers.
Understanding of Parameter-Efficient Fine-Tuning (PEFT) and LoRA.
Knowledge of the TRL library, specifically the concept of a Trainer and reward-based fine-tuning.
Basic Python programming skills.
Instructions
In the code cell under the heading ## Step 1. Load the tokenizer and base model, replace the placeholder strings to load the model and tokenizer for HuggingFaceTB/SmolLM2-135M-Instruct. Use AutoTokenizer.from_pretrained() and AutoModelForCausalLM.from_pretrained(), and then copy the model to the specified device.

In the generate_records function, uncomment and complete the dictionary items. Create a prompt key with a formatted string instructing the model how to spell. Then, create a completion key with the corresponding correctly spelled word, which should be hyphenated, in uppercase, and end with a period.

In the first code cell under the heading ## Step 4. Configure LoRA and train the model, uncomment and define the LoraConfig. Set r to 64, lora_alpha to 16, lora_dropout to 0.05, and task_type to "CAUSAL_LM". Then, apply this configuration by wrapping the model with get_peft_model.

In the proportion_correct function, replace the placeholder comment with a conditional statement. If the characters a and b match, add 1 to the score; otherwise, subtract 1.

In the reward_response_in_form_of_letter_dash_letter function, replace the placeholder rewards list with a list comprehension that returns 1.0 if a completion c matches the regex pattern, and 0.0 otherwise.

In the final training cell, configure the GRPOConfig. Uncomment and set the following parameters: learning_rate to 5e-5, num_train_epochs to 10, per_device_train_batch_size to 8, num_generations to 4, lr_scheduler_type to "cosine", and beta to 0.0.

In the same cell, complete the GRPOTrainer initialization. Add the reward_funcs parameter and assign it a list containing the two reward functions you defined: reward_spelling and reward_response_in_form_of_letter_dash_letter.

Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-18-reinforcement-fine-tuning-on-foundation-models/exercises/starter
Double-click the teach-an-llm-to-spell-with-grpo-starter.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv2) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.