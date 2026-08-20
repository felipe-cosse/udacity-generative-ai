Individual metrics are useful for diagnosis, but you need a single score to track overall system quality over time. This is where the RAGAS (Retrieval-Augmented Generation Assessment) framework comes in.

RAGAS combines four metrics:

Context Precision (retriever signal-to-noise)
Context Recall (retriever completeness)
Faithfulness (generator accuracy)
Answer Relevancy (generator pertinence)
The critical insight is how these metrics are combined: using a harmonic mean rather than a simple average.

Understanding the Harmonic Mean
Why does the math matter? Because the harmonic mean heavily penalizes systems with even one weak component.

Let's compare two hypothetical RAG systems:

System A (Balanced)

Context Precision: 0.8
Context Recall: 0.8
Faithfulness: 0.8
Answer Relevancy: 0.8
Arithmetic Mean: 0.8
Harmonic Mean: 0.8
System B (Unbalanced)

Context Precision: 0.95
Context Recall: 0.95
Faithfulness: 0.95
Answer Relevancy: 0.3
Arithmetic Mean: 0.8
Harmonic Mean: 0.45
Both systems have the same arithmetic average, but the harmonic mean reveals that System B is fundamentally broken. Its answers might be perfectly faithful to retrieved context and based on excellent retrieval, but if the answers consistently fail to address what users actually ask, the system provides no value.

The harmonic mean formula is:

H = n / (1/x₁ + 1/x₂ + ... + 1/xₙ)
For four metrics:

RAGAS_score = 4 / (1/precision + 1/recall + 1/faithfulness + 1/relevancy)
This mathematical structure reflects a fundamental truth about RAG systems: your pipeline is only as strong as its weakest link. Excellence in three components cannot compensate for failure in the fourth.

RAGAS Official Documentation(opens in a new tab) - Complete guide to all evaluation metrics
RAGAS Metrics Explained(opens in a new tab) - Deep dive into context precision, recall, faithfulness, and relevancy
Hugging Face Datasets(opens in a new tab) - Learn about the Dataset format used by RAGAS
RAGAS Research Paper(opens in a new tab) - Academic foundation for the evaluation framework
RAG Best Practices(opens in a new tab) - Comprehensive guide to building better RAG systems



