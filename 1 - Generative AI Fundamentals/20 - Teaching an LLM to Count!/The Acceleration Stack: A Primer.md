This project uses a powerful, modern tool-stack to make fine-tuning possible on a single GPU. Since you haven't seen these tools before, here’s a quick primer on the key technologies and why we're using them.

The Problem: Fine-Tuning is Expensive
Fine-tuning a model like Qwen2.5-3B (3 billion parameters) traditionally requires massive amounts of VRAM and time. Training all 3 billion parameters (full fine-tuning) is not feasible on consumer or most cloud GPUs.

LoRA: The Parameter-Efficient "Adapter"
LoRA (Low-Rank Adaptation) is the solution. Instead of training the entire model, we:

Freeze all 3 billion original parameters.
Inject small, "low-rank" adapter modules into key layers of the model (like the attention and feed-forward layers).
Train only these new, tiny adapters.
This means we might only train ~30-100 million parameters instead of 3 billion. The result is a small adapter_model.safetensors file that plugs into the base model to give it new skills.

In this project: You will configure LoRA in Cell 5 by choosing the lora_rank (the size of the adapter) and the target_modules (which layers to plug it into).
Unsloth: The 2x Faster Training Engine
Unsloth is an optimization library built on top of LoRA. It uses advanced techniques (like re-writing CUDA kernels) to make LoRA training up to 2x faster and reduce memory usage by 60%.

It's the magic that allows us to fine-tune this 3B model on a single 16GB T4 GPU without it crashing.

In this project: Unsloth is used when you call FastLanguageModel.from_pretrained and FastLanguageModel.get_peft_model. It automatically patches the Hugging Face Transformers library for high-speed training.
vLLM: The High-Speed Inference Engine
vLLM is an engine for inference (running the model), not training. In our RLHF loop (using GRPO), we need to constantly generate thousands of sample answers from the model to see how good they are. Doing this one-by-one is incredibly slow.

vLLM uses a smart memory management technique called PagedAttention to batch these generation requests and make inference extremely fast.

In this project: vLLM is automatically used by the GRPOTrainer (when you set use_vllm=True) and by the model.fast_generate calls. This speeds up both the training loop and your final evaluation.
GRPO: The Reinforcement Learning "Teacher"
GRPO (Group Relative Policy Optimization) is the "how" of our project. It's the Reinforcement Learning (RL) algorithm that teaches the model.

It works in a loop:

Generate: The model generates multiple (a "group" of) possible answers for a prompt.
Reward: Our custom reward functions (which you will build) score each answer.
Optimize: GRPO compares the "good" answers to the "bad" ones and updates the LoRA adapters, "nudging" the model's policy (its decision-making process) to be more like the high-reward answers.



