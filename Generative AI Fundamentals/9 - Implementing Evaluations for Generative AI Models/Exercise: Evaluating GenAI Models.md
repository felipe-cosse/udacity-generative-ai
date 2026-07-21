Let's practice exact evaluation, AI-as-judge mechanics, and benchmarking by completing small, focused coding tasks. In this exercise, you will implement several common evaluation techniques for Generative AI models.

Prerequisites
Basic Python programming, including functions, lists, and strings.
Familiarity with evaluation concepts like Exact Match, ROUGE, and Cosine Similarity.
Basic understanding of making API calls to Large Language Models.
Instructions
Exact Match (EM): In the exact_match function, replace the line return_value = "**********" with return_value = int(normalize(pred) == normalize(label)). This will return 1 if the normalized prediction and label are identical, and 0 otherwise.

Lexical Similarity (ROUGE): In the cell under the "Lexical Similarity (ROUGE)" heading, you will use the evaluate library to compute ROUGE scores.

Import the load function: from evaluate import load.
Load the ROUGE metric: rouge = load("rouge").
Compute the scores and assign them to a results variable: results = rouge.compute(predictions=[pred], references=[label]).
Semantic Similarity: In the cell under the "Semantic Similarity using Cosine Similarity" heading, you will generate sentence embeddings and compare them.

First, add a third sentence to the preds list. This sentence should be semantically different from its corresponding label. For example: "Turquoise is a marvelous color".
Next, generate the embeddings for both the preds and labels lists. Replace the placeholder string for pred_embeddings with model.encode(preds) and the placeholder for label_embeddings with model.encode(labels).
Functional Correctness: In the cell under the "Functional Correctness" heading, complete the list comprehension assigned to the results variable. Replace the placeholder comment # "**********" with the expression sort_and_normalize(p) == l to check if the function's output matches the label.

Pass@k: In the cell under the "Pass@k" heading, implement the pass_at_k function. It should return 1 if any of the samples match the label, and 0 otherwise. Add the following function definition in the designated area:

def pass_at_k(samples: List[str], label: str) -> int:
    return int(any(s == label for s in samples))
LLM as a Judge: In the final coding cell, you will complete a function that uses an LLM to evaluate a prediction based on a rubric.

First, define the RUBRIC variable with the specified scoring criteria.
RUBRIC = """
* Return 1.0 if the prediction is the capital of the label value,
* Otherwise, 0.5 if the prediction is a city in the same country as the label value,
* Otherwise, return 0.0
"""
Inside the llm_as_judge function, define the SYSTEM_PROMPT. This multi-line string should instruct the LLM on its role, the rubric to use, and the required XML output format (<reasoning> and <score>).
SYSTEM_PROMPT = f"""You are an expert evaluator. Use the following rubric to score the prediction.
Format your response as:
<reasoning>...</reasoning>
<score>FLOAT_ANSWER</score>

where FLOAT_ANSWER is a float between 0 and 1.

RUBRIC:
{rubric}
"""
Next, create the USER_PROMPT. It should contain the Prediction and the Label if it is provided.
USER_PROMPT = f"Prediction: {pred}\\n"
if label is not None:
    USER_PROMPT += f"Label: {label}\\n"
Call the litellm.completion function to get a response from the model. Use the model gpt-5-nano and pass the system and user prompts.
response = completion(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
)
Finally, extract the floating-point score from the LLM's response. You can do this by splitting the response string to isolate the number between the <score> tags.
float_answer = float(
    text_response.split("<score>")[-1].split("</score>")[0].strip()
)
Accessing the Workspace
Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-8-implementing-evaluations-for-generative-ai-models/exercises/starter
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