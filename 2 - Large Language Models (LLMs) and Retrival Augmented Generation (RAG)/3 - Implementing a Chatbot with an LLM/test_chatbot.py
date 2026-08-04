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