# How Generative AI Works - Training GenAI Models

Generative AI models must capture the essence of human language, audio, and other modalities to be effective. This requires massive amounts of data and a sophisticated, multi-stage training process. This process begins with broad knowledge and is gradually refined to develop specialized skills, moving from simple prediction to complex reasoning.

---

## Pre-Training

Training a generative AI model, like a text-based Transformer, begins with a process called **pre-training**. This stage uses a vast and diverse dataset containing content like books, articles, encyclopedias (e.g., Wikipedia), online forums, and code repositories from sources like GitHub.

The core task during pre-training is next-token prediction. The model is given a snippet of text and must guess the next word. For example, given the phrase "To be or not to...", the model should predict "be". If the model's prediction is correct, its internal parameters (weights) are adjusted to reinforce that choice. If it's incorrect, the weights are adjusted to discourage that choice in the future. This initial step gives the model a foundational understanding of language.

> *Pre-training involves teaching a generative AI model to complete text from a diverse array of sources, such as Shakespeare.*

---

## Fine-Tuning / Post-Training

After pre-training, the model undergoes **fine-tuning**, which is also increasingly referred to as **post-training**. This stage steers the pre-trained model to perform specific tasks or to better understand a particular domain by further adjusting its weights. Fine-tuning typically occurs in two main phases.

### Phase 1: Supervised Fine Tuning (SFT)
This is a form of supervised learning that uses a high-quality, labeled dataset to teach the model to mimic "gold-standard" responses on a token-by-token basis. SFT is crucial for teaching a model to follow instructions (like "translate this to French") and to engage in chat-style interactions. Without it, a model might simply continue generating text from its pre-training data rather than responding to a user's prompt.

### Phase 2: Reinforcement Fine Tuning
Sometimes called preference fine tuning. Instead of optimizing for next-token prediction, this method optimizes for the overall quality of a generated sequence. It uses feedback—either from humans or automated, rubric-based criteria—to learn which responses are "preferred." For instance, it can be trained on a dataset of preferred versus rejected responses. This method generally requires less data than SFT and is key to improving a model's reasoning ability.

> *Supervised fine-tuning encourages a model to mimic a data set exactly token by token, while reinforcement fine-tuning encourages the same model to complete entire sequences that are preferred over others.*

---

## The Emergence of Reasoning

When these training stages are combined, a remarkable capability emerges: **reasoning**. For a Large Language Model (LLM), reasoning is the ability to break down a complex problem into smaller steps and arrive at a correct conclusion, similar to mathematical or analytical thinking.

This can be understood through the analogy of System 1 and System 2 thinking from human psychology.

* **System 1 thinking** is rapid, intuitive, and automatic. This is akin to a basic LLM performing next-token prediction to give an immediate response.
* **System 2 thinking** is slow, deliberate, and analytical. This mirrors an advanced LLM using a technique like **chain of thought**, where it breaks a complex task into intermediate steps to find a solution.

Advances in reinforcement fine-tuning have significantly improved this "System 2" capability, enabling even smaller models to reason about complex topics more effectively than some larger models.

A multi-stage training process—combining broad pre-training with specialized supervised and reinforcement fine-tuning—is what allows generative models to move beyond simple pattern matching to complex reasoning.





Let's talk about how these generative AI models are trained. In order for them to capture the essence of written language or spoken audio, or other modalities, we need data and lots of it. Let's zoom in on training a text based transformer model. We start with a diverse data set filled with books and articles on every topic imaginable. We also include encyclopedias, such as Wikipedia, online forums, and code repositories on GitHub. Now, in order to train our model, we will pick the beginnings of random passages from our dataset. Let's take the famous quote from Shakespeare, to be or not to blank. We then train our model to guess the next word. If the model gets it correct, that's great. We'll reinforce that choice by updating the weights to make it slightly more likely next time. If it's wrong, we'll do the opposite and discourage that word choice instead. This process is called pre-training. This is a first step used to get an LLM to understand things like language at a base level. Then after pre-training, we go through what is called fine-tuning, and increasingly is being referred to as post training. Now, let's talk about fine-tuning and post training generative AI models. Step involves steering a pre-chain model to perform specific tasks or understand a specific domain better by adjusting the models weights. This normally occurs in two main phases. First, supervised fine tuning or SFT. This steers a model toward replicating responses token by token from a dataset demonstrating exactly what we want the model to produce. Two, reinforcement fine tuning, sometimes called preference fine tuning. This steers a model toward producing responses that overall are preferred, based on either human feedback or computer judge criteria. Let's look at these a bit deeper. Supervised fine tuning or SFT requires a high quality label dataset, and is a form of supervised learning. As mentioned, it optimizes a model's ability to predict the next token in the sequence. Notably, this is a part of the training that teaches a model to respond to instructions such as translate this to French. It also teaches a model to engage in chat style format. Without it, the model may endlessly repeat a section from a long part of a book for two reasons. The model is trained to predict the next token, and that is what the pre-training data primarily looks like. Now let's discuss reinforcement fine tuning or preference fine tuning. In this step, we evaluate a model's performance, not by its ability to predict the next token, but by assessing the overall preference for one generated sequence over another. In this situation, we can curate a data set of preferred versus rejected responses from the model. May take some time, but the volume of data needed is generally less than that for supervised fine tuning. In certain cases, we can also provide preference data on the fly by using a computer graded rubric, such as when the final answer is a multiple choice response or when the output should be in an easily verifiable format. There's something quite amazing that happens when we put all of these training steps together from pre-training to supervised fine tuning to reinforcement fine tuning. That's reasoning. For a large language model, the term reasoning essentially refers to the model's ability to take a complex problem, break it down into steps, and finally arrive at a correct conclusion. You might think of it as mathematical or analytic reasoning. Here's a useful analogy involving system 1 versus system 2 thinking, a concept from human psychology. System 1 thinking is rapid, intuitive, and automatic. For AI models, this is akin to how a basic, large language model might operate. Quickly predicting the next word or generating a straightforward response is about providing an immediate output. Now, system 2 thinking is slow, deliberate, analytical. If you ask an advanced LLM to think step by step, it will break down complex tasks into simpler subtasks, performing intermediate computations or analyses. This is called chain of thought. Multiple chains of thought can arrive at the correct or preferred answer, so it's crucial to reward the model based on its entire response. This is exactly what reinforcement fine tuning does, and explains why advances in reinforcement learning have enabled smaller models to reason about complex topics even better than the larger models of before.