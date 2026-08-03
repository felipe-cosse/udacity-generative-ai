Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-12-generating-text-using-llms/exercises/solution/
Double-click the generating-one-token-at-a-time-solution.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.

The first step is to load a pre-trained gpt2 model and its corresponding tokenizer from the Hugging Face transformers library. This is accomplished with the from_pretrained method on the AutoTokenizer and AutoModelForCausalLM classes.

# from transformers import AutoModelForCausalLM, AutoTokenizer
# ...
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
After tokenizing an initial sentence, we use the model to predict the probabilities of all possible next tokens. The task is to identify the single most likely token by finding the index of the highest probability value in the probabilities tensor. We use torch.argmax for this and .item() to convert the resulting tensor to a standard Python number.

# ...
# Get the id of the most probable next token...
next_token_id = torch.argmax(probabilities).item()
# ...
The output shows the ID and the decoded token for the most probable next word, which is "programming."

Next token id: 8300
Next token:  programming
While we can append this token and repeat the process manually, it's inefficient for generating longer text. A better approach is to use the model's built-in .generate() method, which handles the entire token-by-token generation process internally. We provide the starting text and specify a max_length for the output.

# ...
# Start with some text and tokenize it
text = "Once upon a time, generative models"
inputs = tokenizer(text, return_tensors="pt")

# Use the `generate` method to generate a max of 100 tokens
output = model.generate(**inputs, max_length=100, pad_token_id=tokenizer.eos_token_id)

# Show the generated text
# display(Markdown(tokenizer.decode(output[0])))
The method produces a complete block of text. While gpt2 is an older model and may repeat itself, the generated text is coherent.

Once upon a time, generative models of the human brain were used to study the neural correlates of cognitive function. In the present study, we used a novel model of the human brain to investigate the neural correlates of cognitive function. We used a novel model of the human brain to investigate the neural correlates of cognitive function. We used a novel model of the human brain to investigate the neural correlates of cognitive function. We used a novel model of the human brain to investigate the neural correlates of cognitive function.
Key Takeaway
LLMs generate text autoregressively, predicting one token at a time based on the preceding sequence, a process that can be streamlined using a model's built-in generate method.





In this exercise, we see how a large language model generates text. The key takeaway is that it happens one piece or token at a time, using the previous token to predict the next one. The first step is to load a model and a tokenizer from the hugging face library. A tokenizer is what converts our text into a numerical format that the model can process. Here, we load the pre trained GPT-2 model and its corresponding tokenizer. With a transformers library, this takes only two lines of code. Now, we define a starting sentence and pass it to the tokenizer. The output you see is a tensor, which is essentially a list of numbers. Each number is an ID that represents a specific token from our original sentence. Next, let's explore what these token IDs actually mean. This table shows our original sentence broken down into tokens. Notice how some words like is and the are single tokens. But udacity is split into U, D, and acity. This process is called subword tokenization. It allows a model to handle words it hasn't seen before. Now that we understand how text is converted into tokens, we're ready for the next step, using the model to calculate the probability of the next token. Here, we feed our tokenized sentence into the model. The model then predicts a likelihood of every possible token in its vocabulary being the next one. This table displays a top five most likely candidates. The model thinks programming and learning are the most probable words to come next. As a note says, the model's top predictions make a lot of sense in the context of our sentence. In this cell, we programmatically grab the single most probable token. We use the arc Max function to find a token ID with the highest probability, and then decode it back into text. As expected, the model's top choice is programming. Now, we simply add the newly predicted token to the end of our original sentence, making it longer. We've seen how to generate one token. The next step, we'll run a cell repeatedly to generate even more text and watch the process in action. Every time the cell runs, it takes a current text, calculates the probabilities for the next token, displays the top choices, and then appends the single most likely token to our text. You can run the cell over and over again to see the sentence grow. Generating tokens one by one, like that, is great for understanding, but it's inefficient. Now, we'll see how to use a models built in dot generate method to produce a lot of text at once. With a generate method, we provide a starting prompt and tell the model the maximum length of the text we want. The model then handles the entire token by token generation process internally and returns a final result, which you see displayed here. Looking at the output, you can see that GPT-2 is functional, but not as advanced as modern models. It has a tendency to repeat itself. Still, it's impressive that it can generate text that is more or less grammatically coherent. Congratulations for finishing the exercise. You now have a foundational understanding of the auto regressive token by token process that allows LLMs to generate text.