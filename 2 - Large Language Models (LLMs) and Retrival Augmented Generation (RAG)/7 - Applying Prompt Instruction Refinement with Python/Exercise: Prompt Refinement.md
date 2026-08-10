Exercise Introduction: Crafting Precise Prompts for Dietary Analysis
In this exercise, you'll put the principles of Prompt Instruction Refinement into practice. You've learned that the way you structure your instructions to an LLM greatly influences the quality, accuracy, and usefulness of its responses. Now, you'll apply that knowledge to a practical task: getting an LLM to accurately analyze recipes against a list of dietary restrictions.

The Challenge: From Basic Classification to Detailed Analysis

Imagine you give an LLM a recipe and a list of dietary needs. You ask it to tell you if the recipe fits each need. With a simple prompt, the LLM might give you a quick "yes," "no," or "maybe" for each. But is that enough?

What if an ingredient is ambiguous (like "broth" – is it vegetable or chicken?)?
How does it handle "optional" ingredients that could violate a restriction?
Will it explain why a recipe doesn't meet a certain need, and pinpoint the problem ingredient(s)?
Can you get the output in a consistent, structured format that includes these explanations?
How do you refine an initial, basic prompt step-by-step to turn the LLM into a more careful and informative dietary analyst, producing results you can better understand and trust?

Your Mission: Becoming a Prompt Refinement Specialist

In this exercise you will take an initial prompt designed for recipe and dietary analysis and iteratively improve it. You will:

Evaluate an initial, simple prompt and identify its shortcomings.
Analyze the different components of the prompt (like Role, Task definition, Context, Output Format, and Examples).
Methodically refine the prompt by adding clarity, providing necessary context (like definitions for dietary restrictions), specifying a more detailed output structure, and guiding the LLM on how to handle uncertainties.
Test your refined prompts with different recipes to see the improvement in the LLM's analysis.
Instructions
Follow these steps within the "Lesson 3: Prompt Instruction Refinement - Matching Recipes to Dietary Restrictions" Jupyter Notebook:

Open the Notebook: Launch the exercise notebook from your Udacity classroom.
Initial Setup:
Add your API Key
Review Sample Data:
Load sample_recipes and dietary_restrictions. Familiarize yourself with this data as it will be used for testing your prompts.
Initial Prompt and Evaluation:
Examine the initial_prompt and the format_prompt function (using Jinja2 for templating).
Test the initial_prompt with the "Classic Spaghetti Bolognese" recipe.
Your Task: Observe the initial_response. Note its structure and the classifications it provides. Is it giving explanations? How does it handle something like "kosher"?
Prompt Component Analysis:
Read through the "Prompt Component Analysis" and "Initial Analysis of Problems" sections in the notebook. This guides you to think about what's lacking in the initial_prompt.
Prompt Refinement Iteration 1:
This cell contains your first TODO. You need to complete the definitions for various dietary restrictions and provide clear guidelines for the classification logic.
Your Task: Fill in the ********** placeholders.
After filling in the TODOs, test refined_prompt_1 with the same spaghetti recipe.
Your Task: Observe the Iteration 1 response. Notice how the output now includes explanations and critical ingredients due to your improved prompt.
Prompt Refinement Iteration 2:
This cell contains your second TODO. You'll add more guidance on handling common ambiguities in recipes and complete an example within the prompt.
Your Task: Fill in the ********** placeholders in the "Handling ambiguities" section.
After filling in the TODOs, test refined_prompt_2 with the "Vegetable Stir Fry" recipe.
Your Task: Analyze the Iteration 2 response. Does the LLM handle ambiguities (like "soy sauce" for gluten-free, or "sesame seeds" for nut-free) more thoughtfully now?
Testing with Multiple Recipes:
Test your refined_prompt_2 with the "Chocolate Chip Cookies" recipe.
Your Task: Observe the response. Check if the classifications and explanations are consistent and accurate for this different type of recipe (e.g., how it handles "butter" for dairy-free/vegan, "all-purpose flour" for gluten-free, and "chopped nuts (optional)" for nut-free).



