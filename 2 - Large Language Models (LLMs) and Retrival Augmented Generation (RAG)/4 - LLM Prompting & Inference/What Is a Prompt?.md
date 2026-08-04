The Bridge Between Human Intent and AI Understanding
Think about the last time you asked someone for help. You probably gave them context about your situation, explained what you needed, and maybe even shared how you'd like them to approach the problem.

Working with Large Language Models (LLMs) follows a similar pattern. A prompt is essentially your conversation starter with an AI system - it's how you communicate your needs, set expectations, and guide the model toward useful responses.

Next Token Prediction
Fudamentally, every generative LLM operates on a simple principle: predicting what comes next. The model calculates the probability of generating a response Y given your prompt X and its learned parameters Θ (theta).

In mathematical notation, we write this as P(Y|X,Θ).
When you type "The customer service representative", the model doesn't just randomly guess the next word. It calculates probabilities based on patterns it learned during training.

Maybe "responded" gets a 40% probability
"helped" gets a 30%
"resolved" gets a 20%.
The model learned these associations by reading millions of documents.

If you're more traditional machine learning practitioner, you can think of X (the prompt) as your features, Y (the response) as your prediction, and Θ as your model weights. But unlike traditional ML where features are fixed, in LLMs, you control the features through your prompt design.

The Model's Memory: Understanding Weights and Context
The model weights (Θ) represent something like the LLM's long-term memory or accumulated knowledge. During training, the model compressed patterns from vast amounts of text into these billions of parameters.

When your prompt lacks sufficient context, the model must rely heavily on these weights to fill in gaps. This is where hallucinations often originate. It's like asking a chef to recreate a specific dish from a restaurant they've never visited - they'll use their general knowledge to create something plausible but potentially incorrect.

Consider this customer service example:

Insufficient prompt: "Tell me about the refund policy"
Better prompt: "Tell me about the refund policy for electronics purchased within the last 30 days that have manufacturer defects"
The first prompt forces the model to guess which type of product, timeframe, and situation you mean, increasing the chance of fabricated details. The second provides specific context that grounds the response in factual information.

Creating Effective Prompts
A well-crafted prompt typically includes several components, each serving a specific purpose:

System Prompt: Setting the Personality and Expertise
The system prompt defines who the AI should be in your conversation. For a customer service system, you might use:

You are a helpful customer service specialist with expertise in company policies, product information, and issue resolution. Provide accurate, empathetic responses while keeping explanations clear and actionable for customers.
Conversational History: Maintaining Context
Just as humans reference earlier parts of a conversation, LLMs use chat history to maintain coherence. Each exchange builds on the previous ones, creating a shared context. This is why ChatGPT can remember what you discussed earlier in the conversation - it's all part of the expanding prompt.

User Request Specification
This is where you specify exactly what you need. The more precise you are, the better the response. Think about the difference between asking a colleague "Can you help with the report?" versus "Can you review sections 3-5 of the quarterly report for technical accuracy and suggest improvements to the data visualizations?"

Prompt Augmentation: Adding External Knowledge
This is where techniques like Retrieval-Augmented Generation (RAG) come in. Instead of hoping the model remembers specific details about your company's return policy, you retrieve relevant documents and include them in the prompt. It's like giving someone reference materials before asking them to write a summary.

Chain of Thought: Teaching Models to Think Step-by-Step
One of the most powerful discoveries in prompt engineering is that asking models to explain their reasoning improves their accuracy. This technique, called Chain of Thought (CoT) prompting, works because of how LLMs generate text.

Here's a problem-solving scenario. Suppose you need to determine eligibility for a product exchange:

Without Chain of Thought: "Can this customer exchange their product?" Model gives a potentially incorrect yes/no answer

With Chain of Thought: "Determine if this customer is eligible for a product exchange. Think through this step-by-step:

First, check how many days have passed since purchase
Verify the product category and condition
Review the exchange policy for this product type
Identify any special circumstances or exceptions
Provide your determination with reasoning"
The second approach often produces more accurate results because the model generates intermediate reasoning steps that serve as additional context for subsequent predictions.

How Text Generation Really Works
LLMs generate text one token at a time, where each new token becomes part of the context for generating the next one. It's like building a bridge while walking across it - each plank you lay down becomes the foundation for the next step.

This auto-regressive generation creates feedback loops that can be either beneficial or problematic:

Virtuous Cycles: When the model generates correct intermediate steps in chain-of-thought reasoning, each step reinforces the logical progression toward the right answer. It's like momentum building in the right direction.

Vicious Cycles: Sometimes the model gets stuck repeating phrases or ideas. Once a pattern starts repeating, it becomes increasingly likely to continue because the repetition is now part of the context. When this happens, you might experience the AI response repeating the same sentence over and over.





At both training and inference time, generative LLMs use a next token prediction task. Specifically, the task is to predict the probability of generating Y given X and Theta, where X is the prompt, Y is the LLM response, and Theta is the model's weights learned during training. The analog to more traditional ML is X as features, Y as the label or prediction, and Theta as still the model's weights. We will largely ignore these learned model weights for now for two reasons. One, they are frozen for everything except pre-training and fine-tuning. Two, these model weights are a closer analog to the LLM's long-term memory or intelligence. Tasks with insufficient prompt context force a model to rely on learned weights to fill in that missing context, increasing the likelihood of LLM-generated hallucinations. However, with proper prompting techniques, we can also rely on the model's weights to provide the LLM with beneficial context, as we will see soon. This permits our focus on what we know the LLM is good at. Language fluency conditioned on the user prompt, which we can best exploit by providing the LLM a very detailed user prompt, including a system prompt to give the LLM personality, the chat conversational history to give the LLM knowledge of prior interactions, and detailed specification of the user's request, which may be achieved via prompt augmentation, such as the use of a search mechanism. We can use the LLM itself to provide more context as well. This need not require multiple calls to an LLM, as was explored in systems such as React and other flavors of LLM agents that are popular today. Instead, we will consider an earlier method known as chain of thought reasoning, which achieves this effective form of prompt augmentation in a single LLM call. Initially, this was accomplished by pre-pending the user query with several few shot examples of questions answered via step-by-step reasoning. It was also found that similar results can be achieved by triggering the LLM to think step by step, by simply appending this request to the user prompt. Finally, although out of scope for this lesson, once it's discovered that improving performance can be elicited from LLMs by simply appending certain phrases to the prompt at inference time, AI engineers can also employ instruction fine-tuning to teach the LLM to perform step-by-step reasoning without any special prompting. To provide a bit of intuition as to why the chain of thought prompting method is particularly effective, we will look at an interesting aspect of generative LLM models, in particular, their auto-regressive mechanism. Specifically, at inference time, the LLM is producing only one token at a time, while the previously generated tokens appended to the user prompt. This continues until the end of sequence special token is generated. Revisiting the analogy to more traditional ML, we can see how the LLM has a role in generating its own features. Such auto-regressive generation can result in both virtuous and vicious feedback loops, which AI engineers must be aware of. Chain of thought prompting serves as an example of a virtuous feedback loop, where the LLM can assist in providing inference time context for answering the user query. Whereas LLM-generated repetitions, such as the repeating of a token or phrase, serves as an example of a vicious feedback loop.