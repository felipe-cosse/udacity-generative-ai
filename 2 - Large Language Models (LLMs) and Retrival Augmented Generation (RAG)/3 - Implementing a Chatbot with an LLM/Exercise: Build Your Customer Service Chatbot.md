In this hands-on exercise, you'll build a customer service chatbot for ShopEasy, an e-commerce platform. You'll learn how to maintain conversation context, classify customer intents, and generate helpful responses using OpenAI's API.

Objectives:

Initialize and configure the OpenAI API client with proper routing
Design effective system prompts that define bot behavior and personality
Maintain conversation history for contextual, multi-turn dialogues
Classify customer intents using LLMs for intelligent routing
Generate natural, helpful customer service responses
Implement conversation management features (reset, summary, handoff)
Prerequisites:

Python 3.8 or higher
OpenAI API key (Vocareum key provided in course)
Basic understanding of APIs, Python classes, and dictionaries

Your chatbot will handle five types of customer inquiries:

Order Status - "Where is my order?"
Product Information - "Do you have wireless headphones in stock?"
Returns - "What's your return policy?"
Technical Support - "I can't log into my account"
General - Greetings, general questions, other inquiries
Key Components
The CustomerServiceBot class has five main methods to implement:

__init__()                    # Set up client, history, system prompt
classify_intent()             # Categorize customer message
generate_response()           # Create helpful response with context
reset_conversation()          # Clear history for new conversation
get_conversation_summary()    # Summarize for human handoff
Task 1: Set Up the Client
Open exercises/starter/customer_service_bot.py and find the __init__ method .

What to implement:

def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
    # TODO 1: Initialize the OpenAI client
    self.client = OpenAI(api_key=api_key)

    # TODO 2: Store the model name
    self.model = model

    # TODO 3: Initialize conversation history as empty list
    self.conversation_history = []

    # TODO 4: Add system prompt to conversation history
    system_prompt = self._get_system_prompt()
    self.conversation_history.append({
        "role": "system",
        "content": system_prompt
    })
Vocareum API Key Routing
If you're using a Vocareum key (starts with "voc-"), you need to route through Vocareum's proxy:

# Detect Vocareum keys and route appropriately
if api_key.startswith("voc"):
    self.client = OpenAI(
        base_url="https://openai.vocareum.com/v1",
        api_key=api_key
    )
else:
    self.client = OpenAI(api_key=api_key)
Understanding Message Structure
The conversation_history is a list of message dictionaries:

[
    {"role": "system", "content": "You are a helpful assistant..."},
    {"role": "user", "content": "Where is my order?"},
    {"role": "assistant", "content": "I'd be happy to help..."},
    {"role": "user", "content": "Order #12345"},
    {"role": "assistant", "content": "Let me check order #12345..."}
]
Three roles:

system - Defines behavior (first message, always included)
user - Customer messages
assistant - Bot responses
Testing Your Implementation
After implementing __init__, test it:

api_key = "your-api-key"
bot = CustomerServiceBot(api_key)

# Check that initialization worked
print(bot.client)  # Should show OpenAI client object
print(bot.model)   # Should show "gpt-3.5-turbo"
print(len(bot.conversation_history))  # Should be 1 (system prompt)
print(bot.conversation_history[0]["role"])  # Should be "system"
Task 2: Design the System Prompt
Understanding System Prompts
The system prompt is the most important part of your chatbot. It defines:

Role and identity - Who is the bot?
Capabilities - What can it help with?
Tone and personality - How should it communicate?
Guidelines - What rules should it follow?
Boundaries - What should it NOT do?
Task 3: Complete the classify_intent() Method
Find classify_intent() and implement the TODO sections.

Test your implementation:

bot = CustomerServiceBot(api_key)

# Test various customer messages
test_messages = [
    "Where is my order #12345?",           # Should be: order_status
    "Do you have iPhone 15 in stock?",     # Should be: product_info
    "What's your return policy?",          # Should be: returns
    "I can't log into my account",         # Should be: technical_support
    "Hi there!",                           # Should be: general
]

for msg in test_messages:
    intent = bot.classify_intent(msg)
    print(f"Message: {msg}")
    print(f"Intent: {intent}\n")
Task 4: Complete the generate_response() Method
This is the core of your chatbot. Find generate_response():

def generate_response(self, user_message: str, intent: Optional[str] = None) -> str:
    # TODO 1: If intent not provided, classify it
    if intent is None:
        intent = self.classify_intent(user_message)
        print(f"[Intent detected: {intent}]")  # For debugging

    # TODO 2: Add user's message to conversation history
    self.conversation_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        # TODO 3: Make API call with full conversation history
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=0.7,   # Balanced creativity
            max_tokens=300     # Reasonable response length
        )

        # TODO 4: Extract the assistant's response
        assistant_message = response.choices[0].message.content

        # TODO 5: Add assistant's message to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    except Exception as e:
        error_msg = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
        print(f"Error generating response: {e}")
        return error_msg
Task 5: Implement reset_conversation()
Find reset_conversation() :

def reset_conversation(self):
    """Reset the conversation history, keeping only the system prompt."""
    # TODO: Clear history and re-add system prompt
    self.conversation_history = [{
        "role": "system",
        "content": self._get_system_prompt()
    }]
    print("[Conversation reset]")
When to use reset:

Starting conversation with a new customer
Customer explicitly asks to start over
Conversation has gone off-track
Task 6: Implement get_conversation_summary()
Find get_conversation_summary() :

def get_conversation_summary(self) -> str:
    """Get a summary for handoff to human agent."""
    if len(self.conversation_history) <= 1:
        return "No conversation to summarize yet."

    summary_prompt = """Please provide a brief summary of this customer service conversation.
Include:
1. Main customer concerns or questions
2. Information provided by the bot
3. Current status or next steps

Keep it concise (2-3 sentences)."""

    # TODO 1: Create temporary message list with summary request
    summary_messages = self.conversation_history + [{
        "role": "user",
        "content": summary_prompt
    }]

    try:
        # TODO 2: Make API call to get summary
        response = self.client.chat.completions.create(
            model=self.model,
            messages=summary_messages,
            temperature=0.3,  # Lower temperature for factual summary
            max_tokens=200
        )

        # TODO 3: Return the summary text
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Unable to generate summary at this time."
Task 7: Complete the main() Function
Find main() and complete the chat loop:

def main():
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: Please set OPENAI_API_KEY environment variable")
        return

    # Initialize bot
    bot = CustomerServiceBot(api_key)

    print("Customer Service Bot initialized!")
    print("Commands: 'quit', 'reset', 'summary'\n")

    # Chat loop
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Handle commands
        if user_input.lower() in ['quit', 'exit']:
            print("Thank you for using Customer Service Bot!")
            break

        if user_input.lower() == 'reset':
            bot.reset_conversation()
            continue

        if user_input.lower() == 'summary':
            print("\n--- Conversation Summary ---")
            print(bot.get_conversation_summary())
            print("----------------------------\n")
            continue

        # Generate and print response
        response = bot.generate_response(user_input)
        print(f"\nBot: {response}\n")
Running Your Chatbot
# Set your API key
export OPENAI_API_KEY="your-api-key-here"

# Run the bot
python exercises/starter/customer_service_bot.py
Sample Interaction
Try this conversation:

You: Hi, I need help with my order

Bot: Hello! I'd be happy to help you with your order. Could you please
provide your order number so I can look up the details for you?

You: It's order #12345. I placed it 3 days ago.

Bot: Thank you for providing your order number #12345. Let me check the
status for you. Could you tell me what specific information you're looking
for? Are you wondering about the delivery timeline, tracking information,
or something else?

You: Where is it now?

Bot: Based on your order placed 3 days ago, I'd need to look up the
tracking information. Typically, orders take 3-5 business days to arrive.
However, I don't have access to the real-time tracking system. I can
escalate this to our shipping department to get you the exact location
of your package. Would you like me to do that?

You: summary

--- Conversation Summary ---
Customer inquired about order #12345 placed 3 days ago. Bot requested
tracking details and offered to escalate to shipping department for
real-time location information. Awaiting customer decision on escalation.
----------------------------
Instructions
Follow these steps to build your chatbot:

Set up the OpenAI client - Configure your API key and base URL (use Vocareum routing)
Design your system prompt - Define the chatbot's role, tone, and capabilities for TechSupport Plus
Implement the chat function - Create a function that sends messages and maintains conversation history
Test with customer scenarios - Try these queries:
"Where is my order #45678?"
"What's the difference between your X1 and X2 laptops?"
"I want to return a product I bought last week"
Refine your prompt - Adjust the system message based on the responses you get The starter code in the workspace includes TODO comments guiding you through each step. Complete all TODOs to build a working chatbot!



