From Vague Ideas to Precise Instructions
When an AI gives you a response that isn't quite right, what's your first instinct? Many people assume they just need to add more words or make the prompt longer. But is a longer prompt always a better prompt?

The key isn't just adding more detail; it's adding the right kind of detail in a structured way. Let's see this in action.

Scenario: We need an AI to categorize incoming customer support emails for an automated ticketing system.

Attempt 1: The Vague Prompt
Let's start with a simple, vague prompt and see what we get.

# The customer's email
customer_email = """
Hi, I'm writing because I was charged twice for my last order (Order #8675309).
I thought my subscription was paused. Can you please look into this and reverse the extra charge?
Thanks,
Alex
"""

# The vague system and user prompts
system_prompt_vague = "You are a helpful assistant."
user_prompt_vague = f"Please categorize the following email:\n\n{customer_email}"

# Let's see the likely response
# response = get_completion(system_prompt_vague, user_prompt_vague)
# print(response)
Likely Output:This email appears to be a billing issue related to a double charge on an order.

This response is correct, but it's not very useful for an automated system. A downstream program can't easily parse this sentence to create a support ticket, assign it to the right department, or set its priority. We need more structure.

Attempt 2: The Refined, Structured Prompt
Now, let's refine our instructions.

We will add a specific Role,
clear Task instructions
with Context (definitions of the categories),
and a required Output Format (JSON).
system_prompt_refined = """
You are an expert customer support agent responsible for categorizing incoming emails for a ticketing system.

Your task is to analyze the user's email and provide a structured JSON output.

## Email Categories:
- **Billing:** For issues related to charges, subscriptions, or refunds.
- **Technical Support:** For problems with product functionality or bugs.
- **General Inquiry:** For questions that do not fit the other categories.

## Output Format:
You must respond with a single JSON object containing the following keys:
- `category`: (string) One of "Billing", "Technical Support", or "General Inquiry".
- `summary`: (string) A one-sentence summary of the user's issue.
- `urgency`: (string) "High", "Medium", or "Low".
- `customer_id`: (string) Extract the order number or customer ID if available, otherwise "N/A".
"""

user_prompt_refined = f"Please analyze and categorize this email:\n\n{customer_email}"

# response = get_completion(system_prompt_refined, user_prompt_refined)
# print(response)
Likely Output:

{
  "category": "Billing",
  "summary": "The customer was charged twice for order #8675309 and is requesting a refund for the extra charge.",
  "urgency": "High",
  "customer_id": "8675309"
}
By refining our prompt with structured instructions, we transformed the AI's output from a simple sentence into a reliable, machine-readable JSON object. This is the power of prompt instruction refinement.




