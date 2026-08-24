This exercise teaches you the most important skill for production RAG systems: evaluation. Building a RAG system is one thing; knowing whether it's good enough for production is entirely different. Without systematic evaluation, you're unable to compare configurations, detect regressions, or confidently deploy to users.

RAGAS (Retrieval-Augmented Generation Assessment) provides a comprehensive framework for measuring RAG quality across multiple dimensions. Unlike simple accuracy metrics, RAGAS evaluates both retrieval quality (did you find the right documents?) and generation quality (did you create a good answer from those documents?). This separation enables targeted improvements: if retrieval is weak, improve embeddings or chunking; if generation is weak, improve prompts or models.

In this exercise, you'll implement a complete RAGAS evaluation pipeline, learn to interpret metrics, and discover how to use evaluation results to systematically improve your RAG system.

By the end of this exercise, you will be able to:

Understand the RAGAS evaluation framework and how it separates retrieval from generation quality
Implement six core RAGAS metrics: faithfulness, answer relevancy, context precision, context recall, answer correctness, and answer similarity
Create evaluation datasets with questions, ground truth answers, and contexts
Configure metric groupings for different evaluation scenarios (comprehensive, retrieval-focused, generation-focused, quick)
Run RAGAS evaluation on your RAG system and interpret quantitative scores
Diagnose RAG system weaknesses by analyzing which metrics are low
Iterate and improve your RAG system based on evaluation feedback

Use RAGAS metrics to evaluate your RAG system and identify areas for improvement.

Instructions
Prepare test dataset - Create 5 question-answer-context test cases from your RAG system
Install RAGAS - Ensure ragas library is available
Calculate metrics - Run evaluation on your test dataset
Analyze results - Interpret what each metric tells you
Identify improvements - Based on scores, determine what to optimize
The starter code includes sample test data and TODO comments. Complete all tasks to fully evaluate your RAG system.




