How do you choose the right LLM for your project? This is one of the most common places where projects fail. It's tempting to look at a public leaderboard and pick whatever model sits at the top. But that's a technology-first approach that often leads to disappointment.

The selection of an LLM is fundamentally a business decision, not just a technical one. The "best" model on paper might be completely wrong for your specific use case, budget, or regulatory environment. Let me walk you through a framework that starts with your problem, not with the technology.

Deconstructing Your Business Problem
The first and most important step is to forget about the models entirely. Focus on the problem you need to solve. What specific cognitive capabilities does your task require?

Let me illustrate with a real example. A legal tech company came to me with two different AI projects:

Project A: Generate first drafts of contracts based on templates and client requirements

Project B: Analyze complex merger agreements to identify potential risks and liabilities

These might seem similar - they're both "legal AI" - but they require fundamentally different cognitive capabilities. Project A needs fluency and formatting. Project B needs multi-step logical analysis.

The Two Classes of Models: Generation vs. Reasoning
Once you understand your cognitive requirements, you'll find the LLM landscape divides into two distinct classes:

Generation Models: The Creative Writers
Think of models like GPT-4o or Claude Sonnet. Their architecture is optimized for fluency, creativity, and conversation. They excel at:

Writing marketing copy that converts
Powering conversational chatbots
Summarizing documents where style and flow matter
Creating content that needs to sound human
Reasoning Models: The Problem Solvers
On the other side, you have specialized tools like OpenAI's o-series models, Claude Opus, or Google's Gemini 2.5 Pro. These are specifically trained for multi-step logical problem-solving. They have a distinct internal process - often called chain of thought - where they break complex problems into intermediate steps.

The Trade-off: Cognitive Labor Economics
You can force a generation model to solve logical problems, but YOU have to do the heavy lifting.

Let me show you what I mean with a real example from a fintech company:

Forcing Generation Models to Reason
# Complex prompt needed for generation model to handle reasoning
def calculate_loan_eligibility_generation_model(application):
    prompt = f"""
    Calculate loan eligibility step by step.

    STEP 1: Calculate debt-to-income ratio
    Take the monthly debt payments: {application['monthly_debt']}
    Divide by monthly income: {application['monthly_income']}
    Write the calculation: ___

    STEP 2: Check credit score requirements
    If credit score ({application['credit_score']}) is:
    - Above 740: Excellent tier
    - 670-739: Good tier
    - 580-669: Fair tier
    - Below 580: Poor tier
    Your determination: ___

    STEP 3: Verify employment stability
    Check if employed for > 2 years: {application['employment_length']}
    Check if income is stable: {application['income_variance']}
    Your assessment: ___

    [... continues for 15 more steps ...]

    FINAL DECISION: Based on ALL above steps, determine eligibility
    """

    return generation_model.generate(prompt)
The Same Task with a Reasoning Model
# Simple prompt for reasoning model - it handles the steps internally
def calculate_loan_eligibility_reasoning_model(application):
    prompt = f"""
    Determine loan eligibility for this application:
    {application}

    Consider all relevant factors and show your reasoning.
    """

    # Model internally generates reasoning steps
    return reasoning_model.analyze(prompt)
The reasoning model's API call might cost 3x more per token. But that higher price reflects the cognitive labor it's saving you. When you calculate total cost of ownership, include:

Developer time creating complex prompts
Maintenance as requirements change
Debugging when edge cases fail
Quality assurance testing
For reliable complex tasks, a reasoning model is often cheaper in the long run.





Hello again. Last time we look at the broad landscape of what LLMs can do. Today, we can get to the heart of the matter. How do you choose the right ones? This is one of the most common places where projects go wrong. It's tempting to just look at a public leaderboard and pick the model at the top. But that's a technology first approach. The selection of an LLM is a business decision, not just a technical one. The best framework begins by forgetting about the models and focusing entirely on the problem you need to solve. The first and most important step is to deconstruct your business problem into the specific AI cognition it requires. Once you do that, you'll find that LLM landscape is divided into two classes of models. On one side, you have general purpose or generation models. Think of models like Open AI, GPT 4.0 or Atropx Cloud sonnet. Their architecture is optimized for fluency, creativity, and conversation. They excel at task like writing marketing copy, powering advanced chat bots or summarizing documents where the style and flow are important. On the other side, you have reasoning models. These are specialized tools like Open AI's all series models, or Google's Gemini 2.5 Pro. They are specifically trained to perform multi step logical problem solving. They have a distinct internal process, often called a chain of thought, where they break a complex problem into intermediate steps before giving a final answer. This makes them far superior for tasks like complex co generation, data analysis, or planning across multiple steps. Now, here is the crucial trade off. You can force a generation model to solve a logical problem. But you, the developer, have to do the heavy lifting. You have to write a very complex prompt that provides cognitive scaffolding. Manually walking the model through the steps. A reasoning model automates this process. It generates its own internal thinking tokens to figure out the steps. This has a direct economic consequence. The reasoning models API call might be more expensive. But that higher price reflects a cognitive labor it's saving you. When you calculate the total cost of ownership, you must include the significant developer time spent creating and maintaining complex proms for a less suited model. For a reliable complex task, a reasoning model is often cheaper in the long run. Once you have chosen a class of models, how do you evaluate them? We need to move beyond the simple accuracy. A truly robust evaluation is holistic. The helm framework from Standford give us a great model for this. It assesses models across seven metrics. Accuracy, Calibration, does the model confidence match its correctness? Robotness, how does it handle typos, fairness, bias, toxicity, and efficiency? For any application with a user, speed is just as important as quality. We measure this in two key ways. Time to first token, TTFT is the time until the first war of the response appears. This is the key metric for perceived responsiveness. For a chat bot or a code completion tool, a low TTFT is what makes the system feel instant. Total latency is the time until the entire respond is finished. This is more important for a synchroneous task like summarizing a document where the user is waiting for the complete output. The biggest mistake is relying on public benchmarks alone. A model can be great a general knowledge, but fail on the specific language of your business. The most critical step is to create your own customer evaluation set, a gold standard data set of real world examples from your own operations. Test the models against the problems you actually need to solve.