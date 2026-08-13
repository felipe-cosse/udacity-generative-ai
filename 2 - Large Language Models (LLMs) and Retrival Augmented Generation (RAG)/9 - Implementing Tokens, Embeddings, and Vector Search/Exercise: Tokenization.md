In this exercise, you'll manage tokens and control API costs for a customer service chatbot. You'll learn to count tokens, estimate costs, optimize conversation history, and handle long messages efficiently.

Production chatbots can cost thousands per month if not optimized properly. A 5,000-user customer service bot with poor token management might spend $5,000/month.

What you'll build: A complete token management system that can:

Count tokens accurately using tiktoken
Estimate API costs for different models
Optimize conversation history to fit token limits
Chunk long messages while preserving context
Analyze messages for cost optimization opportunities
Task 1: Initialize the Tokenizer
What to implement: Complete the __init__ method to set up tiktoken and pricing information.

Store the model name
self.model = model
Initialize tiktoken encoding
self.encoding = tiktoken.encoding_for_model(model)
This loads the correct tokenization rules for your model. Different models use different encodings:

GPT-3.5-turbo: cl100k_base encoding
GPT-4: cl100k_base encoding
Older models: p50k_base or r50k_base
Define pricing dictionary
self.pricing = {
    "gpt-3.5-turbo": {
        "input": 0.0005 / 1000,   # $0.0005 per 1K tokens
        "output": 0.0015 / 1000   # $0.0015 per 1K tokens
    },
    "gpt-4": {
        "input": 0.03 / 1000,
        "output": 0.06 / 1000
    },
    "gpt-4-turbo": {
        "input": 0.01 / 1000,
        "output": 0.03 / 1000
    }
}
Task 2: Count Tokens in Text
What to implement: Complete the count_tokens() method to count tokens in a string.

Text goes in: "Hello, how are you?"
Encoding converts to token IDs: [9906, 11, 1268, 527, 499, 30]
Count the IDs: 6 tokens
Task 3: Count Tokens in Message Lists
Complete count_message_tokens() to count tokens in conversation format.

Task 4: Estimate API Costs
Complete estimate_cost() to calculate the cost of an API call.

Input tokens: Everything you send (prompt + history + system message)
Output tokens: What the model generates
Output costs more because generation requires more compute.

Task 5: Optimize Conversation History
Complete optimize_conversation_history() to fit conversations within token limits. Conversations grow over time. Each new message must include all previous messages for context. This becomes expensive:

Turn 1: 50 tokens
Turn 2: 50 + 60 = 110 tokens
Turn 3: 50 + 60 + 55 = 165 tokens
Turn 8: 500+ tokens
Eventually you hit model limits or budget constraints.

The solution: Keep only recent messages. Drop older ones that are less relevant.

Keep system prompt (always important)
Work backwards from most recent messages
Add messages while staying under limit
Reverse to restore chronological order
Task 6: Chunk Long Messages
Complete chunk_long_message() to split long texts while maintaining context. Customers sometimes send very long messages (detailed complaints, product reviews with 500+ words). These can:

Exceed model context limits
Become expensive to process
Lose focus if processed all at once
Solution: Split into chunks with overlap. Overlap preserves context at chunk boundaries.

Task 7: Analyze Message Cost
Complete analyze_message_cost() to provide comprehensive cost analysis and recommendations.

Running the Demonstrations
After implementing all methods, uncomment the demo functions:

def main():
    demonstrate_token_counting()
    demonstrate_cost_estimation()
    demonstrate_history_optimization()
    demonstrate_message_chunking()
Run the complete demo:

python message_tokenizer.py



