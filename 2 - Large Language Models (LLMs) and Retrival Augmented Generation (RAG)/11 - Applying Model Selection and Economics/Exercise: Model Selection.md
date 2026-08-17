This exercise introduces a critical skill for AI engineers: model selection and evaluation. Not all language models are created equal—different models excel at different tasks. OpenAI's model lineup includes specialized models optimized for reasoning (like o1-mini) and models optimized for general-purpose generation (like GPT-4o). Understanding which model to use for which task can dramatically impact both the quality of your results and your cost efficiency.

In this hands-on exercise, you'll systematically evaluate two model types across different task categories, measuring not just response quality but also latency and token consumption. This real-world evaluation approach mirrors how production AI systems are optimized—balancing quality, speed, and cost.

By the end of this exercise, you will be able to:

Distinguish between reasoning models and generation models and understand their architectural and behavioral differences
Design task-specific test cases that effectively evaluate model capabilities across reasoning and creative generation
Implement systematic model comparison using consistent test harnesses and evaluation criteria
Measure multiple performance dimensions: accuracy, creativity, latency, and token efficiency
Interpret evaluation results to make informed model selection decisions for production applications
Balance quality, speed, and cost when choosing models for different use cases
Create automated evaluation frameworks that scale across multiple models, tasks, and metrics

Step 1: Configure Models for Comparison
import openai
from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI(api_key="your-api-key-here")

# Model configurations
REASONING_MODEL = {
    "name": "o1-mini",
    "temperature": 1,
    "max_tokens": 500
}

GENERATION_MODEL = {
    "name": "gpt-4o",
    "temperature": 1,
    "max_tokens": 500,
    "top_p": 0.95
}
o1-mini (Reasoning Model):

Temperature: 1 (standard randomness—reasoning models handle this differently internally)
Max tokens: 500 (enough for detailed reasoning)
No top_p (reasoning models use different sampling strategies)
GPT-4o (Generation Model):

Temperature: 1 (standard creativity level)
Max tokens: 500 (same as reasoning model for fair comparison)
Top_p: 0.95 (nucleus sampling—considers top 95% probable tokens)
Why these parameters?

Same max_tokens: Fair comparison of output length
Same temperature: Consistent randomness levels
Top_p for GPT-4o: Standard best practice for generation quality
Step 2: Define Reasoning Task Test Cases
Create a test suite for reasoning tasks that covers different types of logical thinking:

Task 1: Arithmetic Calculation

Tests: Basic math operations, multi-step calculation
Expected: Correct numerical answer ($12.00)
Success criteria: Answer contains exact amount
Task 2: Logical Deduction

Tests: Syllogistic reasoning, avoiding logical fallacies
Expected: Correct conclusion (No) with reasoning
Success criteria: Recognizes the logical fallacy (affirming the consequent)
Task 3: Word Problem (Algebra)

Tests: Problem setup, equation solving, real-world application
Expected: Correct time (12:00 PM)
Success criteria: Shows work and reaches correct answer
Step 3: Define Generation Task Test Cases
Create a test suite for generation tasks that covers different creative outputs:

Task 1: Marketing Copy

Tests: Persuasive writing, feature highlighting, conciseness
Keywords: Must mention hydration, tracking, smart features
Success criteria: Compelling, professional, includes key features
Task 2: Poetry (Haiku)

Tests: Creativity within constraints, thematic consistency
Keywords: Should reference AI and technology
Success criteria: Follows haiku structure (5-7-5 syllables), on-theme
Task 3: Customer Service Email

Tests: Empathy, professionalism, problem-solving
Keywords: Apology language, solution-oriented words
Success criteria: Friendly tone, clear resolution offered
Step 4: Implement Test Execution Function
This function implements a test harness that:

Measures latency: Records time before and after API call
Handles model differences: o1 models use different parameters than GPT models
Extracts results: Gets answer text and token usage
Returns structured data: Packages everything for analysis
Latency measurement:

start_time = time.time()
# ... API call ...
end_time = time.time()
latency = end_time - start_time
Captures total time including network latency, queue time, and generation time.

Token usage extraction:

tokens_used = {
    "prompt_tokens": response.usage.prompt_tokens,    # Input cost
    "completion_tokens": response.usage.completion_tokens,  # Output cost
    "total_tokens": response.usage.total_tokens      # Total cost
}
For cost analysis, different token types have different prices.

Step 5: Implement Evaluation Functions
Implement automated evaluation metrics:

Accuracy Evaluation (for reasoning tasks):

Simple substring matching
Case-insensitive comparison
Returns binary score (1 or 0)
Step 6: Run Full Test Suite for Reasoning Tasks
This function orchestrates a full comparison test:

Loop through all reasoning tasks (3 tasks)
Test both models on each task (6 total tests)
Evaluate results using accuracy metric
Display formatted results with comparison
Highlight winner for each dimension
Step 7: Run Full Test Suite for Generation Tasks
GPT-4o excels at creative writing tasks
o1-mini can generate text but isn't optimized for it
Speed advantage of generation models is clear (30-50% faster)
Quality difference is noticeable in tone and engagement
Step 8: Calculate Cost Analysis
Optimize cost per query type
Improve quality by using specialized models
Reduce latency on simple tasks



