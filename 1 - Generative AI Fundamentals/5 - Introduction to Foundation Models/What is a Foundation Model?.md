# Introduction to Foundation Models — What is a Foundation Model?

Foundation models represent a major shift in AI. Unlike traditional models built for one specific job, a foundation model is a large, general-purpose network trained on vast data. This allows it to be adapted to many different tasks, from writing text to understanding images, often with minimal extra training.

A foundation model is a large scale neural network, trained on vast amounts of data, designed to perform effectively across a wide variety of tasks. Unlike traditional AI models, which are often task specific, foundation models serve as versatile bases or foundations that can be adapted or fine tuned to tackle numerous problems. Imagine a large building that can be used as a hospital, a school, or an office building, with minimal adjustments. Similarly, the strength of foundation models comes from their ability to generalize from immense training data, enabling them to recognize patterns, generate coherent text, understand images, and more, and often with minimal additional training. 

ChatGPT can summarize entire books, distilling complex narratives into concise summaries. It can extract information directly from tables found in PDFs or even from images, quickly making sense of data that previously required manual interpretation. ChatGPT has evolved into an interactive assistant capable of executing real world tasks through its agentic features, an emergent property that allows it to book restaurant reservations or manage calendar appointments. These advanced functionalities highlight how foundation models are not only reshaping traditional AI tasks, but also becoming proactive partners in our everyday lives. 

## Comparing Paradigms: Foundation Models vs. Traditional Models

Now that we have an idea of what a foundation model is, let's compare it with something that it is not. Let's talk about the differences between foundation models and traditional models. Foundation models and traditional models represent two approaches, two paradigms to building and utilizing machine learning systems, each with its own set of principles, methods, and applications. 

Let's compare the key characteristics that define foundation models versus a paradigm of traditional AI models:

* **Data:** 
  * **Traditional Models:** Trained on smaller, task-specific, and domain-specific datasets. These are often meticulously curated and built from scratch based on a specific use case.
  * **Foundation Models:** Trained on very large, general datasets, such as the entire Wikipedia or all of Project Gutenberg.
* **Capability:** 
  * **Traditional Models:** Designed to be task-specific and domain-specific. For example, a model created to classify healthcare documents would largely be useless outside of that use case.
  * **Foundation Models:** Designed to generalize across many tasks. Because of their broad training, they develop such a general understanding that they can perform classification tasks, for example, on examples they have never seen before.
* **Resources:** 
  * **Traditional Models:** Usually smaller, and thus they require fewer computational resources.
  * **Foundation Models:** Often very big and require immense computational resources to capture their generality.
* **Examples:** 
  * **Traditional Models:** Linear regression, decision trees, convolutional neural nets (CNNs), and other types of standard machine learning models.
  * **Foundation Models:** Commercial models like the GPT models from OpenAI, Gemini from Google, and Claude from Anthropic; open-weight models such as Qwen from Alibaba and Llama from Meta.

## The Foundation Model Landscape

The foundation model landscape includes a mix of commercial (closed-source) and open-source models. Commercial models like OpenAI's GPT, Google's Gemini, and Anthropic's Claude are multimodal, meaning they can process not just text, but also images, audio, and video, enabling dynamic and interactive applications. Details of these commercial models are not publicly available, but they are understood to be massive. 

Open-source models provide more transparency and accessibility. Meta is training large open-source variants, with their Llama line ranging from 109 billion to 2 trillion parameters. 

The table below shows several key foundation models available today:

| Model Name | Sizes | Developer | Model Type | Modalities |
| :--- | :--- | :--- | :--- | :--- |
| GPT-5 | Not disclosed | OpenAI | Commercial | Multimodal |
| Gemini (2.5 family) | Not disclosed | Google | Commercial | Multimodal |
| Claude | Not disclosed | Anthropic | Commercial | Multimodal |
| Llama 4 | 109B to 2T | Meta AI | Open-source | Multimodal |
| BLOOM | 176B | Big Science Workshop | Open-source | Text only |
| Mistral Small 3.2 | 24B | Mistral AI | Open-source | Text only |
| Qwen 3 family | 0.6B to 235B | Alibaba | Open-source | Text only |

### Notable Open-Source Variants
* **BLOOM:** A 176 billion parameter decoder-only transformer built by the Big Science workshop. It was developed collaboratively with a commitment to transparency and trained on over 1.6 terabytes of multilingual data, allowing it to generate text across 46 natural languages and 13 programming languages.
* **Mistral Small 3.2:** A 24 billion parameter open-weight model distributed under an Apache 2.0 license. Note that while Mistral offers larger multimodal models, those remain closed-source.
* **Qwen Series:** Developed by Alibaba, this family provides a wide range of sizes (from 0.6B to 235B parameters), making them highly useful when local deployment hardware is limited and a smaller, efficient model is required.

**Conclusion:** Foundation models are large, general-purpose models trained on massive datasets, allowing them to be adapted for a wide variety of tasks, unlike smaller, specialized traditional models.





A foundation model is a large scale neural network, trained on vast amounts of data, designed to perform effectively across a wide variety of tasks. Unlike traditional AI models, which are often task specific, foundation models serve as versatile bases or foundations that can be adapted or fine tuned to tackle numerous problems. Imagine a large building that can be used as a hospital, a school, or an office building, with minimal adjustments. Similarly, the strength of foundation models comes from their ability to generalize from immense training data, enabling them to recognize patterns, generate coherent text, understand images, and more, and often with minimal additional training. Chat GPT can summarize entire books, distilling complex narratives into concise summaries. It can extract information directly from tables found in PDFs or even from images, quickly making sense of data that previously required manual interpretation. Chat GPT has evolved into an interactive assistant capable of executing real world tasks through its agentic features, an emergent property that allows it to book restaurant reservations or manage calendar appointments. These advanced functionalities highlight how foundation models are not only reshaping traditional AI tasks, but also becoming proactive partners in our everyday lives. Now that we have an idea of what a foundation model is, let's compare it with something that it is not. Let's talk about the differences between foundation models and traditional models. Foundation models and traditional models represent two approaches, two paradigms to building and utilizing machine learning systems, each with its own set of principles, methods, and applications. Let's compare the key characteristics that define foundation models versus a paradigm of traditional AI models. First, let's talk about the data they're trained on. Traditional AI models tend to be trained on smaller task specific datasets. In fact, these models will often be trained from scratch based on a meticulously curated data set. In contrast, foundation models are trained on very large general datasets. For instance, this might include the entire Wikipedia in all of Project Gutenberg. This difference in data directly leads to their capabilities, because they are trained on narrow data, traditional models are task specific and domain specific. A model created to classify healthcare documents, for instance, would largely be useless outside of that use case. On the other hand, foundation models are designed to generalize across many tasks. Because of their broad training, they can develop such a general understanding that they can perform classification tasks, for example, if they have never seen before. Next, let's consider their size and computational needs. Traditional models are usually smaller, and thus they require fewer computational resources. Conversely, in order for foundation models to capture this generality, they're often big and thus require immense computational resources. Finally, let's ground this with some specific examples. Examples of traditional AI models include linear regression, decision trees, convolutional neural nets, and other types of machine learning models. When we talk about foundation models, examples include the GPT models from Open AI, Gemini from Google and Claude from Anthropic. There are also open weight models such as Quin from Alibaba and Llama from Meta. Let's take a closer look at some of the foundation LLMs that exist today. Commercially Open AI's GPT, Google's Gemini, and Anthropic's Claude models lead the field. These multi-modal systems process not just text, but also images, audio, and even videos, enabling dynamic and interactive applications. Unfortunately, details of these models are not publicly available, but you can imagine they are very large. Meta is still training its largest open source model, which is 2 trillion parameters, if that gives you any clue. Speaking of Metas Llama 4, these open source models offer multi-modal understanding with models ranging 109 billion to 2 trillion parameters. Additionally, BLOOM is particularly notable. It's a 176 billion parameter decoder only transformer built by the Big Science workshop, designed to generate text across 46 natural languages and 13 programming languages. Developed collaboratively with a commitment to transparency, BLOOM was trained on over 1.6 terabytes of multilingual data, making it one of the most inclusive and democratized large language models available. Another standout is Mistral Small 3.2, which has 24 billion parameters. It's an apache 2.0 license open weight model, and note that Mistral does have larger multimodal models available, but those are actually closed source. Lastly, the Qwen series by Alibaba has a wide range of sizes, which is useful, especially when your hardware is limited, and you're looking for a smaller model.