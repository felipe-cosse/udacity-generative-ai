# ChromaDB RAG System Implementation - Starter Template
# TODO: Complete this script to build a Retrieval-Augmented Generation system using ChromaDB

# TODO: Import necessary libraries
# Hint: You'll need chromadb, openai, pandas, time, json, typing, numpy, datetime, uuid, os, pathlib
import chromadb
from chromadb.config import Settings
import openai
from openai import OpenAI
# TODO: Add remaining imports here
import pandas as pd
import time
import json
from typing import Dict, List, Tuple, Optional
import numpy as np
from datetime import datetime
import uuid
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# TODO: Define embedding configurations for different strategies
# Create configurations for OpenAI embeddings and local alternatives
EMBEDDING_CONFIGS = {
    "openai_embeddings": {
        # TODO: Set provider to "openai"
        "provider": "openai",
        # TODO: Choose OpenAI embedding model (hint: text-embedding-3-small is cost-effective)
        "model": "text-embedding-3-small",  # Cost-effective OpenAI embedding model
        # TODO: Set dimensions (hint: 1536 for text-embedding-3-small)
        "dimensions": 1536,                 # Standard dimension size
        "description": "OpenAI embeddings with excellent semantic understanding"
    },
    "local_embeddings": {
        # TODO: Set provider to "sentence_transformers"
        "provider": "sentence_transformers", 
        # TODO: Choose local model (hint: all-MiniLM-L6-v2 is lightweight)
        "model": "all-MiniLM-L6-v2",       # Lightweight local model
        # TODO: Set dimensions (hint: 384 for all-MiniLM-L6-v2)
        "dimensions": 384,                  # Smaller dimension for efficiency
        "description": "Local embeddings for cost-effective processing"
    }
}

# TODO: Define collection configurations for different document types
# Create configurations for technical docs, FAQ support, and knowledge base
COLLECTION_CONFIGS = {
    "tech_docs": {
        # TODO: Set collection name
        "name": "technical_documentation",
        # TODO: Define metadata fields for technical documentation
        "metadata_fields": ["source", "category", "difficulty", "last_updated"],
        "description": "Technical documentation with structured metadata"
    },
    "faq_support": {
        # TODO: Set collection name
        "name": "faq_customer_support", 
        # TODO: Define metadata fields for FAQ support
        "metadata_fields": ["category", "priority", "department", "tags"],
        "description": "FAQ database for customer support automation"
    },
    "knowledge_base": {
        # TODO: Set collection name
        "name": "general_knowledge",
        # TODO: Define metadata fields for general knowledge
        "metadata_fields": ["topic", "source", "confidence", "date_added"],
        "description": "General knowledge base for information retrieval"
    }
}

# TODO: Create sample documents for testing
# Define realistic business documents with content and metadata
SAMPLE_DOCUMENTS = {
    "tech_docs": [
        {
            "id": "tech_001",
            # TODO: Add content about ChromaDB (200-300 words)
            "content": "ChromaDB is an open-source vector database designed for AI applications. It provides efficient storage and retrieval of high-dimensional vectors, making it ideal for semantic search, recommendation systems, and RAG implementations. ChromaDB supports multiple embedding functions and offers both in-memory and persistent storage options.",
            "metadata": {
                # TODO: Add appropriate metadata
                "source": "ChromaDB Documentation",
                "category": "Database",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-15"
            }
        },
        {
            "id": "tech_002",
            # TODO: Add content about RAG systems (200-300 words)
            "content": "Retrieval-Augmented Generation (RAG) combines the power of large language models with external knowledge retrieval. By retrieving relevant documents before generation, RAG systems can provide more accurate, up-to-date, and contextually relevant responses while reducing hallucinations and improving factual accuracy.",
            "metadata": {
                # TODO: Add appropriate metadata
                "source": "AI Research Papers",
                "category": "Machine Learning",
                "difficulty": "Advanced",
                "last_updated": "2024-02-01"
            }
        },
        {
            "id": "tech_003",
            # TODO: Add content about vector embeddings (200-300 words)
            "content": "Vector embeddings are numerical representations of text that capture semantic meaning. Modern embedding models like OpenAI's text-embedding-3-small can convert text into high-dimensional vectors where similar concepts are positioned closer together in the vector space, enabling semantic search capabilities.",
            "metadata": {
                # TODO: Add appropriate metadata
                "source": "Embedding Guide",
                "category": "NLP",
                "difficulty": "Intermediate", 
                "last_updated": "2024-01-20"
            }
        }
    ],
    "faq_support": [
        {
            "id": "faq_001",
            # TODO: Add FAQ about password reset
            "content": "Q: How do I reset my password? A: To reset your password, click on the 'Forgot Password' link on the login page, enter your email address, and follow the instructions sent to your email. The reset link expires after 24 hours for security purposes.",
            "metadata": {
                # TODO: Add appropriate metadata for customer support
                "category": "Account Management",
                "priority": "High",
                "department": "IT Support",
                "tags": "password, security, login"
            }
        },
        {
            "id": "faq_002",
            # TODO: Add FAQ about business hours
            "content": "Q: What are your business hours? A: Our customer support is available Monday through Friday, 9 AM to 6 PM EST. For urgent technical issues, our emergency support line is available 24/7 for premium customers.",
            "metadata": {
                # TODO: Add appropriate metadata
                "category": "General Information",
                "priority": "Medium",
                "department": "Customer Service",
                "tags": "hours, support, availability"
            }
        },
        {
            "id": "faq_003",
            # TODO: Add FAQ about subscription upgrade
            "content": "Q: How do I upgrade my subscription? A: You can upgrade your subscription by logging into your account, navigating to the 'Billing' section, and selecting 'Upgrade Plan'. Changes take effect immediately, and you'll be prorated for the current billing period.",
            "metadata": {
                # TODO: Add appropriate metadata
                "category": "Billing",
                "priority": "High", 
                "department": "Sales",
                "tags": "subscription, billing, upgrade"
            }
        }
    ]
}

class ChromaDBRAGSystem:
    """
    A comprehensive RAG system implementation using ChromaDB for vector storage and retrieval.
    
    TODO: Complete this class to implement a production-ready RAG system with:
    - ChromaDB integration for vector storage
    - Embedding generation and management
    - Document ingestion and retrieval
    - RAG response generation
    """
    
    def __init__(self, embedding_config: str = "openai_embeddings", persist_directory: str = "./chroma_db"):
        """
        Initialize the ChromaDB RAG system with specified configuration.
        
        TODO: Complete this method to:
        1. Store configuration parameters
        2. Initialize ChromaDB client with persistent storage
        3. Initialize OpenAI client for embeddings and generation
        4. Set up collections dictionary
        5. Print initialization status
        
        Args:
            embedding_config (str): Configuration key for embedding strategy
            persist_directory (str): Directory for persistent storage
        """
        # TODO: Store embedding configuration
        self.embedding_config = EMBEDDING_CONFIGS[embedding_config]
        self.persist_directory = persist_directory
        
        # TODO: Initialize ChromaDB client with persistent storage
        # Hint: Use chromadb.PersistentClient with path and settings
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,  # Disable telemetry for privacy
                allow_reset=True             # Allow database reset for development
            )
        )
        
        # TODO: Initialize OpenAI client for embeddings and generation
        # SECURITY NOTE: Use environment variables for API keys in production
        self.openai_client = OpenAI(
            base_url="https://openai.vocareum.com/v1",
            api_key=os.getenv(
                "OPENAI_API_KEY"
            ),
        )
        
        # TODO: Initialize collections dictionary
        self.collections = {}
        
        # TODO: Print initialization status
        print(f"🚀 ChromaDB RAG System initialized")
        print(f"   Embedding Strategy: {self.embedding_config['description']}")
        print(f"   Persist Directory: {persist_directory}")
        print(f"   Available Collections: {len(self.client.list_collections())}")

    def create_collection(self, collection_key: str):
        """
        Create a new ChromaDB collection with specified configuration.
        
        TODO: Complete this method to:
        1. Validate collection_key exists in COLLECTION_CONFIGS
        2. Get collection configuration
        3. Delete existing collection if it exists (for development)
        4. Create new collection with appropriate settings
        5. Store collection in self.collections
        6. Handle errors gracefully
        
        Args:
            collection_key (str): Key from COLLECTION_CONFIGS
            
        Returns:
            chromadb.Collection: The created collection object
        """
        # TODO: Validate collection_key
        if collection_key not in COLLECTION_CONFIGS:
            raise ValueError(f"Unknown collection configuration: {collection_key}")
            
        # TODO: Get configuration and create collection
        config = COLLECTION_CONFIGS[collection_key]
        collection_name = config["name"]
        
        print(f"\n📁 Creating collection: {collection_name}")
        print(f"   Description: {config['description']}")
        print(f"   Metadata fields: {config['metadata_fields']}")
        
        try:
            # TODO: Delete existing collection if it exists
            # TODO: Create new collection
            # TODO: Store in self.collections
            # TODO: Print success message
            # Delete existing collection if it exists (for development)
            try:
                self.client.delete_collection(collection_name)
                print(f"   ♻️  Deleted existing collection")
            except:
                pass
            
            # Create new collection with embedding function
            if self.embedding_config["provider"] == "openai":
                # Use OpenAI embeddings
                collection = self.client.create_collection(
                    name=collection_name,
                    embedding_function=None,  # We'll handle embeddings manually
                    metadata={"description": config["description"]}
                )
            else:
                # Use default ChromaDB embeddings for local processing
                collection = self.client.create_collection(
                    name=collection_name,
                    metadata={"description": config["description"]}
                )
            
            self.collections[collection_key] = collection
            print(f"   ✅ Collection created successfully")
            return collection
            
        except Exception as e:
            print(f"   ❌ Error creating collection: {str(e)}")
            raise

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using the configured embedding model.
        
        TODO: Complete this method to:
        1. Handle OpenAI embedding generation
        2. Support local embedding generation (optional)
        3. Include proper error handling
        4. Return list of embedding vectors
        
        Args:
            texts (List[str]): List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        print(f"🔄 Generating embeddings for {len(texts)} texts...")
        
        try:
            if self.embedding_config["provider"] == "openai":
                # TODO: Use OpenAI embeddings API
                # Hint: Use self.openai_client.embeddings.create()
                # Use OpenAI embeddings API
                response = self.openai_client.embeddings.create(
                    model=self.embedding_config["model"],
                    input=texts
                )

                embeddings = [embedding.embedding for embedding in response.data]
                print(f"✅ Generated {len(embeddings)} OpenAI embeddings")
                return embeddings
                
            else:
                # TODO: Handle local embeddings (optional)
                print("⚠️  Local embeddings not implemented in this example")
                return []
                
        except Exception as e:
            print(f"❌ Error generating embeddings: {str(e)}")
            raise

    def add_documents(self, collection_key: str, documents: List[Dict]) -> None:
        """
        Add documents to a ChromaDB collection with embeddings and metadata.
        
        TODO: Complete this method to:
        1. Validate collection exists
        2. Extract texts, IDs, and metadata from documents
        3. Generate embeddings for texts
        4. Add documents to collection with embeddings
        5. Handle errors and provide status updates
        
        Args:
            collection_key (str): Key identifying the target collection
            documents (List[Dict]): List of document dictionaries with content and metadata
        """
        # TODO: Validate collection exists
        if collection_key not in self.collections:
            raise ValueError(f"Collection {collection_key} not found. Create it first.")
            
        # TODO: Get collection and extract document data
        collection = self.collections[collection_key]
        
        print(f"\n📄 Adding {len(documents)} documents to {collection.name}")
        
        # TODO: Extract texts, IDs, and metadata
        # TODO: Generate embeddings
        # TODO: Add documents to collection
        # TODO: Print success status
        # Extract texts and metadata
        texts = [doc["content"] for doc in documents]
        ids = [doc["id"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        
        # Generate embeddings
        embeddings = self.generate_embeddings(texts)
        
        if not embeddings:
            print("❌ No embeddings generated, skipping document addition")
            return
        
        try:
            # Add documents to collection
            collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ Successfully added {len(documents)} documents")
            print(f"   Collection now contains: {collection.count()} documents")
            
        except Exception as e:
            print(f"❌ Error adding documents: {str(e)}")
            raise

    def search_documents(self, collection_key: str, query: str, n_results: int = 3, 
                        metadata_filter: Optional[Dict] = None) -> Dict:
        """
        Search for relevant documents using semantic similarity.
        
        TODO: Complete this method to:
        1. Validate collection exists
        2. Generate embedding for query
        3. Perform similarity search with optional metadata filtering
        4. Format and return results with similarity scores
        
        Args:
            collection_key (str): Key identifying the collection to search
            query (str): Search query text
            n_results (int): Number of results to return
            metadata_filter (Optional[Dict]): Metadata filters to apply
            
        Returns:
            Dict: Search results with documents, distances, and metadata
        """
        # TODO: Validate collection exists
        # TODO: Generate query embedding
        # TODO: Perform similarity search
        # TODO: Format and return results
        if collection_key not in self.collections:
            raise ValueError(f"Collection {collection_key} not found")
            
        collection = self.collections[collection_key]
        
        print(f"\n🔍 Searching collection: {collection.name}")
        print(f"   Query: '{query}'")
        print(f"   Requesting: {n_results} results")
        if metadata_filter:
            print(f"   Filters: {metadata_filter}")
        
        try:
            # Generate embedding for query
            query_embeddings = self.generate_embeddings([query])
            
            if not query_embeddings:
                print("❌ Failed to generate query embedding")
                return {"documents": [], "distances": [], "metadatas": []}
            
            # Perform similarity search
            results = collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                where=metadata_filter,
                include=["documents", "distances", "metadatas"]
            )
            
            print(f"✅ Found {len(results['documents'][0])} relevant documents")
            
            # Format results for better readability
            formatted_results = {
                "query": query,
                "n_results": len(results['documents'][0]),
                "results": []
            }
            
            for i in range(len(results['documents'][0])):
                formatted_results["results"].append({
                    "document": results['documents'][0][i],
                    "similarity_score": 1 - results['distances'][0][i],  # Convert distance to similarity
                    "metadata": results['metadatas'][0][i]
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"❌ Error searching documents: {str(e)}")
            return {"documents": [], "distances": [], "metadatas": []}

    def generate_rag_response(self, collection_key: str, query: str, n_context: int = 3,
                            model: str = "gpt-4o-mini") -> Dict:
        """
        Generate a response using Retrieval-Augmented Generation.
        
        TODO: Complete this method to:
        1. Retrieve relevant context documents
        2. Prepare context for generation
        3. Create prompt with context
        4. Generate response using OpenAI
        5. Format comprehensive response with metadata
        
        Args:
            collection_key (str): Collection to search for context
            query (str): User query to answer
            n_context (int): Number of context documents to retrieve
            model (str): OpenAI model to use for generation
            
        Returns:
            Dict: RAG response with context, answer, and metadata
        """
        print(f"\n🤖 Generating RAG response")
        print(f"   Query: '{query}'")
        print(f"   Context documents: {n_context}")
        print(f"   Generation model: {model}")
        
        # TODO: Retrieve relevant context
        # TODO: Prepare context for generation
        # TODO: Create prompt with context
        # TODO: Generate response using OpenAI
        # TODO: Format and return comprehensive response
        start_time = time.time()
        
        # Step 1: Retrieve relevant context
        search_results = self.search_documents(collection_key, query, n_context)
        
        if not search_results["results"]:
            return {
                "query": query,
                "answer": "I couldn't find relevant information to answer your question.",
                "context": [],
                "generation_time": 0,
                "context_used": 0
            }
        
        # Step 2: Prepare context for generation
        context_documents = []
        for result in search_results["results"]:
            context_documents.append({
                "content": result["document"],
                "similarity": result["similarity_score"],
                "source": result["metadata"].get("source", "Unknown")
            })
        
        # Step 3: Create prompt with context
        context_text = "\n\n".join([
            f"Document {i+1} (Similarity: {doc['similarity']:.3f}):\n{doc['content']}"
            for i, doc in enumerate(context_documents)
        ])
        
        prompt = f"""Based on the following context documents, please answer the user's question. If the context doesn't contain enough information to answer the question completely, please say so and provide what information you can.

Context Documents:
{context_text}

User Question: {query}

Please provide a comprehensive answer based on the context provided:"""

        try:
            # Step 4: Generate response using OpenAI
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_completion_tokens=500
            )
            
            generation_time = time.time() - start_time
            
            # Step 5: Format comprehensive response
            rag_response = {
                "query": query,
                "answer": response.choices[0].message.content,
                "context": context_documents,
                "generation_time": round(generation_time, 2),
                "context_used": len(context_documents),
                "model_used": model,
                "tokens_used": response.usage.total_tokens
            }
            
            print(f"✅ RAG response generated successfully")
            print(f"   Generation time: {generation_time:.2f}s")
            print(f"   Context documents used: {len(context_documents)}")
            print(f"   Tokens used: {response.usage.total_tokens}")
            
            return rag_response
            
        except Exception as e:
            print(f"❌ Error generating RAG response: {str(e)}")
            return {
                "query": query,
                "answer": f"Error generating response: {str(e)}",
                "context": context_documents,
                "generation_time": 0,
                "context_used": len(context_documents)
            }

    def display_rag_response(self, rag_response: Dict) -> None:
        """
        Display RAG response in a formatted, readable way.
        
        TODO: Complete this method to:
        1. Display question and answer clearly
        2. Show context sources with similarity scores
        3. Display performance metrics
        4. Format output for readability
        
        Args:
            rag_response (Dict): RAG response dictionary from generate_rag_response
        """
        # TODO: Format and display RAG response
        # Include: question, answer, context sources, performance metrics
        print(f"\n" + "="*80)
        print(f"🤖 RAG RESPONSE")
        print(f"="*80)
        
        print(f"\n❓ QUESTION:")
        print(f"   {rag_response['query']}")
        
        print(f"\n💡 ANSWER:")
        print(f"   {rag_response['answer']}")
        
        print(f"\n📚 CONTEXT SOURCES ({rag_response['context_used']} documents):")
        for i, context in enumerate(rag_response['context']):
            print(f"   {i+1}. Similarity: {context['similarity']:.3f} | Source: {context['source']}")
            print(f"      Preview: {context['content'][:100]}...")
        
        print(f"\n📊 PERFORMANCE METRICS:")
        print(f"   Generation Time: {rag_response['generation_time']}s")
        print(f"   Model Used: {rag_response.get('model_used', 'Unknown')}")
        print(f"   Tokens Used: {rag_response.get('tokens_used', 'Unknown')}")
        print(f"   Context Documents: {rag_response['context_used']}")

def demonstrate_chromadb_rag():
    """
    Comprehensive demonstration of ChromaDB RAG system capabilities.
    
    TODO: Complete this function to:
    1. Initialize the RAG system
    2. Create collections for different document types
    3. Add sample documents to collections
    4. Test various query types
    5. Display results and performance metrics
    """
    print("🚀 ChromaDB RAG System Demonstration")
    print("="*60)
    
    # TODO: Initialize the RAG system
    # TODO: Create collections
    # TODO: Add sample documents
    # TODO: Test various queries
    # TODO: Display results
    # Initialize the RAG system
    rag_system = ChromaDBRAGSystem(
        embedding_config="openai_embeddings",
        persist_directory="./demo_chroma_db"
    )
    
    # Create collections for different document types
    print("\n📁 Setting up document collections...")
    rag_system.create_collection("tech_docs")
    rag_system.create_collection("faq_support")
    
    # Add sample documents to collections
    print("\n📄 Adding sample documents...")
    rag_system.add_documents("tech_docs", SAMPLE_DOCUMENTS["tech_docs"])
    rag_system.add_documents("faq_support", SAMPLE_DOCUMENTS["faq_support"])
    
    # Demonstrate different types of queries
    test_queries = [
        {
            "collection": "tech_docs",
            "query": "What is ChromaDB and how does it work?",
            "description": "Technical documentation query"
        },
        {
            "collection": "tech_docs", 
            "query": "How do vector embeddings enable semantic search?",
            "description": "Conceptual understanding query"
        },
        {
            "collection": "faq_support",
            "query": "I forgot my password, how can I reset it?",
            "description": "Customer support query"
        },
        {
            "collection": "faq_support",
            "query": "What are your business hours?",
            "description": "General information query"
        }
    ]
    
    # Execute test queries and display results
    print("\n🔍 Testing RAG system with various queries...")
    for i, test in enumerate(test_queries, 1):
        print(f"\n{'='*20} TEST QUERY {i}: {test['description']} {'='*20}")
        
        rag_response = rag_system.generate_rag_response(
            collection_key=test["collection"],
            query=test["query"],
            n_context=2
        )
        
        rag_system.display_rag_response(rag_response)
    
    print(f"\n🎉 ChromaDB RAG demonstration completed successfully!")
    print(f"   Collections created: {len(rag_system.collections)}")
    print(f"   Documents processed: {sum(len(docs) for docs in SAMPLE_DOCUMENTS.values())}")
    print(f"   Queries tested: {len(test_queries)}")

# TODO: Example usage - uncomment and test when ready
# Run the comprehensive demonstration
# demonstrate_chromadb_rag()
# Example usage and testing
if __name__ == "__main__":
    # Run the comprehensive demonstration
    demonstrate_chromadb_rag()

# TODO: Additional examples you can implement:
# 
# Example 1: Custom metadata filtering
# rag_system = ChromaDBRAGSystem()
# rag_system.create_collection("tech_docs")
# rag_system.add_documents("tech_docs", SAMPLE_DOCUMENTS["tech_docs"])
# filtered_results = rag_system.search_documents(
#     "tech_docs", 
#     "database information",
#     metadata_filter={"category": "Database"}
# )
#
# Example 2: Batch processing multiple queries
# queries = ["What is RAG?", "How do embeddings work?", "ChromaDB features"]
# for query in queries:
#     response = rag_system.generate_rag_response("tech_docs", query)
#     rag_system.display_rag_response(response)

"""
EXERCISE COMPLETION CHECKLIST:
□ Import all necessary libraries
□ Complete EMBEDDING_CONFIGS with appropriate models and parameters
□ Fill in COLLECTION_CONFIGS with meaningful names and metadata fields
□ Create comprehensive SAMPLE_DOCUMENTS with realistic content
□ Implement ChromaDBRAGSystem.__init__() with proper initialization
□ Complete create_collection() with ChromaDB collection creation
□ Implement generate_embeddings() with OpenAI API integration
□ Complete add_documents() with embedding generation and storage
□ Implement search_documents() with similarity search and filtering
□ Complete generate_rag_response() with full RAG pipeline
□ Implement display_rag_response() with formatted output
□ Complete demonstrate_chromadb_rag() with comprehensive testing
□ Test your implementation with the example usage
□ Add your own API key and test the complete workflow

BONUS CHALLENGES:
□ Add support for local embedding models using sentence-transformers
□ Implement batch processing for large document collections
□ Add metadata-based filtering and advanced search capabilities
□ Create a web interface for the RAG system using Flask or FastAPI
□ Implement document update and deletion functionality
□ Add support for different file formats (PDF, Word, etc.)
□ Create performance monitoring and analytics dashboard
□ Implement user authentication and access control
□ Add support for multi-modal documents (text + images)
□ Create automated document ingestion from external sources
"""
