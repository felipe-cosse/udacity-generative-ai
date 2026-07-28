Large language models (LLMs) are notoriously bad at spelling. This is partly because tokenizers break words into smaller pieces, so the model learns about sub-word units rather than whole words and their spellings.

In this exercise, you'll use supervised fine-tuning (SFT) and a technique called Parameter-Efficient Fine-Tuning (PEFT) with Low-Rank Adaptation (LoRA) to teach a small LLM how to spell words. This is a classic example of teaching a model a new skill that isn't well-represented in its pre-training data.

Prerequisites
Understanding of Large Language Models (LLMs).
Familiarity with the Hugging Face transformers and datasets libraries.
Basic knowledge of model fine-tuning concepts like SFT and PEFT/LoRA.
Instructions
In the cell under the "Step 1. Load the tokenizer and base model" heading, replace the *********** placeholders to load the model and tokenizer.
Navigate to the generate_records function and construct the prompt.
In the check_spelling function, implement the logic to evaluate the model's performance. Replace all the commented-out placeholder lines inside the function.
In the cell under the "Step 4. Configure LoRA and train the model" heading, uncomment and complete the LoRA configuration.
In the next cell, uncomment and define the training arguments by completing the SFTConfig.
In the final task cell, create an instance of SFTTrainer and begin the training process. Uncomment the lines and complete them.
Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace by clicking on the Cloud Resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-16-applying-peft-on-foundation-models/exercises/starter/
Double-click the teach-an-llm-to-spell-with-sft-starter.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv2) from the list.
If the kernel is not listed, click the *refresh icon* at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv2/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.