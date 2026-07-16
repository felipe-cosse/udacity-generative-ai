Module Summary
This module demonstrated how to build powerful text classifiers using foundation models. We started by classifying movie review sentiment, learning how to use a SYSTEM_PROMPT to define the task and require a specific JSON output format. We explored both zero-shot (instructions only) and few-shot (instructions with examples) prompting techniques. You then applied these skills in an exercise to build your own spam classifier.

Key Takeaways
A SYSTEM_PROMPT is a powerful tool for guiding a foundation model. It should clearly define the model's role, the specific task (e.g., "classify text messages as SPAM or NOT SPAM"), and the exact output format (like JSON) for reliable parsing.
Zero-shot prompting instructs the model on a task without providing any prior examples, relying entirely on the model's pre-existing knowledge.
Few-shot prompting enhances the prompt by including a few complete, labeled examples. This gives the model in-context examples to follow, which can often improve its accuracy.
The core prompting structure (defining a role, specifying format, and providing examples) is a highly adaptable pattern that can be easily modified for many different classification tasks.
While few-shot prompting is a valuable technique, it is not a guaranteed fix for all classification errors, especially when dealing with ambiguous or difficult examples.