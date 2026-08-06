When you're working with a Large Language Model (LLM), you have two main levers to pull to control its output.

Prompting: This is the what—the set of instructions, examples, and context you provide.

Inference: This is the how—the set of parameters like temperature that control the mechanics of how the model generates its response.

In this lesson, you'll see demos that visualize how a model "thinks" by looking at next-token probabilities and how a powerful technique called Chain of Thought prompting can guide a model toward more accurate reasoning.

In the exercises, you'll implement prompting strategies and experiment directly with inference parameters to see how you can shape a model's output to be more factual, creative, or constrained to your specific needs.

Explore the demo below to:

Understand how LLMs generate text token by token
Use the logprobs parameter to inspect model decisions
Interpret log probability values and what they reveal about model confidence
Recognize how models evaluate multiple word choices before selecting the most likely one

Token-by-Token Generation
LLMs don't generate entire sentences at once—they predict one token (word or word piece) at a time.

The model receives the prompt: "Give me a short description of what an embedding is"
It generates the response word by word, starting with "An"
At each step, the model evaluates multiple possible next words
Log Probabilities (logprobs)
Log probabilities reveal the model's confidence in each token choice.

Setting logprobs=True enables probability tracking
Setting top_logprobs=5 shows the top 5 alternative words considered
The response includes probability scores for each token
Key Parameters:

logprobs = True        # Enable probability logging
top_logprobs = 5       # Show top 5 alternatives at each step
Examining logprobs helps you:

Detect when the model is uncertain (low probabilities)
Identify potential hallucinations (model "guessing")
Debug unexpected outputs
Understand model reasoning
Interpreting Log Probability Values
Log probabilities are negative numbers—less negative means more likely.

-9.96: High confidence (first token "An")
-19: Very low confidence (alternative "sure")
Range interpretation:
Close to 0 (e.g., -0.5 to -2): Very confident
-5 to -10: Moderately confident
Below -15: Low confidence/unlikely choice
Explore Different Prompts
Run the same code with these variations:

"What is machine learning?" (general knowledge)
"Explain quantum entanglement" (complex topic)
"Write a haiku about APIs" (creative task)
Observation Goal: Notice how logprobs differ across factual vs. creative tasks.

Compare Models
Run the same prompt with different models (GPT-3.5 vs GPT-4) and compare logprobs. Do more advanced models show higher confidence (less negative logprobs)?






For our demo, we're going to be looking at how an LLM is generating our answer. For this, we're going to leverage the OpenAI API. We're going to be doing a regular call, and we're going to be asking LLM to give us a short description of what an embedding is. Additional to the request, we're going to be adding two new parameters, the logprobs = True, and the top_logprobs = 5. This will give us the Top 5 words that the LLM evaluated at every step. Let's take a look at how this looks. We're going to send the request, and this is going to take a couple of seconds, and we're going to get our answer. An embedding is a method of representing complex data like words, sentences, images or items. For this particular demo, we are not particularly interested in the final answer, but rather, the evaluation that happened behind the scenes. We are going to gather this information from the logprobs key. Now, in here, we have our first token, and we have a log probability of -9.96. Take a notice that this is a negative. Any values that are lower are going to be like -10 or -11. We are going to be looking at this, and we are going to have our five words available to us. We have An, which is the top choice, we have In, which will be a little bit weird, but impossible, depending on what the answer will be. We have a double asterisk, and finally, we have our Sure word with a very low probability of -19. You can see here, the model is evaluating different words and based on the probability, choosing the most likely word to go after our sentence. Now, there is a lot more words for each of the turns that it takes. I will let you explore if you have completed this demo.