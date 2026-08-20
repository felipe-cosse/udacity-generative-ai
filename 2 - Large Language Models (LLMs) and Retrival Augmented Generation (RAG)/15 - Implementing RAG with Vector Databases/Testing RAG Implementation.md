Testing RAG Implementation
Create a comprehensive demonstration:

def demonstrate_chromadb_rag():
    """Comprehensive demonstration of ChromaDB RAG system capabilities."""

    print("🚀 ChromaDB RAG System Demonstration")
    print("="*60)

    # Initialize the RAG system
    rag_system = ChromaDBRAGSystem(
        embedding_config="openai_embeddings",
        persist_directory="./demo_chroma_db"
    )

    # Create collections
    print("\n" + "="*60)
    print("STEP 1: Creating Collections")
    print("="*60)
    rag_system.create_collection("tech_docs")
    rag_system.create_collection("faq_support")

    # Add sample documents
    print("\n" + "="*60)
    print("STEP 2: Adding Documents")
    print("="*60)
    rag_system.add_documents("tech_docs", SAMPLE_DOCUMENTS["tech_docs"])
    rag_system.add_documents("faq_support", SAMPLE_DOCUMENTS["faq_support"])

    # Test various queries
    print("\n" + "="*60)
    print("STEP 3: Testing Queries")
    print("="*60)

    # Query 1: Technical question
    response1 = rag_system.generate_rag_response(
        "tech_docs",
        "What is ChromaDB and what are its key features?"
    )
    rag_system.display_rag_response(response1)

    # Query 2: Customer support question
    response2 = rag_system.generate_rag_response(
        "faq_support",
        "I forgot my password, how do I reset it?"
    )
    rag_system.display_rag_response(response2)

    # Query 3: With metadata filtering
    print("\n" + "="*60)
    print("STEP 4: Testing Metadata Filtering")
    print("="*60)

    filtered_results = rag_system.search_documents(
        "faq_support",
        "contact support",
        n_results=2,
        metadata_filter={"priority": "High"}
    )

    print(f"\n🔍 Filtered Search Results:")
    for i, (doc, metadata) in enumerate(zip(filtered_results["documents"], filtered_results["metadatas"])):
        print(f"\n   Result {i+1}:")
        print(f"   Metadata: {metadata}")
        print(f"   Content: {doc[:150]}...")

    print("\n" + "="*60)
    print("✅ Demonstration Complete!")
    print("="*60)
Run Your Implementation
Uncomment the demonstration call at the bottom of the file:

# Run the comprehensive demonstration
if __name__ == "__main__":
    demonstrate_chromadb_rag()
Run the script:

python chromadb_rag_system.py



