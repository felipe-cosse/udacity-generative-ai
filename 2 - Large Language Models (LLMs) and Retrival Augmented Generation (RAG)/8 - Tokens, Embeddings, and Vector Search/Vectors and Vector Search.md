You know that embeddings transform text into high-dimensional vectors that capture semantic meaning. You know that similar concepts have similar vector representations - "cat" and "kitten" are close together in vector space, while "cat" and "pizza" are far apart.

But here's the question that makes everything practical: How do you actually use this to find relevant information? If you have a database with millions of document embeddings, how do you quickly find the ones most similar to a user's query?

This is where vector search (also called semantic search or similarity search) comes in. It's the technology that powers:

Search engines that understand what you mean, not just what you type
Recommendation systems that find products you'll love
RAG systems that retrieve the most relevant context for LLM prompts
Duplicate detection systems that find similar content
Content moderation that identifies similar violations

What Is a Vector?
Embeddings are vectors. A vector is simply a list of numbers with geometric properties. You can think of it as coordinates in space:

# 2D vector (point on a plane)
vector_2d = [3, 4]

# 3D vector (point in space)
vector_3d = [3, 4, 5]

# Word embedding (point in 1536-dimensional space)
word_embedding = [0.234, -0.891, 0.445, ..., 0.672]
Vector Operations You Need to Know
Distance (How far apart are two concepts?)
Similarity (How alike are two concepts?)
Addition/Subtraction (Combining or removing concepts)
Finding Needles in Vector Haystacks
Imagine you're building a customer support system with 100,000 help articles, each converted to a 1536-dimensional embedding vector. A customer asks: "How do I reset my password?"

The naive approach:

# Convert question to embedding
query_vector = embed("How do I reset my password?")

# Compare against ALL 100,000 article embeddings
similarities = []
for article_embedding in all_article_embeddings:
    similarity = cosine_similarity(query_vector, article_embedding)
    similarities.append(similarity)

# Find highest similarity
best_match_index = similarities.index(max(similarities))
This works, but it's slow. Calculating 100,000 similarity scores takes time. With millions of documents, it becomes impractical. We need something faster.

Cosine Similarity: The Industry Standard
Cosine similarity measures the angle between two vectors, regardless of their magnitude. It's the most common metric for text embeddings. Text embeddings are normalized (magnitude = 1), so cosine similarity simplifies to just the dot product:

# For normalized vectors
cosine_similarity(vec1, vec2) = dot_product(vec1, vec2)
This is why many vector databases use dot product.

Euclidean Distance: Straight-Line Distance
Euclidean distance measures the straight-line distance between vectors in space.

def euclidean_distance(vec1, vec2):
    """
    Calculate Euclidean distance.
    Returns value >= 0:
    - 0: Identical vectors
    - Larger values: More different
    """
    return np.sqrt(np.sum((vec1 - vec2) ** 2))

# Example
vec1 = np.array([1, 2, 3])
vec2 = np.array([4, 5, 6])

distance = euclidean_distance(vec1, vec2)
print(f"Distance: {distance}")
# Output: 5.196 (they're moderately far apart)
When to use Euclidean distance:

Image embeddings (where magnitude matters)
Geographic coordinates
Feature vectors with meaningful magnitudes
When NOT to use it:

Text embeddings (magnitude is arbitrary)
When you care about direction, not distance
Dot Product: Fast Similarity for Normalized Vectors
For normalized vectors, dot product equals cosine similarity but computes faster:

def dot_product_similarity(vec1, vec2):
    """
    Fast similarity for normalized vectors.
    Equivalent to cosine similarity when vectors are normalized.
    """
    return np.dot(vec1, vec2)
Many vector databases use this internally

Approximate Nearest Neighbors (ANN): Trading Accuracy for Speed
You don't always need the absolute best matches**. If the top result has 0.95 similarity and you find one with 0.94 instead, users won't notice.

Approximate Nearest Neighbor (ANN) algorithms trade a small amount of accuracy for massive speed improvements:

Brute force: O(n) - guaranteed perfect results
ANN: O(log n) or O(1) - ~95-99% accuracy, 10-1000x faster
HNSW: The Algorithm Behind Modern Vector Search
Hierarchical Navigable Small World (HNSW) is the most popular ANN algorithm.

Imagine you're trying to find a specific house in a city:

Bad approach (brute force):

Visit every house and check the address
O(n) time - scales linearly
Smart approach (like HNSW):

Start at a major highway intersection (top layer)
Take highway to nearest major road (middle layer)
Take major road to nearest street (bottom layer)
Walk down street to exact house (final layer)
O(log n) time - scales logarithmically
HNSW builds a similar multi-layer navigation structure for vectors.

Search process:

Start at top layer, jump to roughly the right area
Descend to next layer, refine your position
Continue until bottom layer
Do final local search for exact matches

Resources
Vector Search Algorithms
"Efficient and Robust Approximate Nearest Neighbor Search Using HNSW" (Malkov & Yashunin, 2018)
ArXiv: https://arxiv.org/abs/1603.09320(opens in a new tab)
"Billion-scale similarity search with GPUs" (Johnson et al., 2017)
ArXiv: https://arxiv.org/abs/1702.08734(opens in a new tab)
Libraries and Tools
hnswlib - Fast HNSW implementation
https://github.com/nmslib/hnswlib(opens in a new tab)
FAISS - Facebook AI Similarity Search
https://github.com/facebookresearch/faiss(opens in a new tab)
Annoy - Approximate Nearest Neighbors (Spotify)
https://github.com/spotify/annoy(opens in a new tab)
Vector Databases
Pinecone Documentation
https://docs.pinecone.io/(opens in a new tab)
Weaviate Vector Search
https://weaviate.io/developers/weaviate/search(opens in a new tab)
Milvus Vector Database
https://milvus.io/docs(opens in a new tab)
Qdrant Documentation
https://qdrant.tech/documentation/(opens in a new tab)
Practical Guides
"Vector Search at Scale" - Pinecone Learning Center
https://www.pinecone.io/learn/(opens in a new tab)
"Building Production Vector Search" - Weaviate Blog
https://weaviate.io/blog(opens in a new tab)
"Optimizing Vector Search Performance" - Qdrant Blog
https://qdrant.tech/articles/(opens in a new tab)






In this video, we'll walk through the basics of vector search, we'll learn how to compute the distance between vectors and how to use those distance functions to find similar items. When we say embedding or vector, we mean a list of floating point numbers. Anything from text to images, to videos can be turned into such a vector. The length of the vector is called the number of dimensions this vector has. It's important to note that all vectors within a vector column must have the same number of dimensions. Now, for vector search, the query vector must also have the same number of dimensions as the database vectors. For example, Open AI texts embeddings have 15, 36 dimensions, and many Bert base embeddings have 768 dimensions. We can think of each vector as a point in a high-dimensional space. Which means that retrieving relevant information can be thought of as finding points that are closest to the query. One way to define the distance between two points is the straight line or Euclidean distance. This is the definition of distance that we're familiar with from geometry class. In two-dimensions, this is the square root of (y2-y1)^2+(x2-x1)^2. Generalized across arbitrary dimensions is the formula that you see on the right. As a simple example, suppose we have two two-dimensional vectors, 2, 1 and 5, 5. To compute the Euclidean distance between them, we compute (5-1)^2 and add it to (5-2)^2, then we take the square root of the sum, which gives us five. Now that we have a way to compute the distance between two points, we will apply it repeatedly to find vectors closest to the query vector. This is commonly referred to as K-nearest neighbors or KNN. Here, k refers to the number of results that are returned. For example, suppose we wanted the three closest points to the query cat. We would compute the distance between cat and each vector in the data set. Then we return the three closest vectors, which happens to be the three vectors in purple, Euclidean distance is not the only way to compute the distance between two vectors. Another just as popular method is called the cosine distance. If we remember, the Euclidean distance measures the straight line distance between two points. The cosine distance measures the angular distance instead, the formula that you see on the right computes the cosine of the angle between two vectors, which is defined as the dot product divided by the length of each vector. This is also called cosine similarity. The cosine distance is then just one minus that cosine similarity. The two distance functions can give different results. For example, it's easy to see that cup is closer to cat than bicycle by straight line distance. But if we're looking at angular distance, bicycle is closer to cat instead.In this video, we discussed how we can think of vectors visually as points in a high-dimensional vector space. From text to images to audio, we can represent anything as an embedding vector. We saw how we can compute the distance between vectors using either straight line or angular distance. Using these distance metrics, we can use a technique called K-nearest neighbors to retrieve information that's most relevant to the user query. These concepts are at the very core of vector databases.