Applying Role-Based Prompts to Different Domains
Let’s explore how to apply this technique with concrete examples across three different domains: coding, data analysis, and creative writing. For each, we'll look at a complete prompt, breaking down how the role, task, format/tone specifications, and included examples work together to guide the AI agent

Try it in Udacity AI!
Open the Udacity AI interface in the top right corner of the classroom (dialog icon) and try some of these role-based prompts!

.1. Senior Python Developer

Imagine we need a Python function that calculates the Fibonacci sequence using memoization. We want robust, well-structured code.

System Prompt (Role):

You are a Senior Python Developer specializing in efficient algorithms and clean code practices. You write robust, well-documented Python code.  Include type hints for the function signature and return value.  Ensure the code is clean, readable, and follows standard Python conventions (PEP 8).
This sets an expectation for quality and style. When working with an LLM’s API, we’ll normally specify a system prompt for general instructions. If using an LLM app like ChatGPT, you typically combine system and user prompts.

User Prompt (Task & Examples):

Write a Python function called fibonacci_memoized that takes an integer n as input and returns the n-th Fibonacci number using memoization. The function should handle edge cases like n=0 and n=1.
Write a Python function called reverse_string that takes a string s as input and returns the reversed version of the string.A: ..." (example code would follow)
Here the task is clearly defined. Examples provide concrete input/output pairs. This detailed instruction enables agents to create code snippets.

Text description of a writing prompt for a fantasy author, emphasizing the creation of futuristic, atmospheric worlds and flawed characters, characterized by stark prose, realism, and a sense of underlying hope. Includes icons for writing and editing.
2. Marketing Data Analyst

Suppose we have sales data and need a summary of trends and marketing recommendations.

System Prompt (Role):

You are a Marketing Data Analyst with extensive experience in consumer product sales. Your goal is to analyze data and provide actionable insights and strategic recommendations for marketing campaigns.
This prompts the AI to interpret data through a marketing lens, focusing on aspects relevant to campaigns.

User Prompt (Task, Data & Example Format):

Analyze the provided sales data for the 'EcoWidget' product category over the last 12 months. Identify key sales trends, customer demographics (if available in data), and geographical performance variations. Based on this analysis, provide a concise summary of findings (using bullet points) and strategic recommendations for optimizing our next marketing campaign.
SALES DATA: 
Example of a key finding format:
  Finding: [Describe trend or insight, e.g., "Sales in Region X increased by 15% in Q3."]
Example of a recommendation format:  
  Recommendation: [Suggest an action, e.g., "Increase marketing spend in Region X in Q4 targeting demographic Y."]
The task is clearly stated, including the provision of data. The output is structured like a business report with bullet points and actionable insights. We could even provide an example format for the entire document.

3. Fantasy Author

Suppose we want the opening scene of a fantasy novel.

System Prompt (Role):

You are a Fantasy Author, known for crafting futuristic, atmospheric worlds and flawed characters. Your writing is characterized by stark prose, a focus on realism within the fantasy setting, and a sense of underlying hope. 
User Prompt (Task & Details):

Write the opening line (approximately 30 words) of a new fantasy story. The scene should focus on the protagonist, Zeb, a cynical mercenary, as he stumbles upon a hidden, ancient magical artifact in the ruins beneath a dried-up lake.  
   - Use a third-person perspective.  
   - Emphasize sensory details (dusty stones, dim light).  
   - Hint at the potential danger or unsettling nature of the artifact.
Here we provide the task and details like perspective, sensory focus, and foreshadowing.

Example Output: "Dust swirled in the dim light filtering through cracks in the dead lakebed above as Zeb navigated the ruins. His boot nudged something smooth amidst the rubble—an obsidian shard, radiating a silence colder than stone." Is this a story you would continue reading? If not, you could refine the prompt to get an opening line you do like!
A dark, atmospheric environment with a figure standing in front of a large, reflective obsidian shard. The scene is illuminated by colorful lights in blue and red hues, revealing cracked stone pathways and ancient ruins in the background.
Applying role-based prompting, combined with clear task definitions, specific format and tone requirements, and well-chosen examples enhances your ability to guide AI agents across domains. This layered approach provides the structure and context for the AI to understand intent and produce outputs that are tailored to your specific needs.