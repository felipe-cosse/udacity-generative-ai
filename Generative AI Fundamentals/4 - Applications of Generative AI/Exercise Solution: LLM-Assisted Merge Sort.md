Solution Walkthrough
This exercise uses a Large Language Model (LLM) to first generate an implementation of the merge sort algorithm and then generate a comprehensive suite of unit tests for it.

The first step is to craft a detailed USER_PROMPT that clearly defines the requirements for the merge_sort function. This includes specifying the function name, its input/output types, and the request for inline comments to explain the logic.

# Student task: Write the USER_PROMPT to request a merge sort implementation in Python.
# ...

# <<< START SOLUTION SECTION
USER_PROMPT = """
Write a Python function that implements the merge sort algorithm.
The name of the function should be `merge_sort`.
The function should take a list of integers as input and return a new list containing the integers sorted in
ascending order.
Include comments in the code to explain each step of the algorithm.
"""
# >>> END SOLUTION SECTION
After generating the function with the LLM and pasting it into the notebook, we perform a quick functional check. This is done by defining the expected sorted lists for two sample inputs and comparing them against the function's actual output.

# ...
# Expected outputs
expected_A = "**********"
expected_B = "**********"

# <<< START SOLUTION SECTION
# Expected sorted results
expected_A = [5, 7, 16, 23, 42, 91]
expected_B = [-4, 0, 1, 2, 3, 3, 5]
# >>> END SOLUTION SECTION

# Run merge_sort on the sample inputs
# ...
Next, we prompt the LLM to generate a more robust set of test cases using Python's unittest framework. The prompt specifies that the tests should cover basic functionality, edge cases (like empty lists or duplicates), and invalid inputs (like strings or None).

# Student task: Write the USER_PROMPT to request test cases for the merge_sort function.
# ...

# <<< START SOLUTION SECTION
USER_PROMPT = """Please generate test cases for the merge_sort function, covering the following scenarios:
    - Basic functionality
    - Edge cases (empty list, single element, duplicates)
    - Invalid inputs (strings, None, mixed types)

The test cases should be implemented using Python's unittest framework in a class named TestMergeSort.
    """
# >>> END SOLUTION SECTION
Finally, we paste the generated TestMergeSort class into the notebook and run the tests. The output reveals one failure. This is an important learning moment: the test test_invalid_string_input_raises_typeerror fails because our original prompt for the merge_sort function did not ask it to handle invalid data types by raising a TypeError. The function instead attempts to sort the list of strings, which succeeds, causing the assertRaises assertion to fail. This highlights the need for precise requirements in prompts for both implementation and testing.

.......F.
======================================================================
FAIL: test_invalid_string_input_raises_typeerror (__main__.TestMergeSort)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/var/folders/5s/r3p544z57kxbmgkzvz_jv1gw0000gn/T/ipykernel_69501/732058859.py", line 45, in test_invalid_string_input_raises_typeerror
    with self.assertRaises(TypeError):
AssertionError: TypeError not raised

----------------------------------------------------------------------
Ran 9 tests in 0.003s

FAILED (failures=1)


Key Takeaway
Using a Large Language Model (LLM) can accelerate development by generating both functional code and corresponding unit tests, but it requires careful prompting and validation to ensure the output aligns perfectly with all explicit and implicit requirements.






Let's talk about the LLM assisted merge sort exercise. The goal here is to collaborate with a large language model, to design, implement, and test the merge sort algorithm in Python. We'll follow these steps in the notebook, prompting for Merge sort code, quick functional check, merge sort reflection, prompting for merge sort test cases, and then running the merge sort tests. First, if you're using the Vocareum API key, you can paste it in here or set it as an environment variable. Cool. Now, let's get started. Prompting for merge sort code. First, we define our prompts for the LLM. We're using a system prompt that instructs the model to act as a helpful coding assistant and only return the code. Our user prompt clearly specifies a requirement such as write a Python function. The function must be named Merge Sort. It should take a list of integers and return a new list. We also ask for clear comments to explain each step. In this cell, we use Light LLMs completion method to send our prompts to the LLM and get back the generated code, which we paste into the next cell. Now, let's take a look at the code the LLM generated. It handles the base case, returning a copy of the list if its length is zero or one. It also finds a middle and recursively calls itself on the left and right halves. Finally, it includes a core merge logic, comparing elements from the two sorted halves to build the final sorted list. Now, let's do a quick functional check. Let's test this function to see if it works as expected. We run a quick check with two sample inputs. Input A and input B. We also provide the expected sorted outputs for both. Running the cell. We see if the function produces a correct results. Does it? Yes, both test cases pass. Merge sort reflection. Now, let's reflect on this implementation. One, did the implementation correctly sort both sample inputs? Why, yes it did. Two, does a structure align with the conical merge sort algorithm? Why, yes, of course. Three, is a code readable and maintainable? Why, yes. Four, how terse or verbose is a solution relative to your expectations, I would say it's appropriately concise, standard for an educational merge sort solution. Now, as part of our evaluation, let's check merge sort on some edge cases, such as an empty list, a single element list, and a list with duplicate elements. In these edge cases, you'll notice the algorithm appropriately found the right answer. To cap off our reflection, how are these edge cases handled? Actually, they're handled quite well. Moving on, prompting for merge sort test cases. Next, we ask the LLM to generate more comprehensive unit tests using the unit test framework. Again, we set a system prompt to simplify the output to just return what we want, just a unit test class in this case. We also explicitly request coverage for three main areas, basic functionality, edge cases, and invalid inputs. Again, we use light LLM to generate the code, which brings us to running the merge sort tests. Then we take the code and we paste it into this cell. Here you can see the LLM generated a test merge sort class, including a helpful private method, assert sorted, either in place or returned to handle functions that might sort either in place or return a new list, which might be nice or not, since we actually initially wanted a new list. But anyway, and now we run the tests. Here the outs represent passing tests, and the F indicates a failure. The specific failure is test invalid string input raises type error. Type error not raised. This failure occurs because we ask the LLM to generate a test that expects a type error for an invalid input involving sorting strings. Never explicitly instructed our merge sort function to implement error handling. The function simply attempted to run, and in this case, it actually succeeded, returning a sorted list of strings. This highlights a key part of LLM assisted development. Very often, the LLM will include these features automatically. We will need to be extra vigilant in our use of AI for coding to ensure these features actually align with our intentions. We made it. Congrats. We've successfully used an LLM to generate a functional merge sort implementation and tests. Give yourself a hand.