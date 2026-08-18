Let's build up a sophisticated prompt system using proven patterns. We'll start simple and progressively add structure.

Pattern 1: Strictly Grounded Generation
This is your foundation—the pattern that prevents hallucination by forcing the model to stay faithful to provided context.

Weak version (what most developers write):

Context: {retrieved_documents}

Question: {user_question}

Answer the question based on the context provided.
This is far too vague. "Based on" could mean anything. The model might interpret this as "use the context as inspiration" or "supplement the context with your knowledge."

Strong version (explicit and restrictive):

You are answering questions using ONLY information from the provided documents.

CRITICAL RULES:
1. Every fact in your answer MUST come directly from the documents below
2. If the documents don't contain enough information to answer the question, you MUST say so
3. DO NOT use any knowledge from your training data
4. DO NOT make inferences beyond what is explicitly stated
5. DO NOT fill in gaps with plausible-sounding information

DOCUMENTS:
{retrieved_documents}

QUESTION:
{user_question}

Provide your answer following the rules above.
Let's see how this changes output:

Query: "How many employees does the company have?"

Context: "The company operates in 15 countries. Our headquarters is located in Seattle. We recently expanded our engineering team."

Weak prompt output: "Based on the company's presence in 15 countries and recent engineering expansion, they likely employ several thousand people, probably in the range of 3,000-5,000 employees."

This is pure hallucination. The model invented a plausible number based on the clues about size.

Strong prompt output: "Based on the provided documents, I cannot determine the exact number of employees. The documents mention the company operates in 15 countries and recently expanded the engineering team, but no specific employee count is stated."

This is faithful to the context and acknowledges the limitation.

Pattern 2: Expert Persona Assignment
The language model can adjust its vocabulary, reasoning style, and depth based on who you tell it to be. This is especially powerful for domain-specific RAG systems.

You are a senior financial analyst with 15 years of experience in equity research. You specialize in analyzing technology companies and providing investment recommendations.

Your communication style is:
- Precise and quantitative, citing specific numbers and metrics
- Balanced, acknowledging both risks and opportunities
- Professional but accessible, avoiding unnecessary jargon
- Structured, organizing analysis into clear categories

When answering questions, you:
- Focus on material information that would affect investment decisions
- Provide numerical context (growth rates, margins, comparisons)
- Distinguish between facts, company guidance, and your analysis
- Flag uncertainties and information gaps

DOCUMENTS:
{retrieved_documents}

QUESTION:
{user_question}

Provide your analysis in your capacity as a financial analyst.
This persona guides the model toward the right style and focus for financial analysis use cases.

Query: "How is the company performing?"

Without persona: "The company is doing well. Revenue increased and they launched new products."

With financial analyst persona: "Financial performance shows mixed signals. Q3 revenue of $45M represents 12% YoY growth, but this is a deceleration from Q2's 18% growth. Gross margin improved 200 bps to 64%, suggesting better unit economics or product mix. However, the documents don't provide sufficient detail on customer acquisition costs or churn rates to fully assess unit economics."

The persona drives more relevant analysis.

Pattern 3: Structured Output Formatting
If your RAG system feeds downstream applications, you need consistent, parseable output. Instruct the model to follow a specific format.

You must format your response as valid JSON matching this structure:

{
  "direct_answer": "A concise 1-2 sentence answer to the question",
  "supporting_evidence": [
    {
      "claim": "A specific claim made in your answer",
      "source": "Direct quote from documents that supports this claim",
      "document_id": "Identifier of the source document"
    }
  ],
  "confidence": "HIGH/MEDIUM/LOW based on how completely the documents answer the question",
  "gaps": ["List of specific information not found in documents that would improve the answer"]
}

DOCUMENTS:
{retrieved_documents}

QUESTION:
{user_question}

Respond only with valid JSON matching the structure above.
This produces machine-readable output:

{
  "direct_answer": "Business checking accounts require two forms of government-issued ID, proof of business registration, and a $100 minimum opening deposit.",
  "supporting_evidence": [
    {
      "claim": "Requires two forms of government-issued ID",
      "source": "To open a business checking account, provide two forms of government-issued identification",
      "document_id": "account_requirements_2024"
    },
    {
      "claim": "Proof of business registration required",
      "source": "You must present proof of business registration in your state",
      "document_id": "account_requirements_2024"
    },
    {
      "claim": "$100 minimum opening deposit",
      "source": "Initial deposit of $100 minimum is required at account opening",
      "document_id": "account_requirements_2024"
    }
  ],
  "confidence": "HIGH",
  "gaps": []
}
This structured format makes it easy to:

Display answers with inline citations in your UI
Log evidence for audit purposes
Filter answers by confidence level
Track which documents contribute to answers
Pattern 4: Chain-of-Thought for Complex Questions
For questions requiring multi-step reasoning, instruct the model to show its work:

Answer the question by thinking through it step-by-step:

1. UNDERSTAND: Restate the question in your own words to confirm understanding
2. GATHER: Identify which document excerpts are relevant
3. ANALYZE: Explain how these excerpts relate to answering the question
4. SYNTHESIZE: Combine the information into a coherent answer
5. VERIFY: Check that your answer is fully supported by the documents

Show each step of your reasoning before providing the final answer.

DOCUMENTS:
{retrieved_documents}

QUESTION:
{user_question}
Query: "Is the company profitable and growing?"

Output with chain-of-thought:

1. UNDERSTAND:
The question asks two distinct things: current profitability status and whether growth is occurring.

2. GATHER:
- Document A states: "Q3 2024 revenue reached $45M, up from $40M in Q3 2023"
- Document B states: "The company reported a net loss of $3M in Q3 2024"
- Document C states: "Operating expenses decreased 8% year-over-year"

3. ANALYZE:
Revenue growth: $45M vs $40M = 12.5% YoY growth, indicating positive growth
Profitability: Net loss of $3M indicates the company is not currently profitable
Expense trend: 8% reduction in operating expenses suggests improving efficiency

4. SYNTHESIZE:
The company is growing (positive revenue growth) but not yet profitable (net loss), though the situation may be improving given expense reductions.

5. VERIFY:
All claims tie back to specific statements in the provided documents.

FINAL ANSWER:
The company is experiencing growth with 12.5% year-over-year revenue increase to $45M in Q3 2024, but is not currently profitable, posting a $3M net loss in the same quarter. However, operating expenses declined 8% year-over-year, suggesting a path toward profitability.
This reasoning transparency helps you debug failures and builds user trust.

Handling Real-World Complexity: Edge Cases and Conflicts
The clean examples above work well when retrieval is perfect and documents are consistent. Real systems face messier situations.

Conflicting Information
Documents contradict each other constantly—policy updates, different regional rules, conflicting data from different time periods.

Poor handling (what most systems do): The model picks one version as "correct" or tries to average conflicting information, producing a nonsensical answer.

Proper handling (explicit instruction):

If you encounter conflicting information in the documents:

1. DO NOT choose which source is correct
2. DO NOT blend contradictory information
3. INSTEAD, clearly state that sources conflict:
   "The documents contain conflicting information on this point:
   - Source A states: [exact quote]
   - Source B states: [exact quote]
   Both are provided as documented facts; clarification is needed."

DOCUMENTS:
{retrieved_documents}

QUESTION:
{user_question}
Example:

Documents:

Doc 1: "Free shipping on orders over $50"
Doc 2: "Free shipping on orders over $75"
Output: "The documents contain conflicting information about the free shipping threshold:

One document states: 'Free shipping on orders over $50'
Another document states: 'Free shipping on orders over $75'
This may reflect different promotions, regions, or time periods. I recommend verifying which threshold currently applies to your situation."

This honesty builds trust far more than a made-up compromise.

Insufficient Information
When documents partially answer a question but miss key details:

When the provided documents don't fully answer the question:

1. Provide whatever information IS available from the documents
2. Explicitly state what information is MISSING
3. DO NOT fill gaps with plausible assumptions

Use this format:

BASED ON PROVIDED DOCUMENTS:
[What you can answer from the documents]

INFORMATION NOT FOUND IN DOCUMENTS:
[Specific details needed but missing]

DOCUMENTS:
{retrieved_documents}

QUESTION:
{user_question}
Query: "What are the eligibility requirements and costs for the premium membership?"

Documents: Only contain eligibility requirements, no pricing information

Output:

BASED ON PROVIDED DOCUMENTS:
Premium membership eligibility requires:
- Active account for at least 6 months
- Minimum of 10 transactions in the past year
- Good standing with no policy violations

INFORMATION NOT FOUND IN DOCUMENTS:
- Membership cost or pricing structure
- Payment frequency (monthly/annual)
- Whether there are setup or cancellation fees
This transparency is invaluable. Users know what they can trust and what they need to verify elsewhere.




