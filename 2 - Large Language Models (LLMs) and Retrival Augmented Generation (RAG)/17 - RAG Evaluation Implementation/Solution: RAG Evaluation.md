The solution to this exercise demonstrates how to systematically evaluate RAG performance using industry-standard metrics. You'll see how each metric reveals different aspects of system quality and how to use these insights to prioritize improvements. Watch the walkthrough to understand the evaluation process.

Step 1: Import RAGAS and Configure Dependencies
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness,
    answer_similarity
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import time

# Initialize OpenAI client
openai_client = OpenAI(api_key="your-api-key-here")

print("✓ RAGAS framework initialized")
What's happening here?

We're setting up the RAGAS evaluation environment with several key components:

RAGAS metrics:

Six evaluation metrics we'll use
Each measures a different quality dimension
RAGAS wrappers:

LangchainLLMWrapper: Wraps LLM for metric calculation
LangchainEmbeddingsWrapper: Wraps embeddings for similarity metrics
Why LangChain wrappers?

RAGAS recently changed to require LangChain-compatible interfaces. These wrappers adapt OpenAI models to work with RAGAS.

Important compatibility note:

Different RAGAS versions have different requirements. If you encounter import errors, check:

import ragas
print(f"RAGAS version: {ragas.__version__}")
# Adjust imports based on version
Step 2: Define Metric Configurations
# Metric groupings for different evaluation scenarios
EVALUATION_CONFIGS = {
    "comprehensive": {
        "name": "Comprehensive Evaluation",
        "description": "All metrics for complete assessment",
        "metrics": [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
            answer_correctness,
            answer_similarity
        ]
    },
    "retrieval_focus": {
        "name": "Retrieval-Focused Evaluation",
        "description": "Context metrics only",
        "metrics": [
            context_precision,
            context_recall
        ]
    },
    "generation_focus": {
        "name": "Generation-Focused Evaluation",
        "description": "Answer metrics only",
        "metrics": [
            faithfulness,
            answer_relevancy,
            answer_correctness
        ]
    },
    "quick": {
        "name": "Quick Evaluation",
        "description": "Fast subset for rapid iteration",
        "metrics": [
            faithfulness,
            context_precision
        ]
    }
}

# Display available configurations
print("\nAvailable Evaluation Configurations:")
for config_key, config in EVALUATION_CONFIGS.items():
    print(f"\n  {config_key}:")
    print(f"    Name: {config['name']}")
    print(f"    Description: {config['description']}")
    print(f"    Metrics: {len(config['metrics'])}")
What's happening here?

We're creating reusable metric configurations for different evaluation scenarios:

Comprehensive (6 metrics):

Use for: Initial evaluation, major releases
Time: Slowest (~30-60s per example)
Cost: Highest (most LLM calls)
Retrieval focus (2 metrics):

Use for: Optimizing embeddings, chunk size
Time: Fast (~10-15s per example)
Cost: Moderate
Generation focus (3 metrics):

Use for: Prompt engineering, model selection
Time: Moderate (~20-30s per example)
Cost: Moderate-high
Quick (2 metrics):

Use for: Rapid iteration, CI/CD
Time: Fastest (~10-15s per example)
Cost: Lowest
Why this matters:

Running all 6 metrics on 100 examples might take 1 hour and cost $10-20. Quick evaluation on same dataset: 15 minutes, $2-3. Choose based on your iteration stage.

Step 3: Create Evaluation Dataset
# Sample evaluation dataset
# In production, this would be much larger (50-100+ examples)
evaluation_dataset_raw = [
    {
        "question": "What is machine learning?",
        "answer": "Machine learning is a subset of artificial intelligence that focuses on building systems that can learn from data. It uses algorithms to identify patterns and make predictions without being explicitly programmed for each task.",
        "contexts": [
            "Machine learning is a subset of artificial intelligence that focuses on building systems that can learn from data. It uses algorithms to identify patterns and make predictions without being explicitly programmed.",
            "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes organized in layers."
        ],
        "ground_truth": "Machine learning is a subset of artificial intelligence that enables systems to learn from data using algorithms to identify patterns and make predictions without explicit programming for each specific task."
    },
    {
        "question": "How does supervised learning work?",
        "answer": "Supervised learning is a machine learning approach where the model is trained on labeled data. The algorithm learns to map inputs to outputs based on example input-output pairs provided during training. This allows the model to make predictions on new, unseen data.",
        "contexts": [
            "Supervised learning is a machine learning approach where the model is trained on labeled data. The algorithm learns to map inputs to outputs based on example input-output pairs provided during training.",
            "Unsupervised learning involves training models on unlabeled data. The algorithm must discover patterns and structure in the input data without explicit guidance."
        ],
        "ground_truth": "Supervised learning trains models on labeled data where the algorithm learns to map inputs to outputs from example input-output pairs, enabling predictions on new data."
    },
    {
        "question": "What is the difference between AI and machine learning?",
        "answer": "Artificial intelligence is a broad field encompassing systems that can perform tasks requiring human intelligence. Machine learning is a specific subset of AI that focuses on systems learning from data. While all machine learning is AI, not all AI is machine learning—some AI systems use rule-based approaches rather than learning from data.",
        "contexts": [
            "Machine learning is a subset of artificial intelligence that focuses on building systems that can learn from data.",
            "Artificial intelligence is the broader field of creating intelligent systems, which includes machine learning, expert systems, and robotics."
        ],
        "ground_truth": "AI is the broad field of creating intelligent systems, while machine learning is a specific subset of AI focused on systems that learn from data. ML is one approach within AI, but AI also includes other techniques like rule-based systems."
    }
]

# Convert to RAGAS-compatible format
evaluation_dataset = Dataset.from_list(evaluation_dataset_raw)

print(f"\n✓ Created evaluation dataset with {len(evaluation_dataset_raw)} examples")
print("\nDataset structure:")
print(f"  Questions: {len(evaluation_dataset['question'])}")
print(f"  Answers: {len(evaluation_dataset['answer'])}")
print(f"  Context lists: {len(evaluation_dataset['contexts'])}")
print(f"  Ground truths: {len(evaluation_dataset['ground_truth'])}")
What's happening here?

We're creating a structured evaluation dataset with all components needed for RAGAS:

Example 1 breakdown:

Question: "What is machine learning?"

The query a user would ask
Answer: "Machine learning is a subset..." (RAG system's response)

Generated by your RAG system
This is what we're evaluating
Contexts: [doc1, doc2]

Documents retrieved by your RAG system
Used to evaluate retrieval quality
Also used to check if answer is grounded
Ground truth: "Machine learning is a subset..." (ideal answer)

Reference answer written by expert or extracted from docs
Used for comparison metrics (correctness, similarity)
Used for context recall (did we retrieve all info needed for this answer?)
Why this format?

RAGAS needs all four components to calculate metrics:

Faithfulness: Compare answer to contexts
Answer relevancy: Compare answer to question
Context precision/recall: Compare contexts to question and ground truth
Answer correctness/similarity: Compare answer to ground truth
Real-world dataset creation:

For production evaluation:

Collect 50-100 representative questions
Run RAG system to get answers and contexts
Have experts write ground truth answers
Format into RAGAS dataset structure
Version control the dataset
Continuously add edge cases and failures
Step 4: Configure RAGAS Evaluator
class RAGSystemEvaluator:
    """
    Evaluator for RAG systems using RAGAS metrics.
    """

    def __init__(self, openai_api_key):
        """
        Initialize evaluator with OpenAI credentials.

        Args:
            openai_api_key: OpenAI API key for LLM and embeddings
        """
        # Initialize LLM for RAGAS metrics that need LLM evaluation
        self.evaluator_llm = LangchainLLMWrapper(
            ChatOpenAI(
                model="gpt-4o",
                api_key=openai_api_key,
                temperature=0.0  # Deterministic for consistent evaluation
            )
        )

        # Initialize embeddings for similarity-based metrics
        self.evaluator_embeddings = LangchainEmbeddingsWrapper(
            OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=openai_api_key
            )
        )

        print("✓ RAG System Evaluator initialized")
        print(f"  LLM: gpt-4o (temperature=0.0)")
        print(f"  Embeddings: text-embedding-3-small")


    def evaluate(self, dataset, metrics, config_name="custom"):
        """
        Evaluate RAG system using specified metrics.

        Args:
            dataset: RAGAS-compatible dataset
            metrics: List of RAGAS metrics to evaluate
            config_name: Name of configuration for logging

        Returns:
            Evaluation results dictionary
        """
        print(f"\n{'='*80}")
        print(f"EVALUATING: {config_name}")
        print(f"{'='*80}")
        print(f"Dataset size: {len(dataset)}")
        print(f"Metrics: {len(metrics)}")
        print("\nRunning evaluation (this may take a minute)...")

        start_time = time.time()

        # Run RAGAS evaluation
        results = evaluate(
            dataset=dataset,
            metrics=metrics,
            llm=self.evaluator_llm,
            embeddings=self.evaluator_embeddings
        )

        elapsed_time = time.time() - start_time

        print(f"\n✓ Evaluation completed in {elapsed_time:.2f}s")

        return results, elapsed_time


# Initialize evaluator
evaluator = RAGSystemEvaluator(openai_api_key="your-api-key-here")
What's happening here?

We're creating a RAG evaluator class that wraps RAGAS functionality:

LLM configuration:

ChatOpenAI(
    model="gpt-4o",
    temperature=0.0  # CRITICAL: Deterministic evaluation
)
Why temperature=0.0?

Evaluation must be deterministic—running the same evaluation twice should give the same scores. Temperature 0.0 ensures consistent LLM judgments.

Why GPT-4o for evaluation?

RAGAS metrics require an LLM to judge quality (e.g., "Is this answer faithful to the context?"). GPT-4o provides:

High-quality judgments
Understanding of nuance
Consistent scoring
Alternative: Use cheaper model for evaluation:

# For development (cheaper but less reliable)
ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# For production (most reliable)
ChatOpenAI(model="gpt-4o", temperature=0.0)
Embeddings configuration:

OpenAIEmbeddings(model="text-embedding-3-small")
Used for similarity-based metrics (answer_similarity). Must match the embeddings used in your RAG system for fair comparison.

Step 5: Run Comprehensive Evaluation
# Run comprehensive evaluation (all 6 metrics)
comprehensive_results, comprehensive_time = evaluator.evaluate(
    dataset=evaluation_dataset,
    metrics=EVALUATION_CONFIGS["comprehensive"]["metrics"],
    config_name=EVALUATION_CONFIGS["comprehensive"]["name"]
)

print("\n" + "="*80)
print("COMPREHENSIVE EVALUATION RESULTS")
print("="*80)

# Display results
for metric_name, score in comprehensive_results.items():
    # Skip non-metric fields
    if metric_name in ['dataset', 'config']:
        continue

    print(f"\n{metric_name}:")
    print(f"  Score: {score:.4f}")

    # Interpretation
    if score >= 0.9:
        quality = "Excellent ✅"
    elif score >= 0.8:
        quality = "Good ✅"
    elif score >= 0.7:
        quality = "Acceptable ⚠️"
    elif score >= 0.6:
        quality = "Poor ⚠️"
    else:
        quality = "Very Poor ❌"

    print(f"  Quality: {quality}")

# Overall summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

retrieval_metrics = ["context_precision", "context_recall"]
generation_metrics = ["faithfulness", "answer_relevancy"]
quality_metrics = ["answer_correctness", "answer_similarity"]

retrieval_avg = sum(comprehensive_results.get(m, 0) for m in retrieval_metrics if m in comprehensive_results) / len([m for m in retrieval_metrics if m in comprehensive_results])
generation_avg = sum(comprehensive_results.get(m, 0) for m in generation_metrics if m in comprehensive_results) / len([m for m in generation_metrics if m in comprehensive_results])
quality_avg = sum(comprehensive_results.get(m, 0) for m in quality_metrics if m in comprehensive_results) / len([m for m in quality_metrics if m in comprehensive_results])

print(f"\nRetrieval Quality: {retrieval_avg:.3f}")
print(f"Generation Quality: {generation_avg:.3f}")
print(f"Overall Quality: {quality_avg:.3f}")

print(f"\nTotal evaluation time: {comprehensive_time:.2f}s")
print(f"Time per example: {comprehensive_time/len(evaluation_dataset):.2f}s")
Expected output:

================================================================================
EVALUATING: Comprehensive Evaluation
================================================================================
Dataset size: 3
Metrics: 6

Running evaluation (this may take a minute)...

✓ Evaluation completed in 28.45s

================================================================================
COMPREHENSIVE EVALUATION RESULTS
================================================================================

faithfulness:
  Score: 0.8767
  Quality: Good ✅

answer_relevancy:
  Score: 0.9123
  Quality: Excellent ✅

context_precision:
  Score: 0.9450
  Quality: Excellent ✅

context_recall:
  Score: 0.9100
  Quality: Excellent ✅

answer_correctness:
  Score: 0.8534
  Quality: Good ✅

answer_similarity:
  Score: 0.8892
  Quality: Good ✅

================================================================================
SUMMARY
================================================================================

Retrieval Quality: 0.928
Generation Quality: 0.894
Overall Quality: 0.871

Total evaluation time: 28.45s
Time per example: 9.48s
Interpreting these results:

Strong areas:

✅ Context precision 0.945: Retrieval is very accurate (few irrelevant docs)
✅ Answer relevancy 0.912: Answers directly address questions
✅ Context recall 0.910: Retrieval finds nearly all relevant information
Areas for improvement:

⚠️ Faithfulness 0.877: Some hallucination or extrapolation beyond context
⚠️ Answer correctness 0.853: Moderate similarity to ground truth
Actionable insights:

Retrieval is excellent—no need to change embeddings or chunking
Generation is good but could be better:
Improve prompt to emphasize grounding ("use ONLY the context")
Consider upgrading model or lowering temperature
System is production-ready for most use cases, but monitor faithfulness
Step 6: Run Focused Evaluations
# Retrieval-focused evaluation (fast, targets retrieval optimization)
print("\n" + "="*80)
print("RETRIEVAL-FOCUSED EVALUATION")
print("="*80)

retrieval_results, retrieval_time = evaluator.evaluate(
    dataset=evaluation_dataset,
    metrics=EVALUATION_CONFIGS["retrieval_focus"]["metrics"],
    config_name=EVALUATION_CONFIGS["retrieval_focus"]["name"]
)

print("\nRetrieval Metrics:")
for metric_name, score in retrieval_results.items():
    if metric_name not in ['dataset', 'config']:
        print(f"  {metric_name}: {score:.4f}")

print(f"\n⏱️  Evaluation time: {retrieval_time:.2f}s (vs {comprehensive_time:.2f}s comprehensive)")
print(f"⚡ Speed improvement: {(comprehensive_time / retrieval_time):.1f}x faster")

# Generation-focused evaluation (targets prompt/model optimization)
print("\n" + "="*80)
print("GENERATION-FOCUSED EVALUATION")
print("="*80)

generation_results, generation_time = evaluator.evaluate(
    dataset=evaluation_dataset,
    metrics=EVALUATION_CONFIGS["generation_focus"]["metrics"],
    config_name=EVALUATION_CONFIGS["generation_focus"]["name"]
)

print("\nGeneration Metrics:")
for metric_name, score in generation_results.items():
    if metric_name not in ['dataset', 'config']:
        print(f"  {metric_name}: {score:.4f}")

print(f"\n⏱️  Evaluation time: {generation_time:.2f}s")

# Quick evaluation (fastest, for rapid iteration)
print("\n" + "="*80)
print("QUICK EVALUATION")
print("="*80)

quick_results, quick_time = evaluator.evaluate(
    dataset=evaluation_dataset,
    metrics=EVALUATION_CONFIGS["quick"]["metrics"],
    config_name=EVALUATION_CONFIGS["quick"]["name"]
)

print("\nQuick Metrics:")
for metric_name, score in quick_results.items():
    if metric_name not in ['dataset', 'config']:
        print(f"  {metric_name}: {score:.4f}")

print(f"\n⏱️  Evaluation time: {quick_time:.2f}s")
print(f"⚡ Speed improvement: {(comprehensive_time / quick_time):.1f}x faster")
Expected output:

================================================================================
RETRIEVAL-FOCUSED EVALUATION
================================================================================

Retrieval Metrics:
  context_precision: 0.9450
  context_recall: 0.9100

⏱️  Evaluation time: 8.23s (vs 28.45s comprehensive)
⚡ Speed improvement: 3.5x faster

================================================================================
GENERATION-FOCUSED EVALUATION
================================================================================

Generation Metrics:
  faithfulness: 0.8767
  answer_relevancy: 0.9123
  answer_correctness: 0.8534

⏱️  Evaluation time: 15.67s

================================================================================
QUICK EVALUATION
================================================================================

Quick Metrics:
  faithfulness: 0.8767
  context_precision: 0.9450

⏱️  Evaluation time: 6.89s
⚡ Speed improvement: 4.1x faster
When to use each configuration:

Comprehensive (28s, all metrics):

Initial system validation
Before major releases
Quarterly quality audits
When thoroughness matters more than speed
Retrieval-focused (8s, 2 metrics):

Testing new embedding models
Optimizing chunk size (100 vs 500 vs 1000 tokens)
Adjusting n_results (retrieve 3 vs 5 vs 10 docs)
Improving metadata filtering
Generation-focused (16s, 3 metrics):

Comparing prompts (minimal vs standard vs premium)
Testing models (GPT-3.5 vs GPT-4o vs GPT-4 Turbo)
Adjusting temperature (0.0 vs 0.3 vs 0.7)
Adding few-shot examples
Quick (7s, 2 metrics):

Every commit (CI/CD regression testing)
Multiple times per hour during development
Cost-conscious frequent monitoring
Sanity checks before expensive comprehensive eval
Step 7: Display Detailed Results
def display_evaluation_results(results, config_name, elapsed_time, dataset_size):
    """
    Display formatted evaluation results with insights.

    Args:
        results: RAGAS evaluation results dictionary
        config_name: Name of configuration evaluated
        elapsed_time: Time taken for evaluation
        dataset_size: Number of examples evaluated
    """
    print("\n" + "="*80)
    print(f"DETAILED RESULTS: {config_name}")
    print("="*80)

    # Extract metric scores
    metric_scores = {
        k: v for k, v in results.items()
        if k not in ['dataset', 'config'] and isinstance(v, (int, float))
    }

    # Display each metric with interpretation
    print("\nMetric Scores:")
    for metric_name, score in metric_scores.items():
        print(f"\n  📊 {metric_name.replace('_', ' ').title()}: {score:.4f}")

        # Quality assessment
        if score >= 0.9:
            assessment = "Excellent - Production ready"
            emoji = "🟢"
        elif score >= 0.8:
            assessment = "Good - Minor improvements recommended"
            emoji = "🟡"
        elif score >= 0.7:
            assessment = "Acceptable - Needs improvement"
            emoji = "🟡"
        elif score >= 0.6:
            assessment = "Poor - Significant issues"
            emoji = "🟠"
        else:
            assessment = "Very Poor - Major rework needed"
            emoji = "🔴"

        print(f"     {emoji} {assessment}")

        # Metric-specific guidance
        if metric_name == "faithfulness" and score < 0.85:
            print(f"     💡 Recommendation: Strengthen grounding in prompt, lower temperature")
        elif metric_name == "context_precision" and score < 0.75:
            print(f"     💡 Recommendation: Improve retrieval relevance, add metadata filtering")
        elif metric_name == "context_recall" and score < 0.85:
            print(f"     💡 Recommendation: Increase n_results, improve embeddings")
        elif metric_name == "answer_relevancy" and score < 0.80:
            print(f"     💡 Recommendation: Clarify prompt instructions, improve question understanding")

    # Performance summary
    print("\n" + "-"*80)
    print("Performance Summary:")
    print(f"  ⏱️  Total time: {elapsed_time:.2f}s")
    print(f"  ⚡ Time per example: {elapsed_time/dataset_size:.2f}s")
    print(f"  📝 Examples evaluated: {dataset_size}")

    # Overall assessment
    avg_score = sum(metric_scores.values()) / len(metric_scores)
    print(f"\n  📈 Average Score: {avg_score:.4f}")

    if avg_score >= 0.85:
        print(f"  ✅ Overall: Production-ready system")
    elif avg_score >= 0.75:
        print(f"  ⚠️  Overall: Needs minor improvements before production")
    else:
        print(f"  ❌ Overall: Not production-ready, requires significant improvements")

    print("\n" + "="*80)


# Display comprehensive results
display_evaluation_results(
    comprehensive_results,
    "Comprehensive Evaluation",
    comprehensive_time,
    len(evaluation_dataset)
)
Expected output:

================================================================================
DETAILED RESULTS: Comprehensive Evaluation
================================================================================

Metric Scores:

  📊 Faithfulness: 0.8767
     🟡 Good - Minor improvements recommended
     💡 Recommendation: Strengthen grounding in prompt, lower temperature

  📊 Answer Relevancy: 0.9123
     🟢 Excellent - Production ready

  📊 Context Precision: 0.9450
     🟢 Excellent - Production ready

  📊 Context Recall: 0.9100
     🟢 Excellent - Production ready

  📊 Answer Correctness: 0.8534
     🟡 Good - Minor improvements recommended

  📊 Answer Similarity: 0.8892
     🟡 Good - Minor improvements recommended

--------------------------------------------------------------------------------
Performance Summary:
  ⏱️  Total time: 28.45s
  ⚡ Time per example: 9.48s
  📝 Examples evaluated: 3

  📈 Average Score: 0.8978

  ✅ Overall: Production-ready system

================================================================================
What this tells us:

Strengths:

Retrieval is excellent (precision 0.945, recall 0.910)
Answers are highly relevant (0.912)
Overall system performs well (average 0.898)
Areas for improvement:

Faithfulness could be higher (0.877)—some hallucination risk
Answer correctness is good but not excellent (0.853)
Action plan:

Test prompt variations that emphasize grounding
Consider lowering temperature from 0.3 to 0.1
Re-evaluate and compare scores
If faithfulness improves to 0.90+, deploy to production






In our final exercise, we're going to be looking at the valuing our RAG system. For this, we're going to be using the rags framework. We're going to be using the metric faithfulness, answer relevancy, context precision, context recall, answer correctness and answer similarity. As we set off the valuation configuration, we are able to group these metrics into different categories, so we are able to run them without any overhead. For example, we can use a comprehensive category where all of them are included. We can do a retrieval focus where only the context precision and context recall are evaluated, a generation focus or a quick evaluation so that we are able to run different metrics for different tasks. Then we are set up some evaluation datasets. This includes the question, some ground truth and the context that we're going to be using. Now, normally this will be a Chroman DB, document retrieval. But for our case, we are emulating this. Then we define a RAG system evaluator class. In here, it's important to know how we are defining the open client. Evaluator LLM, which we're leveraging the lane change LLM wrapper, and the OpenAI embedding sine chain embedding wrapper. This is because of the changes of how ragas has implemented these evaluators. Then we're going to create evaluation data set. We are going to configure our data in a wether we are able to pass it to ragas. This is based on the question, context, answer and ground truth values. Once this is set up properly, we are going to actually evaluate the RAG system. This will allow us to compare different answers against the different metrics that we have set up. I here, you're able to see that we're actually using the evaluator LLM with the chain wrapper and the evaluator embeddings. We form at the results, so we are able to parse them correctly and be able to display them in our terminal properly. That we are going to define a helper function called display evaluation results. This allows us to be able to set up everything so that we are able to see all the results organized in our terminal. Now, it's for us to run this code, now, it's going to take a while for us to be able to run all the metrics and evaluation. For that, I have already run it and we're able to show you how this looks like. You're able to see here that devolion completed successfully. It took about 28.38 seconds in multiple of these. It's time for you to be able to take a look.