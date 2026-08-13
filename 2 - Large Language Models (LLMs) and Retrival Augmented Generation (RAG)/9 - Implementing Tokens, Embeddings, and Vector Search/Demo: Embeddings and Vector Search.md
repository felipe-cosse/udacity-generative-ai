In this demo, you'll explore embeddings and vector search:

Understand what embeddings are and how they numerically represent semantic meaning
Generate text embeddings using the OpenAI API
Calculate cosine similarity between embedding vectors
Interpret similarity scores and understand what they reveal about semantic relationships
Recognize practical applications of embeddings in real-world AI systems

What Are Embeddings?
Embeddings are dense numerical representations of text that capture semantic meaning in high-dimensional space.

Vector Dimensions and Meaning
Each dimension in an embedding vector captures some aspect of meaning.

Cosine Similarity: Measuring Semantic Distance
Cosine similarity quantifies how "close" two vectors are in meaning space.

The Formula (for understanding, not memorization):

cosine_similarity = (A · B) / (||A|| × ||B||)

Where:
- A · B = dot product of vectors A and B
- ||A|| = magnitude (length) of vector A
- ||B|| = magnitude (length) of vector B
def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    magnitude1 = np.linalg.norm(v1)
    magnitude2 = np.linalg.norm(v2)
    return dot_product / (magnitude1 * magnitude2)
Why Use Cosine (Not Euclidean Distance)?:

Cosine: Measures angle (direction) - good for meaning
Euclidean: Measures physical distance - good for coordinates
For semantics: Direction matters more than magnitude
Interpreting Similarity Scores
Similarity scores range from -1 to 1, and different ranges have practical meanings.

Score Interpretation Guide:

Score Range	Interpretation	Practical Meaning
0.95 to 1.0	Nearly identical	Duplicates, paraphrases, same topic
0.80 to 0.95	Very similar	Related articles, similar questions
0.60 to 0.80	Somewhat similar	Same domain, related concepts
0.40 to 0.60	Weakly similar	Loose connection, shared words
0.20 to 0.40	Barely similar	Few overlapping concepts
0.0 to 0.20	Unrelated	Different topics entirely
-0.20 to 0.0	Opposite contexts	Contrasting statements
-1.0 to -0.20	Contradictory	Direct opposites (rare in practice)
Step 7: Calculate Similarity (Similar Texts)
similarity_1_3 = cosine_similarity(embedding_1, embedding_3)
print(f"Similarity: {similarity_1_3:.2f}")  # Output: 0.74
Expected Result: ~0.74 (moderately high)

What This Means:

Same subject: "cat" (animal)
Same structure: "[Subject] is [color]"
Different content: blue vs. green (both colors, semantically close)
Score of 0.74: Captures the high structural similarity despite the color change
Key Insight: The model understands:

Both sentences describe a cat with unusual coloring
Blue and green are both colors (semantically related)
Sentence structure is identical
Overall meaning is similar (fantasy/hypothetical colored cat)
Step 8: Interpretation and Comparison
Summary Table:

Comparison	Text 1	Text 2	Similarity	Interpretation
Pair 1	"The cat is blue."	"The universe is very large."	0.15	Unrelated topics
Pair 2	"The cat is blue."	"The cat is green."	0.74	High similarity





Let's take a look at how we are able to generate embeddings using OpenAI, as well as how we are able to measure the distance between these two embeddings or vectors so that we are able to understand the similarities or difference in meaning. First, we're going to define a cosine similarity, which is one of our most popular ways of measuring the distance. In production, this is going to be part of the vector database. Next, we are going to define our OpenAI client. Now let's generate embedding for a very simple sentence, The cat is blue. After a couple of seconds, we can see that embedding is being generated and storing our variable embedding one. Now, an embedding on its own is meaningless. The value of it comes when we are able to compare it to a second embedding. In this case, we are going to generate embedding for the sentence, The universe is very large. As you can see, the meaning of these two sentences is very different. How does this compare in the distance? Well, let's take a look at this. We're able to see that the distance in our constant similarities coming very low close to zero at 0.15. This means that it is very different and there is no really a correlationship between these two sentences. Now, let's do another embedding for another sentence. The cat is green. This one has a much closer meaning to our first sentence. When we generate the embedding for this one and we calculate the distance, we're going to see that the distance is actually much higher at 0.74. When two embeddings are close to 1, that means that their meaning is very similar. When they are close to -1, that means that the meaning is extremely different, the opposite in that sense. But when the distance is close to zero, that means that the sentences have nothing in common.