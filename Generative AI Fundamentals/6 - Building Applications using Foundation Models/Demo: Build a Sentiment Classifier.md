This demo walks through building a simple sentiment classifier for movie reviews using a foundation model. You'll see how to prepare data, classify text using a basic "zero-shot" prompt, and then improve the model's performance by providing examples in a "few-shot" prompt. This is a common approach for solving text classification problems quickly and effectively.

In this demonstration, we'll build a simple sentiment classifier for movie reviews using a foundation model. We'll start by preparing a small dataset, then build a basic classifier with a zero-shot prompt, and finally, see how it improves with a few-shot prompt.

First, we set up our connection to the model's API. This code detects if a Vocareum API key is being used and configures the base URL automatically.

import litellm
import os

if os.getenv("OPENAI_API_KEY"):
    litellm.openai_key = os.getenv("OPENAI_API_KEY")

# ... other setup code ...

if (litellm.openai_key or "").startswith("voc-"):
    litellm.api_base = "https://openai.vocareum.com/v1"
    print("Detected vocareum API key. Using Vocareum OpenAI API base URL.")
Step 1: Prepare the Data
Next, we create a small, hard-coded dataset of five movie reviews. Each review has a text snippet and a numeric label, where 1 indicates a positive sentiment and 0 indicates a negative one.

# A tiny, sample dataset of movie reviews
demo_dataset = [
    {"review": "An absolute masterpiece, the best film of the year!", "label": 1},  # 0
    {
        "review": "I was bored from start to finish. A total waste of time.",
        "label": 0,
    },  # 1
    {
        "review": "The acting was incredible and the story was so moving.",
        "label": 1,
    },  # 2
    {"review": "While not perfect, it had some good moments.", "label": 1},  # 3
    {"review": "A confusing plot and terrible dialogue.", "label": 0},  # 4
]

print(f"Dataset created with {len(demo_dataset)} reviews.")
The numeric labels 0 and 1 are great for machine learning but aren't very descriptive for humans. We'll map them to more intuitive, human-readable strings: "NEGATIVE" and "POSITIVE".

# Map numeric labels to human-readable labels
id2label = {0: "NEGATIVE", 1: "POSITIVE"}

# Print the first two entries to see the new labels
for i in range(2):
    review = demo_dataset[i]["review"]
    label_id = demo_dataset[i]["label"]
    print(f"label={id2label[label_id]}, review={review}")
Step 2: Build a Basic Classifier (Zero-Shot)
With our data ready, we can build our first classifier using a zero-shot prompt. This means we'll tell the model what to do without providing any examples. First, we format all our reviews into a single string for the user prompt. Then, we define a system prompt that tells the model its role and instructs it to respond only with a JSON object.

# First, format our reviews into a single string for the prompt
reviews_string = ""
for i, entry in enumerate(demo_dataset):
    reviews_string += f"{i} -> {entry['review']}\n"

# Define the prompts
SYSTEM_PROMPT = """You are a helpful assistant that classifies movie reviews as POSITIVE or NEGATIVE.
Respond only with a JSON object where the keys are the review numbers and the values are the classification."""

USER_PROMPT = reviews_string
Now, we send our system and user prompts to the model.

from litellm import completion

resp = completion(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
)

print("\nMODEL RESPONSE:")
print(resp.choices[0].message.content)
The model correctly classifies all five reviews and returns the response in the requested JSON format.

{
  "0": "POSITIVE",
  "1": "NEGATIVE",
  "2": "POSITIVE",
  "3": "POSITIVE",
  "4": "NEGATIVE"
}
To evaluate the performance, we'll store the model's response in a variable and use a helper function to calculate the accuracy.

# Let's paste the response here
response_1 = {
    "0": "POSITIVE",
    "1": "NEGATIVE",
    "2": "POSITIVE",
    "3": "POSITIVE",
    "4": "NEGATIVE",
}

def get_accuracy(response, dataset):
    correct = 0
    total = len(response)

    for entry_number, prediction in response.items():
        entry_number = int(entry_number)
        actual_label_id = dataset[entry_number]["label"]
        actual_label = id2label[actual_label_id]

        if prediction.lower() == actual_label.lower():
            correct += 1
        else:
            print(
                f"Mismatch for entry {entry_number}: predicted={prediction}, actual={actual_label}"
            )

    accuracy = correct / total * 100
    return accuracy

accuracy_1 = get_accuracy(response_1, demo_dataset)
print(f"Accuracy: {accuracy_1}")
Our zero-shot classifier achieves 100% accuracy on this small dataset.

Step 3: Build an Improved Classifier (Few-Shot)
While our model performed perfectly, on a larger or more complex dataset, it might need more guidance. We can provide this guidance using a "few-shot" prompt, which includes examples directly in the prompt. We'll create an improved system prompt by adding a section with two correctly labeled examples.

# Create a string with the first two reviews as examples
example_string = """
Here are some examples:

EXAMPLE INPUT:
0 -> An absolute masterpiece, the best film of the year!
1 -> I was bored from start to finish. A total waste of time.

EXAMPLE OUTPUT:
{
  "0": "POSITIVE",
  "1": "NEGATIVE"
}
"""

# The new SYSTEM_PROMPT now includes the examples
IMPROVED_SYSTEM_PROMPT = SYSTEM_PROMPT + example_string
Now, we send the new few-shot prompt to the model. The user prompt containing the reviews to be classified remains the same.

resp = completion(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": IMPROVED_SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
)
print("\nMODEL RESPONSE:")
print(resp.choices[0].message.content)
The model processes the request and again returns the classifications in the specified JSON format. We calculate the accuracy just as before.

response_2 = {
    "0": "POSITIVE",
    "1": "NEGATIVE",
    "2": "POSITIVE",
    "3": "POSITIVE",
    "4": "NEGATIVE",
}

accuracy_2 = get_accuracy(response_2, demo_dataset)
print(f"Accuracy: {accuracy_2}")
Again, we get a perfect score of 100%. While prompt engineering techniques like few-shot prompting can improve a model's accuracy, it's important to remember that this tiny demo isn't enough to prove it definitively. To truly validate the improvement for a specific use case, you would need a much larger dataset and a more rigorous evaluation process.

By crafting clear system prompts, you can guide foundation models to perform specific text classification tasks and improve their accuracy by providing in-prompt examples.