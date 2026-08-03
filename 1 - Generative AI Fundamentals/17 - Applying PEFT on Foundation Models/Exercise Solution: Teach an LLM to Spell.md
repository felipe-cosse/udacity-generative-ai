Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-16-applying-peft-on-foundation-models/exercises/solution/
Double-click the teach-an-llm-to-spell-with-sft-solution.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv2/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.

First, we load the small, instruction-tuned base model (HuggingFaceTB/SmolLM2-135M-Instruct) and its corresponding tokenizer from Hugging Face. We then ensure the model is loaded onto the appropriate device (GPU, MPS, or CPU) for computation.

# <<< START SOLUTION SECTION
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
# <<< END SOLUTION SECTION

print("Model parameters (total):", sum(p.numel() for p in model.parameters()))
Next, we create a custom dataset for the spelling task. The generate_records function creates prompt-completion pairs. The prompt is structured to instruct the model on how to spell a word, and the completion provides the correctly hyphenated, uppercase spelling. We then split this dataset into training (75%) and testing (25%) sets.

def generate_records():
    for word in ALL_WORDS:
        yield {
            # ...
            # <<< START SOLUTION SECTION
            "prompt": (
                f"You spell words with hyphens between the letters like this W-O-R-D.\\nWord:\\n{word}\\n\\n"
                + "Spelling:\\n"
            ),
            # >>> END SOLUTION SECTION
            "completion": "-".join(word).upper() + ".",  # Of the form W-O-R-D.
        }

ds = Dataset.from_generator(generate_records)
# ...
# <<< START SOLUTION SECTION
ds = ds.train_test_split(test_size=0.25, seed=42)
# >>> END SOLUTION SECTION
Before fine-tuning, we establish a baseline by evaluating the base model's performance. We create a helper function, check_spelling, that takes a prompt, generates text from the model, and compares the model's proposed spelling to the actual one.

def check_spelling(
    model, tokenizer, prompt: str, actual_spelling: str, max_new_tokens: int = 20
) -> (str, str):
    # <<< START SOLUTION SECTION
    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Generate text from the model
    gen = model.generate(
        **inputs, max_new_tokens=max_new_tokens
    )  # No parameters = greedy search

    # Decode the generated tokens to a string
    output = tokenizer.decode(gen[0], skip_special_tokens=True)

    # Extract the generated spelling from the full output string
    proposed_spelling = output.split("Spelling:")[-1].strip().split("\n")[0].strip()

    # strip any whitepsace from the actual spelling
    actual_spelling = actual_spelling.strip()

    # Remove hyphens for a character-by-character comparison
    proposed_spelling = proposed_spelling.replace("-", "")
    actual_spelling = actual_spelling.replace("-", "")

    # Calculate the number of correct characters
    num_correct = sum(1 for a, b in zip(actual_spelling, proposed_spelling) if a == b)
    # >>> END SOLUTION SECTION
    #...
As expected, the base model performs poorly, getting none of the spellings correct.

Proposed: sphinx | Actual: SPHINX. | Matches: ❌
Proposed: brawn | Actual: BRAWN. | Matches: ❌
...
Proposed: maze | Actual: MAZE. | Matches: ❌
Proposed:  | Actual: SUMMIT. | Matches: ❌
0.0/20.0 words correct
Now, we configure a LoRA adapter for the model. This is a Parameter-Efficient Fine-Tuning (PEFT) technique that drastically reduces the number of trainable parameters, making the fine-tuning process much faster and more memory-efficient.

# ...
# <<< START SOLUTION SECTION
lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
# >>> END SOLUTION SECTION

# Print the number of trainable parameters after applying LoRA
# ...
The output confirms that after applying LoRA, we are only training about 2.67% of the total parameters.

Trainable params BEFORE: 134,515,008 / 134,515,008 (100.00%)
Trainable params AFTER: 3,686,400 / 138,201,408 (2.67%)
We then set up the training arguments using SFTConfig from the TRL library, defining hyperparameters like batch size, learning rate, and the number of epochs.

# <<< START SOLUTION SECTION
training_args = SFTConfig(
    output_dir=output_dir,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=2,
    num_train_epochs=20,
    learning_rate=5 * 1e-4,
    logging_steps=20,
    eval_strategy="steps",
    eval_steps=20,
    save_strategy="no",
    report_to=[],
    fp16=False,
    lr_scheduler_type="cosine",
)
# >>> END SOLUTION SECTION
Finally, we instantiate the SFTTrainer with our model, datasets, and training arguments, and then call trainer.train() to start the fine-tuning process.

# <<< START SOLUTION SECTION
trainer = SFTTrainer(
    model=model,
    train_dataset=ds["train"],
    eval_dataset=ds["test"],
    args=training_args,
)
trainer.train()
# >>> END SOLUTION SECTION
After training, we evaluate the fine-tuned model. On the same training examples, the performance has dramatically improved.

Proposed: SPHINX. | Actual: SPHINX. | Matches: ✅
Proposed: BRAWN. | Actual: BRAWN. | Matches: ✅
Proposed: GOSSIPY. | Actual: GOSSIPY. | Matches: ✅
...
Proposed: MAZE. | Actual: MAZE. | Matches: ✅
Proposed: SUMMTI. | Actual: SUMMIT. | Matches: ❌
16.41190476190476/20.0 words correct
To confirm the model has generalized the skill of spelling rather than just memorizing the training data, we evaluate it on the unseen test set. The model still performs well, indicating it has successfully learned the new skill.

Proposed: WRIYLY. | Actual: WRYLY. | Matches: ❌
Proposed: GLINES. | Actual: GLISTEN. | Matches: ❌
...
Proposed: IVORY. | Actual: IVORY. | Matches: ✅
Proposed: ONSHORD. | Actual: ONSET. | Matches: ❌
Proposed: ELUDE. | Actual: ELUDE. | Matches: ✅
8.418253968253968/16.0 words correct
Key Takeaway
Supervised fine-tuning with PEFT (LoRA) can efficiently teach a small LLM a new skill, like spelling, using a minimal dataset and computational resources.






