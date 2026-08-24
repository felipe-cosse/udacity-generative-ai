import chromadb
import os
from chromadb.config import Settings
from openai import OpenAI
from typing import Dict, List, Optional
from pathlib import Path

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")
    
    # Look for ChromaDB directories
    # TODO: Create list of directories that match specific criteria (directory type and name pattern)
    chroma_directories = sorted(
        path
        for path in current_dir.glob("chroma_db*")
        if path.is_dir()
    )
    # TODO: Loop through each discovered directory
    for chroma_directory in chroma_directories:
        # TODO: Wrap connection attempt in try-except block for error handling
        try:
            # TODO: Initialize database client with directory path and configuration settings
            client = chromadb.PersistentClient(
                path=str(chroma_directory),
                settings=Settings(
                    anonymized_telemetry=False,
                ),
            )
            # TODO: Retrieve list of available collections from the database
            collections = client.list_collections()
            # TODO: Loop through each collection found
            for collection_reference in collections:
                collection_name = (
                    collection_reference
                    if isinstance(collection_reference, str)
                    else collection_reference.name
                )
                # TODO: Create unique identifier key combining directory and collection names
                backend_key = (
                    f"{chroma_directory.name}::{collection_name}"
                )
                # TODO: Build information dictionary containing:
                backend_info = {}
                # TODO: Store directory path as string
                backend_info["directory"] = str(
                    chroma_directory.resolve()
                )
                # TODO: Store collection name
                backend_info["collection_name"] = collection_name
                # TODO: Get document count with fallback for unsupported operations
                try:
                    if (
                        hasattr(collection_reference, "count")
                        and callable(collection_reference.count)
                    ):
                        document_count = collection_reference.count()
                    else:
                        collection = client.get_collection(
                            name=collection_name,
                            embedding_function=None,
                        )
                        document_count = collection.count()
                except Exception:
                    document_count = 0

                backend_info["document_count"] = document_count
                # TODO: Create user-friendly display name
                backend_info["display_name"] = (
                    f"{collection_name} "
                    f"({chroma_directory.name}) - "
                    f"{document_count} documents"
                )
                # TODO: Add collection information to backends dictionary
                backends[backend_key] = backend_info
        
        # TODO: Handle connection or access errors gracefully
        except Exception as error:
            error_message = " ".join(str(error).split())

            if len(error_message) > 100:
                error_message = f"{error_message[:97]}..."
            # TODO: Create fallback entry for inaccessible directories
            fallback_key = (
                f"{chroma_directory.name}::unavailable"
            )
            # TODO: Include error information in display name with truncation
            display_name = (
                f"{chroma_directory.name} "
                f"(unavailable: {error_message})"
            )
            # TODO: Set appropriate fallback values for missing information
            backends[fallback_key] = {
                "directory": str(chroma_directory.resolve()),
                "collection_name": "",
                "display_name": display_name,
                "document_count": 0,
                "error": error_message,
            }

    # TODO: Return complete backends dictionary with all discovered collections
    return backends

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""
    database_path = Path(chroma_dir)

    if not database_path.is_dir():
        raise FileNotFoundError(
            f"ChromaDB directory does not exist: {database_path}"
        )

    if not collection_name or not collection_name.strip():
        raise ValueError("collection_name cannot be empty")
    # TODO: Create a chomadb persistentclient
    client = chromadb.PersistentClient(
        path=str(database_path),
        settings=Settings(
            anonymized_telemetry=False,
        ),
    )
    # TODO: Return the collection with the collection_name
    collection = client.get_collection(
        name=collection_name.strip(),
        embedding_function=None,
    )

    # Required by chat.py: collection, success, error.
    return collection, True, None

def retrieve_documents(collection, query: str, n_results: int = 3, 
                      mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""
    if collection is None:
        raise ValueError("A ChromaDB collection is required")

    if not query or not query.strip():
        raise ValueError("query cannot be empty")

    if n_results <= 0:
        raise ValueError("n_results must be greater than 0")

    if collection.count() == 0:
        return {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }
    # TODO: Initialize filter variable to None (represents no filtering)
    where_filter = None
    # TODO: Check if filter parameter exists and is not set to "all" or equivalent
    if (
        mission_filter
        and mission_filter.strip().lower()
        not in {"all", "all missions", "any"}
    ):
        normalized_mission = (
            "_".join(mission_filter.strip().lower().split())
            .replace("-", "_")
        )

        mission_aliases = {
            "apollo11": "apollo_11",
            "apollo13": "apollo_13",
            "sts_51l": "challenger",
        }
        normalized_mission = mission_aliases.get(
            normalized_mission,
            normalized_mission,
        )
    # TODO: If filter conditions are met, create filter dictionary with appropriate field-value pairs
        where_filter = {
            "mission": normalized_mission,
        }
    api_key = (
        os.getenv("CHROMA_OPENAI_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )

    if not api_key or not api_key.strip():
        raise ValueError(
            "An OpenAI API key is required to embed the query"
        )

    collection_metadata = collection.metadata or {}
    embedding_model = str(
        collection_metadata.get(
            "embedding_model",
            "text-embedding-3-small",
        )
    )
    base_url = os.getenv(
        "OPENAI_BASE_URL",
        "https://openai.vocareum.com/v1",
    )
    embedding_client = OpenAI(
        api_key=api_key.strip(),
        base_url=base_url,
    )
    embedding_response = embedding_client.embeddings.create(
        model=embedding_model,
        input=query.strip(),
    )
    query_embedding = embedding_response.data[0].embedding

    if not query_embedding:
        raise RuntimeError("OpenAI returned an empty query embedding")

    # TODO: Execute database query with the following parameters:
    results = collection.query(
        # TODO: Pass search query in the required format
        query_embeddings=[query_embedding],
        # TODO: Set maximum number of results to return
        n_results=min(n_results, collection.count()),
        # TODO: Apply conditional filter (None for no filtering, dictionary for specific filtering)
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    # TODO: Return query results to caller
    return results

def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""

    # Ensure every document has a corresponding metadata dictionary.
    metadata_items = list(metadatas or [])

    if len(metadata_items) < len(documents):
        metadata_items.extend(
            {} for _ in range(len(documents) - len(metadata_items))
        )
    # TODO: Initialize list with header text for context section
    context_parts = [
        "=== RETRIEVED NASA MISSION CONTEXT ==="
    ]
    # TODO: Loop through paired documents and their metadata using enumeration
    for index, (document, metadata) in enumerate(
        zip(documents, metadata_items),
        start=1,
    ):
        metadata = metadata or {}
        document_text = str(document).strip()

        if not document_text:
            continue
        # TODO: Extract mission information from metadata with fallback value
        mission = str(metadata.get("mission", "unknown mission"))
        # TODO: Clean up mission name formatting (replace underscores, capitalize)
        mission_display = mission.replace("_", " ").title()
        # TODO: Extract source information from metadata with fallback value  
        source = str(metadata.get("source", "unknown source"))
        source = " ".join(source.split())
        # TODO: Extract category information from metadata with fallback value
        category = str(
            metadata.get(
                "document_category",
                "general document",
            )
        )
        # TODO: Clean up category name formatting (replace underscores, capitalize)
        category_display = category.replace("_", " ").title()
        # TODO: Create formatted source header with index number and extracted information
        source_header = (
            f"[Source {index}]\n"
            f"Mission: {mission_display}\n"
            f"Source: {source}\n"
            f"Category: {category_display}"
        )
        # TODO: Add source header to context parts list
        context_parts.append(source_header)
        # TODO: Check document length and truncate if necessary
        maximum_document_length = 1000

        if len(document_text) > maximum_document_length:
            document_text = (
                document_text[:maximum_document_length].rstrip()
                + "... [truncated]"
            )
        # TODO: Add truncated or full document content to context parts list
        context_parts.append(document_text)

    if len(context_parts) == 1:
        return ""

    # TODO: Join all context parts with newlines and return formatted string
    return "\n\n".join(context_parts)
