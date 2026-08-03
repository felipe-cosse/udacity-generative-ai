This demonstration walks through a practical collaboration with a Large Language Model (LLM) to generate a Python function and its corresponding unit tests. We'll solve the classic programming problem of creating a factorial function, but we'll let the LLM do the heavy lifting for both the implementation and the quality assurance.


Start Workspace

Workspaces will shut down after 30 minutes of inactivity. Any running processes will be stopped.

Workspaces may take up to 5 minutes to start.

First, we need to set up our connection to the language model. This cell imports the necessary libraries and configures the API key. The code includes a check to automatically configure the correct API endpoint if a Vocareum key is detected.

import litellm
import os

if os.getenv("OPENAI_API_KEY"):
    litellm.openai_key = os.getenv("OPENAI_API_KEY")

# ... other setup code ...

if (litellm.openai_key or "").startswith("voc-"):
    litellm.api_base = "https://openai.vocareum.com/v1"
    print("Detected vocareum API key. Using Vocareum OpenAI API base URL.")
Our first major step is to ask the LLM to write the factorial function for us. We define two prompts: a SYSTEM_PROMPT that sets the LLM's role and a USER_PROMPT that details our specific requirements for the function.

SYSTEM_PROMPT = """You are a helpful coding assistant. Return only the Python code, with no explanation or preamble."""
USER_PROMPT = """Write a Python function that implements the factorial algorithm using recursion.
The name of the function should be `factorial`.
The function should take a single non-negative integer as input.
Include a docstring explaining what the function does."""
Now, we'll send these prompts to the model. We use the completion function from the litellm library, specifying the model gpt-5-mini and passing our prompts. Then we print the generated code from the response.

from litellm import completion

response = completion(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
)
print("Generated Code:\n")
print(response.choices[0].message.content)
The LLM has generated a Python function that implements the recursive logic and also includes type and value checking for the input, along with a detailed docstring, just as we asked.

def factorial(n):
    """Return the factorial of a non-negative integer n computed recursively.

    The factorial of n (written n!) is the product of all positive integers
    up to n. By definition, 0! == 1.

    Args:
        n (int): A non-negative integer.

    Returns:
        int: The factorial of n.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
With the function defined, we can perform a quick check to see if it works correctly. We'll test it with a simple case: the factorial of 5, which should be 120.

input_val = 5
expected_val = 120

output_val = factorial(input_val)

print(f"Input: {input_val}")
print(f"Output: {output_val}")
print(f"Expected: {expected_val}")
print(f"Match: {output_val == expected_val}")
print()

if output_val == expected_val:
    print("Test case passed! ✅")
else:
    print("Test case failed. ❌")
A single manual check is good, but a full test suite is better. Now, we'll ask the LLM to generate a comprehensive set of tests using Python's built-in unittest framework. We'll specifically ask it to cover a basic positive integer, the edge case of 0, and an invalid negative number.

SYSTEM_PROMPT = """You are a helpful coding assistant that writes unit tests using the unittest framework. Return only the code, no explanations."""
USER_PROMPT = """Please generate test cases for the `factorial` function.
The test cases should be in a class called `TestFactorial` that inherits from `unittest.TestCase`.
Include tests for a positive integer, the number zero, and a negative number.
The test for the negative number should check that a `ValueError` is raised.
Do not include any imports or a main block.
"""
We send this new prompt to the model.

response = completion(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
)
print("Generated Test Cases:\n")
print(response.choices[0].message.content)
The LLM generates the Python code for a test class complete with three distinct test methods that cover our requested scenarios.

For the final step, we'll take the LLM-generated test code, place it in our notebook, and run it to formally validate our factorial function.

import unittest

class TestFactorial(unittest.TestCase):
    def test_positive_integer(self):
        self.assertEqual(factorial(5), 120)

    def test_zero(self):
        self.assertEqual(factorial(0), 1)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            factorial(-3)

# Run the tests
unittest.main(argv=["notebook-tests"], exit=False)
The output confirms that all three tests ran and passed, giving us confidence that our LLM-generated function is behaving as expected.

By crafting clear and specific prompts, you can leverage an LLM to automate the generation of both functional code and its corresponding validation tests.








In this demonstration, we walk through how to use a large language model or LLM to generate a Python function and its corresponding tests. We'll be using the factorial function as our example. First, we need to set up our connection to the language model. This cell imports a necessary library and configures the API key. If you're using a vocarium key, it detects that and sets a correct API base URL. Now, prompting for a factorial function. Our first major step is to ask the LLM to write the factorial function for us. Here we define the prompts, we will send to the model. The system prompt tells the AI, it's a helpful coding assistant and should only return Python code. The user prompt provides a detailed instructions. Create a recursive function named factorial that takes a non-negative integer and includes a helpful doc string. Now, this is a cell that actually makes API call. We use a library called Light LLM, and with that, we use GPT-5 Mini. We construct the messages consisting of the system prompt and the user prompt, and we print out the response. As you can see, the LLM has generated a Python function that not only implements a recursive factorial logic, but also includes type and value checking for the input. Along with a detailed doc string, just as we asked with the function defined, we can perform a quick check to see if it works correctly. We'll test it with a simple case, the factor of five, which should be 120. A single manual check is good, but a full test suite is better. Now, we'll ask the LLM to generate a more comprehensive set of tests using Python's built-in unit test framework. We'll specifically ask it to cover a basic positive integer, the edge case of zero, and an invalid negative number. Here, we define a new set of prompts. This time, the system prompt instructs us to act as a unit test writer. The user prompt asks for a test class name, test factorial, and specifies the three test cases we want, including one that checks for a value error when the input is negative. We send this new prompt to the model, and the LLM generates the Python code for a test class, complete with three distinct test methods that cover our requested scenarios. Now for the final step, we'll take the LLM-generated test code and run it to formally validate our factorial function. We paste in the tests and then run unittest.main. The output shows that all three tests ran and passed, which gives us confidence that our LLM-generated function is behaving as expected for the cases we care about. This demo shows the successful use of an LLM for coding. It's important to remember that you might need to refine your prompts for more complex problems. You can always be more specific about requirements like doc string formatting, custom error types, or handling other edge cases like non-integer inputs.