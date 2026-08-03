Large Language Models are powerful, but they don't know everything. Sometimes, you need to teach them a new, specific skill. This demo shows how to efficiently fine-tune a small LLM to perform a new task—adding the suffix "-ish" to the end of words—using Supervised Fine-Tuning (SFT) and an efficient technique called LoRA.

Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-16-applying-peft-on-foundation-models/demo/
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

We'll walk through the process of setting up the environment, loading a model, creating a custom dataset, and then fine-tuning the model to learn its new skill.

First, we load our base model and tokenizer. For this demo, we're using SmolLM2-135M-Instruct, a small model with 135 million parameters, which is perfect for a quick demonstration on a standard computer. The tokenizer prepares our text into a format the model can understand.

# Model ID from Hugging Face
model_id = "HuggingFaceTB/SmolLM2-135M-Instruct"

# Load the tokenizer, which prepares text for the model
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Load the model itself
model = AutoModelForCausalLM.from_pretrained(model_id)

# Move the model to our selected device (GPU/CPU)
model = model.to(device)
Next, we'll create the dataset for our new task. We start with a simple Python list of words. Then, we use a generator function, generate_records, to format each word into a prompt and a completion. The prompt provides instructions and a couple of examples (a technique called few-shot prompting), and the completion is the correct answer we want the model to learn.

# This function creates prompt/completion pairs for our dataset.
def generate_records():
    for word in DEMO_WORDS:
        # The prompt tells the model what to do.
        prompt = (
            f"Add -ish to the end of the word.\n"
            "hello -> hello-ish\n"
            "learn -> learn-ish\n"
            f"{word} -> "
        )
        # The completion is the correct answer.
        completion = f"{word}-ish"
        yield {"prompt": prompt, "completion": completion}

# Create a Hugging Face Dataset from our generator
ds = Dataset.from_generator(generate_records)

# Split the dataset: 80% for training, 20% for testing
ds = ds.train_test_split(test_size=0.2, seed=42)

# Let's look at the first training example
print("First training example:")
print(ds["train"][0])
The output shows the structure of our first training example:

First training example:
{'prompt': 'Add -ish to the end of the word.\nhello -> hello-ish\nlearn -> learn-ish\nivory -> ', 'completion': 'ivory-ish'}
Before training, it's crucial to see how the base model performs. This gives us a baseline to measure our improvement against. We run an evaluation loop over our test set.

print("--- Evaluating Base Model (Before Training) ---")
num_correct = 0
num_examples = len(ds["test"])

for example in ds["test"]:
    prompt = example["prompt"]
    completion = example["completion"]
    # check_translation is a helper function that gets the model's prediction
    # and compares it to the correct answer.
    if check_translation(model, tokenizer, prompt, completion):
        num_correct += 1

print(f"\nResult: {num_correct}/{num_examples} correct.")
[IMAGE_PLACEHOLDER: Screengrab of the base model evaluation results, showing a mix of correct and incorrect answers and the final score "Result: 7/13 correct."]

Now, we'll configure Low-Rank Adaptation (LoRA) to fine-tune our model efficiently. LoRA freezes the model's original weights and adds a small number of new, trainable parameters. This makes the training process much faster and more memory-efficient.

# LoRA configuration
lora_config = LoraConfig(
    r=64,  # Rank of the update matrices. Lower is fewer parameters.
    lora_alpha=16,  # LoRA scaling factor. Generally set to 16.
    lora_dropout=0.05,  # Dropout for LoRA layers
    bias="none",
    task_type="CAUSAL_LM",
)

# Wrap the base model with LoRA layers
model = get_peft_model(model, lora_config)

# Print the percentage of trainable parameters
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
print(
    f"Trainable params: {trainable_params:,} / {total_params:,} ({100 * trainable_params / total_params:.2f}%)"
)
Notice that we are only training about 2.67% of the total parameters, which is what makes LoRA so powerful.

Trainable params: 3,686,400 / 138,201,408 (2.67%)
Next, we define our training arguments using SFTConfig. This controls settings like the output directory, batch size, number of epochs, and learning rate.

# Training arguments for the SFTTrainer
training_args = SFTConfig(
    output_dir="data/model_demo",      # Directory to save artifacts
    per_device_train_batch_size=8,      # Small batch size for demo
    num_train_epochs=20,                # Number of times to go through the data
    learning_rate=2e-4,                 # Controls how much the model weights are updated
    gradient_accumulation_steps=2,      # Two forward and backward passes per update step
    logging_steps=50,                   # Log training progress every 50 steps
    save_strategy="no",                 # Don't save model checkpoints
    report_to=[],                       # Disable reporting to services like Weights & Biases
    fp16=False,                         # Use full precision (fp32) for wider compatibility
)
Finally, we create an SFTTrainer instance with our model, datasets, and arguments, and then call trainer.train() to begin the fine-tuning process.

# Create the SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=ds["train"],
    eval_dataset=ds["test"],
    args=training_args,
)

# Start the training process!
print("--- Starting Training ---")
trainer.train()
print("--- Training Complete ---")
With training complete, we run the same evaluation loop one last time to see if our fine-tuned model has learned the task.

print("--- Evaluating Fine-Tuned Model (After Training) ---")
num_correct = 0
num_examples = len(ds["test"])

for example in ds["test"]:
    prompt = example["prompt"]
    completion = example["completion"]
    if check_translation(model, tokenizer, prompt, completion):
        num_correct += 1

print(f"\nResult: {num_correct}/{num_examples} correct.")
The output shows that the model's performance has improved, confirming that our fine-tuning was successful.

After a short, efficient training run using PEFT, the model's performance on the new task improved, demonstrating the effectiveness of this fine-tuning approach.






Welcome. We're going to walk through a short demonstration of how to teach a large language model a new skill, using Supervised Fine-Tuning or SFT and Parameter Efficient Fine-Tuning or PEFT. While LLMs are very capable, they don't know everything, obviously. Sometimes we need to teach them a new specific task. In this demo, we'll teach a small LLM how to add the suffix ISH to the end of words. Here's a quick outline of what we'll cover. First, we'll handle the initial setup then we'll load a small pre trained model. Next, we'll create a simple data set for a new task. After that, we'll evaluate the model's performance before any training to get a baseline, then we'll configure a technique called LoRA to train the model efficiently. Finally, we'll evaluate the model again to see how much it has learned. Let's begin with the setup. In this cell, we import all the libraries we need for this demo. This includes torch for the CR machine learning framework, data sets from Hugging Face for data handling, and transformers, PEFT, and TRL, for the model, tokenizer, and training components. We also have a bit of logic to select the best available hardware, like a GPU, if you have one, to make everything run faster. Now, for first step, we'll load the tokenizer and the base model we'll be starting with. Here, we're loading a model called Small LM2 from the Hugging Face hub. It's a small model with about 135 million parameters, which makes it perfect for a quick demonstration. We load both a tokenizer, which prepares our text into a format, the model understands, and the model itself. Finally, we move the model to our selected device, like the GPU. Next, in Step 2, we'll create the dataset that we'll use to teach a model or new task. This cell simply defines a Python list of words. We'll use these words to automatically generate the examples for training and test datasets. This is where we actually build the dataset. We have a function called generate records that takes each word from our list and formats it into a prompt to completion. The prompts provides instructions in a couple of examples, and the completion is a correct answer the model should learn to produce. We then create a hugging face data set, split it into a training set and test set, and print the first training example, so you can see its structure. For Step 3, we'll evaluate the base model. Before we start training, it's crucial to see how well the model can already perform the task. This gives us a baseline to measure our improvement against. This cell defines a helper function that we'll use to test the model. It takes a prompt, has a model generated response, extracts just the answer, and then compares it to the correct completion to see if the model got it right. It will print a check mark for correct answers and the next for an incorrect one. Now, we run the evaluation on our test set using the base model. As you can see from the output, the model gets some of them right, but it's not perfect. The final score shows us exactly how many it answered correctly out of the total. This is our baseline performance. The model's performance is okay, but we can improve it with fine tuning. For Step 4 we'll configure LoRA and train the model. LoRA, which stands for low rank adaptation, is a parameter efficient fine tuning method. It freezes and models original weights and only trains a small number of new parameters, making the training process much faster and more memory efficient. Here, we set up the LoRA configuration. We then use the get PEFT model function to apply this configuration to our base model. The output here is key. Notice that we're only going to train about 2.67% of the models total perimeters. This is what makes LoRA so powerful. With LoRA configured, we now need to set the training arguments. This cell defines our training arguments using the SFT configure object. Here, we specify things like where to save the output, the batch size, the number of training epics, and the learning rate. These settings control how the training process runs. Now we put it all together. We train an SFT trainer passing in our LoRA configured model, our training and evaluation data sets, and the arguments we just defined. Then we call trainer.train to start the fine tuning process. You can watch the training progress bar and see the training loss go down as a model learns. Training is complete. Now for the final step, evaluating our fine tune model. Let's see if our efforts paid off and the model has learned its new skill. We run the exact same evaluation loop as before. But this time on our newly fine tuned model. As the output shows, the model is now getting more of the answers correct. The final score at the bottom confirms its improved performance on the test dataset. That's a success. After a very brief training session on a tiny dataset, our model's performance on the task improved. It went from seven correct answers to nine. While a modest improvement, it clearly shows that perimeter efficient fine tuning is a way an effective way to teach a model new skills.