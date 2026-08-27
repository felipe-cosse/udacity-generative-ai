Summary
The Transformer architecture grew from text-only models into the foundation of modern multimodal AI. Starting with the 2017 Transformer paper “Attention Is All You Need,” the story moves through Vision Transformers (ViT), CLIP’s cross-modal alignment, diffusion-based generation guided by CLIP, and practical recipes for Vision-Language Models (VLMs) like GPT-4V and LLaVA. The central theme: embeddings enable a shared space where text and images can be compared, aligned, and used together for understanding and generation.

From text to everything

Transformers, introduced in 2017, replaced recurrent networks with attention, enabling efficient parallel training and long-range reasoning in sequences.
Their flexibility allowed rapid adaptation beyond language.
Vision Transformers (ViT, 2020)

Images are split into patches and treated as sequences, just like words.
This approach scales well, learning from far larger image datasets than many CNNs and achieving strong results in supervised and unsupervised tasks.
Embeddings and conceptual structure

An embedding is a vector that summarizes content (text or image) so similar content lies close in the embedding space.
Simple vector arithmetic can reflect abstract relations. Example: embedding(“king”) − embedding(“man”) ≈ embedding(“royal”); adding embedding(“woman”) yields a vector near embedding(“queen”).
This property supports analogies, retrieval, and alignment across modalities.
CLIP (2021): Alignment across text and images

CLIP learns a joint space where matching images and captions are close together.
This enables zero-shot classification: compare an image embedding with candidate text embeddings and select the closest match—no task-specific training needed.
CLIP’s alignment remains a backbone for many multimodal systems.
From understanding to generation: DALL·E 2 with diffusion

Diffusion models turn noise into images step by step.
CLIP guides generation by scoring how well an image matches a text prompt, acting like a judge during sampling.
This creates a feedback loop: better alignment improves generation; generation pressures improve alignment quality.
Practical recipe for Vision-Language Models (VLMs)

Start with a strong language model and attach a vision encoder (often CLIP-based).
Insert a small adapter that translates visual embeddings into a format the language model understands.
LLaVA demonstrated a simple, efficient approach: keep the vision and language components frozen and train only the connector.
This strategy made multimodal systems accessible to broader research groups and supports reasoning over multiple high-resolution images within long conversations.

Review
Transformers

Attention-centric architecture enabling scalable learning on sequences.
General-purpose design that extends beyond text.
Vision Transformers (ViT)

Treat images as sequences of patches.
Competitive with or superior to CNNs at large scale.
Embeddings

Vector representations capturing meaning and structure.
Distances reflect similarity; arithmetic can mirror concept relations.
CLIP and multimodal alignment

Shared embedding space for images and text.
Supports zero-shot recognition and robust retrieval.
Diffusion + CLIP for generation

CLIP guides diffusion models to match prompts with images.
Alignment and generation reinforce each other.
VLM construction with adapters

Vision encoder + language model + small translation layer.
LLaVA shows freezing main components and training the adapter can work remarkably well.
Modern systems can process multiple images and integrate them with ongoing dialogue.
Resources
Vaswani et al., “Attention Is All You Need” (2017): https://arxiv.org/abs/1706.03762(opens in a new tab)
Dosovitskiy et al., “An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale” (ViT, 2020): https://arxiv.org/abs/2010.11929(opens in a new tab)
Radford et al., “Learning Transferable Visual Models From Natural Language Supervision” (CLIP, 2021): https://arxiv.org/abs/2103.00020(opens in a new tab)
Ramesh et al., “Hierarchical Text-Conditional Image Generation with CLIP Latents” (DALL·E 2, 2022): https://arxiv.org/abs/2204.06125(opens in a new tab)
Liu et al., “Visual Instruction Tuning” (LLaVA, 2023): https://arxiv.org/abs/2304.08485(opens in a new tab)
OpenAI, “GPT-4 Technical Report” (GPT-4V context): https://arxiv.org/abs/2303.08774(opens in a new tab)







To understand how we got to the current crop of multimodal AI, we need to talk about transformers model architecture, our first milestone. Originally designed for natural language processing in 2017, with the pivotal paper, attention is all you need. Transformers have become the dominant architecture for multimodal AI. Then in 2020, came the vision transformer or VIT. Researchers discovered that by treating image patches as sequences, transformers could process images directly with very little modifications. They could then learn from vastly larger image collections than state of the art architectures at the time like convolution angular networks, CNN, achieving better performances in both supervised and unsupervised tasks. Then in 2021, we had the first true multimodal breakthrough. CLIP showed that transformers could combine vision and language in the same model. They introduced the foundational idea of all multimodal AI, which we can call embedding alignment. An embedding is a numerical vector representation of a piece of data, a piece of text, an image that captures and represents its content. Sometimes, embeddings are also called latent representations. In layman terms, an embedding is a summary of the relevant content of the data in numerical format. Embeddings are mathematical objects, vectors, and mathematical operations on them mapped to conceptual operations. For example, if we take the embedding of the word king and we subtract the embedding of the word man, we get a vector very close to the embedding of the word royal because a king is a man who happens to be royal. If we then take this royal embedding and we add the embedding for woman, we get the embedding for queen because a queen is a woman that happens to be royal. As you can see, mathematical operations in the embedding space map to conceptual operations. Moreover, embeddings for concepts that are related to each other are going to be close to each other in the embedding space. The revolution of CLIP was to provide a method to embed text and image in the same vector space so that an image and the caption for that image would be represented by very similar embedding vectors. Going back to our royal example, using CLIP to embed an image of a king and using CLIP to also embed to text an image of a king would give us two very similar embedding vectors, establishing a relationship between an image and its text and vice versa. This is what made CLIP the first mainstream multi modal model. By using this embedding alignment, CLIP is capable, for example, to do zero shot classification. Given an image and two or more possible captions for it, we can measure how close the embedding of the image is to the embedding of each caption separately, and then associate the image with the closest caption. Even though today we have more advanced models and methods to perform the same multimodal alignment in the embedding space, CLIP is still widely used in many multimodal architectures. While CLIP learned to understand which images matched with which text, models like DALL-E 2 reversed this process. It could create images from text descriptions. It used the diffusion models which gradually transform random noise into coherent images, guided by CLIPs understanding of how text and images relate. CLIP acted as a judge, ensuring the generated images actually matched their text props. This created a powerful feedback loop. CLIP'S understanding improved generation, while generation tasks helped refine understanding. The path to vision language models, VLMs, like GPT4V, came with a relatively simple idea. Take an existing language model that already understands text and teach it to see images too. Rather than starting over, researchers bolted on vision components, usually based on CLIP, two existing LLMs, with a small translation layer in between that was strained ad hoc. Think of it as an adapter that converts visual information into a format, the language model already understands. For example, projecting images in the same embedding space of the language, just like CLIP. A model called LLaVa proved the simple approach worked remarkably well. Keep both the vision and language parts frozen, just train the connector between them. These made building multimodal AI accessible to many more researchers. Today's models can juggle multiple high resolution images throughout a conversation. Understanding not just what's in each image, but how they relate to each other and to the ongoing discussion.