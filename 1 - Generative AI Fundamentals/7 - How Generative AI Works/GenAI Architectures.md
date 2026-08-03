# How Generative AI Works - GenAI Architectures

## Introduction to Generative AI Architectures
While some AI models are designed to classify existing data, like telling a cat from a dog, generative AI models go a step further. They are designed to produce entirely new data samples—like a unique image of a dog that has never existed before—by learning the underlying patterns and distribution of their training data.

Generative AI models create new data samples with characteristics similar to the data they were trained on. This is a crucial distinction from *discriminative models*, which focus on classification and prediction tasks based on existing data. For example, a discriminative model might answer the question "Is this a cat?" with a simple "yes" or "no."

In contrast, a generative model learns the underlying distribution of the input data. This allows it to do more than just recognize a dog; it can generate an entirely new image of a dog based on the features and characteristics it has learned.

Because of the random nature of generative AI, the outputs can sometimes be unexpected. The model might produce an image that looks more like a bear than a dog, or even an abstract representation. Depending on the use case, this creativity can be seen as either a flaw to be controlled or a feature to be explored.

---

## The Transformer Architecture
The *Transformer* architecture is a type of neural network that forms the backbone of modern generative AI systems like ChatGPT, Claude, and Gemini. Transformers have transformed our ability to generate sequential data, such as text and audio.

* They excel at processing sequential data in parallel and handling long-range dependencies, which is why they are so effective with long documents.
* They are also central to a new generation of models, such as those used for text-to-video generation.

### Tokens and Autoregression
Transformer-based models work by breaking their input into small chunks called *tokens*. For text, a token can be a word or part of a word. The model then functions like a sophisticated autocomplete, predicting the next token in a sequence. For example, given the input "Hello! How," a Transformer might predict the next tokens to be "are," "you," and "?". This process also applies to other sequential data, like audio, where the tokens are short snippets of sound.

This method of predicting the next token from existing tokens and repeating the process over and over is called *autoregression*. It is the core mechanism Large Language Models (LLMs) use to generate new text or audio. The model calculates probabilities for various possible next tokens based on its training.

For instance, after the phrase "The cow jumped over the," an LLM might assign probabilities to the next word:
* moon (85%)
* house (10%)
* cheese (5%)

By repeatedly choosing the next token and appending it to the sequence, the model can generate creative and coherent text, such as completing the nursery rhyme "The cow jumped over the moon, and the little dog laughed to see such a sport."

---

## Diffusion and Flow Matching Models
Another important class of generative models includes *Diffusion and Flow Matching Models*, which are often used for image generation. These models work like a magic eraser, starting with a completely noisy image and gradually removing the noise to reveal a clear picture.

### Training Mechanics
To train these models, the process is reversed. Developers start with real, clear images, systematically add noise to them, and then train the model to predict what the image looked like before the noise was added. 

This process can be guided by text prompts. For example, by providing the phrase "dog with pyramids" during training and generation, the model learns to steer the denoising process to create an image that matches that description.

### Theoretical Convergence
Interestingly, while diffusion and flow matching models were often discussed as different approaches, researchers at Google DeepMind have shown that they are mathematically the same. Different implementation details can lead to different outputs, but the core frameworks can be used interchangeably.

## Summary Conclusion
Generative AI models create novel content by learning data distributions, with key architectures like Transformers using autoregression for sequences and Diffusion models using a denoising process for images.




Generative AI models are designed to produce new data samples with characteristics similar to their training data. Unlike discriminative models that predict labels, generative models learn the underlying distribution of the input data. This is a crucial distinction from discriminative models. Think of it this way. A discriminative model might tell you, Yes, that's a cat, or no that's a dog. It classifies or predicts based on existing data. But a generative model doesn't just recognize a dog. It can dream up and create an entirely new dog based on certain features and characteristics it's familiar with. We also see that because of the random nature of generative AI, we occasionally get responses that don't even appear to be a dog. For instance, this one looks more like a bear. This one here, it's an abstract representation of a dog, perhaps. Depending on your use case for generative AI, this could be seen as either a flaw to be rained in or a feature to be explored. Let's take a look at the model architecture that is at the center of the GenAI revolution, the transformer. Transformers are neural networks that form the backbone of modern AI systems, like ChatGPT, Claude and Gemini. They excel at processing sequential data in parallel, as well as handling long range dependencies in data. This is one reason they can handle long documents so well. Transformers have transformed the way we generate sequential data, such as text, and audio, such as voices. In fact, they have been so successful that they are playing a more pivotal role in larger AI systems, for example, text-to-video generation. Let's take a look at how transformers work. Transformer-based models break up their input into small chunks called tokens. For simplicity, we'll use entire words here, but often they could be smaller parts of words. Now, you can think of a transformer as a really sophisticated autocomplete. In this case, hello, how, could be completed with are, you, and then a question mark. It could also be completed with how is the weather, or how do you like your eggs cooked? For audio, it works in a very similar way. Except that instead of discrete tokens of parts of written text, we have short snippets of audio. In general, this process of predicting the next single token from existing tokens, and then repeating the process over and over again is called autoregression. It is the method that LLMs used to generate new text or audio. For instance, if we start a sentence with, the cow jumped over the, the LLM might provide three possible continuations with probabilities. House with a 10% probability, moon with an 85% probability, and cheese with a probability of 5%. These probabilities are computed or rather learned by the LLM through the course of its training on large amounts of text data. By repeating the process to generate more and more words, we eventually get texts that can sound like it came from a human being. Starting with the cow jumped over the, let's see different ways and LLM completes it. First, moon, and the little dog laughed to see such a sport. Or moon and landed on a star. Finally, moon and landed in a field of stars. She twirled and pranced among the constellations, her laughter echoing through the cosmos. Now, how is that? Let's turn our attention now to diffusion models, as well as the more modern flow matching models. In both cases, the model is like a magic eraser that slowly removes the noise from a picture. It does this by starting with completely noisy image and gradually adds in details until the final image is clear. Of course, there's a whole lot of imagination needed on the part of the model, since when the image is complete noise, there isn't actually anything there. How the model is trained to do this is nothing short of genius. How do you get a model to produce a clear image out of noise? Well, that's easy. You just turn the arrows around. You start with real images, add noise to them, and get the model to be able to predict what it looked like before the noise. The reason this is possible is that there's a great deal of coherence in images we see in real life, and our minds, like these models, fill in the gaps when needed. This is why we can imagine the original image without looking directly at it. If you want, go ahead and cover up the right most or even both right most images with your hand. Do you see the dog? Do you see the pyramids? You can also give the model additional information to steer it in a certain direction. A short phrase, such as dog with pyramids or rather a numerical version of it called an embedding is also provided to the model during its training process. This way, it knows how to take complete noise and eventually get a dog with the pyramids of Giza. In the end, we get a model that can take entirely new phrases and turn the noise into an entire new image. Here we start with the phrase Giza cat, and an image of pure noise. Then, if you repeat a partial denoising process many times, this denoising process is steered in such a way that you end up with an image that appears to be a real image with no noise, matching the description you gave. That's how diffusion and flow matching models work in a nutshell. By the way, what's the difference between these two models? The interesting thing is that, even though they are discussed as different models, researchers at Google DeepMind have shown they are actually very similar. In fact, mathematically, the models are the same. But aspects of their implementation are different. Interesting.