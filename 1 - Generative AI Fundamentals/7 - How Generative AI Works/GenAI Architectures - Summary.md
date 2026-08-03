# Summary: GenAI Architectures

## Core Concepts
* **Generative vs. Discriminative Models:** Discriminative models classify or predict based on existing data (e.g., "Is this a cat?"). Generative models learn the underlying data distribution to produce entirely new data samples (e.g., generating a unique image of a dog).
* **Stochastic Nature:** Due to the probabilistic nature of generative models, outputs can be unpredictable or highly creative, requiring controlled tuning depending on the enterprise use case.

## Architecture Types

### 1. Transformer Architecture
* **Primary Use Case:** Text, audio, and sequential data generation (e.g., ChatGPT, Claude, Gemini).
* **Key Capabilities:** Excels at parallel processing of sequential data and managing long-range dependencies across large documents.
* **Mechanism:** 
  * Breaks inputs into **tokens** (words or sub-words).
  * Uses **autoregression** to act as an advanced autocomplete engine, predicting the next token in a sequence based on calculated probabilities from training data.

### 2. Diffusion & Flow Matching Models
* **Primary Use Case:** Image and visual data generation.
* **Mechanism:** 
  * Works like a "magic eraser" by starting with pure noise and iteratively removing it to reveal a clear image (denoising).
  * **Training:** Reverses the process by taking clear images, adding noise systematically, and training the model to predict and remove the noise based on text-prompt steering.
* **Industry Note:** Research from Google DeepMind confirms that Diffusion and Flow Matching models are mathematically equivalent despite differing implementation details.