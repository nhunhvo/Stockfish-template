"""
Pinecone vector database utilities for fish recognition.
Handles upserting and retrieving fish embeddings with metadata.
"""

from typing import List, Dict, Any
from pinecone import Pinecone
from pinecone.exceptions import PineconeException


class FishVectorDB:
    """Handles Pinecone vector database operations for fish embeddings."""
    
    def __init__(
        self,
        index_name: str,
        namespace: str
    ):
        """
        Initialize Pinecone client and connect to index.
        
        Args:
            index_name: Name of the Pinecone index
            namespace: Namespace for data isolation (mandatory)
        """

        # Initialize Pinecone client
        pc = Pinecone(api_key="FILL IN YOUR API KEY HERE")
        self.index_name = index_name
        self.namespace = namespace

        # Get index reference
        try:
            self.index = pc.Index(index_name)
            # Get index dimension from Pinecone
            try:
                index_description = pc.describe_index(index_name)
                self.index_dimension = index_description.dimension
            except Exception as desc_error:
                # If we can't get dimension, it will be caught on first upsert
                self.index_dimension = None
        except Exception as e:
            raise ValueError(f"Failed to connect to index '{index_name}'. Ensure it exists. Error: {e}")

    def upsert_batch(
        self,
        fish_records: List[tuple[str, List[float], Dict[str, Any]]],
        batch_size: int = 20
    ) -> None:
        """
        Upsert multiple fish records in batches.

        Args:
            fish_records: List of tuples (fish_id, embedding, metadata_dict)
            TODO batch_size: Maximum records per batch
        """
        vectors = [
            (fish_id, embedding, metadata)
            for fish_id, embedding, metadata in fish_records
        ]
        try:
            self.index.upsert(vectors=vectors, namespace=self.namespace)
        except PineconeException as e:
            raise ValueError(f"Failed to upsert batch: {e}")

    def clear_index(self) -> None:
        """
        Delete all records from the namespace.

        ⚠️ WARNING: This will permanently delete ALL records in the namespace.
        This operation cannot be undone. Use with caution.
        """
        try:
            self.index.delete(namespace=self.namespace, delete_all=True)
            print(f"All records deleted from namespace '{self.namespace}'")
        except PineconeException as e:
            raise ValueError(f"Failed to clear index: {e}")
