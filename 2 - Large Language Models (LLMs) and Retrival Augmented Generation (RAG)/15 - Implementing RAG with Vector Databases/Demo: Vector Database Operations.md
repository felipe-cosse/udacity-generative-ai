This demo introduces ChromaDB, a powerful open-source vector database designed specifically for storing and querying embeddings. ChromaDB represents a critical infrastructure component in modern AI applications, enabling semantic search, RAG systems, and similarity-based retrieval. Unlike traditional databases that match exact keywords, vector databases like ChromaDB understand meaning and context, making them essential for building intelligent applications.

In this demonstration, you'll learn how to perform complete CRUD (Create, Read, Update, Delete) operations on a local vector database, understand how semantic search works under the hood, and discover why vector databases are revolutionizing how we build AI-powered applications.

Set up and configure ChromaDB for local development, understanding the difference between persistent and ephemeral storage modes
Create and manage collections (the vector database equivalent of tables) with appropriate configuration
Perform CRUD operations on vector embeddings, including adding documents, querying semantically, updating records, and deleting entries
Apply metadata filtering to combine semantic search with structured queries for more precise results
Understand auto-embedding functionality and how ChromaDB handles the embedding generation process transparently
Inspect collection contents to understand what data is stored and how it's organized within the vector database

What is ChromaDB?
ChromaDB is an open-source embedding database designed to make it easy to build AI applications with embeddings. Think of it as a specialized database that doesn't just store text—it stores the meaning of text as high-dimensional vectors.

Traditional Database Search:

Query: "Find records where title contains 'Python'"
Result: Exact text matches only
Limitation: Misses "coding in Python", "Pythonic programming", "snake programming language"
Vector Database Search (ChromaDB):

Query: "programming with Python"
Result: All semantically similar documents, regardless of exact wording
Advantage: Finds "Python tutorials", "learn to code in Python", "Python development guide"
The magic happens because ChromaDB converts your text into embeddings (numerical representations of meaning) and uses mathematical similarity (like cosine similarity) to find related content.

Collections: Your Vector Database Tables
In ChromaDB, a collection is analogous to a table in traditional databases. Each collection:

Stores a group of related documents and their embeddings
Has a unique name for identification
Contains documents, embeddings, metadata, and IDs
Can use different embedding functions (models) for different use cases
Why Collections Matter:

Imagine you're building a customer service AI. You might have:

product_documentation collection: Technical manuals and guides
customer_faqs collection: Common questions and answers
support_tickets collection: Historical customer issues and resolutions
Each collection can be searched independently, allowing you to control which knowledge base the AI accesses for different queries.

The CRUD Operations for Vector Databases
Vector databases support the same fundamental operations as traditional databases, but with semantic superpowers:

Create (Add): Add documents along with their embeddings and metadata
Read (Query): Search semantically to find similar documents
Update: Modify existing documents while preserving their unique identity
Delete: Remove documents from the collection
The key difference: your "Read" operations use semantic similarity instead of exact matching.

Auto-Embedding: The Invisible Helper
One of ChromaDB's most powerful features is auto-embedding. When you add documents to a collection, ChromaDB can automatically:

Generate embeddings for your text using a default model
Store both the original text and its embedding
Handle embedding generation transparently during queries
This means you can focus on your application logic without worrying about calling embedding APIs, managing API keys, or handling rate limits during development.

Default Embedding Model:

ChromaDB uses the all-MiniLM-L6-v2 sentence transformer model by default. This lightweight model:

Runs entirely on your local machine (no API calls)
Generates 384-dimensional embeddings
Works well for general-purpose semantic search
Is fast enough for development and moderate production loads
Metadata Filtering: Structured Meets Semantic
Metadata filtering combines the precision of traditional databases with the intelligence of vector search. You can attach structured data (tags, categories, dates, authors) to your documents and then search using both:

Semantic criteria: "Find documents about machine learning" AND structured criteria: "Only from the 'tutorial' category"

This hybrid approach gives you the best of both worlds—semantic understanding with structured precision.

Persistent vs Ephemeral Storage
ChromaDB offers two storage modes:

Ephemeral (in-memory):

client = chromadb.Client()  # Data lost when program ends
Fast for testing and experimentation
Data disappears when the program terminates
Good for prototyping and temporary operations
Persistent (disk-based):

client = chromadb.PersistentClient(path="./chroma_data")  # Data saved to disk
Data survives program restarts
Essential for production applications
Allows you to build and query the same database over time
Step-by-Step Demo Walkthrough
Step 1: Import ChromaDB and Initialize the Client
import chromadb
from chromadb.config import Settings

# Create a persistent client that saves data locally
client = chromadb.PersistentClient(path="./chroma_demo_db")
We're creating a ChromaDB client with persistent storage. The path parameter specifies where on your disk the vector database will be stored. This directory will contain:

The vector embeddings
The original documents
All metadata
Index structures for fast retrieval
Why persistent storage?

In this demo, we want our vector database to survive beyond the execution of the script. This mirrors real-world applications where you build your database once and query it many times.

Step 2: Create a Collection
# Create or get a collection named "demo_collection"
collection = client.get_or_create_collection(
    name="demo_collection",
    metadata={"description": "A collection for demonstration purposes"}
)
The get_or_create_collection method is idempotent—it creates the collection if it doesn't exist, or retrieves it if it already exists. This is a best practice pattern that makes your code safe to run multiple times.

Collection Naming:

Collection names should be:

Descriptive of their content
Unique within a ChromaDB instance
Lowercase with underscores (by convention)
Step 3: Prepare Sample Documents
# Define five sample documents
documents = [
    "Python is a versatile programming language widely used in data science.",
    "Machine learning models require large amounts of training data.",
    "Natural language processing helps computers understand human language.",
    "Cloud computing provides scalable resources for applications.",
    "Database systems store and retrieve structured data efficiently."
]

# Generate unique IDs for each document
ids = [f"doc_{i}" for i in range(len(documents))]

# Add metadata to categorize documents
metadatas = [
    {"category": "programming", "language": "Python"},
    {"category": "AI", "subcategory": "machine_learning"},
    {"category": "AI", "subcategory": "NLP"},
    {"category": "infrastructure", "type": "cloud"},
    {"category": "infrastructure", "type": "database"}
]
We're preparing three essential components:

Documents: The actual text content we want to store
IDs: Unique identifiers for each document (critical for updates and deletes)
Metadata: Structured tags that enable filtering and organization
Why unique IDs matter:

IDs serve as the primary key in your vector database. They must be:

Unique across the entire collection
Stable over time (don't change)
Meaningful enough for debugging (like doc_0 or product_123)
Metadata strategy:

Good metadata design enables powerful queries. Consider:

What categories make sense for your domain?
What filters will users want to apply?
What structured data enhances semantic search?
Step 4: Add Documents to the Collection
# Add documents with their IDs and metadata
collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas
)

print(f"Added {len(documents)} documents to the collection.")
Behind the scenes, ChromaDB is:

Taking each document text
Generating an embedding using the default model (all-MiniLM-L6-v2)
Storing the document text, embedding, ID, and metadata
Building index structures for fast retrieval
The Auto-Embedding Process:

You don't see any embedding code because ChromaDB handles it automatically. This is equivalent to:

# What ChromaDB does internally (conceptually)
for doc in documents:
    embedding = default_embedding_model.encode(doc)  # Generate embedding
    store(embedding, doc, id, metadata)  # Store everything together
Performance consideration:

Adding documents is typically fast because:

The default model runs locally (no network latency)
Batch operations are optimized
Index updates happen incrementally
Step 5: Query the Collection Semantically
# Query for documents related to "coding and software development"
results = collection.query(
    query_texts=["coding and software development"],
    n_results=2  # Return top 2 most similar documents
)

print("Query: 'coding and software development'")
print(f"Results: {results['documents']}")
ChromaDB performs several operations:

Embeds your query: Converts "coding and software development" to a 384-dimensional vector
Calculates similarity: Compares the query embedding against all document embeddings using cosine similarity
Ranks results: Orders documents by similarity score (highest first)
Returns top N: Gives you the most relevant results
The query "coding and software development" is semantically similar to:

"Python" (a programming language used for coding)
"Natural language processing" (involves programming and algorithms)
Even though neither result contains the exact words "coding" or "software development", the vector embeddings capture the semantic relationship.

Step 6: Query with Different Semantic Intent
# Query for documents related to "artificial intelligence and data"
results = collection.query(
    query_texts=["artificial intelligence and data"],
    n_results=2
)

print("Query: 'artificial intelligence and data'")
print(f"Results: {results['documents']}")
Expected Output:

Results: [
    "Machine learning models require large amounts of training data.",
    "Natural language processing helps computers understand human language."
]
This query demonstrates how semantic search understands domain relationships:

"artificial intelligence" → machine learning, NLP (subfields of AI)
"data" → training data (essential for ML)
Notice that "Natural language processing" appears in both queries' results, but for different reasons:

First query: NLP involves programming
Second query: NLP is a subfield of AI
This shows how vector embeddings capture multiple semantic relationships simultaneously.

Step 7: Apply Metadata Filtering
# Query with metadata filter for only "programming" category
results = collection.query(
    query_texts=["coding and software development"],
    n_results=2,
    where={"category": "programming"}  # Metadata filter
)

print("Query with filter (category='programming'):")
print(f"Results: {results['documents']}")
ChromaDB now performs a two-stage retrieval:

Filter stage: First, filter documents where category == "programming"
Semantic stage: Then, perform semantic search only within the filtered subset
Expected Output:

Results: [
    "Python is a versatile programming language widely used in data science."
]
Only one document in our collection has category: "programming", so even though we requested n_results=2, ChromaDB returns only the available matches.

Step 8: Inspect Collection Contents
# Get basic information about the collection
print(f"Collection name: {collection.name}")
print(f"Collection count: {collection.count()}")

# Peek at all stored data
all_data = collection.get()
print(f"All documents: {all_data['documents']}")
print(f"All metadata: {all_data['metadatas']}")
The get() method (without parameters) retrieves everything in the collection:

All document texts
All IDs
All metadata
All embeddings (if you request them)
Expected Output:

Collection name: demo_collection
Collection count: 5
All documents: ["Python is a versatile...", "Machine learning models...", ...]
All metadata: [{"category": "programming"...}, {"category": "AI"...}, ...]
Debugging tip:

Use collection.get() to:

Verify documents were added correctly
Inspect metadata structure
Debug why certain queries aren't returning expected results
Understand what data is actually stored
Step 9: Update a Document
# Update the first document with new content
collection.update(
    ids=["doc_0"],
    documents=["Python 3.12 is the latest version with improved performance and new features."],
    metadatas=[{"category": "programming", "language": "Python", "version": "3.12"}]
)

print("Updated doc_0")

# Verify the update
updated_doc = collection.get(ids=["doc_0"])
print(f"Updated document: {updated_doc['documents'][0]}")
print(f"Updated metadata: {updated_doc['metadatas'][0]}")
The update() method:

Locates the document by ID (doc_0)
Replaces the document text with new content
Regenerates the embedding (because the text changed)
Updates the metadata
Maintains the same ID (preserving references)
Expected Output:

Updated document: "Python 3.12 is the latest version with improved performance and new features."
Updated metadata: {"category": "programming", "language": "Python", "version": "3.12"}
When to update vs delete-and-add:

Use update() when:

The document's identity remains the same (same topic, updated version)
You want to preserve the ID for references
You're fixing errors or adding new information
Use delete-and-add when:

The document's meaning changes fundamentally
You want a new ID
You're replacing deprecated content with something entirely different
Step 10: Delete a Document
# Delete a document by ID
collection.delete(ids=["doc_4"])

print("Deleted doc_4")
print(f"Collection count after deletion: {collection.count()}")
The delete() method:

Locates the document by ID
Removes the document text
Removes the embedding
Removes all metadata
Updates indexes to reflect the deletion
Expected Output:

Deleted doc_4
Collection count after deletion: 4
Deletion is permanent:

Unlike some databases with soft deletes or trash bins, ChromaDB deletion is immediate and permanent. The document and its embedding are completely removed from the collection.

Batch deletion:

You can delete multiple documents at once:

collection.delete(ids=["doc_1", "doc_2", "doc_3"])
Or delete by metadata filter:

# Delete all documents in the "deprecated" category
collection.delete(where={"status": "deprecated"})






Let's jump into ChromaDB. Our vector database that we are able to utilize locally. For this demo, we are going to define our ChromaDB imports, then we're going to define our client with a path so that we can save the data locally. We are going to generate a collection. This is in other terms a table that we are able to use to store our embeddings. Now, we are going to define five sample documents. With these documents, we are going to generate unique ideas, as well as metadata and we are going to add all of that into our collection. Then we can actually query that collection and this is using a default embedding as part of the vector database or ChromaDB. For this demo, we are actually not utilizing OpenAI, but rather a default ChromaDB embedding model. As you can see, we're able to get the results for our query coding and software development. In this case, it is returning the correct answers in Python and natural language processing. Now, let's take another example to find queries about artificial intelligence and data. As you can see, it's able to return the proper documents that we had imported in our collection. What if we want to do some filtering by metadata? Well, we can definitely do so. In this case, we are able to filter by category and programming. When we are doing the search is able to return the right information that we're looking for. Additionally, we can get additional information about our collection, such as the name, the documents that we have, as well as the metadata that is part of these documents. As well, we're able to take a look at the store data and be able to explore what is part of our collection. Now, what if we want to update our document? Well, we will be able to do this by using the collection, that update, in where we specified the ID, the document, or the new information that we want to store, as well as the metadata. Everything is linked by the unique ID that we're able to provide. In this case, we're able to see that it has updated our document correctly. Finally, we are also able to delete the document, given that we are able to provide a unique ID. In this case, we're able to show you how you are able to work with ChromaDB to manage your vector database.