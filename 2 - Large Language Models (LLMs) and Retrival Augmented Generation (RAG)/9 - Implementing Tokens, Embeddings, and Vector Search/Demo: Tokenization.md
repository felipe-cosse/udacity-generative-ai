In this demo, you'll learn how LLMs process text and how to calculate the costs of running AI applications.

How text gets converted into tokens
Why token count matters more than word count
How to calculate API costs for your applications
How conversation history affects costs exponentially
Strategies to optimize token usage and reduce costs by 60-80%
Part 1: Understanding Tokens
Run the cell that loads the tokenizer
Test the show_tokens() function with different texts
Pay attention to how punctuation and special characters affect token count
"Hello world" vs "Hello, world!" - Does punctuation add tokens?
"Tokenization" - How does this technical word split?
"GPT-3.5-turbo" - How are numbers and hyphens handled?
Add your own examples to see how they tokenize:

show_tokens("Your text here")
show_tokens("Try some emojis 🚀💡")
show_tokens("Test technical terms like API, HTTP, JSON")
You'll discover that 1 token ≈ 4 characters for English text, but this varies widely based on the vocabulary.

Part 2: Token Count Comparisons
Run the cell that compares different message types
Study the table showing characters, words, and tokens
Calculate the tokens-per-word ratio
Which message type has the highest tokens-per-word ratio? Why?
Do emojis increase token count significantly?
How do technical error messages tokenize compared to natural language?
You should see a table showing that:

Short queries: ~1.2 tokens per word
Technical messages: ~1.5 tokens per word (specialized vocabulary)
Messages with emojis: Higher ratio (each emoji is typically 1-3 tokens)
Part 3: Calculating API Costs
Review the pricing table for different models
Run the cost calculation example
Study the breakdown of input vs output costs
Output tokens cost 2-3x more than input tokens. This means:

Shorter, more concise responses save money
Setting max_tokens limits can control costs
Verbose prompts are less expensive than verbose responses
Part 4: Conversation History Token Growth
Run the conversation simulation
Watch the graphs showing token growth over time
Calculate the growth rate
The demo simulates an 8-turn conversation. Watch how:

Turn 1: 50 tokens
Turn 4: 290 tokens (5.8x growth)
Turn 8: 710 tokens (14x growth)
Part 5: Text Chunking Demonstration
Run the chunking function on the long customer message
Observe how overlap works
Count the total tokens vs. chunked tokens
Chunking parameters:

max_tokens=100 - Maximum tokens per chunk
overlap=20 - Tokens shared between adjacent chunks
Without overlap, you might split a sentence awkwardly:

Chunk 1: "I ordered three items on January 15th: a blue"
Chunk 2: "hiking backpack, a water bottle, and boots."
With overlap, you maintain context:

Chunk 1: "I ordered three items on January 15th: a blue hiking backpack"
Chunk 2: "a blue hiking backpack, a water bottle, and boots."
When to use this:

Processing long documents that exceed model context limits
RAG systems (chunking documents for embedding)
Batch processing where you need to maintain context
Part 6: Cost Optimization Strategies
Study the four strategies presented
Compare their token usage patterns in the graph
Calculate total cost for each strategy



