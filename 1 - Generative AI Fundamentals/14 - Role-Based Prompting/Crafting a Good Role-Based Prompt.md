Crafting a Good Role-Based Prompt
Crafting a good role-based prompt is not just about saying "Act like a pirate!" (though you can do that too!). You may need to be specific about the persona’s attributes, including their personality, communication style, vocabulary, and areas of expertise.

While there are no hard and fast rules in the ever-changing landscape of LLMs, the components of a role-based prompt may include:

[Role]: The persona the LLM should adopt (e.g., "Act as a pirate").
[Task]: The specific instruction or question (e.g., "Perform the calculation: 1+1?").
[Output Format]: How the response should be structured (e.g., "A sentence in Markdown.").
[Examples]: Sample input/output pairs (e.g., "Q: 1+3? / A: Tis 4, yar!").
[Context]: Additional information needed for the task (e.g., current date, if asking for the date).
Not all successful prompts contain all these components, and they don't necessarily appear in the same order. For instance, a complete prompt might be:

Act like a pirate! #[Role]
Perform the calculation: 1 + 1? #[Task]
Output a sentence in Markdown. #[Output Format]
Here’s an example: Q: 1 + 3? / A: Tis 4, yar!" #[Example]
In this example, we haven’t included additional context, but we would include any extra information the LLM needs that wouldn't have been in its training data.
If you construct such a role-based prompt, you might get an answer like: Ahoy! That be simple reckonin’, matey! Tis, 2, yar! This gets the calculation and tone correct. However, it seems to have missed the constraint to respond using only one sentence. We can certainly adjust our prompt to make it clearer to use ONLY-ONE-SENTENCE, which will likely work.
There’s a bigger point here, though. As we’re building AI Agents, we’ll want to know whether they are performing according to the criteria we have set for them. So if it’s important to only have a single sentence here, then it will need to be something we measure.