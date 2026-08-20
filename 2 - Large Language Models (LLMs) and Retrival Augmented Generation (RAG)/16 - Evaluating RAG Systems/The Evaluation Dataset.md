Before you can measure anything, you need a benchmark—a golden dataset that represents ground truth. This is not just a list of questions you hope your system can answer. A proper RAG evaluation dataset requires three components for every test case:

1. The Question
This is straightforward but still requires careful design. Your questions should reflect real user queries, not sanitized examples that happen to work well. If your system serves customer support, use actual support tickets. If it serves researchers, use genuine research questions from your domain.

For an e-commerce product database, a good test question might be: "Which wireless headphones under $150 have active noise cancellation and at least 20 hours of battery life?"

This question is specific, measurable, and represents a realistic user need.

2. The Ground Truth Answer
This is the ideal response your system should generate. It's not about matching exact wording—it's about capturing the factual content that should be present.

For our headphones question, the ground truth might be: "Based on current inventory, the Sony WH-CH720N ($149) offers active noise cancellation with up to 35 hours of battery life, and the Soundcore by Anker Life Q30 ($79) provides active noise cancellation with 40 hours of battery life. Both models meet the specified criteria."

Notice this answer is specific, cites actual products with prices, and includes measurable specifications that can be verified.

3. The Ideal Context
This is the most important part and the piece most teams skip. You need to identify which specific document chunks contain the information required to answer the question correctly.

For our headphones question, the ideal context might be:

Document ID: product_catalog_2024_03, Chunk 47 (Sony WH-CH720N specifications)
Document ID: product_catalog_2024_03, Chunk 89 (Soundcore Life Q30 specifications)
Document ID: pricing_updates_2024_03_15, Chunk 12 (Current pricing for both models)
These are the exact chunks your retriever should find. If it finds these chunks, you can fairly evaluate whether your generator uses them correctly. If it doesn't find these chunks, you know immediately that retrieval is the problem.

Building this dataset is labor-intensive. For a production system, you might need 100-500 test cases to get comprehensive coverage of your domain. But this investment pays dividends—it becomes your regression test suite, your debugging tool, and your proof of improvement over time.