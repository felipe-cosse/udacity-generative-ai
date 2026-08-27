Summary
The Transformer’s evolution moved beyond words to sound and motion, weaving multiple sensory streams into shared representation spaces. From early audio-text alignment to unified multimodal understanding, each breakthrough expanded how machines perceive and generate the world.

Audio-language alignment: Models like CLAP link sounds with text for retrieval and zero-shot tasks.
Speech processing: Sequence-to-sequence architectures such as Whisper handle transcription, translation, and summarization.
Generative audio: Text-to-speech and text-to-music transformers use diffusion models guided by CLIP-like alignments.
Video understanding: TimeSformer captures spatial and temporal structure with 3D patches, while CLIP4Clip and Frozen align text and video through hierarchical representations.
Reasoning across modalities: Systems like Video-LLaMA connect encoders to large language models, enabling narrative reasoning.
Unified multimodality: ImageBind extends this integration, aligning text, images, video, audio, depth, thermal, and motion within one coherent embedding space.
Contrastive alignment vs. sequence-to-sequence:

Contrastive models (CLIP, CLAP) learn to place different modalities in a shared embedding space, enabling retrieval and zero-shot classification. This is effective when matching inputs across modalities (e.g., “barking dog” text with dog-bark audio).
Sequence-to-sequence models (Whisper) use an encoder-decoder transformer. The encoder maps audio into a learned latent space; the decoder converts this representation into text. This approach favors structured generation tasks such as transcription, translation, and summarization, without requiring embeddings to match a text space directly.
Generative audio models:

Text-to-speech and text-to-music models often combine transformer backbones with diffusion or other generative techniques.
Guidance from CLIP-like audio-text models helps ensure outputs match prompts semantically, improving content fidelity and prompt adherence.
Spatiotemporal modeling for moving imagery:

Extending Vision Transformers, TimeSformer treats inputs as cubes spanning height, width, and time, handling temporal dependencies with attention mechanisms.
This approach recognizes evolving actions and context, an essential capability missing from static-image models.
Multimodal matching and reasoning:

CLIP4Clip broadens contrastive alignment to clips and descriptions, enabling zero-shot classification and retrieval without task-specific finetuning.
Frozen introduces hierarchical embeddings, aligning not only entire clips but also individual frames and scenes with textual descriptions—useful for granular retrieval and localized reasoning.
Adaptor-based systems (e.g., Video-LLaMA) connect frozen LLMs to specialized encoders. Adapters translate visual or audio features into token-like inputs for LLMs, enabling question answering, narrative reasoning, and prediction tasks over long sequences.
Unified embeddings and holistic understanding:

True multimodal fusion maps related signals across sight, sound, and language into nearby coordinates. For example, a barking clip, the bark waveform, and “a dog making noise” cluster together.
ImageBind generalizes alignment beyond typical modalities, jointly linking text, images, moving imagery, audio, depth, thermal, and motion. This yields richer semantic grounding and enables cross-modal transfer even when some modalities are missing at inference.

Review
Shared embedding spaces:

Contrastive learning aligns modalities (text, audio, moving imagery) in the same vector space.
Benefits: retrieval, zero-shot classification, cross-modal matching.
Encoder-decoder vs. decoder-only:

Whisper uses encoder-decoder for ASR, translation, and summarization from audio.
CLIP and GPT-style models are decoder-only or rely on contrastive losses for alignment and generation.
Generative conditioning:

Diffusion or autoregressive generators guided by CLIP-like models improve semantic faithfulness in text-to-speech and text-to-music.
Spatiotemporal attention:

TimeSformer handles temporal dynamics by attending over 3D patches.
Hierarchical alignment:

Frozen aligns multiple granularities (frame, scene, full clip), aiding fine-grained search and understanding.
Adapters with LLMs:

Video-LLaMA-style systems bridge encoders and LLMs to support complex reasoning over multimodal inputs.
Multimodal unification:

ImageBind aligns six-plus modalities, supporting robust transfer and richer context even with incomplete data.
Resources
Elizalde et al., “CLAP: Learning Audio Concepts From Natural Language Supervision” (2022): https://arxiv.org/abs/2206.04769(opens in a new tab)
Bertasius, Wang & Torresani, “Is Space-Time Attention All You Need for Video Understanding?” (TimeSformer, 2021): https://proceedings.mlr.press/v139/bertasius21a.html(opens in a new tab)
Luo et al., “CLIP4Clip: An Empirical Study of CLIP for End-to-End Video Clip Retrieval” (2021): https://arxiv.org/abs/2104.08860(opens in a new tab)
Zhang et al., “Video-LLaMA: An Instruction-tuned Audio-Visual Language Model for Video Understanding” (2023): https://arxiv.org/abs/2306.02858(opens in a new tab)
Girdhar et al., “ImageBind: One Embedding Space to Bind Them All” (2023): https://arxiv.org/abs/2305.05665(opens in a new tab)







The famous clip model developed for computer vision, pioneer the idea of creating shared embedding spaces between different modalities. The same idea can be applied to audio. Models like clap, learned, general purpose, audio embeddings, aligned with text, and just like clip for images can be used for retrieval or zero shark classification tasks between text and audio. However, there is a completely different approach that was started by the Whisper model, a milestone model by Open AI. While still based on transformers, Whisper is much more similar to a language translation transformer than it is to a contrastive learning model like clip. The model has an encoder decoder architecture instead of a decoder only architecture like clip and the GPT family of models. The encoder brings the audio data to a learned representation space, not necessarily aligned with a textual representation like in clip. Then the decoder starts from there and transforms it to the output text. Whisper is an automatic speech recognition system, ASR, and I can do speech to text tasks, such as transcribing, translating, and summarizing, starting from audio inputs. There are also text to speech models that are based on transformers and even text to music models, which can generate entire songs from a text prompt. Some of these use ideas similar to DALLE 2 for images. A diffusion model or other generative model generates data informed by a clip like model for audio to ensure adherence with the prompt. Video transformers extended the approach taken by the vision transformer VIT by treating videos as sequences of spatio temporal patches. Just like vision transformers divide an image in 2D patches, video transformers divide the video in 3D cubes, spanning space and time. Models like times Former showed transformers could handle videos temporal dimension effectively. The multi modal breakthrough came with clip for clip, which applied clips embedding alignment idea to video. Learning to place video clips and their text descriptions in the same vector space. This enabled zero shot video classification just like clip had done for images. Videos posed unique challenges. Like static images, they contain evolving narrative and multiple actions. Models like frozen created hierarchical embeddings that could align not just entire videos, but also individual frames or scenes with corresponding text descriptions. Today's video language models like Video lama, follow the same pattern successfully applied in the image domain by visual language models. They connect video encoders to existing LLMs, possibly frozen, trough learned adapters. These models can answer complex questions about videos, going beyond simple matching to understanding narratives and predicting what happens next. What makes video special is its intrinsic multimodal nature. Visual, audio, and text naturally coexist. This has led to models that create unified embedding spaces where a dog barking video, the bark sound audio, and a dog making noise text all map to nearby points, achieving true multimodal understanding. It is worth also meshing the image bind model and similar endeavors, that take the clip idea and implement it simultaneously across many modalities. Image bind creates a unified embedding space that connects, text, images, video, audio, depth, thermal, and motion data, giving machines holistic understanding of how objects look, sound, feel, and move.