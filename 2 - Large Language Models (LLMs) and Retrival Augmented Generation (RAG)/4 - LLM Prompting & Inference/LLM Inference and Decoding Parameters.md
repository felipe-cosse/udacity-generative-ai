LLM Inference Settings: Controlling the Generation Process
You've written the perfect prompt. You hit "generate" and wait for the response. What happens in that moment? How does the language model actually decide what words to produce?

Most developers treat LLM generation as a black box—text goes in, text comes out, and the process in between is mysterious. But understanding and controlling the generation process is necessary for building reliable applications.

The same prompt can produce drastically different results depending on inference settings.

Consider this prompt:

"Complete this sentence: The weather today is"
With different settings, you might get:

"sunny and warm" (conservative, predictable)
"absolutely magnificent with crystal clear skies" (creative, descriptive)
"sunny and warm sunny and warm sunny and warm" (repetitive, broken)
"green giraffe dancing on clouds" (random, nonsensical)
The difference isn't the prompt, it's the inference settings. These parameters control how your language model explores possibilities, balances creativity with coherence, and decides when to stop generating.

Let's explore these settings and learn to control them with precision.

Probability Distributions
A language model doesn't generate words directly. It generates probability distributions over possible next tokens.

Seeing Inside the Model
Imagine you prompt the model with "The cat sat on the"

The model doesn't think "mat" and output it. Instead, it produces something like this:

# Simplified probability distribution over vocabulary
next_token_probabilities = {
    'mat': 0.35,
    'floor': 0.20,
    'couch': 0.15,
    'chair': 0.10,
    'table': 0.08,
    'bed': 0.05,
    'roof': 0.03,
    'moon': 0.01,
    'car': 0.01,
    # ... thousands more tokens with tiny probabilities
}
The model assigns probabilities to every token in its vocabulary (typically 30,000-50,000 tokens). Most get near-zero probability, but many plausible options get non-trivial scores.

The question is: How do we choose which token to actually generate?

This is what inference settings control. They're algorithms for sampling from this probability distribution.

Temperature: Controlling Randomness
Temperature is the most important inference parameter. It controls how "creative" or "conservative" the model's choices of the next word/token are.

Temperature = 0: Greedy Decoding
# Temperature 0 means: always pick the most probable token
# No randomness, deterministic output

prompt = "The capital of France is"

# With temperature 0
response = model.generate(prompt, temperature=0)
print(response)
# "Paris"  (always)

# Run it 100 times, you get "Paris" every time
for _ in range(100):
    assert model.generate(prompt, temperature=0) == "Paris"
When to use temperature = 0:

Factual question answering (you want the most likely correct answer)
Code generation (you want idiomatic, standard code)
Translation (you want the most probable translation)
Classification (you want the most confident prediction)
Even with temperature = 0, LLM inference is NOT perfectly deterministic due to implementation details like GPU floating-point operations. You might get slightly different outputs on different hardware or with different batch sizes. But it's close to deterministic.

Top P: Probability Mass Cutoff
Top P (also called nucleus sampling) is an alternative to temperature for controlling randomness. Instead of flattening the distribution, it truncates it.

How Top P Works
Top P samples from the smallest set of tokens whose cumulative probability exceeds P.

# Token probabilities (sorted)
tokens = [
    ('the', 0.30),
    ('a', 0.25),
    ('an', 0.20),
    ('that', 0.10),
    ('this', 0.08),
    ('my', 0.04),
    ('your', 0.02),
    ('our', 0.01),
]

# Top P = 0.9
cumulative = 0
nucleus = []
for token, prob in tokens:
    nucleus.append((token, prob))
    cumulative += prob
    if cumulative >= 0.9:
        break

print("Nucleus (top P = 0.9):", nucleus)
# [('the', 0.30), ('a', 0.25), ('an', 0.20), ('that', 0.10), ('this', 0.08)]
# Cumulative: 0.93 >= 0.9, stop here

# Sample only from these tokens (renormalized)
# 'my', 'your', 'our' have been excluded
Top P vs Temperature
Temperature: Adjusts all probabilities

Low temp: Makes high-probability tokens even more likely
High temp: Makes low-probability tokens more likely
Top P: Hard cutoff

Excludes tokens below probability threshold
Keeps distribution shape among remaining tokens
When to Use Top P
Top P is particularly good for:

Avoiding nonsensical low-probability tokens
Adapting to context (nucleus size changes naturally)
For most applications, use temperature (more intuitive). Use top_p when you specifically want to exclude unlikely tokens regardless of distribution shape.





Next, we will put into practice some of these theoretical ideas using the OpenAI playground. But first we must understand the settings at our disposal here. First we select the model we will be using. Here we see the original GPT 3 model, although in our exercise and demos we will use GPT 3.5 Turbo Instruct. Then we can select a temperature. The temperature setting can be understood by first looking at this hypothetical probability distribution for an LLM's next token prediction. Rather than the single next token, an LLM's output is actually a probability distribution across tokens, where here we show them sorted from most to least probable, and simplify the distribution as continuous even though really it's discrete. In order to choose the single next token to generate, a decoding mechanism must be specified. Most generally, decoding involves sampling directly from the probability distribution, such that this token at the top is the most probable to be sampled, and it's about half as likely that this token halfway down will get sampled instead. Increasing the temperature flattens the probability distribution, making it far more likely to sample a token that is not at the very top of the distribution. Increasing the likelihood of sampling from these less probable tokens can make the LLM response seem more creative. Alternative to sampling is greedy decoding. Greedy decoding always picks the most probable token. With greedy decoding, the actual shape of the distribution does not matter, as the top of the peak is always associated with the same token no matter how we transform the distribution. Setting the temperature to zero is a common way to request greedy decoding. Note however, that LLM inference is not deterministic, even when greedy decoding, because the underlying inference time operators are not implemented in a deterministic fashion. Two tokens with similar probabilities may swap back and forth as the most probable token, and due to the nature of the auto-aggressive next token prediction mechanism, once a different token has been selected, all subsequent tokens will condition upon this different token, causing the remainder of the generation to likely head off in a different direction. Next we have the maximum length parameter, which can be explained by looking at tokens along a line where the x-axis is now the index in the sequence of tokens. These are the tokens that most generally compose a prompt sent to the LLM. First we have the system prompt setting the tone for the interaction, then in a chat history that may have occurred over the course of the conversation. It must be flattened and included in the prompt in order for the LLM to have any memory of these prior conversational turns, as we will see soon in more detail in our exercise. Then we have the actual prompt just provided by the user. Finally, we have some number of tokens that are pre-allocated for the LLM response. In the Python OpenAI API, maximum length is referred to as max tokens. The LLM will not be able to exceed this number, stopping mid-sentence if needed when the max tokens value is hit. All of this must fit within the attention window of the LLM, often from about 2k to 64k, depending on the model being used. You may wonder why the LLM cannot continue generating well past the attention window with some sliding window once it started off with the next token prediction. A simple explanation is that each newly generated token must be able to attend to all previously generated tokens, and there's no mechanism in the standard transformer implementation to allow a token to attend to a representation of an earlier token. That's outside of the LLM attention window. We will explore workarounds in the coming exercise. Next, we look at the top P setting, starting from the same point as when we looked at temperature, but here, instead of flattening the distribution, we'll just chop everything off below some percentage P of the probability mass, and the remaining probability distribution, excluding these less probable tokens, can be renormalized for sampling the next token. As was the case with temperature, greedy decoding is unimpacted by changes to top P. Now, quickly looking at these two penalty settings, they serve to reduce the likelihood of sampling specific tokens that have already appeared in the generated sequence, aimed towards reducing the likelihood of repeated sequences, a phenomenon that can particularly impact smaller models. Unlike the other settings, adjusting these values can impact greedy decoding if the most probable token is hit with a repetition penalty. We finally skip to the show probability setting. This setting motivates why we chose to use the legacy completion playground rather than the chat completion playground, which is almost identical except that it doesn't expose this feature. Introspecting the probability of the generated tokens can provide helpful insights into the LLM's generation process, as we will see now in the demo.





Encoders and decoders are distinct components that process the input and generate the output in transformer based LLMs. In the original transformer model, as described in the attention is all you need Paper, the encoder and decoder are separate components that interact with each other. In this set up, the encoder processes the input text of an LLM and the decoder generates text based on the encoder's output. The encoder's job is to process the input text. It converts the input data, words, sentences, and so forth, into a series of numerical values known as embeddings. These embeddings are then passed through multiple layers of the encoder, which use self attention mechanisms to allow the model to consider other words in the input when understanding each particular word. The result is a context rich representation of the input text. The decoder uses the representations produced by the encoder to generate output text. It also contains multiple layers of self attention mechanisms, but operates slightly differently. In a model where the output is generated one token at a time, the decoder also uses the previously generated tokens as additional context when producing the next token. Decoding strategies are methods used by the decoder to generate text sequentially. Greedy decoding is the simplest strategy where the model picks the most likely next word at each step. While efficient, greedy decoding can sometimes lead to sub optimal overall sequences. Another strategy is beam search. Instead of just considering the single best word, beam search keeps track of a number of possible sequences, which we call the beam width, and explores a tree of possibilities to find a better sequence of words. It balances between the best local choices and the best overall sequence up to that point. A decoding strategy that can make output a text more creative, is top K sampling. This method randomly picks the next word from the top K most likely candidates according to the model's predictions. This introduces randomness, making the text generation less deterministic and potentially more diverse. A similar strategy is top P or nucleus sampling. Rather than limiting the choice to the top k words, top sampling chooses from the smallest set of words whose cumulative probability exceeds the threshold being P. It focuses on a nucleus of high probability options leading to more dynamic and contextually varied outputs. In all cases, the type of decoding strategy used can significantly impact the quality and style of the generated text. We have different strategies leading to different balances between coherence, diversity, and computational efficiency. A setting for the model when it runs, which we call a high parameter, that can be used to effect decoding is called temperature. Setting the temperature of a model can control the randomness of token predictions. A higher temperature leads to more randomness, while a lower temperature makes the model more confident in its predictions, less random. It's worth mentioning that some LLM models don't use separate encoders and decoders. The model uses only the decoder component to both understand the input and generate the output text. The architecture relies on a self attention mechanism in the decoder to process the entire sequence of tokens at once.