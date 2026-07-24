Large Language Models (LLMs) can seem like magic, but their text generation process is a logical, step-by-step procedure. This demo demystifies that process, showing exactly how a model like GPT-2 builds a sentence one piece at a time. Understanding this core mechanic is fundamental to effectively using and customizing generative AI models.

Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-12-generating-text-using-llms/generating-text-demo
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

First, we load a pre-trained model and its corresponding tokenizer from the Hugging Face transformers library. The tokenizer is a tool that converts our text into numbers the model can understand, and the model is what will predict the text. For this demo, we'll use distilgpt2, a smaller, more efficient version of GPT-2.

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# For this demo, we'll use 'distilgpt2', a smaller and faster version of GPT-2
model_name = "distilgpt2"

# Load the tokenizer and model associated with our chosen model name
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
Next, let's examine what the tokenizer does. We'll define a starting phrase, or prompt, and pass it to the tokenizer. This process, called tokenization, converts the string into a sequence of numerical token IDs.

# Define a starting phrase, also known as a prompt
prompt_text = "Machine learning is a field of"

# Use the tokenizer to convert the text prompt into input tensors for the model
inputs = tokenizer(prompt_text, return_tensors="pt")

# The 'input_ids' are the numerical representations of our text
print("Prompt text:", prompt_text)
print("Token IDs:", inputs["input_ids"])
To better understand these tokens, we can decode them back into text. You'll notice that some tokens are whole words, while others are parts of words. This method is called subword tokenization.

import pandas as pd

# Get the list of token IDs from our inputs
token_ids = inputs["input_ids"][0].tolist()

# Decode each token ID back to its string representation
tokens = [tokenizer.decode(token_id) for token_id in token_ids]

# Display the IDs and their corresponding tokens in a table for clarity
token_df = pd.DataFrame({"ID": token_ids, "Token": tokens})

print(token_df.to_string(index=False))
Now for the exciting part. We feed our sequence of token IDs into the model. The model's job is to predict the single most likely token that should come next. It calculates a probability for every possible token and selects the one with the highest score.

# We use torch.no_grad() to disable gradient calculations, as we are not training the model
with torch.no_grad():
    # Get the model's raw output, called 'logits'
    outputs = model(**inputs)

    # We only care about the logits for the very last token in our input sequence
    next_token_logits = outputs.logits[:, -1, :]

    # Convert logits into probabilities using the softmax function
    probabilities = torch.nn.functional.softmax(next_token_logits, dim=-1)

    # Find the token ID with the highest probability
    most_likely_next_token_id = torch.argmax(probabilities).item()

print(f"The most likely next token ID is: {most_likely_next_token_id}")
print(f"This token is: '{tokenizer.decode(most_likely_next_token_id)}'")
The model predicts that the token for " research" is the most likely to follow our phrase.

To generate longer sentences, we simply repeat this process. We predict the next token, add it to our input sequence, and then feed the new, longer sequence back into the model to predict the next token. This cell puts that idea into a loop to generate five new tokens.

# Let's generate a few more tokens by repeating the process in a loop
generated_ids = inputs["input_ids"]

print("Generating 5 tokens one at a time:")
print(tokenizer.decode(generated_ids[0]), end="")

# This loop generates one token at a time
for _ in range(5):
    with torch.no_grad():
        outputs = model(generated_ids)
        next_token_logits = outputs.logits[:, -1, :]
        next_token_id = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)

    # Append the newly predicted token ID to our sequence
    generated_ids = torch.cat([generated_ids, next_token_id], dim=-1)

    # Print the newly generated token
    print(tokenizer.decode(next_token_id[0]), end="")
Generating tokens manually in a loop is great for understanding the mechanics, but it's inefficient. Fortunately, the transformers library provides a simple .generate() method that automates this entire iterative process for us. We provide the same starting prompt and tell the model we want a sequence with a maximum length of 50 tokens.

from IPython.display import Markdown, display

# We start with the same tokenized prompt
inputs = tokenizer(prompt_text, return_tensors="pt")

# Use the .generate() method to create a sequence of a desired length
output_ids = model.generate(
    **inputs, max_length=50, pad_token_id=tokenizer.eos_token_id
)

# Decode the entire sequence of token IDs into a single string
generated_text = tokenizer.decode(output_ids[0])

print("--- Text Generated with model.generate() ---")
display(Markdown(generated_text))
This demo shows how a language model generates text by tokenizing an input and then iteratively predicting the most likely next token, one at a time.






This notebook demonstrates the core process of how a large language model or LLM generates texts. We'll go through this step by step, seeing how text is built one piece at a time. Our first step is to load a pre-trained model and its tokenizer from the Hugging Face library. The tokenizer is a tool that converts our text into numbers the model can understand, and the model is actually what predicts the next piece of text. We are loading the DistilGPT2, which is a smaller, more efficient version of GPT2. We're also loading the specific tokenizer that was trained with this model. Now, let's take a closer look at what the tokenizer does. This process is called tokenization, and we're about to see how a simple sentence is converted into a list of token IDs. Here, we define our starting phrase or prompt. Machine learning is a field of the tokenizer converts this text into a sequence of numbers or token IDs that you see in the output. This is the actual input the model will receive. To better understand these tokens, we can decode them back into text. It's important to notice that a token isn't always a full word. This method is called subword tokenization, where tokens can be parts of words, entire words, or punctuation. This table clearly shows each token ID from the previous step and the text it represents. You can see how our original phrase is broken down into six distinct tokens. Machine, learning, is, A, field, and of. Now for the exciting part. In step three, we feed our sequence of token IDs into the model. The model's job is to predict the single most likely token that should come next. After feeding the prompt to the model, it calculates a probability for every possible next token. As the output shows, the model predicts that the token with ID 2267, which corresponds to the word research is the most likely word to follow our phrase. How do we generate longer sentences? We simply repeat the process. We predict the next token, add it to our input sequence and then feed the new longer sequence back into the model to predict the next token. This cell puts that idea into practice with a loop. We start with our original prompt, and for five iterations, we ask the model to predict the next token and append it. The output shows the text being generated one token at a time, resulting in the phrase, machine learning is a field of research that has been growing. Generating texts manually like this is great for understanding the mechanics, but it's not very efficient. Fortunately, the transformers library gives us a simple.generate method that automates this entire loop for us. Here, we use that convenient.generate method. We provide the same starting prompt and tell the model, we want to sequence with a maximum length of 50 tokens. The model then handles the entire iterative process internally, and we can see the much longer, more complete text it generates. And that's it. This demonstration has walked through the fundamental logic of how an LLM generates text by tokenizing an input and then predicting the most likely next token, one at a time.