This exercise teaches you how to build a semantic search system using embeddings for customer service applications. You'll learn how to convert text into numerical vectors that capture meaning, enabling search and automatic clustering of customer feedback.

Create embeddings for product reviews
Search for similar reviews semantically (meaning-based, not keyword-based)
Calculate similarity between any two reviews
Cluster feedback to identify common themes
Save and load embeddings for reuse
Understand the Data
The exercise includes 10 sample product reviews with metadata:

{
    "text": "The laptop arrived quickly and works great!...",
    "metadata": {
        "product": "laptop",
        "rating": 5,
        "date": "2024-01-15"
    }
}
Reviews cover:

Positive experiences (5-star ratings)
Negative experiences (1-2 star ratings)
Mixed experiences (3-4 star ratings)
Different topics: product quality, shipping, customer service
Task 1: Initialize the Embedding System
What to implement: Complete the __init__ method to set up the OpenAI client and storage.

Task 2: Create Embeddings
Complete the create_embedding() method to convert text into a vector.

Call the OpenAI embedding API
response = self.client.embeddings.create(
    model=self.model,
    input=text
)
Extract the embedding vector
embedding = response.data[0].embedding
Return the embedding
return embedding
Add error handling:

try:
    response = self.client.embeddings.create(...)
    embedding = response.data[0].embedding
    return embedding
except Exception as e:
    print(f"Error creating embedding: {e}")
    raise
Task 3: Embed Reviews with Metadata
What to implement: Complete embed_review() to create embeddings and store them with metadata. Metadata lets you filter results by product, rating, date, etc.

Create the embedding
embedding = self.create_embedding(review_text)
Create a dictionary with all information
review_entry = {
    "text": review_text,
    "embedding": embedding,
    "metadata": metadata
}
Store it in the embeddings_store
self.embeddings_store.append(review_entry)
Return the entry
return review_entry
Task 4: Batch Process Reviews
Complete embed_reviews() to process multiple reviews at once.

def embed_reviews(self, reviews: List[Dict]) -> List[Dict]:
    embedded_reviews = []

    for review in reviews:
        try:
            # Extract text and metadata
            text = review["text"]
            metadata = review["metadata"]

            # Embed the review
            embedded = self.embed_review(text, metadata)
            embedded_reviews.append(embedded)

        except Exception as e:
            print(f"Error embedding review: {e}")
            continue  # Skip failed reviews

    return embedded_reviews
Why try/except? In production, some reviews might fail (network issues, API errors). You don't want one failure to stop the entire batch.

Task 5: Calculate Cosine Similarity
What to implement: Complete calculate_similarity() to measure how similar two embeddings are. Cosine similarity measures the angle between two vectors:

1.0: Identical direction (very similar meaning)
0.0: Perpendicular (unrelated)
-1.0: Opposite direction (contradictory meaning)
For text, you'll typically see values between 0.5 and 1.0 for related content.

The formula:

similarity = dot(A, B) / (||A|| × ||B||)
Where:

dot(A, B) = sum of element-wise products
||A|| = magnitude (length) of vector A
Convert to numpy arrays
vec1 = np.array(embedding1)
vec2 = np.array(embedding2)
Calculate dot product
dot_product = np.dot(vec1, vec2)
Calculate vector norms (magnitudes)
norm1 = np.linalg.norm(vec1)
norm2 = np.linalg.norm(vec2)
Compute similarity
if norm1 == 0 or norm2 == 0:
    return 0.0  # Avoid division by zero

similarity = dot_product / (norm1 * norm2)
return float(similarity)
Task 6: Implement Semantic Search
Complete find_similar_reviews() to search for reviews semantically.

Create embedding for the query
query_embedding = self.create_embedding(query)
Calculate similarity with all stored reviews
results = []
for review in self.embeddings_store:
    similarity = self.calculate_similarity(
        query_embedding,
        review["embedding"]
    )

    # Only include if above threshold
    if similarity >= min_similarity:
        results.append((review, similarity))
Sort by similarity (highest first)
results.sort(key=lambda x: x[1], reverse=True)
Return top K results
return results[:top_k]
Complete implementation:

def find_similar_reviews(
    self,
    query: str,
    top_k: int = 5,
    min_similarity: float = 0.5
) -> List[Tuple[Dict, float]]:
    # Create query embedding
    query_embedding = self.create_embedding(query)

    # Calculate similarities
    results = []
    for review in self.embeddings_store:
        similarity = self.calculate_similarity(
            query_embedding,
            review["embedding"]
        )

        if similarity >= min_similarity:
            results.append((review, similarity))

    # Sort and return top K
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]
Task 7: Find Similar Reviews
Complete find_similar_to_review() to find reviews similar to a specific stored review. When a customer service agent is viewing a complaint, show them similar past issues and how they were resolved.

Implementation:

def find_similar_to_review(
    self,
    review_index: int,
    top_k: int = 5
) -> List[Tuple[Dict, float]]:
    # Get the reference review
    reference_review = self.embeddings_store[review_index]
    reference_embedding = reference_review["embedding"]

    # Calculate similarities
    results = []
    for i, review in enumerate(self.embeddings_store):
        if i == review_index:
            continue  # Skip the reference review itself

        similarity = self.calculate_similarity(
            reference_embedding,
            review["embedding"]
        )
        results.append((review, similarity))

    # Sort and return top K
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]
Task 8: Cluster Feedback (Advanced)
Complete cluster_feedback() to automatically group reviews by theme. With 10,000 reviews, you can't read them all. Clustering automatically identifies:

Cluster 1: Shipping/delivery issues
Cluster 2: Product quality problems
Cluster 3: Customer service complaints
Cluster 4: Positive experiences
Cluster 5: Pricing concerns
def cluster_feedback(
    self,
    num_clusters: int = 5,
    method: str = "kmeans"
) -> Dict[int, List[Dict]]:
    if len(self.embeddings_store) == 0:
        return {}

    # Extract all embeddings
    embeddings = np.array([r["embedding"] for r in self.embeddings_store])

    # Simple K-means implementation
    # 1. Randomly initialize centroids
    indices = np.random.choice(len(embeddings), num_clusters, replace=False)
    centroids = embeddings[indices]

    # 2. Assign each review to nearest centroid
    clusters = {i: [] for i in range(num_clusters)}

    for review in self.embeddings_store:
        emb = np.array(review["embedding"])

        # Find closest centroid
        distances = [
            1 - self.calculate_similarity(emb.tolist(), c.tolist())
            for c in centroids
        ]
        cluster_id = np.argmin(distances)
        clusters[cluster_id].append(review)

    return clusters
Task 9: Save and Load Embeddings
Complete save_embeddings() and load_embeddings() for persistence.

Why save embeddings? Creating embeddings costs money and time:

1,000 reviews × $0.00002 per embedding = $0.02
Time: ~10 seconds for 1,000 reviews
Save them once, reuse forever (until you get new reviews).

Save implementation:

def save_embeddings(self, filepath: str):
    try:
        with open(filepath, 'w') as f:
            json.dump(self.embeddings_store, f, indent=2)
        print(f"Saved {len(self.embeddings_store)} embeddings to {filepath}")
    except Exception as e:
        print(f"Error saving embeddings: {e}")
        raise
Load implementation:

def load_embeddings(self, filepath: str):
    try:
        with open(filepath, 'r') as f:
            self.embeddings_store = json.load(f)
        print(f"Loaded {len(self.embeddings_store)} embeddings from {filepath}")
    except Exception as e:
        print(f"Error loading embeddings: {e}")
        raise
Running the Exercise
After implementing all methods, uncomment the demo functions in main():

def main():
    # Uncomment these as you complete the implementation
    demonstrate_embedding_creation()
    demonstrate_similarity_search()
    demonstrate_similarity_calculation()
    demonstrate_clustering()
    demonstrate_practical_use_cases()
Run the complete exercise:

python review_embedding_system.py



