Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-18-reinforcement-fine-tuning-on-foundation-models/exercises/solution
Double-click the teach-an-llm-to-spell-with-grpo-solution.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv2) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv2/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.

First, we load the small, instruction-tuned model HuggingFaceTB/SmolLM2-135M-Instruct and its corresponding tokenizer from the Hugging Face Hub. We use AutoModelForCausalLM and AutoTokenizer to handle the loading and then move the model to the appropriate compute device.

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
Next, we create a dataset by defining a generator function that formats each word from our list. For each word, we create a prompt that instructs the model on the task and a completion which serves as the ground truth answer for the initial Supervised Fine-Tuning (SFT) phase.

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
            # ...
            # <<< START SOLUTION SECTION
            "completion": "-".join(word).upper() + ".",
            # >>> END SOLUTION SECTION
            # ...
        }
Before fine-tuning, an evaluation of the base model shows it performs poorly, failing to spell any of the words correctly.

...
Proposed: zeal | Actual: Z-E-A-L-O-U-S | Matches: ❌
0.0/20.0 words correct
To prepare for efficient fine-tuning, we configure and attach a Low-Rank Adaptation (LoRA) adapter to the model. This significantly reduces the number of trainable parameters from 100% to just over 2.5%, making the training process much faster and more memory-efficient.

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
For GRPO, we need reward functions to score the model's outputs. The first function, proportion_correct, calculates a score based on character-by-character comparison. It adds 1 for each matched character and subtracts 1 for each mismatch.

def proportion_correct(word, proposed_spelling):
    # ...
    for a, b in zip(correct_spelling_padded, proposed_spelling_padded):
        # Add 1 for matched characters, and subtract one for mismatched
        # <<< START SOLUTION SECTION
        if a == b:
            score += 1
        else:
            score -= 1
        # >>> END SOLUTION SECTION

    return score / (
        len(correct_spelling)
    )  # Normalize by length of spelling, including dashes
The second reward function, reward_response_in_form_of_letter_dash_letter, checks if the model's output adheres to the required L-E-T-T-E-R format using a regular expression. It provides a reward of 1.0 for correctly formatted responses and 0.0 otherwise, incentivizing the model to learn the desired structure.

def reward_response_in_form_of_letter_dash_letter(completions, word, **kwargs):
    # ...
    # <<< START COMPLETION SECTION
    rewards = [
        1.0 if pattern.match(c) else 0.0 for w, c in zip(words, completion_strings)
    ]
    # >>> END COMPLETION SECTION
    # ...
Finally, we configure the GRPOConfig with training parameters and initialize the GRPOTrainer. Crucially, we pass our two custom reward functions to the trainer, which will use them to guide the model's learning process.

training_args = GRPOConfig(
    # ...
    # <<< START SOLUTION SECTION
    learning_rate=5e-5,
    num_train_epochs=10,  # We'll train just for a few epochs
    per_device_train_batch_size=8,  # The batch size for training
    num_generations=4,  # Determines the number of completions to compute for each single prompt
    lr_scheduler_type="cosine",
    beta=0.0,
    # >>> END SOLUTION SECTION
)
trainer = GRPOTrainer(
    model=model,
    # <<< START SOLUTION SECTION
    reward_funcs=[
        reward_spelling,
        reward_response_in_form_of_letter_dash_letter,
    ],
    # >>> END SOLUTION SECTION
    args=training_args,
    train_dataset=ds["train"],
)
trainer.train()
After training, evaluating the model on the unseen test set shows a marked improvement, demonstrating that it has successfully learned and generalized the new skill of spelling.

Proposed: W-R-Y-I-L-Y. | Actual: W-R-Y-L-Y. | Matches: ❌
Proposed: G-L-I-N-E. | Actual: G-L-I-S-T-E-N. | Matches: ❌
...
Proposed: K-N-A-R-C-E. | Actual: K-N-A-C-K. | Matches: ❌
2.6416666666666666/7.0 words correct
Key Takeaway
Using Group Relative Policy Optimization (GRPO) with multiple reward functions allows for fine-tuning a language model on complex, multi-faceted tasks like correct spelling and formatting.

Accessing the Workspace
Follow these steps to access the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the module-18-reinforcement-fine-tuning-on-foundation-models/exercises /solution directory under which you will find the starter notebook.
Double-click the *-solution.ipynb notebook.
You can also access this notebook on GitHub here(opens in a new tab).








In this exercise, we teach a large language model, how to spell, using a technique called group relative policy optimization or GRPO. Here, we'll fine-tune a small LLM on a spelling task. We'll start by setting up our environment, loading a model, creating a dataset, and then evaluating its baseline performance. After that, we'll use a method called LoRA to fine-tune the model and then evaluate it again to see the improvement. Let's get it set up. This cell handles our initial setup. We import all the necessary libraries, including PyTorch, Hugging Face Transformers, etc. The code also automatically selects the best available hardware to run on. Now we load our base model. We're using a small 135 million parameter instruction-tuned model. Here, we specify the model ID from the Hugging Face hub and use AutoTokenizer and AutoModelForCausalLM classes to download and load both tokenizer and the model weights. We then copy the model to a selected device. With model loaded, the next step is to create our training dataset. This cell simply defines a Python list containing all the words we'll use to teach a model how to spell. Now, we format our word list into a structure that the trainer can use. The generate records function creates a prompt for each word, asking the model to spell it with hyphens. It also creates a completion, which is a correct, properly formatted spelling. We then convert this into a Hugging Face dataset and split it into training and test sets. The output shows an example of a single record. Before we start training, it's important to see how the model performs on the task without any fine-tuning. This cell defines a helper function called check spelling. This function takes a prompt, sends it to the model, gets a generated spelling, and compares it to the correct answer. It prints whether the spelling matches and calculates a score based on how many characters were correct. Now we use our helper function to evaluate the base model on 20 examples from our training set. As you can see, the model performs very poorly. The results are clear. Base model is terrible at this task. Now it's time to fine-tune it. Let's move on to the main part of the exercise, configuring the training process and fine-tuning the model. We'll use a technique called low-rank adaptation or LoRa. Instead of retraining all 135 million parameters, LoRa adds a very small number of new trainable parameters. Here, we set up our LoRaConfig. This tells the model how to create the small trainable adapter layers. After applying the LoRa configuration, we print the number of trainable parameters again. You can see that it has significantly decreased. Next, we define our training arguments. We use the SFTConfig object from the TRL library, which helps us set things like the number of training epics, the batch size, and the learning rate. Before we use the more advanced GRPO method, we start with a few epics of standard supervised fine-tuning or SFT. This gives the model an initial push in the right direction. The model has already improved significantly. Now, let's see if we can make it even better using GRPO. To do that, we first need to create some reward functions. This is our first reward function, proportion correct. It takes a model's proposed spelling and scores it. For every character that matches a correct spelling, the score goes up by one, and for every mismatch, it goes down by one. This reward spelling function is a simple wrapper. During training, GRPO will generate multiple completions at once, and this function applies the scoring logic to the entire batch completions. This is how the GRPO trainer expects its reward functions. Here is our second batch reward function. This one is a bit different. It doesn't check for spelling accuracy. Instead, it uses a regular expression to check at the models output is in the correct format. It gives a reward of one if the format is right, and zero, if it's wrong. This encourages a model to provide answers in the structure we want. Now, we put it all together for GRPO training. We define a GRPOConfig with our training settings and then create a GRPO trainer. The key step here is passing our two reward functions. Then we call trainer.train. The output logs, immense as they are, show the model generating completions in our reward function scoring them during the training process. Now that the model is fully fine-tuned, let's see how well it performs. First, we'll evaluate the fine-tune model on the same training examples that we used for our earlier tests. The model's performance on the training data is a bit better after GRPO compared to SFT alone. The model has learned the training data, but the real test is whether it can generalize this new skill to words it has never seen before. Here, we evaluate the model on the unseen test set. The results show that the model spelling has definitely improved. While it's not perfect, it's much better than the base model, indicating that it has successfully generalized some of its new spelling ability. It looks like fine-tuning was a success. With a larger dataset and more training data and more training time, we could likely improve its performance even further.