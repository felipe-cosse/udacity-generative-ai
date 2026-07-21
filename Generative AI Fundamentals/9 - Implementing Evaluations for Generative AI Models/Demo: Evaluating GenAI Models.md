How do you know if a Generative AI model is performing well? Measuring the quality of generated text, code, or other outputs is a critical challenge. This demo walks through several common evaluation techniques, from simple string comparison to using another AI as a judge, providing a toolkit for assessing model performance.

Environment Setup and Workspace Access
Navigate to the file explorer and open: cd13303-genai-c1-classroom/module-8-implementing-evaluations-for-generative-ai-models/demo/demo.ipynb
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To run commands in the terminal activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.

This notebook provides a brief demonstration of several common techniques used to evaluate the output of Generative AI models. First, we'll run some initial setup, including importing the necessary libraries. This brings in tools for data handling, math, and specific evaluation metrics.

# Import necessary libraries
import numpy as np
from evaluate import load
from sentence_transformers import SentenceTransformer
import random

# Set a seed for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
Exact Match (EM)
Our first technique is Exact Match. This is the simplest and strictest evaluation metric. It checks if the model's output is perfectly identical to the reference answer. It's most useful for tasks that have a single, clear correct answer, like a multiple-choice question.

In this example, we compare a list of predicted fruit names against the correct labels. We define a simple normalize function to make the text lowercase and remove extra whitespace before comparing.

# Let's compare predicted fruit names with the correct labels.
preds = ["Apple", "banana ", " Orange"]
labels = ["apple", "banana", "grape"]

def normalize(s: str) -> str:
    """Normalize a string by lowercasing and stripping whitespace."""
    return s.lower().strip()

def exact_match(pred: str, label: str) -> int:
    """Return 1 if normalized strings are identical, else 0."""
    return int(normalize(pred) == normalize(label))

# Calculate EM score for each pair
em_scores = [exact_match(p, l) for p, l in zip(preds, labels)]

# The final score is the average of individual scores
em_accuracy = sum(em_scores) / len(em_scores)

print(f"Individual Scores: {em_scores}")
print(f"Average Exact Match Accuracy: {em_accuracy:.2f}")
As you can see from the output, two of the three predictions match perfectly after normalization, so the average accuracy is about 67%.

Lexical Similarity (ROUGE)
Exact Match is too strict when a correct answer can be phrased in different ways. For that, we can use ROUGE (Recall-Oriented Understudy for Gisting Evaluation). Instead of requiring a perfect match, ROUGE measures the overlap of words or n-grams between the model's prediction and the reference label. It's very commonly used for evaluating text summarization.

Here, we compare two sentences with similar words but different structures. We use the evaluate library to load the ROUGE metric. The output shows two scores:

ROUGE-1 measures the overlap of individual words.
ROUGE-L measures the longest common sequence of words.
# Define a prediction and a reference text
pred = "the quick brown fox"
label = "the fox is quick and brown"

# Load the ROUGE metric from the 'evaluate' library
rouge = load("rouge")

# Compute the scores
results = rouge.compute(predictions=[pred], references=[label])

print(f"ROUGE-1 Score: {results['rouge1']:.4f}")
print(f"ROUGE-L Score: {results['rougeL']:.4f}")
The high scores indicate a strong lexical similarity between the two sentences.

Semantic Similarity
What if two sentences mean the same thing but use completely different words? That's where Semantic Similarity comes in. This technique converts sentences into numerical vectors called embeddings and then measures the similarity between them, typically using cosine similarity. A score close to 1.0 means the sentences are very similar in meaning.

First, we load a pre-trained model good at creating sentence embeddings. We then generate embeddings for our predictions and labels and calculate the cosine similarity for each pair.

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Define prediction and label sentences
labels = ["A dog is a loyal pet", "Cats are independent animals", "The sky is blue"]
preds = [
    "Dogs make great companions",
    "A cat is a solitary creature",
    "The ocean is vast",
]

# 3. Generate embeddings for each list
pred_embeddings = model.encode(preds)
label_embeddings = model.encode(labels)

# 4. Calculate cosine similarity for each pair
for i in range(len(preds)):
    similarity = np.dot(pred_embeddings[i], label_embeddings[i]) / (
        np.linalg.norm(pred_embeddings[i]) * np.linalg.norm(label_embeddings[i])
    )
    print(
        f"Pair {i + 1}:\n  Pred:  '{preds[i]}'\n  Label: '{labels[i]}'\n  Similarity: {similarity:.4f}\n"
    )
Notice the sentences about cats and dogs have a high similarity score because their meanings are related. In contrast, the sentences about the ocean and sky have a low score because they are semantically very different.

Functional Correctness
For tasks involving code generation, we need to know if the code actually works. Functional Correctness evaluates this by running the generated code against a set of unit tests. The final score is the proportion of tests that pass.

In this example, we have a Python function that is supposed to reverse and capitalize a string but contains a bug: it fails if the input contains a number. We test it with three inputs.

# This function is supposed to reverse and capitalize a string,
# but it has a bug: it fails if the string contains a number.
def reverse_and_capitalize(s: str) -> str:
    """Reverse and capitalize a string, with a hidden bug."""
    if any(char.isdigit() for char in s):
        return "ERROR - CONTAINS DIGITS"
    return s[::-1].upper()

# Test cases: one prediction will trigger the bug
code_preds = ["hello", "world1", "python"]
test_labels = ["OLLEH", "1DLROW", "NOHTYP"]

# Run the generated code against the test labels
results = []
for pred_code, label in zip(code_preds, test_labels):
    output = reverse_and_capitalize(pred_code)
    print(f"Input: '{pred_code}' -> Output: '{output}', Expected: '{label}'")
    results.append(output == label)

pass_rate = sum(results) / len(results)
print(f"\nProportion of tests passed: {pass_rate:.2f}")
The function works for "hello" and "python" but fails for "world1". As a result, the pass rate is 2 out of 3, or about 67%.

Pass@k
Sometimes we ask a model to generate multiple (k) possible answers for a single problem. The Pass@k metric measures if at least one of these k attempts is correct. If any sample is correct, the entire set is considered a "pass" with a score of 1.

Here, we imagine a model generated four possible answers when asked to name a primary color. Our function checks if the correct label, "blue," is present in the list of samples.

def pass_at_k(samples: list[str], label: str) -> int:
    """Return 1 if any sample in the list matches the label, else 0."""
    return int(any(s == label for s in samples))

# The model generated 4 possible answers for "Name a primary color."
label = "blue"
samples = ["red", "yellow", "green", "blue"]

# Check if any of the 4 samples is correct
pass_score = pass_at_k(samples, label)

print(f"Samples: {samples}")
print(f"Label: {label}")
print(f"Pass@4 Score: {pass_score}")
Since the correct answer is in the list, the function returns a score of 1, indicating a successful pass.

LLM-as-a-Judge
For complex and subjective tasks, like judging creativity or helpfulness, we can use another powerful LLM to act as a judge. We provide this judge with the model's prediction, a reference answer, and a detailed rubric. The judge then provides a score and its reasoning.

First, we define a clear rubric for scoring animal predictions. Our judge function then evaluates three different test cases based on this rubric.

# This is our rubric for the judge.
RUBRIC = """
Score 1.0 if the predicted animal is the same as the label.
Score 0.5 if the prediction is a different animal but from the same biological class (e.g., both are mammals).
Score 0.0 otherwise (e.g., a mammal and a reptile).
"""

# ... A mock function `llm_as_judge` is defined here to simulate an LLM's response ...

# --- Test Case 1: Perfect Match ---
score1 = llm_as_judge(pred="Lion", label="Lion", rubric=RUBRIC)
print(f"--> Final Score: {score1}\n")

# --- Test Case 2: Same Class ---
score2 = llm_as_judge(pred="Tiger", label="Lion", rubric=RUBRIC)
print(f"--> Final Score: {score2}\n")

# --- Test Case 3: Different Class ---
score3 = llm_as_judge(pred="Snake", label="Lion", rubric=RUBRIC)
print(f"--> Final Score: {score3}\n")
The first case is a perfect match, scoring 1.0. The second compares two different animals from the same biological class, giving a 0.5. The third compares animals from different classes, which correctly scores 0.0.

Choosing the right metric from this toolkit is crucial for accurately understanding your model's performance and making targeted improvements.




Notebook provides a brief demonstration of several common techniques used to evaluate the output of generative AI models. We'll walk through simple clear examples for each method. This cell handles the initial setup for using the Light LLM library, which allows us to interact with different large language models. Here, we import the necessary Python libraries for this demo. This brings in tools for data handling, math, and the specific evaluation metrics we'll be using. Now, we'll look at our first technique, exact match. This is the simplest and strictest evaluation metric. It checks if the models output is perfectly identical to the reference answer. It's most useful for tasks that have a single, clear, correct answer, like a multiple choice question. In this example, we compare a list of predicted fruit names against the correct labels. We define a simple normalized function to make the text lower case and remove extra white space before comparing. As you can see from the output, two of the three predictions match perfectly after normalization, so the average accuracy is about 67%. Now, exact match is too strict when a correct answer can be phrased in different ways. For that, we can use Rouge, which stands for recall oriented under study for disting evaluation. Rouge doesn't require a perfect match. Instead, it measures the overlap of words or n grams between the models prediction and the reference label. It's very commonly used for evaluating text summarization. Here, we compare two sentences that have similar words, but different structures. We use the evaluates library to load the rouge metric. The output shows two scores. Rouge1 measures the overlap of individual words. While rougel measures the longest common sequence of words. The high scores indicate a strong lexical similarity. What if two sentences mean the same thing but use completely different words? That's where semantic similarity comes in. This technique converts sentences into numerical vectors called embeddings, and then measures the similarity between them. A score close to one means the sentences are very similar in meaning. First, we load a pre trained model that's good at creating these sentence embeddings. We then generate embeddings for a list of predictions and labels and calculate the cosine similarity for each pair. Notice that the sentences about cats and dogs have a high similarity score because their meanings are related. In contrast, the sentences about the ocean in the sky have a low score because they are semantically very different. For tasks involving code generation, we need to know if the code actually works. Functional correctness evaluates by simply running the generated code against a set of unit tests. The final score is a proportion of tests that pass. In this example, we have a Python function that's supposed to reverse and capitalize a string. However, it contains a bug. It fails if the input string contains a number. We test it with three inputs. The function works for hello and Python, but fails for World1. As a result, the pass rate is two out of three or about 67%. Sometimes, we ask a model to generate multiple possible answers for a single problem. The pass at K metric is used in the scenario. It measures if at least one of these k attempts is correct. Here, we imagine the model generated four possible answers when asked to name a primary color. Our pass a K function checks if the correct label, blue is present in the list of samples. Since it is, the function returns a score one, indicating a successful pass. For complex and subjective tasks, like judging creativity or helpfulness, we can use another powerful LLM to act as a judge. We provide this judge with a model's prediction, a reference answer, and a detailed rubric. The judge then provides a score and its reasoning. First, we define a clear rubric for scoring animal predictions. Our judge function then evaluates three different test cases based on this rubric. The first is a perfect match, which scores a one. The second compares two different animals from the same biological class, which gives a 0.5. The third compares animals from different classes, which correctly scores zero. That's a quick tour of several key evaluation methods. Each one has its strengths and is suited for different types of tasks. Choosing the right metric is crucial for understanding your model's performance and making improvements.