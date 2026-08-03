Large language models can seem like magic, but their text generation process is a logical, step-by-step routine. This demo demystifies that process by showing how a model reads a text prompt, converts it to numbers, and then predicts the next word in the sequence. We'll build up from generating a single token to a full sentence.

Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-12-generating-text-using-llms/huggingface-demo/
Double-click the huggingface_demo.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.W

First, we load a pre-trained model and its tokenizer from the Hugging Face transformers library. For this demo, we use distilgpt2, a smaller, more efficient version of GPT-2, which is great for quick demonstrations. The tokenizer will convert our text prompt into numbers (tokens), and the model will predict the next tokens in the sequence.

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "distilgpt2"

# Load the tokenizer and model for "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
Next, let's define a prompt and see how the tokenizer handles it. The process of converting text into a sequence of token IDs is called tokenization.

# Define a starting phrase, or prompt
prompt_text = "Machine learning is a field of"

# Convert the text prompt into input tensors for the model
inputs = tokenizer(prompt_text, return_tensors="pt")

print("Prompt text:", prompt_text)
print("Token IDs:", inputs["input_ids"])
The output shows the numerical representation of our prompt:

Prompt text: Machine learning is a field of
Token IDs: tensor([[37573,  4673,   318,   257,  2214,   286]])
To understand what these IDs mean, we can decode each one back into text. This reveals the model's use of subword tokenization, where some tokens are complete words (Machine, is) while others might be parts of words or punctuation.

# Get the list of token IDs
token_ids = inputs["input_ids"][0].tolist()

# Decode each token ID back to its string representation
tokens = [tokenizer.decode(token_id) for token_id in token_ids]

# Display the IDs and their corresponding tokens
# ... (pandas DataFrame creation omitted for brevity)
Here is the mapping from ID to token for our prompt:

   ID     Token
37573   Machine
 4673  learning
    318        is
    257         a
 2214     field
    286        of
Now, let's feed these token IDs to the model to predict the single most likely next token. The model outputs raw scores called logits. We convert these logits into probabilities using a softmax function and then find the token with the highest probability using torch.argmax.

with torch.no_grad(): # Disable gradient calculations for inference
    # Get the model's raw output (logits)
    outputs = model(**inputs)

    # We only need the logits for the last token in the sequence
    next_token_logits = outputs.logits[:, -1, :]

    # Convert logits to probabilities
    probabilities = torch.nn.functional.softmax(next_token_logits, dim=-1)

    # Find the token ID with the highest probability
    most_likely_next_token_id = torch.argmax(probabilities).item()

print(f"The most likely next token ID is: {most_likely_next_token_id}")
print(f"This token is: '{tokenizer.decode(most_likely_next_token_id)}'")
The model predicts the next token is " research":

The most likely next token ID is: 2267
This token is: ' research'
By repeating this process—predicting the next token and appending it to our input—we can generate a longer sequence. Here, we run this loop five times to generate five new tokens.

# Start with our initial tokenized prompt
generated_ids = inputs["input_ids"]

print("Generating 5 tokens one at a time:")

# This loop generates one token at a time
for _ in range(5):
    with torch.no_grad():
        outputs = model(generated_ids)
        next_token_logits = outputs.logits[:, -1, :]
        next_token_id = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)

    # Append the new token to the sequence
    generated_ids = torch.cat([generated_ids, next_token_id], dim=-1)

# Decode and print the final sequence
print(tokenizer.decode(generated_ids[0]))
This manual, step-by-step generation produces the following output:

Generating 5 tokens one at a time:
Machine learning is a field of research that has been growing
While instructive, generating tokens one-by-one is inefficient. The transformers library provides a convenient .generate() method that automates this entire loop for us. We can specify a max_length to control the length of the output.

from IPython.display import Markdown, display

# Use the .generate() method to create a sequence of 50 tokens
output_ids = model.generate(
    **inputs, max_length=50, pad_token_id=tokenizer.eos_token_id
)

# Decode the entire sequence into a single string
generated_text = tokenizer.decode(output_ids[0])

print("--- Text Generated with model.generate() ---")
display(Markdown(generated_text))
The .generate() method produces a more complete and coherent completion of our original prompt.

--- Text Generated with model.generate() ---
Machine learning is a field of research that has been growing in the past few years.
This walkthrough reveals that text generation is an iterative process where a model predicts the most probable next token based on the sequence it has seen so far.








In this lesson, we're taking a deep dive into HuggingFace. HuggingFace is a company that has become central to the world of natural language processing or NLP. They are best known for their open source library, transformers, which gives developers and researchers easy access to thousands of cutting edge models. We're going to focus on four key components of the HuggingFace ecosystem. We'll start with tokenizers which prepare text for a model, then we'll look at models, the core of the library. After that, we'll explore data sets, which is how we access data for training. Let's begin with tokenizers. Tokenization is a process of breaking down texts into smaller pieces called tokens that a model can understand. Here, we're loading a pre-train tokenizer from the transformers library. Specifically, it's a tokenizer for the bert-base-uncased model. We can see that this particular tokenizer has a vocabulary of 30,522 unique tokens. Let's look at that in a bit more detail. The name, bert-base-uncased tells us that the model doesn't differentiate between upper case and lower case letters. The vocabulary of over 30,000 tokens is made up of a mix of characters, words, and parts of words. Now let's see it in action. We're taking the sentence "I heart generative AI" and running it through a tokenizer. As you can see, the tokenizer has split her sentence into several tokens. Interestingly, the word generative was broken down into two separate tokens, genera and tive. This is a common technique that allows a model to understand words it hasn't seen before. While these string tokens are easy for us to read, the model works with numbers. This next step converts those string tokens into their unique numerical IDs from the tokenizers vocabulary, and here are the results. These are the actual numbers that the model will process, representing our original sentence. It's worth noting that HuggingFace tokenizers are incredibly fast. They are written in a programming language called Rust, which makes them highly efficient, even when processing huge amounts of text. Next up, let's talk about models. The HuggingFace hub is home to a massive collection of open source models, including famous ones like GPT, Qwen, and Google's Gemini models, as well as many specialized versions, fine tuned by the community. In this cell, we are downloading one of these pre-trained models. We're grabbing a model that has been fine-tuned for sentiment analysis on movie reviews. Our goal is to use this model to classify the sentiment of the sentence, "I love generative AI." The model we've chosen is based on bert. It's uncased, and it has been specifically trained by user named text attack on the IMDB movie review data set. Now, we pass our sentence of the tokenizer, and then we feed the resulting token IDs into the model. The code then processes models output to determine if the sentiment is positive or negative and calculates a confidence of that prediction. Let's break down what just happened. First, the input sentence was tokenized, second, we told the model, we're just making a prediction, not training it, which is what no grad means. Third, the model produced probabilities for positive and negative sentiment. Finally, we checked which probability was higher and printed the result. The model is 89% confident that I love generative AI has a positive sentiment. Now let's turn our attention to the data sets library. This library is a powerful tool designed to make it easy to access and work with the vast amounts of data needed for AI projects. Here, we're importing the low data set function from the library. With a just as one line of code, we can download and load the entire IMDB movie review data set. It's that simple. The library gives us a standardized way to work with thousands of different data sets. Now that we have the data set loaded, let's take a look at the specific example. We're going to pull out review number 42 from the training set and print its text along with its corresponding label. Here's the review. It starts with a spoiler warning and is quite critical of the film, even making a sarcastic remark about the close encounters of the third kind. The label is negative, which definitely seems appropriate after reading the text. Just like the Tokenizers library, the Data Sets library is built for efficiency. It uses a technology called apache arrow in the background, which allows it to process even massive data sets very quickly without using a lot of memory. Finally, let's take a look at the trainer class. HuggingFace also simplifies the process of training a model. The trainer handles all the complicated parts of a training loop, like optimization and evaluation. To set up our training job, we first load a pre-trained model and its tokenizer. We then define a function that will tokenize our data set entries, making sure to pad shorter reviews and truncate longer ones so they are all the same length. We then load the IMDB data set, and to make this demonstration run quickly, we select a small subset of 100o examples for training and 1000 for testing. Finally, we apply our tokenization function to the subset. Next, we need to define our training arguments. This training arguments object lets us configure all the hyper-parameters for a training run. Here, we're setting things like the output directory, the learning rate, the batch size, for training and evaluation, and the total number of training epics. With our arguments defined, we've set the essential parameters for a training process. We've specified where to save the results and how the model should learn, and for how long. We've also told the trainer which data splits to use for training and for evaluation. Now, we create an instance of the trainer class, passing in or model, the training arguments, our prepared data sets, and the tokenizer. Then with everything in place, we start the training process by simply calling trainer.train. As a trainer runs, the trainer class is handling the entire fine tuning loop for us. We can monitor its progress here. This abstracts away the need to write our own complex training loop. Just to quickly review the data preparation one last time. We're starting with a distill bert-based-uncased model and its tokenizer. We have a function that prepares text by tokenizing, padding, and truncating it. We're using a small subset of the IMDB data set to ensure the training process is fast for this demo. We then map our tokenization function across this data to get it ready for the model.