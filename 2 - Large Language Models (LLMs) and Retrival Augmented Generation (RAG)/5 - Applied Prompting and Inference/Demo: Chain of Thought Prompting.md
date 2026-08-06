In this demo, explore

What Chain-of-Thought (CoT) prompting is and why it improves model outputs
Applying CoT techniques by adding simple trigger phrases to prompts
Comparing direct responses vs. step-by-step reasoning
Recognizing when to use CoT prompting for complex tasks

Chain-of-Thought (CoT) Prompting
CoT prompting instructs the LLM to break down complex problems into intermediate reasoning steps before providing a final answer.

First attempt (Direct): "How would you measure the diameter of planet Earth using Eratosthenes' method?"
Second attempt (CoT): Same question + "Give a step-by-step process to achieve this."
The Power of "Step-by-Step"
Simple trigger phrases activate reasoning mode in LLMs.

Phrases That Work:

"Let's think step by step"
"Give a step-by-step process"
"Explain your reasoning"
"Show your work"
"Break this down into steps"
You don't need complex prompt engineering—a simple phrase can double response quality.

When to Use Chain-of-Thought Prompting
Use CoT When:
Complex reasoning required (multi-step problems)
Transparency is important (need to verify logic)
Accuracy is critical (reduce errors)
Teaching or explaining concepts
Debugging or troubleshooting
Decision-making with multiple factors
Don't Need CoT When:
Simple factual queries ("What is the capital of France?")
Creative writing (storytelling, poetry)
Quick lookups (definitions, dates)
Binary yes/no without justification needed
Already well-defined processes (model knows the steps)






For our demo, we're going to take a look at how we can improve the responses of our LLM. We are going to ask OpenAI for a very simple task. How will you measure the diameter of planet Earth using Eratosthenes' method? We're going to run this, and it's going to take a few seconds for the response to come back to us. As models come more advanced, [inaudible] is becoming the default way that they are generated in a response. However, this technique is still very useful for us to be able to get more precise answers. As you can see here, it's giving us an answer on how we can do this. Also, is giving us a lot of information on the history of this method. Now, we can give a little more detail, and sometimes this is necessary for the answers that we're looking for. We can add, give a step-by-step process to achieve this. We run these requests, and it's going to take a few more seconds to be able to give us the answer. As you can see, this has given us a lot more detail into how we are able to do this measurement. Now this is important because many times we are looking for a very detailed explanation of a process.