Exercise Introduction: Bringing History to Life with AI Personas
You've learned that giving an AI a specific role can significantly shape its responses. Now, you'll put that into practice in a creative way: by instructing an AI to adopt the persona of a famous historical figure for an interactive Q&A.

The Challenge: Crafting a Believable Historical Character

Imagine you want to "interview" Albert Einstein. A simple request to an AI might give you facts about Einstein, or perhaps a very superficial impersonation. But how do you get the AI to respond with a voice that truly feels like the historical figure – capturing their likely personality, manner of speaking, contemporary knowledge, and even their characteristic way of explaining ideas?

Your Mission: Becoming an AI Character Director

In this exercise you'll act as a director, guiding the AI step-by-step to embody Albert Einstein. You will:

Start with basic prompts and observe the AI's initial attempts.
Systematically add layers of detail to your prompts, defining persona-specific attributes like personality and areas of knowledge.
Specify tone and stylistic elements to refine the character's voice.
Conduct a mock Q&A to test how well the AI maintains the persona.
Instructions
Follow these steps to complete the exercise in your Udacity classroom workspace:

Open the Notebook: Launch the "Lesson 1: Role-Based Prompting (Agent Personas) - Historical Figure Interviewer" exercise notebook.
Initial Setup:
Add your API key to the notebook.
Step 1: Plain Prompt
Find the section "1. Plain Prompt".
Run the code cell that sends a control_system_prompt ("You are a helpful assistant.") and asks the user_prompt ("Can you tell me about relativity?").
Observe this initial, non-role-playing response. This is your control.
Step 2: Baseline Historical Figure Prompt
Go to section "2. Baseline Historical Figure Prompt".
You'll see a TODO: baseline_system_prompt = "**********."
Your Task: Change this line to give the AI the basic role of Albert Einstein. For example: baseline_system_prompt = "You are Albert Einstein."
Run this cell. The same user_prompt about relativity will be used.
Review the AI's first attempt at portraying Einstein. Use the "Observations" questions in the notebook to guide your thoughts.
Step 3: Define Persona-Specific Attributes
Move to section "3. Define Persona-Specific Attributes".
You will find several TODO items within the persona_system_prompt string, marked with **********.
Your Task: Fill in these attributes for Albert Einstein.
Run the cell.
Compare this response to the previous one. Note differences based on the "Observations" prompts.
Step 4: Add Tone and Style Specifications
Proceed to section "4. Add Tone and Style Specifications".
Find the TODO items in the tone_system_prompt string.
Your Task: Add specific details about Einstein's tone and conversational style.
Run this cell.
Observe how these specifications refine the AI's portrayal.
Step 5: Q&A Session Format
Navigate to section "5. Q&A Session Format".
Find the TODO in the user_prompt for three questions.
Your Task: Write three questions to ask "Albert Einstein," keeping in mind the 1950 context.
Run the cell.
Analyze "Einstein's" answers for consistency, historical appropriateness, and depth.
Step 6: Reflection & Transfer
Go to section "6. Reflection & Transfer".
In the markdown cell, find the TODO and type your thoughts on which prompt refinement you felt was most effective in creating an authentic persona and why.



