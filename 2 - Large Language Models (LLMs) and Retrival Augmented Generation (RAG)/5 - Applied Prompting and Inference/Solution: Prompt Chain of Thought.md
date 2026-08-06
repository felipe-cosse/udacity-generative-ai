Zero-Shot Prompting
Definition: Prompting without providing examples, relying solely on the model's pre-training.

When to use:

Simple, common tasks (sentiment analysis, summarization)
Tasks the model has seen during training
When you don't have examples
Quick prototyping
Good for:

"Summarize this article"
"Translate to French"
"What is machine learning?"
Not good for:

Custom classification schemes
Specific output formats
Domain-specific terminology
Few-Shot Prompting
Definition: Providing 2-5 examples to demonstrate the desired format, style, or pattern.

When to use:

Need consistent output format
Domain-specific tasks
Custom classification categories
Specific writing style
Optimal number of examples:

1 example: Better than zero-shot, but may not generalize
2-3 examples: Sweet spot for most tasks
4-5 examples: Diminishing returns
10+ examples: Usually unnecessary, uses too many tokens
Chain-of-Thought (CoT) Prompting
Definition: Instructing the model to show its reasoning steps before giving the final answer.

When to use:

Multi-step problems (math, logic)
Complex reasoning tasks
When you need to verify the logic
Debugging incorrect answers
Effective phrases:

"Let's think step by step."
"Show your reasoning."
"Explain your thought process."
"Work through this problem step by step."
Without CoT:

# Prompt
"A bakery sells cupcakes for $3 each. They offer a 20% discount on orders of 10 or more.
If a customer orders 15 cupcakes, what is the total cost?"

# Response
"$36"  # Wrong! (Correct answer is $36 with discount = $36 * 0.8 = $28.80)
With CoT:

# Prompt
"A bakery sells cupcakes for $3 each. They offer a 20% discount on orders of 10 or more.
If a customer orders 15 cupcakes, what is the total cost?

Let's think step by step and show the reasoning:"

# Response
"Let's solve this step by step:

Step 1: Calculate the base price
15 cupcakes × $3 each = $45

Step 2: Check if discount applies
15 cupcakes ≥ 10, so yes, 20% discount applies

Step 3: Calculate discount amount
$45 × 20% = $45 × 0.20 = $9

Step 4: Calculate final price
$45 - $9 = $36

Alternatively: $45 × (1 - 0.20) = $45 × 0.80 = $36

The total cost is $36."
Research findings:

Improves accuracy on GSM8K (math problems) from 17% to 78% (Wei et al., 2022)
Works across models (GPT-3, PaLM, LLaMA)
Effective for reasoning, not just math
Advanced CoT techniques:

Few-shot CoT: Combine examples with reasoning
"""
Example 1:
Q: Roger has 5 tennis balls. He buys 2 more. How many does he have?
A: Let's think step by step.
   * Roger starts with 5 balls
   * He buys 2 more
   * 5 + 2 = 7
   Answer: 7 tennis balls

Now solve:
Q: Sarah has 3 apples. She buys 4 more, then gives 2 away. How many does she have?
A: Let's think step by step.
"""
Self-consistency: Generate multiple CoT paths and take majority vote
# Generate 5 different reasoning paths
# If 4/5 say "36", that's the answer
Structured Output Prompting
Definition: Explicitly specifying the format of the response (JSON, CSV, tables, etc.).

When to use:

Integrating with code (need to parse output)
Data extraction tasks
Need consistent schema
Building APIs
Common formats:

JSON:```python prompt = """Extract person info in JSON format: 'John Smith, 35, lives in Seattle, works as engineer at TechCorp'
Format: {"name": "...", "age": ..., "city": "...", "occupation": "...", "company": "..."} """

1. **Markdown Table:**
```python
prompt = """Compare these products in a markdown table:
Product A: $50, 4.5 stars
Product B: $40, 4.0 stars

Format:
| Product | Price | Rating |
|---------|-------|--------|
| ...     | ...   | ...    |
"""
CSV:```python prompt = """Extract data as CSV: 'John, 35, Seattle' 'Jane, 28, Portland'
Format: name,age,city """


### Experiment 1: Zero-Shot vs Few-Shot

**Zero-shot response:**
"The sentiment is mixed/neutral. The customer expresses moderate satisfaction..."


* Verbose, inconsistent format
* Includes explanation (not requested)
* Format varies each time

**Few-shot response:**
"Neutral"


* Concise, matches example format
* Consistent across runs
* Easy to parse

**Lesson:** Few-shot dramatically improves format consistency.

### Experiment 2: Chain-of-Thought

**Without CoT:**
"$36"


* Just the answer, no work shown
* May be wrong, can't verify

**With CoT:**
"Step 1: Base price = 15 × $3 = $45 Step 2: Discount applies (15 ≥ 10) Step 3: Discount = $45 × 20% = $9 Step 4: Final price = $45 - $9 = $36 Answer: $36"


* Shows all work
* Can verify each step
* Builds trust in answer

CoT improves accuracy and trustworthiness for complex problems.

### Experiment 3: Structured Output

**Without format specification:**
"Name: John Smith Age: 35 years old City: Seattle, Washington Occupation: He works as a software engineer Company: TechCorp"


* Inconsistent structure
* Hard to parse
* Extra words ("years old", "He works as")

**With JSON format:**

```json
{
  "name": "John Smith",
  "age": 35,
  "city": "Seattle",
  "occupation": "software engineer",
  "company": "TechCorp"
}
Clean, parseable structure
Consistent field names
Easy integration with code
Always specify format for data extraction tasks.

Experiment 4: Comprehensive Comparison
Problem: Average speed with a stop

Zero-shot:

"52.5 mph"  # Wrong! Didn't account for stop time
Few-shot:

"Total distance = 210 miles
Total time = 4 hours
Average speed = 210 / 4 = 52.5 mph"  # Still wrong!
Chain-of-thought:

"Step 1: Distance = 120 + 90 = 210 miles
Step 2: Travel time = 2 + 1.5 = 3.5 hours
Step 3: Stop time = 0.5 hours
Step 4: Total time = 3.5 + 0.5 = 4 hours
Step 5: Average speed = 210 / 4 = 52.5 mph
Answer: 52.5 mph"  # Correct!
CoT helps catch subtle details (like the stop time).

Experiment 5: Real-World Application
Task: Extract structured product review data

Combining few-shot + structured output:

Provides example of desired JSON structure
Shows what fields to extract
Demonstrates handling of pros/cons lists
Result:

{
  "product_name": "UltraBook Pro 15\"",
  "price": 1299,
  "pros": [
    "excellent performance",
    "Intel i7 processor",
    "16GB RAM",
    "impressive battery life (10 hours)"
  ],
  "cons": [
    "mushy keyboard",
    "unresponsive trackpad"
  ],
  "rating": 4,
  "recommendation": "Yes, especially for productivity work"
}
Real-world tasks often require combining multiple techniques.

Congratulations! You now have a toolkit of prompt engineering techniques that work for virtually any LLM task. These patterns will serve you throughout your AI development journey!




