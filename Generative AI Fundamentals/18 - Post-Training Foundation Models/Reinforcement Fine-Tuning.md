Preference fine-tuning is the second major step in post-training foundation models, following supervised fine-tuning. Its primary purpose is to align a model's outputs more closely with human preferences and values, addressing nuanced issues like factual accuracy, ethical considerations, and desired behaviors that are difficult to teach through simple examples alone.

Preference fine-tuning is a crucial stage for refining foundation models after their initial supervised fine-tuning (SFT). It focuses on aligning model outputs with human values and increasing their capabilities.

The goals of preference fine-tuning include:

Aligning outputs with human preferences and values: This addresses issues like factual incorrectness, ethical problems, or undesired behaviors such as excessive politeness.
Increasing model capabilities: This can enhance complex skills like reasoning.
Refining behaviors not easily taught via SFT: Some nuanced behaviors are better shaped through preference feedback than through static examples.
Because this stage typically uses techniques from reinforcement learning (RL), it is sometimes referred to as Reinforcement Fine-Tuning.

A visual diagram illustrating 'Preference Fine-Tuning,' featuring a gear icon with sliders and colored dots. Key points include: aligning model outputs with human preferences, enhancing model capabilities for reasoning, and a note that it's sometimes referred to as Reinforcement Fine-Tuning.
Preference fine-tuning goals.

Reinforcement Learning from Human Feedback (RLHF)
The classical method for preference fine-tuning is Reinforcement Learning from Human Feedback (RLHF). This process involves human annotators providing direct feedback on the model's outputs.

The RLHF process typically involves three steps:

Human Annotation: Human labelers are given a prompt and multiple model-generated responses. They rank or compare these responses to indicate which one is preferred. This creates a preference dataset containing a prompt, a "winning" response, and a "losing" response. This task is generally easier for humans than directly scoring a response from scratch.
Reward Model Training: A separate reward model (RM) is trained on the preference dataset. The RM learns to predict a scalar score that reflects how much a human would prefer a given response.
Model Optimization: The foundation model's policy is fine-tuned using an RL algorithm, most famously Proximal Policy Optimization (PPO). The model learns to generate responses that maximize the score given by the trained reward model.
A diagram illustrating a reward model training process in natural language processing. It depicts preference data where a user prompt generates responses scored by a reward model. The process includes arrows indicating the flow from ranking responses, through the reward model, to sampling completions, highlighting phases of human annotation, model training, and optimization. Additional text references a research paper by Rafailov et al. (2023) regarding direct preference optimization.
Reinforcement learning from human feedback (RLHF).

Direct Preference Optimization (DPO)
While effective, RLHF can be complex and resource-intensive. Newer methods like Direct Preference Optimization (DPO) have emerged to simplify the alignment process. DPO is a more efficient alternative to traditional RLHF.

The key difference in DPO is that it eliminates the need to train a separate reward model. Instead, it directly optimizes the foundation model's weights using the preference dataset. DPO adjusts the model to increase the likelihood of the preferred response and decrease the likelihood of the rejected response.

To prevent the model from deviating too far from its original capabilities during training, DPO uses a reference model (often the base, pre-trained model). This stabilizes training and helps avoid catastrophic forgetting.

The industry has seen a shift towards this simpler approach. For example, Meta switched from using RLHF for Llama 2 to DPO for Llama 3 to reduce pipeline complexity.

A diagram illustrating a process involving preference data for generating a poem about the history of jazz. It shows a user request ("write me a poem about the history of jazz") leading to two text outputs (Y_w and Y_L), where one output is preferred over the other, linked to a reward model represented by a neural network structure.
Direct preference optimization (DPO)

Group Relative Policy Optimization (GRPO)
Another advanced method is Group Relative Policy Optimization (GRPO), which uses explicit, computable rewards that do not require human annotators. GRPO was specifically designed to improve reasoning tasks like solving math problems or debugging code.

Like DPO, GRPO eliminates the reward network of RLHF. However, it also alleviates the need for a human-labeled preference dataset.

The GRPO process works as follows:

A query is passed to the model being optimized to generate a group of multiple responses.
These responses are scored using explicit reward functions (e.g., checking for correct format or final answer).
The scores are normalized to create relative "advantages" for each response within the group.
An objective function uses these advantages and the distance from a reference model to update the main model.
This process increases the likelihood of responses with positive advantages and decreases it for those with negative ones, effectively teaching the model to prefer higher-scoring outputs without direct human preference labels.

Preference fine-tuning uses human or explicit feedback to align foundation models with desired behaviors and values, with modern methods like DPO and GRPO offering simpler and more efficient alternatives to the traditional RLHF pipeline.

A flowchart illustrating the optimization process of a model. At the top, a 'Query' leads to 'Model Being Optimized,' which generates 'Responses.' Connected to this model is an 'Objective Function' assessing the 'Distance between reference model and optimized model' and producing 'Rewards.' Additionally, 'Normalized, relative “advantages”' are derived from the process.
Group Relative Policy Optimization (GRPO)








Preference fine-tuning is a second major step in post-training foundation models, right after supervised fine-tuning. One goal is to align the model's outputs with human preferences and values, addressing issues such as factual incorrectness, ethical problems, or undesired behaviors like excessive politeness. Another goal is to increase the capabilities of the model, for instance, reasoning, and to be able to more finely tune behavior that cannot be easily demonstrated just using examples as an SFT. This is typically achieved using reinforcement learning or at least methods that are inspired by reinforcement learning. For this reason, sometimes a step is also referred to as reinforcement fine-tuning. Speaking of reinforcement learning, the classical method in preference fine-tuning is reinforcement learning from human feedback, which involves human annotators providing preference comparisons of model outputs. The process typically involves human annotation. Human labelers rank or compare multiple responses generated by the model for a given prompt, indicating which outputs are preferred. This yields preference data in the format of prompt winning response and then the losing response. This task is considered easier for humans than directly scoring responses. Reward model training: a separate reward model is trained on this human preference data. Its function is to output a score reflecting how good a response is. Then the foundation model optimization. The foundation model is further fine-tuned using a reinforcement learning algorithm. Most famously, proximal policy optimization or PPO. The model learns to generate responses that maximize the scores given by the trained reward model. While effective reinforcement learning from human feedback can be complex and resource-intensive. Newer methods like direct preference optimization or DPO have emerged to simplify this alignment process. DPO stands out as a simplified and more efficient alternative to traditional reinforcement learning from human feedback. Key difference is that DPO eliminates the need to train a separate reward model. Instead, it directly optimizes the foundation model weights based on the human preference data. Specifically, given a human preferred response and ejected response for a given prompt, DPO directly adjusts a model to increase the likelihood of the preferred output and decrease the likelihood of the rejected one. DPO also uses a reference model, often the base pre-trained model, to stabilize training to keep the model from changing too much and forget its original capabilities. This simplification of DPO leads to a much simpler and more straightforward alignment pipeline. For example, Meta switched from reinforcement learning, from human feedback for Llama 2 to DPO for Llama 3, and this was to reduce the complexity of their pipelines. Let's talk about another method called GRPO, or a group relative policy optimization. GRPO uses explicit rewards that are calculated without human annotators. Group relative policy optimization, or GRPO, was specifically designed to improve reasoning tasks like solving math problems or debugging code. Developed by the DeepSeek team and introduced in late 2024, GRPO was a key technique for training their R1 reasoning model. Like DPO, GRPO also eliminates the reward network, but it also alleviates the need for a label preference data set. Instead, we take a prompt, which we run through the model to be optimized, and obtain a group of responses. We run these responses through explicit reward functions, which are easy to compute, like checking the format and the correctness of the final answer. The idea is that some of these responses will get higher scores than others. We calculate the mean, and we subtract the mean from these scores and divide by the standard deviation to normalize. We call these new scores advantages. We then calculate an objective function based on these advantages and the distance between a reference model and the model we're optimizing. Finally, that objective function is used to update the model to increase the likelihood of responses with positive advantage and to decrease it for those with negative advantage.