The RAGAS Evaluation Framework
RAGAS provides six complementary metrics that evaluate different aspects of RAG quality:

Retrieval Metrics (Did we find the right documents?)

Context Precision: Are the retrieved documents relevant to the query?
Measures: Retrieval accuracy (no irrelevant documents)
Scale: 0 (all irrelevant) to 1 (all relevant)
Context Recall: Did we retrieve all the information needed to answer correctly?
Measures: Retrieval completeness (no missing documents)
Scale: 0 (missed everything) to 1 (found everything)
Generation Metrics (Did we create a good answer?)

Faithfulness: Is the generated answer factually consistent with retrieved context?
Measures: Hallucination and factual accuracy
Scale: 0 (completely unfaithful) to 1 (perfectly grounded)
Answer Relevancy: Is the generated answer relevant to the user's question?
Measures: Whether answer addresses the query
Scale: 0 (off-topic) to 1 (directly answers question)
Hybrid Metrics (Overall quality)

Answer Correctness: How semantically similar is the answer to ground truth?
Measures: Overall answer quality
Scale: 0 (completely wrong) to 1 (matches ground truth)
Answer Similarity: How similar is the answer to ground truth (embedding-based)?
Measures: Semantic similarity
Scale: 0 (very different) to 1 (nearly identical)
Why Multiple Metrics Matter
A single metric can't capture RAG complexity. Consider these scenarios:

Scenario 1: Good retrieval, poor generation

Context precision: 0.95 ✅
Context recall: 0.90 ✅
Faithfulness: 0.45 ❌
Answer relevancy: 0.50 ❌
Diagnosis: Retrieval is excellent, but the LLM is hallucinating or going off-topic. Fix: Improve prompt (emphasize grounding), upgrade LLM model, lower temperature.

Scenario 2: Poor retrieval, good generation

Context precision: 0.50 ❌
Context recall: 0.40 ❌
Faithfulness: 0.85 ✅
Answer relevancy: 0.80 ✅
Diagnosis: LLM generates good answers, but retrieval isn't finding the right documents. Fix: Improve embeddings, adjust chunk size, add more documents, improve metadata.

Scenario 3: Everything is mediocre

All metrics: 0.6-0.7
Diagnosis: Systemic issues—poor document quality, wrong domain, insufficient training data. Fix: Rebuild knowledge base, collect better ground truth, reconsider approach.

Metric Categories and Use Cases
RAGAS supports grouped evaluation for different scenarios:

Comprehensive Evaluation (All 6 metrics)

metrics_comprehensive = [
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness,
    answer_similarity
]
Use when:

Initial system evaluation
Before major releases
Comparing fundamentally different approaches
Building confidence for stakeholders
Retrieval-Focused Evaluation (Context metrics only)

metrics_retrieval = [
    context_precision,
    context_recall
]
Use when:

Optimizing embedding models
Testing chunk size variations
Improving metadata filtering
Debugging retrieval issues
Generation-Focused Evaluation (Answer metrics only)

metrics_generation = [
    faithfulness,
    answer_relevancy,
    answer_correctness
]
Use when:

Comparing LLM models
Optimizing prompts
Adjusting temperature/top_p
Testing few-shot examples
Quick Evaluation (Fast subset)

metrics_quick = [
    faithfulness,
    context_precision
]
Use when:

Rapid iteration during development
CI/CD regression tests
High-frequency monitoring
Cost-conscious evaluation
Ground Truth: The Foundation of Evaluation
All RAGAS metrics require ground truth—reference answers that represent the ideal response.

What makes good ground truth?

Accurate: Factually correct based on your knowledge base
Complete: Contains all relevant information
Concise: Focused on answering the specific question
Consistent: Similar format and style across examples
Representative: Covers diverse query types and difficulty levels
Ground truth sources:

Manual creation (highest quality):

ground_truth = {
    "question": "What is the capital of France?",
    "answer": "The capital of France is Paris, located in the north-central part of the country."
}
Expert annotation (gold standard):

Domain experts write ideal answers
Expensive but highest quality
Essential for high-stakes applications (medical, legal, financial)
Existing documentation (practical):

Extract from FAQs, documentation
Curate and validate
Good balance of cost and quality
Synthetic generation (scalable):

Use LLMs to generate ground truth
Human review and correction
Can scale to thousands of examples
Quality varies
User feedback (continuous improvement):

Collect thumbs up/down from users
Mine successful responses
Identify common failure cases
Iteratively improve
The Evaluation Dataset Format
RAGAS expects data in a specific format:

evaluation_dataset = {
    'question': [
        "What is machine learning?",
        "How does authentication work?"
    ],
    'answer': [
        "Machine learning is a subset of AI that enables systems to learn from data...",
        "Authentication verifies user identity using credentials like passwords..."
    ],
    'contexts': [
        [  # List of retrieved documents for question 1
            "Machine learning algorithms learn patterns from data...",
            "ML is used in recommendation systems and prediction..."
        ],
        [  # List of retrieved documents for question 2
            "Authentication requires valid credentials...",
            "Common methods include passwords and API keys..."
        ]
    ],
    'ground_truth': [
        "Machine learning is a subset of artificial intelligence...",
        "Authentication is the process of verifying user identity..."
    ]
}
Key requirements:

All lists must be the same length
contexts is a list of lists (each question has multiple context documents)
answer is the RAG-generated answer
ground_truth is the ideal answer
Interpreting RAGAS Scores
Score ranges and interpretations:

Score Range	Quality	Action
0.9 - 1.0	Excellent	Production-ready, monitor for regression
0.8 - 0.9	Good	Production-ready with minor improvements
0.7 - 0.8	Acceptable	Needs improvement before production
0.6 - 0.7	Poor	Significant issues, not production-ready
0.0 - 0.6	Very Poor	Fundamental problems, major rework needed
Metric-specific thresholds:

Different metrics have different acceptable thresholds:

Faithfulness: Should be very high (0.85+)

Low faithfulness = hallucination risk
Critical for trust and safety
Never compromise on this metric
Answer Relevancy: Should be high (0.80+)

Low relevancy = poor user experience
Indicates prompt or model issues
Affects user satisfaction directly
Context Precision: Should be high (0.75+)

Low precision = wasted context tokens
Indicates retrieval is too broad
Affects cost and latency
Context Recall: Should be very high (0.85+)

Low recall = incomplete answers
Indicates retrieval misses relevant docs
Affects answer quality directly
Answer Correctness/Similarity: Should be high (0.75+)

Measures overall quality
Balance against other metrics
Less critical than faithfulness
Evaluation-Driven Development
Use RAGAS to guide iterative improvement:

1. Baseline Evaluation
   ↓
2. Identify Weakest Metric
   ↓
3. Hypothesize Root Cause
   ↓
4. Make Targeted Change
   ↓
5. Re-Evaluate
   ↓
6. Compare Before/After
   ↓
7. Keep if Improved, Revert if Not
   ↓
8. Repeat
Example iteration cycle:

Iteration 1: Baseline

Faithfulness: 0.65
Answer relevancy: 0.72
Context recall: 0.88
Context precision: 0.91
Analysis: Generation is weak (faithfulness/relevancy low), retrieval is strong.

Iteration 2: Improve prompt

Change: Add explicit grounding instructions
Result: Faithfulness: 0.78 (+0.13), Answer relevancy: 0.81 (+0.09)
Keep change
Iteration 3: Upgrade model

Change: GPT-3.5 Turbo → GPT-4o
Result: Faithfulness: 0.89 (+0.11), Answer relevancy: 0.88 (+0.07)
Keep change
Iteration 4: Test complete

All metrics > 0.85
Ready for production



