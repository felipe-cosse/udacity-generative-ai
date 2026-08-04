If you ran into issues building your chatbot, here's some common problems and resolutions you can try, as well as a test script you can create and run.

Forgetting to Add Messages to History
Problem:

# Wrong - only adds user message, not assistant response
self.conversation_history.append({"role": "user", "content": user_message})
response = self.client.chat.completions.create(...)
return response.choices[0].message.content  # ❌ Didn't add to history!
Solution:

# Correct - adds both user and assistant messages
self.conversation_history.append({"role": "user", "content": user_message})
response = self.client.chat.completions.create(...)
assistant_message = response.choices[0].message.content
self.conversation_history.append({"role": "assistant", "content": assistant_message})
return assistant_message
Not Including System Prompt
Problem:

# Wrong - system prompt missing
self.conversation_history = []  # ❌ Empty!
Solution:

# Correct - always starts with system prompt
self.conversation_history = [{
    "role": "system",
    "content": self._get_system_prompt()
}]
Using Wrong Temperature for Classification
Problem:

# Wrong - temperature=0.7 for classification
response = self.client.chat.completions.create(
    model=self.model,
    messages=[...],
    temperature=0.7  # ❌ Too random for classification!
)
Solution:

# Correct - temperature=0 for deterministic classification
response = self.client.chat.completions.create(
    model=self.model,
    messages=[...],
    temperature=0  # ✅ Consistent classification
)
Not Validating Intent Categories
Problem:

# Wrong - trusts LLM output blindly
intent = response.choices[0].message.content.strip()
return intent  # ❌ Might return unexpected value!
Solution:

# Correct - validates against expected categories
intent = response.choices[0].message.content.strip().lower()
valid_intents = ['order_status', 'product_info', 'returns',
                'technical_support', 'general']
if intent not in valid_intents:
    intent = 'general'  # Default fallback
return intent
Missing Error Handling
Problem:

# Wrong - no error handling
response = self.client.chat.completions.create(...)
return response.choices[0].message.content  # ❌ Crashes on API error!
Solution:

# Correct - wraps in try/except
try:
    response = self.client.chat.completions.create(...)
    return response.choices[0].message.content
except Exception as e:
    print(f"Error: {e}")
    return "I apologize, but I'm having trouble right now. Please try again."
Long Conversations Hitting Token Limits
Problem: After 20+ exchanges, you might hit the model's context limit (4096 tokens for gpt-3.5-turbo).

Solution: Implement history truncation (advanced):

def truncate_history(self, max_messages=20):
    """Keep only recent messages plus system prompt."""
    if len(self.conversation_history) > max_messages:
        # Keep system prompt + most recent messages
        system_prompt = self.conversation_history[0]
        recent_messages = self.conversation_history[-(max_messages-1):]
        self.conversation_history = [system_prompt] + recent_messages
Testing Your Complete Implementation
Create a test file to verify all functionality:

# test_chatbot.py
from customer_service_bot import CustomerServiceBot
import os

api_key = os.getenv("OPENAI_API_KEY")
bot = CustomerServiceBot(api_key)

print("Test 1: Intent Classification")
print("="*50)
intents_to_test = {
    "Where is my order?": "order_status",
    "Do you have laptops?": "product_info",
    "How do I return something?": "returns",
    "Can't log in": "technical_support",
    "Hello": "general"
}

for message, expected in intents_to_test.items():
    actual = bot.classify_intent(message)
    status = "✅" if actual == expected else "❌"
    print(f"{status} '{message}' → {actual} (expected: {expected})")

print("\n\nTest 2: Conversation Context")
print("="*50)
bot.reset_conversation()
bot.generate_response("Do you have wireless headphones?")
response = bot.generate_response("What colors?")
print(f"Context-aware response: {response}")
# Should mention headphones, not ask "what product?"

print("\n\nTest 3: Conversation Summary")
print("="*50)
bot.reset_conversation()
bot.generate_response("I need to return a laptop")
bot.generate_response("I bought it 2 weeks ago")
bot.generate_response("It doesn't turn on")
summary = bot.get_conversation_summary()
print(f"Summary: {summary}")

print("\n\nTest 4: Reset Functionality")
print("="*50)
before = len(bot.conversation_history)
bot.reset_conversation()
after = len(bot.conversation_history)
print(f"History before reset: {before} messages")
print(f"History after reset: {after} message (system prompt)")
print(f"Reset working: {'✅' if after == 1 else '❌'}")
Run the test suite:

python test_chatbot.py



