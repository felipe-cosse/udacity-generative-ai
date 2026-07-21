Accessing the Workspace
Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-8-implementing-evaluations-for-generative-ai-models/exercises/solution
Double-click the gen-ai-evaluation-medley-starter.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To run commands in the terminal, activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.

This exercise walks through several key techniques for evaluating generative AI models. We'll start with simple string comparisons and progress to more complex methods like semantic analysis and using another LLM as an evaluator.

First, we implement the exact_match function. The core logic involves normalizing both the predicted and label strings by making them lowercase and stripping whitespace, then checking for equality. We cast the resulting boolean to an integer (1 for a match, 0 otherwise).

# ...

def exact_match(pred: str, label: str) -> int:
    # return 1 if normalized strings are identical, else 0
    return_value = "**********"

    # <<< START SOLUTION SECTION
    return_value = int(normalize(pred) == normalize(label))
    # >>> END SOLUTION SECTION

    return return_value

# ...
Next, we calculate lexical similarity using the ROUGE score, which is common for evaluating text summaries. We use the Hugging Face evaluate library to import the load function, load the rouge metric, and compute the scores between our prediction and reference sentences.

# ...

# <<< START SOLUTION SECTION

# Import the evaluate library
from evaluate import load

# Load the ROUGE metric
rouge = load("rouge")

# Compute ROUGE scores
results = rouge.compute(predictions=[pred], references=[label])

# >>> END SOLUTION SECTION

# ...
For semantic similarity, we move beyond word matching to compare meaning. The task is to add a sentence to the preds list that is semantically different from its corresponding label. We then use a pre-loaded sentence-transformers model to encode all predictions and labels into numerical vectors, or embeddings.

# ...

labels = ["Cusco is in Peru", "Ayacucho is a region", "Trujillo beaches are marvelous"]
preds = [
    "Peru includes Cusco",
    "Ayacucho is a department",
    # Write a sentence that is very semantically different from the prediction
    # "***********"
    # <<< START SOLUTION SECTION
    "Turquoise is a marvelous color",
    # >>> END SOLUTION SECTION
]

# Get the embeddings for each sentence
pred_embeddings = "**********"
label_embeddings = "**********"

# <<< START SOLUTION SECTION
pred_embeddings = model.encode(preds)
label_embeddings = model.encode(labels)
# >>> END SOLUTION SECTION

# ...
A subsequent cell calculates the cosine similarity between these embedding pairs, confirming that our semantically different sentence has a much lower similarity score.

Pair 1:
    Pred: Peru includes Cusco
    Label: Cusco is in Peru
    Cosine Similarity: 0.9358

Pair 2:
    Pred: Ayacucho is a department
    Label: Ayacucho is a region
    Cosine Similarity: 0.7663

Pair 3:
    Pred: Turquoise is a marvelous color
    Label: Trujillo beaches are marvelous
    Cosine Similarity: 0.2680
To evaluate the functional correctness of code, we test if the output of a function matches the expected label. We complete the list comprehension to compare the output of sort_and_normalize(p) against each label l.

# ...

# Write tests to check if sort_and_normalize works correctly
results = [
    # "**********"
    # <<< START SOLUTION SECTION
    sort_and_normalize(p) == l
    # >>> END SOLUTION SECTION
    for p, l in zip(preds, labels)
]

# ...
The Pass@k metric is useful for code generation where a model might produce several solutions. It checks if at least one of the first k attempts is correct. We implement the pass_at_k function to return 1 if any of the provided samples exactly match the label.

# ...

# Implement pass_at_k with signature (samples: List[str], label: str) -> int
# **********

# <<< START SOLUTION SECTION
def pass_at_k(samples: list[str], label: str) -> int:
    return int(any(s == label for s in samples))

# >>> END SOLUTION SECTION

# ...
Finally, we implement the LLM-as-a-Judge technique. This involves creating a detailed system prompt that instructs a judge model on how to score a prediction based on a provided rubric. We also construct a user prompt with the prediction and label, call the LLM using litellm, and parse the final score from its response.

def llm_as_judge(pred: str, rubric: str, label: str | None = None) -> float:
    # ...
    # <<< START SOLUTION SECTION
    SYSTEM_PROMPT = f"""You are an expert evaluator. Use the following rubric to score the prediction.
    Format your response as:
    <reasoning>...</reasoning>
    <score>FLOAT_ANSWER</score>

    where FLOAT_ANSWER is a float between 0 and 1.

    RUBRIC:
    {rubric}
    """
    # >>> END SOLUTION SECTION

    # ...
    # <<< START SOLUTION SECTION
    USER_PROMPT = f"Prediction: {pred}\n"
    if label is not None:
        USER_PROMPT += f"Label: {label}\n"
    # >>> END SOLUTION SECTION

    # ...
    # <<< START SOLUTION SECTION
    response = completion(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT},
        ],
    )
    # >>> END SOLUTION SECTION
    # ...
    # <<< START SOLUTION SECTION
    float_answer = float(
        text_response.split("<score>")[-1].split("</score>")[0].strip()
    )
    # >>> END SOLUTION SECTION

    return float_answer

# Write a rubric for evaluating if the prediction is the capital of the label country
# 1.0 if correct, 0.5 if a city in the same country, 0.0 otherwise

# **********

# <<< START SOLUTION SECTION
RUBRIC = """
* Return 1.0 if the prediction is the capital of the label value,
* Otherwise, 0.5 if the prediction is a city in the same country as the label value,
* Otherwise, return 0.0
"""
# >>> END SOLUTION SECTION

# ...
The test assertions confirm that our judge LLM correctly applies the rubric to score predictions.

LLM response: <reasoning>Manila is the capital city of the Philippines, which exactly matches the label value. Therefore, the prediction is correct.</reasoning>
<score>1.0</score>
LLM response: <reasoning> The label is Philippines (a country). The prediction Cebu is a city in the Philippines but not the capital (Manila). Therefore it matches the country but not the capital, yielding a score of 0.5. </reasoning>
<score>0.5</score>
LLM response: <reasoning>Tokyo is not the capital of the Philippines (the capital is Manila). It is not in the same country as the label, so the prediction is incorrect.</reasoning>
<score>0.0</score>
This exercise demonstrates a suite of essential GenAI evaluation techniques, from simple string comparison and lexical overlap to complex semantic analysis, functional code testing, and rubric-based scoring with an LLM-as-a-Judge.






Welcome to the Gen AI Evaluation Medley Exercise. In this notebook, we practice several key techniques for evaluating generative AI models. We'll cover exact match, lexical similarity with ROUGE, semantic similarity with embeddings, functional correctness for code, the Pass@K metric, and finally, using an LLM as a judge. Let's get everything set up. This next section is where we import the libraries, we need and handle some basic configuration. This cell sets up our API access. If you're using Vocareum, you can uncommment the line and paste your key directly into the code. The script also automatically sets a correct API endpoint if a vocarum key is detected. Our first evaluation technique is exact match. This is a straightforward method where we check if the model's output is identical to the expected answer after some basic text cleaning. In this cell, we implement the exact match function. The task here is to complete the function, so it normalizes a prediction and a label by making them lower case and removing extra white space. It then returns one if they match and zero if they don't. We then apply this to our sample data and confirm that the overall exact match score is 0.75. We're three out of four correct. Next, we'll look at lexical similarity using the ROUGE score. ROUGE is commonly used to evaluate text summaries by measuring the overlap of words or word sequences between the prediction and the reference. Here, the task is to use a hugging face evaluate library to calculate rouge scores. We import the load function, load the rouge metric, and then compute the scores by comparing our prediction and reference sentences. The output shows us different rouge scores, which measure overlap in unigrams and the longest common subsequence. Now we move to semantic similarity. Instead of just matching words, this method helps us determine if two sentences have a similar meaning, which is crucial for evaluating more nuanced AI responses. Well, uses cosine similarity on sentence embeddings to do this. This cell introduces a sentence transformers library. We load a pretrained model that's designed to convert sentences into meaningful numerical vectors or embeddings. We test it on two simple sentences and verify that it produces embeddings with the expected dimensions. Here, we have three pairs of labels and predictions. The task is to write a third prediction that is semantically different from its corresponding label. After that, we use a sentence transformer model to encode all the predictions and labels into embeddings. With our embeddings generated, this cell calculates the cosine similarity for each prediction label pair. As you can see from the output, the first two pairs are semantically similar and have high scores. While the third pair we wrote has a very low score, confirming they are not closely related in meaning. Now, let's switch to a different domain, evaluating code generation. Here we focus on functional correctness, which we measure by executing the generated code and checking if it passes a series of unit tests. In this cell, we're given a simple Python function that has a small bug. The task is to write the single line of code that evaluates our list of predictions by running them through the function and checking if the output matches the label. The result shows that the function passes two out of three tests. Next, we'll implement the Pass@K metric. This is especially useful in co-generation where model might generate several potential solutions. Pass@K tells us if at least one of the first K attempts is correct. The task is to implement. The Passt@k function. It takes Alyssa samples in a label, and it should return one if any of the samples exactly match the label. We test it with our list of four samples, and since a correct answer appears, our pass of four score is one. Our final technique is LLM as a judge. This powerful method involves using a separate capable LLM to score model's output based on a detailed rubric that we provide. This cell is where we bring it together. The task is to complete the LLM as judge function by writing the system prompt, the user prompt, and the API call to a model. We also define a specific rubric for scoring geography questions. We then run three assertions to confirm that our LLM judge correctly scores predictions as right, partially right or wrong, based on our rubric. Congratulations. You've now completed the exercise and practiced a wide array of essential evaluation techniques. Proper evaluation is fundamental to building robust and trustworthy AI systems. Great job.