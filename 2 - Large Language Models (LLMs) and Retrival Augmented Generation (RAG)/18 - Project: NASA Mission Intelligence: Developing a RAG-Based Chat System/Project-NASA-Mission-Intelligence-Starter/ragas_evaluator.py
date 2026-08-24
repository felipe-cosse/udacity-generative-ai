import os
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from typing import Dict, List, Optional

# RAGAS imports
try:
    from ragas import SingleTurnSample
    from ragas.metrics import BleuScore, NonLLMContextPrecisionWithReference, ResponseRelevancy, Faithfulness, RougeScore
    from ragas import evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

def evaluate_response_quality(question: str, answer: str, contexts: List[str]) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics"""
    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}
    
    if not question or not question.strip():
        return {"error": "Question cannot be empty"}

    if not answer or not answer.strip():
        return {"error": "Answer cannot be empty"}

    clean_contexts = [
        context.strip()
        for context in (contexts or [])
        if isinstance(context, str) and context.strip()
    ]

    if not clean_contexts:
        return {"error": "At least one valid context is required"}

    api_key = (
        os.getenv("CHROMA_OPENAI_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )

    if not api_key:
        return {"error": "OpenAI API key is not configured"}

    base_url = os.getenv(
        "OPENAI_BASE_URL",
        "https://openai.vocareum.com/v1",
    )

    try:
    # TODO: Create evaluator LLM with model gpt-3.5-turbo
        evaluator_llm = LangchainLLMWrapper(
            ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=api_key,
                base_url=base_url,
                temperature=0,
            )
        )
    # TODO: Create evaluator_embeddings with model test-embedding-3-small
        evaluator_embeddings = LangchainEmbeddingsWrapper(
            OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=api_key,
                base_url=base_url,
            )
        )
    # TODO: Define an instance for each metric to evaluate
        metrics = {
            "response_relevancy": ResponseRelevancy(
                llm=evaluator_llm,
                embeddings=evaluator_embeddings,
            ),
            "faithfulness": Faithfulness(
                llm=evaluator_llm,
            ),
        }

        sample = SingleTurnSample(
            user_input=question.strip(),
            response=answer.strip(),
            retrieved_contexts=clean_contexts,
        )
    # TODO: Evaluate the response using the metrics
        evaluation_results = {}

        for metric_name, metric in metrics.items():
            score = metric.single_turn_score(sample)
            evaluation_results[metric_name] = float(score)
    # TODO: Return the evaluation results
        return evaluation_results

    except Exception as error:
        return {
            "error": f"RAGAS evaluation failed: {error}"
        }
