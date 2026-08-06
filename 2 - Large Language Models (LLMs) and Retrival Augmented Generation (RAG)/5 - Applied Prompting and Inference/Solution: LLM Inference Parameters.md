Understanding Temperature
Temperature Range: 0.0 to 2.0

The temperature parameter controls how the model selects the next token:

temperature = 0.0: Always picks the most likely token (argmax)
Use for: Factual Q&A, classification, code generation
Output: Completely deterministic and consistent
temperature = 0.3-0.5: Slightly randomized, focused
Use for: Technical writing, data analysis
Output: Consistent with minor variations
temperature = 0.7: Balanced (OpenAI's default)
Use for: Conversational AI, customer service
Output: Natural and varied but coherent
temperature = 0.9-1.0: Creative and diverse
Use for: Creative writing, brainstorming
Output: Surprising and original
temperature = 1.5-2.0: Highly random
Use for: Experimental creative content
Output: Unpredictable, may be incoherent
Low temperature → steeper probability distribution → picks most likely token
High temperature → flatter probability distribution → considers many tokens
Understanding Top-P (Nucleus Sampling)
Top-P Range: 0.0 to 1.0

Top-p sampling considers only the smallest set of tokens whose cumulative probability exceeds the threshold:

top_p = 0.1: Very focused
Considers only tokens that make up top 10% of probability mass
Most conservative, least diverse
top_p = 0.5: Moderately focused
Balanced between safety and diversity
top_p = 0.9: Diverse but coherent (most common)
Excludes only the least likely tokens
Good default for most applications
top_p = 1.0: No filtering
Considers all possible tokens
Equivalent to not using top-p
Example:

Suppose the model predicts the next word with these probabilities:

"the": 0.40
"a": 0.30
"an": 0.15
"this": 0.10
"that": 0.05
With top_p = 0.8:

Cumulative: "the" (0.40) + "a" (0.30) + "an" (0.15) = 0.85 > 0.8
Samples only from: ["the", "a", "an"]
Excludes: ["this", "that"]
Important: Don't use both high temperature AND high top_p simultaneously. Typically, set one to control diversity:

Set temperature, leave top_p at 1.0 (default)
OR set top_p, use temperature = 1.0
Understanding Max Tokens
Range: 1 to model's maximum (4096 for gpt-3.5-turbo, 8192 for gpt-4)

max_tokens limits the length of the generated response:

Includes only the response tokens, not the prompt
Responses may be cut off mid-sentence if limit is reached
Useful for controlling costs (you pay per token)
Useful for ensuring concise responses
Example:

# Short response (budget-friendly)
response = generate_with_max_tokens("Explain machine learning", max_tokens=50)
# Output: ~30-40 words, may be incomplete

# Medium response (balanced)
response = generate_with_max_tokens("Explain machine learning", max_tokens=200)
# Output: ~150 words, usually complete

# Long response (comprehensive)
response = generate_with_max_tokens("Explain machine learning", max_tokens=500)
# Output: ~375 words, detailed explanation
Cost Implications:

GPT-3.5-turbo: $0.002/1K output tokens
50 tokens: $0.0001
200 tokens: $0.0004
500 tokens: $0.001
Understanding Frequency Penalty
Range: -2.0 to 2.0 (typically use 0.0 to 2.0)

frequency_penalty penalizes tokens based on how often they've appeared so far:

0.0: No penalty (default)
May repeat words, phrases, or patterns
Natural for some contexts (e.g., "the" appears often)
0.5: Mild penalty
Reduces obvious repetition
Maintains natural language flow
1.0: Moderate penalty
Actively avoids repeating words
Good for lists, variety in responses
2.0: Maximum penalty
Strongly avoids any repetition
May use awkward synonyms to avoid repeating
Example:

Prompt: "List 10 benefits of exercise."

With frequency_penalty = 0.0:

1. Exercise improves cardiovascular health
2. Exercise strengthens muscles
3. Exercise enhances flexibility
4. Exercise boosts energy
5. Exercise improves mood
(Notice "Exercise" repeated at the start of each line)
With frequency_penalty = 1.5:

1. Improves cardiovascular health
2. Strengthens muscles
3. Enhances flexibility
4. Boosts energy levels
5. Elevates mood
(Varied sentence structures, avoids repetition)
Understanding Logprobs
What are logprobs?

Logprobs (log probabilities) show the model's confidence for each generated token:

High logprob (closer to 0): Model is confident
Example: logprob = -0.001 → probability ≈ 0.999 (99.9% confident)
Low logprob (very negative): Model is uncertain
Example: logprob = -3.0 → probability ≈ 0.05 (5% confident)
Use cases:

Debugging: Understand why model chose certain words
Confidence scoring: Identify uncertain predictions
Alternative generation: See what the model almost said
Quality assessment: Low-confidence tokens may indicate issues
Example Output:

# Prompt: "The capital of France is"
{
  'text': 'Paris.',
  'logprobs': {
    'tokens': ['Paris', '.'],
    'token_logprobs': [-0.0001, -0.0512],  # High confidence on "Paris"
    'top_logprobs': [
      {
        'Paris': -0.0001,   # 99.99% probability
        'France': -9.2103,  # 0.01% probability
        'Lyon': -10.3144    # 0.003% probability
      },
      {
        '.': -0.0512,
        '!': -3.0146,
        ',': -4.1234
      }
    ]
  }
}
Interpreting:

Model is extremely confident "Paris" is correct (logprob ≈ 0)
Alternative answers have very low probability
This indicates a factual, well-known answer
Experiment 1: Temperature Effects
temp=0.0: Same response every time
"In the year 2157, Dr. Sarah Chen discovered..."
Run it 5 times → identical output
temp=0.5: Slight variations
"In 2157, scientist Dr. Chen found..."
"Dr. Sarah Chen, in the year 2157..."
temp=1.0: Noticeable creativity
"The quantum clock shattered at midnight..."
"Nobody expected time itself to crack open..."
temp=1.5: Very creative, sometimes weird
"When yesterday became tomorrow, Marcus..."
"Time folded like origami in Dr. Webb's laboratory..."
Lesson: Use low temperature for consistency, high temperature for creativity.

Experiment 2: Top-P Sampling
top_p=0.1: Very focused answers
"...thorough testing and quality assurance."
(Picks from only the most likely words)
top_p=0.5: Moderately varied
"...comprehensive documentation and peer review."
top_p=0.9: Diverse responses
"...collaborative team communication and iterative feedback."
top_p=1.0: Maximum diversity
"...fostering a culture of continuous learning and adaptation."
Lesson: Lower top_p = safer, more predictable; Higher top_p = more creative variety.

Experiment 3: Length Control
Prompt: "Explain machine learning in detail."

max_tokens=50:
Machine learning is a subset of artificial intelligence that enables
computers to learn from data without being explicitly programmed. It
involves algorithms that can identify patterns...
(Cuts off incomplete)

max_tokens=100:
Machine learning is a subset of artificial intelligence that enables
computers to learn from data without being explicitly programmed. It
involves algorithms that identify patterns, make decisions, and improve
performance over time through experience. Common applications include...
(Still incomplete but more useful)

max_tokens=200:
[Complete explanation with introduction, key concepts, and examples]
(Full, coherent response)

Lesson: Set max_tokens based on desired response length, but allow buffer for completion.

Experiment 4: Repetition Penalty
Prompt: "List 10 benefits of exercise."

frequency_penalty=0.0:
Repetitive structure
"Exercise improves X, Exercise boosts Y..."
frequency_penalty=0.5:
More varied language
Mixes sentence structures
frequency_penalty=1.0:
Actively avoids repetition
Uses diverse vocabulary
frequency_penalty=2.0:
Maximum variety
May use unusual synonyms to avoid repeating
Use frequency_penalty for lists, varied responses, or to avoid monotonous language.

Experiment 5: Logprobs Analysis
Prompt: "The capital of France is"

High confidence on factual answer ("Paris")
Very low probability for alternatives
Shows model "knows" the answer with certainty
Prompt: "The best programming language is"

More evenly distributed probabilities
Multiple alternatives with decent probability
Shows model recognizes subjectivity



