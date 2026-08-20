Expected Output
When you run the completed exercise, you should see output similar to:

🚀 ChromaDB RAG System Demonstration
============================================================

🚀 ChromaDB RAG System initialized
   📂 Storage: ./demo_chroma_db
   🔧 Embedding: text-embedding-3-small

============================================================
STEP 1: Creating Collections
============================================================

📁 Creating collection: technical_documentation
   🗑️  Deleted existing collection
   ✅ Collection created successfully
   📋 Description: Technical documentation with structured metadata

📁 Creating collection: customer_support_faq
   ✅ Collection created successfully
   📋 Description: FAQ database for customer support automation

============================================================
STEP 2: Adding Documents
============================================================

📄 Adding 3 documents to technical_documentation
🔄 Generating embeddings for 3 texts...
   ✅ Generated 3 embeddings
   📊 Dimension: 1536
   ✅ Successfully added 3 documents
   📊 Collection now has 3 total documents

... [continues with RAG responses] ...
Verification Checklist
After completing the exercise, verify your implementation:














Common Issues and Solutions
Issue 1: "OPENAI_API_KEY not set"
Solution: Set your API key as an environment variable:

export OPENAI_API_KEY="sk-..."
Issue 2: "ModuleNotFoundError: No module named 'chromadb'"
Solution: Install ChromaDB:

pip install chromadb
Issue 3: Collections not persisting between runs
Solution: Check that you're using PersistentClient with a valid path, not just Client()

Issue 4: Embedding dimension mismatch
Solution: Make sure you're using consistent embedding models - don't mix OpenAI embeddings (1536D) with local embeddings (384D) in the same collection

Issue 5: Search returns no results
Solution:

Verify documents were actually added: collection.count()
Check that you're searching the correct collection
Try increasing n_results parameter
Additional Resources
ChromaDB Documentation: https://docs.trychroma.com/(opens in a new tab)
OpenAI Embeddings Guide: https://platform.openai.com/docs/guides/embeddings(opens in a new tab)
Key Takeaways

RAG prevents hallucinations by grounding answers in real documents
The pipeline: chunk → embed → store → retrieve → generate
ChromaDB makes it easy to search documents by meaning (semantic search)
Always enforce "answer from documents only" in your prompts
RAG systems are updatable—add new docs without retraining the model







For this exercise, we're going to be playing with Chroma DB. We're going to start by defining our embedding model. We're going to be using text embedding 3-small from OpenAI. As an alternative, we can leverage a local embedding model as well. We're going to define the collection configuration, and this is going to be using three collections, tech documents, FAQ support, and knowledge base. Then we're going to define our sample documents. For this, we're only going to be using tech documents as well as FAQ support, but you can also add the knowledge base documents if you like. Then we're going to find functions that are going to be part of our Chroma DB system. We're going to create our collection. This is going to be based on the configurations that we have set before. Then we are going to generate our embeddings. This is something that we're going to do manually, so we are able to have more control of the embeddings and the configuration that we would like for them. This is making an OpenAI API call so that we are able to generate the embeddings for each of the texts that we want to add to our collection. Then we are going to add our documents. This is going to be a collection of the texts, the ID, metadata, and the embeddings that we are generating. This gets added to our collection, and we will get a successful message if this goes without any errors. Then we add our helper function search documents, so we are able to retrieve the information that we are looking for to assist us in the queries that we are asking. We are going to be using our helper function for generating our RAG response. This is going to be combining the query that we are getting, the documents, as well as the question that we are asking altogether to create a context that then we can able to send to our LLM. Then we're going to define a helper function called generate RAG response. This is going to help us retrieve the context or the documents that we want to be able to use with our question, then prepare the context for generation. This is going to be combining the content, the similarity, and the source if we have one, and then create the prompt for doing this. This is combined in our context, the question or query that we are asking, and then being able to make the call to OpenAI so that we are able to receive a response. This is going to be formatted appropriately, so we are able to display it nicely. Then to finalize all of this, we're going to display the RAG response. This is going to help us be able to read our response and be able to see how many tokens are being used, the documents that are being utilized, and how long it took for our response to come through. Given all of this information, we're able to run our script, and it's going to be taken a few moments for us to be able to see the responses that we are generating and how well our system is working with Chroma DB in the back end. You can see here we are getting performance metrics, such as the time that it took, the model that we use, the tokens being utilized, and the contexts that we have. Play around with different texts. Play around with different queries, and be able to evaluate what is the best model and the best way to be able to retrieve these documents using Chroma DB.