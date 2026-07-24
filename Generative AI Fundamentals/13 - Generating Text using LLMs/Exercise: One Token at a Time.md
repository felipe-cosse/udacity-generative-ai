In this exercise, you will get to understand how an LLM generates text: one token at a time, using the previous tokens to predict the following ones. You will load a model and tokenizer from Hugging Face, calculate the next token in a sequence, and finally use the model's built-in generate method to create a longer piece of text.

Prerequisites
Familiarity with the Hugging Face transformers library.
Basic knowledge of PyTorch.
Understanding of the concept of tokenization.
Instructions
In the third code cell, under the heading "Step 1. Load a tokenizer and a model", load the pre-trained gpt2 tokenizer. Replace the commented-out line # tokenizer = ********** with tokenizer = AutoTokenizer.from_pretrained("gpt2").

In the same cell, load the pre-trained gpt2 model for causal language modeling. Replace the commented-out line # model = ********** with model = AutoModelForCausalLM.from_pretrained("gpt2").

In the ninth code cell, after calculating the token probabilities, obtain the ID of the most probable next token. Replace the commented-out line # next_token_id = ********** with next_token_id = torch.argmax(probabilities).item().

In the final code cell, under "Step 4. Use the generate method", use the model's generate method to create a sequence of up to 100 tokens. Replace the commented-out line # output = ********** with output = model.generate(**inputs, max_length=100, pad_token_id=tokenizer.eos_token_id).

Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-12-generating-text-using-llms/exercises/starter/
Double-click the generating-one-token-at-a-time-starter.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.