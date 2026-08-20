Evaluating the Generator: Faithfulness and Relevancy
Once your retriever delivers context, your generator must do two things: stay faithful to that context and actually answer the question. We measure these capabilities separately.

Faithfulness: The Hallucination Check
Faithfulness is your direct defense against hallucination. It asks: "Is every claim in the generated answer factually supported by the provided context?"

This is stricter than it sounds. A claim is faithful only if you can point to specific text in the retrieved documents that directly supports it. Paraphrasing is fine, but introducing new facts—even if they're generally true—counts as unfaithful.

Let's examine this with an example. You're building a historical information system about World War II. A user asks: "What happened at the D-Day invasion?"

Your retrieved context contains:

"The Allied invasion of Normandy began on June 6, 1944, involving forces from the United States, United Kingdom, and Canada."
"Approximately 156,000 troops landed on five beaches codenamed Utah, Omaha, Gold, Juno, and Sword."
"The operation was commanded by General Dwight D. Eisenhower."
Your generator produces: "The D-Day invasion occurred on June 6, 1944, when Allied forces including American, British, and Canadian troops landed on five Normandy beaches. Led by General Eisenhower, approximately 156,000 soldiers participated. The invasion marked the beginning of the end for Nazi Germany and led to their defeat within a year."

Let's evaluate faithfulness claim by claim:

"The D-Day invasion occurred on June 6, 1944" — FAITHFUL (directly stated in context)
"Allied forces including American, British, and Canadian troops" — FAITHFUL (paraphrase of context)
"landed on five Normandy beaches" — FAITHFUL (combines two pieces of context)
"Led by General Eisenhower" — FAITHFUL (directly stated)
"approximately 156,000 soldiers participated" — FAITHFUL (directly stated)
"marked the beginning of the end for Nazi Germany" — UNFAITHFUL (interpretation not in context)
"led to their defeat within a year" — UNFAITHFUL (historical fact not in provided context)
Faithfulness score = 5 faithful claims / 7 total claims = 0.71

Those last two claims might be historically accurate, but they weren't in the retrieved documents. The model pulled them from its training data, which means it's potentially unreliable. If it can add true facts that weren't in context, it can also add false facts.

A faithfulness score of 1.0 means the model made no unsupported claims. This is your gold standard for high-stakes applications where every fact must be verifiable.

Answer Relevancy: Actually Addressing the Question
An answer can be 100% faithful to context and still be useless. Answer relevancy measures whether the generated response actually addresses what the user asked.

Consider a customer service chatbot for a telecommunications company. A frustrated customer asks: "Why is my internet so slow this week?"

Your retriever finds relevant documents about network maintenance, typical connection speeds, and troubleshooting steps. Your generator produces:

"Internet speeds can vary based on several factors including network congestion, equipment age, and service plan limitations. Our standard residential plans offer download speeds between 50-300 Mbps depending on subscription tier. If you're experiencing connectivity issues, you can reset your modem by unplugging it for 30 seconds."

Let's evaluate this answer:

Is it faithful? Yes, every claim comes from the retrieved documents.
Does it answer the question? Not really.
The customer asked why their internet is slow this week—a specific timeframe suggesting a recent change. The answer provides general information about internet speeds and generic troubleshooting but doesn't address the specific timing of the issue.

A relevant answer might have been: "Our records show scheduled network maintenance in your area from March 10-15, which may be affecting speeds. Additionally, we're currently experiencing higher than normal traffic during evening hours due to a popular streaming event."

This answer directly addresses the "this week" timeframe and provides specific reasons tied to the customer's situation.

Answer relevancy penalizes:

Incomplete answers: Only addressing part of a multi-part question
Tangential information: Including correct but unrequested details that distract from the core question
Generic responses: Providing boilerplate information when the question asked for something specific
For our customer service example:

Relevancy to the timeframe: LOW (doesn't address "this week")
Relevancy to the cause: MEDIUM (mentions factors but not specific recent causes)
Overall relevancy score: 0.4



