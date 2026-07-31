Your main task is to complete the project/starter/gen_ai_fundamentals_project_starter.ipynb notebook. Follow the steps below, which correspond to the "TODO" sections in the notebook.

Phase 1: Project Setup
Run the initial cells to install dependencies and verify your GPU memory (nvidia-smi).
Task (Cell 5): Load the Qwen2.5-3B-Instruct model.
Determine and set an appropriate lora_rank value. A good starting point is 64.
Choose the target_modules for LoRA. You should target all the key linear layers in the attention and MLP blocks ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj").
Explain your choices in the code comments.
Phase 2: Prompt Engineering Baseline
Run the cell (Cell 7) with a blank system prompt to see the model's (poor) baseline performance.
Task (Cell 8): Develop a new SYSTEM_PROMPT.
It must incorporate Chain-of-Thought (CoT) prompting, telling the model to think step-by-step.
It must include at least one few-shot example (like the "room" example) for the model to follow.
Run the cell again. You should see a much-improved (though still not perfect) response. This motivates the need for RL fine-tuning.
Phase 3: Dataset Creation
Run the cells to create the ALL_WORDS list and the generate_records function.
Run the ds.map cell to format the dataset with your SYSTEM_PROMPT.
Run the final cell in this section to see how the (untuned) model performs on a sample from the dataset.
Phase 4: Building the Reward Functions (Core Task)
This is the most critical part of the project. You will implement the logic that teaches the model what a "good" answer is.

Task (Cell 12): numbering_reward_func
Complete the logic to reward in-order numbering (e.g., +0.5), penalize out-of-order numbering (e.g., -0.5), and penalize for continuing beyond the word's length (e.g., -1.0).
Task (Cell 13): spelling_reward_func
Complete the logic to:
Reward exactly correct spelling (e.g., +2.0).
Penalize for differences in length (e.g., -0.5 per letter).
Penalize for extra letters (e.g., -1.0 per letter).
Penalize for missing letters (e.g., -0.5 per letter).
Task (Cell 14): counting_reward_func
Complete the if/else block to reward an accurate running total at each step (e.g., +1.0) and penalize an inaccurate one (e.g., -1.0).
Complete the final res.append(...) line to normalize and scale the reward.
Task (Cell 15): format_reward_func
Complete the logic to:
Reward the model for using the correct <reasoning>...</reasoning><answer>...</answer> format (e.g., +0.5).
Reward the model if the extracted answer is a digit (e.g., +0.5).
Task (Cell 16): correct_answer_reward_func
Complete the list comprehension to provide a strong positive reward for a correct final answer (e.g., 2.0) and a negative reward for an incorrect one (e.g., -1.0).
Phase 5: Model Training
Task (Cell 18): Set the COMMON_GRPO_TRAINING_PARAMS.
Fill in values for learning_rate, beta, per_device_train_batch_size, num_generations, and gradient_accumulation_steps.
Refer to the provided documentation links for guidance. (Good defaults are 10e-6, 0.0001, 16, 4, and 1).
Task (Cell 19): Run the Quick Train (5 steps).
Analyze the log table output. Are the reward functions working? You should see non-zero values.
Task (Cell 21): Run the Slower Train.
Set max_steps for a longer run (e.g., 80 to 100 steps), which should take 30-60 minutes.
Execute the training and observe the log table. You should see the reward and rewards/correct_answer_reward_func/mean columns trend upwards.
Run the cell (Cell 22) to plot your training rewards.
Phase 6: View the Results
Run the cells to save your LoRA adapter (Cell 23) and define the compare_old_and_new_model function (Cell 24).
Task (Cell 25): Compare models on the letter-counting task.
Run the cell to load the first dataset item.
Observe the "OLD" (untuned) vs. "NEW" (your tuned model) output. The "NEW" model should now follow the reasoning steps and get the correct answer.
Task (Cell 26): Check for Catastrophic Forgetting.
Write a general knowledge question (e.g., "What is the capital of the Philippines?").
Run the compare_old_and_new_model function with your question.
Verify that both the "OLD" and "NEW" models answer correctly, proving that your fine-tuning taught a new skill without erasing the model's existing knowledge.
Once all cells are run and all outputs are visible, you are ready to submit your project!




