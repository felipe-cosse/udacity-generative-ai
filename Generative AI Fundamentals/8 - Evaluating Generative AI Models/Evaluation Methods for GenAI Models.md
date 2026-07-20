# Evaluating Generative AI Models - Evaluation Methods for GenAI Models

Evaluating generative AI can feel subjective, but for many critical applications, we need objective, quantifiable proof that a model is performing correctly. This lesson introduces "exact evaluation," a class of methods that provides clear, deterministic judgments about a model's performance, moving beyond subjective impressions to rigorous, data-driven assessment.

When using Generative AI, one of the first classes of evaluation methods to consider are exact evaluation methods. These methods involve establishing clear, quantifiable metrics and designing evaluation frameworks that can objectively measure a model's performance. They are particularly useful for tasks where correctness can be definitively determined, such as code generation, mathematical problem-solving, or factual summarization.

Exact Evaluation is a method that yields unambiguous, deterministic judgments about a model's performance. This contrasts sharply with subjective evaluations, like grading an essay, which can vary between evaluators. While this approach is perfect for tasks with a single clear, correct answer, it can also be adapted for more open-ended responses.

There are two primary approaches to exact evaluation:

### 1. Functional Correctness
This evaluates whether a system performs its intended functionality. For example, if a model is asked to book a restaurant reservation, functional correctness assesses if the reservation was accurately made. In coding tasks, this translates to execution accuracy—whether the generated code runs and produces the expected output. While functional correctness is the ultimate metric for an application's success, it isn't always straightforward to measure and can be challenging to automate.

### 2. Similarity Measurements Against Reference Data
This method involves comparing a model's outputs to pre-existing ground truth or canonical responses (reference data). The effectiveness of this approach depends on the quality of the reference data, which can be costly and time-consuming to generate.

There are three main ways to measure this similarity:
* **Exact Match:** A binary (yes/no) measure suitable for simple questions with definitive answers, like trivia or basic math problems.
* **Lexical Similarity:** Measures the overlap of words or tokens between the generated output and the reference text. Techniques include edit distance or n-gram overlap metrics like BLEU and ROUGE. A drawback is that high lexical similarity doesn't always guarantee a better or semantically equivalent response.
* **Semantic Similarity:** This is a continuous measure that determines if two texts convey the same meaning, regardless of the exact words used. It's typically measured by comparing text embeddings using metrics like cosine similarity.

---

## AI as a Judge

A powerful and increasingly common method for evaluating generative AI models in production is AI as a Judge, also known as LLM-as-a-judge. This approach uses one AI model to evaluate the outputs of another.

The workflow is as follows:
1. A **Prompt** is sent to the Language Model (LLM) being tested.
2. The LLM generates a **Response**.
3. A new **Evaluation Prompt** is created, containing the original prompt and the response, along with specific instructions or a question for the evaluator model (e.g., "Is the response contained within the prompt?").
4. This evaluation prompt is sent to an **Evaluation LLM** (the "judge").
5. The judge provides an **Evaluation Result** (e.g., "Yes/No").

Effective use of AI judges requires careful prompt engineering, including clearly explaining the evaluation task, criteria, and scoring system, often using few-shot examples to guide the judge. Its primary advantages are speed, ease of use, and lower initial cost compared to human evaluators. Critically, AI judges can work without reference data, making them suitable for open-ended tasks where a ground truth might not exist. However, the AI judge is itself a probabilistic system and must be evaluated before it can be trusted.

---

## Effective Evaluation

For robust and reliable assessment, it's best to combine multiple methods. An effective evaluation strategy integrates human feedback, quantitative exact evaluation metrics, and the scalability of an AI judge.

A robust evaluation strategy for generative AI combines human judgment, exact quantitative metrics, and automated AI-as-a-judge methods to ensure reliability.




Let's talk about some of the possible evaluation methods when using Gen AI. The first class of evaluation methods we'll look at are exact evaluation methods. This often involves establishing clear, quantifiable metrics, and designing evaluation frameworks that can objectively measure performance. For instance, in tasks like code generation, mathematical problem solving, or factual summarization, the correctness of the Gen AI output can often be definitively determined. Let's take a closer look. Exact evaluation is a method that yields unambiguous deterministic judgments about a model's performance. Contrasting with subjective evaluations like essay grading. This approach is particularly suitable for tasks where there's a clear, correct answer. That can also be applied to open ended responses. There are two primary approaches to exact evaluation. One, functional correctness. This evaluates whether a system performs its intended functionality. For instance, if a model is asked to book a restaurant reservation, functional correctness assesses if the reservation was accurately made. In coding tasks, this translates to execution accuracy. Whether the generated code runs and produces the expected output. While it's the ultimate metric for an application success, functional correctness isn't always straightforward to measure and can be challenging to automate. Two, there are similarity measurements against reference data. This method involves comparing a model's outputs to pre existing ground truth or canonical responses. The effectiveness of this approach is often limited by the speed and cost of generating high quality reference data, which can be done by humans or by AI. There are three main ways to measure the similarity. Exact match, which is a binary measure suitable for simple questions with definitive answers, such as trivia or basic math problems. Lexical similarity, a measure assessing the overlap of tokens between the generated output and reference. Techniques include edit distance or N gram overlap metrics, such as BLEU and ROUGE. Drawback is that higher lexical similarity doesn't always guarantee a better or semantically equivalent response, and semantic similarity. This continuous measure determines if two texts convey the same meaning, irrespective of the exact words used. It's typically measured by comparing text embeddings using metrics like cosine similarity. These exact methods provide valuable, quantifiable insights into model performance, especially when human evaluation is too slow or expensive. We're creating a reliable, robust system, especially in high stakes domains. Exact evaluation methods are super important. They do require a bit of effort to create and maintain. When I say a bit, I mean a lot. However, the work will be worth it. Now, moving on, let's discuss another evaluation tool, which is useful when combining exact evaluation methods in a production pipeline. AI as a judge, also known as LLM as a judge. It's a powerful and increasingly common method for evaluating generative AI models in production. This approach involves using one AI model to evaluate the outputs of another AI model. How does it work? Well, you start with a prompt and LLM that you will be testing? You then get a response. The goal is to evaluate how well this response matches the original prompt. You then create a new prompt containing the original prompt and response along with some instructions and/or a question. For example, if your original prompt is expected to contain the correct answer in its context, and the model responds with an answer out of thin air, you might expect, Hey, wait. This is a hallucination. So you ask, Is this response contained in the prompt? You then run this through an LLM capable of answering your question, and voila. You get a response. In practice, effective use of AI judges requires careful prompt engineering, including clearly explaining the evaluation task, criteria, and scoring system, if applicable, and often with few shot examples to guide the judge. Its primary advantages include being fast, easy to use, and initially cheap compared to human evaluators. Critically, AI judges can work without reference data, making them suitable for open ended tasks where a ground truth might not even exist. Then again, an AI as a judge is yet another probabilistic system, which you will need to evaluate before you can trust it. Yes, evaluate the evaluator. Whoa, is me. While promising, AI judges should often be supplemented with exact evaluation methods and human evaluation for robust and reliable assessment. In fact, you need all three. Human evaluation, exact evaluation, and AI as a judge. Using these, we'll put you on the path to effective evaluations.