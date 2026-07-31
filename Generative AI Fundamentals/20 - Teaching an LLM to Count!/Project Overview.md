Welcome to the team, new Generative AI Engineer!

You've joined a new AI startup focused on building "Reasoning Engines." While our foundational Large Language Models (LLMs) are incredibly fluent and creative, we've hit a common but critical problem: they struggle with precise, procedural reasoning.

Ask an LLM to write a poem, and it excels. Ask it to count the number of 'e's in the word "effectiveness," and it will often fail, even while confidently giving a wrong answer. This "reasoning gap" is a major hurdle to building truly intelligent and reliable systems.

Your first project is to tackle this problem head-on.

The Challenge
Your challenge is to teach an instruction-tuned LLM to perform perfect, step-by-step reasoning for a specific task: counting the occurrences of a letter in a word.

This task is deceptively difficult for an LLM. It can't "see" the word all at once as we do. It must be taught to break the problem down, just as a person would:

Spell the word letter by letter.
At each letter, check if it's the one we're looking for.
Keep a running total.
State the final count.
You will use an advanced reinforcement learning (RL) method called Group Relative Policy Optimization (GRPO) to teach the model this behavior.

Your Product
Your final product will be a fine-tuned Qwen2.5-3B-Instruct model that demonstrates reliable step-by-step reasoning for the letter-counting task.

Because fine-tuning a 3-billion-parameter model is computationally expensive, you'll be using LoRA (Low-Rank Adaptation). This means your "product" won't be a whole new 3B model, but rather a small, efficient "adapter" file (adapter_model.safetensors). This adapter plugs into the base model and imparts the new reasoning skill without altering the model's original knowledge.

Deliverables
To complete this project, you will need to submit your fully completed project/starter/gen_ai_fundamentals_project_starter.ipynb notebook.

This notebook should:

Have all TODO sections completed.
Include your explanations for hyperparameter choices (like lora_rank and target_modules).
Contain the complete, functional code for all reward functions.
Show the output of all training and evaluation cells.



