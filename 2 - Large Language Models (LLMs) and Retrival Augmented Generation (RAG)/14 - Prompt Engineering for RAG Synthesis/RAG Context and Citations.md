The Citation Imperative: Enforcing Verifiability
In any serious application, an answer without a source is worthless. Users need to verify claims, and you need to audit your system's behavior.

Basic Citation Pattern
MANDATORY REQUIREMENT:
For every factual claim in your answer, provide an inline citation in the format [DOC_ID: excerpt].

CITATION RULES:
1. Every sentence containing a fact MUST include at least one citation
2. Citations should be the exact phrase from the source that supports your claim
3. If you make a claim you cannot cite to a provided document, DO NOT make that claim

Example format:
"The policy requires 30 days notice [DOC_5: 'Termination requires written notice 30 days in advance']."

DOCUMENTS:
{retrieved_documents_with_ids}

QUESTION:
{user_question}

Answer with inline citations.
Query: "What is the company's return policy?"

Output: "Products can be returned within 30 days of purchase [DOC_3: 'Returns accepted within 30 days of purchase date'] for a full refund [DOC_3: 'Full refund issued for returns within 30 days'], provided they are in original packaging [DOC_7: 'Items must be in original packaging for refund eligibility']. Electronics and software have special restrictions [DOC_3: 'Electronics and software subject to additional return restrictions']."

This citation requirement creates a self-enforcing mechanism against hallucination. If the model can't find a source for a potential claim, it cannot generate that claim without violating its core instruction.

Advanced Citation with Confidence
For each claim, provide both a citation and a confidence indicator:

[DIRECT] = The document explicitly states this fact
[INFERRED] = This is a reasonable inference from the documents
[UNCERTAIN] = The documents hint at this but aren't fully clear

Example:
"The service costs $49 per month [DIRECT: DOC_2 'monthly subscription: $49'] and includes 24/7 support [INFERRED: DOC_5 mentions 'around-the-clock availability' which suggests 24/7]."

DOCUMENTS:
{retrieved_documents_with_ids}

QUESTION:
{user_question}
This nuance helps users calibrate their trust appropriately.

Domain-Specific Prompt Patterns
Different applications need different emphasis. Here are proven patterns for common RAG use cases.

Legal Document Analysis
You are a legal research assistant analyzing contract documents.

IMPORTANT LEGAL STANDARDS:
1. Distinguish between binding terms and general statements
2. Pay attention to definitions sections that may alter plain meaning
3. Note qualifications, exceptions, and conditional language
4. Flag ambiguous language that could be interpreted multiple ways
5. Never provide legal advice—only summarize what the documents state

When analyzing contracts:
- Use exact quotes for binding language
- Note defined terms in [brackets]
- Identify operative language (shall, must, may, etc.)
- Flag missing standard clauses

DOCUMENTS:
{retrieved_documents}

QUESTION:
{user_question}

Provide your analysis following these legal research standards.
Medical Information Retrieval
You are a medical information specialist helping healthcare providers find relevant clinical information.

CRITICAL SAFETY RULES:
1. Always note the date and source of medical information
2. Distinguish between research findings, clinical guidelines, and case reports
3. Highlight any contraindications or safety warnings prominently
4. Never extrapolate beyond the specific population studied
5. Always recommend consulting updated clinical guidelines for treatment decisions

Use this output structure:
FINDING: [What the research shows]
POPULATION: [Who was studied]
LEVEL OF EVIDENCE: [Study type]
LIMITATIONS: [Important caveats]
DATE: [When this information was published]

DOCUMENTS:
{retrieved_documents}

QUESTION:
{user_question}
Customer Support
You are a friendly and knowledgeable customer support specialist.

YOUR APPROACH:
1. Address the customer's concern directly and empathetically
2. Provide clear, actionable steps when applicable
3. Be honest about limitations or when escalation is needed
4. Use simple language—avoid technical jargon unless the customer uses it first
5. End with a clear next step or confirmation

TONE GUIDELINES:
- Professional but warm
- Patient and non-judgmental
- Concise—respect their time
- Proactive—anticipate follow-up questions

DOCUMENTS:
{retrieved_documents}

CUSTOMER QUESTION:
{user_question}

Provide your response following these customer support standards.
Technical Documentation
You are a technical documentation specialist helping developers use an API.

TECHNICAL COMMUNICATION STANDARDS:
1. Be precise with terminology—use exact parameter names, types, and values
2. Include code examples when relevant
3. Specify prerequisites and dependencies
4. Note version-specific behavior
5. Explain not just WHAT but WHY when it aids understanding

Output structure:
BRIEF ANSWER: [One-sentence summary]
DETAILS: [Fuller explanation]
EXAMPLE: [Code snippet if applicable]
GOTCHAS: [Common pitfalls or confusing aspects]
RELATED: [Other relevant documentation]

DOCUMENTS:
{retrieved_documents}

DEVELOPER QUESTION:
{user_question}
Advanced Technique: Prompt Compression and Context Management
As conversations grow longer or questions require more context, you hit token limits. Here are strategies for managing context efficiently.

Document Relevance Filtering
Before even sending documents to your prompt, use the language model to filter:

def filter_relevant_chunks(query, retrieved_chunks, max_chunks=5):
    """Use LLM to identify most relevant chunks before generating answer"""

    filter_prompt = f"""
    Analyze these document chunks and identify the {max_chunks} most relevant
    to answering this question: "{query}"

    Rank by relevance and return ONLY the document IDs in order.

    CHUNKS:
    {format_chunks_with_ids(retrieved_chunks)}

    Return as comma-separated list: DOC_1,DOC_5,DOC_3
    """

    relevant_ids = llm.generate(filter_prompt, temperature=0)
    return [c for c in retrieved_chunks if c.id in relevant_ids.split(',')]
This two-stage approach lets you retrieve broadly but generate narrowly, staying within token limits while maintaining high recall.

Hierarchical Summarization
For very long documents, use a hierarchy:

def get_relevant_context(query, long_document):
    """Break long document into sections, summarize, then drill down"""

    # Stage 1: Summarize each section
    section_summaries = []
    for section in long_document.sections:
        summary = llm.generate(
            f"Summarize this section in 2-3 sentences:\n{section.text}",
            temperature=0
        )
        section_summaries.append({
            'id': section.id,
            'summary': summary,
            'full_text': section.text
        })

    # Stage 2: Identify relevant sections
    relevance_prompt = f"""
    Which sections are relevant to this question: "{query}"

    SECTION SUMMARIES:
    {format_summaries(section_summaries)}

    Return relevant section IDs.
    """

    relevant_ids = llm.generate(relevance_prompt, temperature=0)

    # Stage 3: Return full text of only relevant sections
    return [s['full_text'] for s in section_summaries if s['id'] in relevant_ids]
Testing and Iteration: Making Your Prompts Better
Prompt engineering is experimental. You need systematic testing to know what works.

A/B Testing Framework
class PromptABTest:
    def __init__(self, test_questions, ground_truth_answers):
        self.test_questions = test_questions
        self.ground_truth = ground_truth_answers

    def compare_prompts(self, prompt_a, prompt_b):
        """Run both prompts on test set and compare results"""

        results_a = []
        results_b = []

        for question, truth in zip(self.test_questions, self.ground_truth):
            # Test prompt A
            response_a = rag_system.generate(
                question,
                prompt_template=prompt_a
            )
            results_a.append({
                'question': question,
                'answer': response_a,
                'faithfulness': self.score_faithfulness(response_a, truth),
                'relevance': self.score_relevance(response_a, question)
            })

            # Test prompt B
            response_b = rag_system.generate(
                question,
                prompt_template=prompt_b
            )
            results_b.append({
                'question': question,
                'answer': response_b,
                'faithfulness': self.score_faithfulness(response_b, truth),
                'relevance': self.score_relevance(response_b, question)
            })

        # Compare aggregate scores
        print(f"Prompt A - Avg Faithfulness: {np.mean([r['faithfulness'] for r in results_a]):.3f}")
        print(f"Prompt B - Avg Faithfulness: {np.mean([r['faithfulness'] for r in results_b]):.3f}")
        print(f"Prompt A - Avg Relevance: {np.mean([r['relevance'] for r in results_a]):.3f}")
        print(f"Prompt B - Avg Relevance: {np.mean([r['relevance'] for r in results_b]):.3f}")

        return results_a, results_b
Prompt Version Control
# prompts/v1_basic.txt
PROMPT_V1 = """
Context: {context}
Question: {question}
Answer:
"""

# prompts/v2_grounded.txt
PROMPT_V2 = """
Using ONLY the information in the documents below, answer the question.
If the documents don't contain the answer, say so.

Documents:
{context}

Question: {question}

Answer:
"""

# prompts/v3_cited.txt
PROMPT_V3 = """
Using ONLY the information in the documents below, answer the question.
Cite your sources using [DOC_ID: excerpt] format after each claim.

Documents:
{context}

Question: {question}

Answer with inline citations:
"""

# Track performance over versions
version_performance = {
    'v1': {'faithfulness': 0.65, 'relevance': 0.78},
    'v2': {'faithfulness': 0.82, 'relevance': 0.80},
    'v3': {'faithfulness': 0.91, 'relevance': 0.82}
}
Version control for prompts is as important as for code.

Complete RAG Prompt Template
Putting it all together, here's a production-ready prompt template:

# ROLE AND CONTEXT
You are a {domain_expert_persona} helping users find accurate information.
You have access to a curated set of documents relevant to the user's question.

# CORE PRINCIPLES
1. ACCURACY: Every claim must be supported by the provided documents
2. TRANSPARENCY: Acknowledge gaps, conflicts, and limitations in the documents
3. RELEVANCE: Answer what was asked, not what you think should be asked
4. VERIFIABILITY: Provide citations for all factual claims

# RESPONSE REQUIREMENTS

## Citations
Format: [DOC_{id}: "{exact_quote}"]
Example: "Returns are accepted within 30 days [DOC_3: 'all returns must be initiated within 30 days of purchase']."

## Conflicts
If documents contradict each other:
"The documents contain conflicting information:
- Source A states: {quote_a}
- Source B states: {quote_b}
Please verify which applies to your situation."

## Insufficient Information
If documents only partially answer the question:
"Based on the provided documents:
{what_you_can_answer}

The following information was not found in the documents:
{what_is_missing}"

## Prohibitions
- DO NOT use information from your training data
- DO NOT make assumptions to fill gaps
- DO NOT blend conflicting information into a compromise

# SOURCE DOCUMENTS
{retrieved_documents_with_ids}

# USER QUESTION
{user_question}

# YOUR RESPONSE
Provide your answer following all requirements above:
Real-World Example: Customer Support RAG
Let's walk through a complete example showing how prompting transforms results.

Scenario: Customer service chatbot for a bank

User Question: "How do I dispute a charge on my credit card?"

Retrieved Documents:

"To dispute a transaction, call 1-800-555-0123 or use the mobile app."
"Disputes must be filed within 60 days of the transaction date."
"You'll need the transaction date, amount, and merchant name."
"Fraudulent charges are covered by our zero liability policy."
Basic Prompt Result (no special instructions): "You can dispute charges by calling customer service or using the app. Make sure to do it within 60 days and have the transaction details ready. Don't worry, you won't be liable for fraud."

This is okay but informal, lacks specificity, and doesn't cite sources.

Production Prompt Result (with our template): "To dispute a charge on your credit card, you have two options [DOC_1: 'call 1-800-555-0123 or use the mobile app'].

Important requirements:

File your dispute within 60 days of the transaction date [DOC_2: 'Disputes must be filed within 60 days of the transaction date']
Have ready: transaction date, amount, and merchant name [DOC_3: 'You'll need the transaction date, amount, and merchant name']
If the charge is fraudulent, you're protected by our zero liability policy [DOC_4: 'Fraudulent charges are covered by our zero liability policy'].

What specific transaction would you like to dispute? I can help you gather the required information."

This response:

Provides actionable steps with specific details
Cites sources for verifiability
Organizes information clearly
Proactively offers next steps
Maintains professional tone
The prompt made all the difference.




