"""
Vector store for semantic similarity search
"""
import numpy as np
import faiss
from core.config import VECTOR_DIMENSION

class VectorStore:
    """
    Manages vector embeddings and similarity search using FAISS
    """
    
    def __init__(self, dimension=VECTOR_DIMENSION):
        """
        Initialize the vector store
        
        Args:
            dimension (int): Dimensionality of vectors
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.id_to_vector = {}
        self.vector_to_id = []
    
    def text_to_vector(self, text):
        """
        Convert text to a simple vector representation
        
        Args:
            text (str): Input text
            
        Returns:
            np.array: Vector representation
        """
        # Simple word-based hashing approach
        words = text.lower().split()
        vector = np.zeros(self.dimension, dtype=np.float32)
        
        # Hash each word to a position and increment
        for word in words:
            # Remove punctuation
            word = ''.join(c for c in word if c.isalnum())
            if word:
                position = hash(word) % self.dimension
                vector[position] += 1.0
        
        # Normalize to unit length
        magnitude = np.linalg.norm(vector)
        if magnitude > 0:
            vector = vector / magnitude
        
        return vector
    
    def add(self, memory_id, text):
        """
        Add a text entry to the vector store
        
        Args:
            memory_id (str): Unique identifier for this entry
            text (str): Text to vectorize and store
        """
        vector = self.text_to_vector(text)
        
        # Store mappings
        self.id_to_vector[memory_id] = vector
        self.vector_to_id.append(memory_id)
        
        # Add to FAISS index
        self.index.add(np.array([vector]))
    
    def search(self, query_text, top_k=5):
        """
        Search for similar entries
        
        Args:
            query_text (str): Query text
            top_k (int): Number of results to return
            
        Returns:
            list: List of tuples (memory_id, similarity_score)
        """
        if self.index.ntotal == 0:
            return []
        
        # Convert query to vector
        query_vector = self.text_to_vector(query_text)
        
        # Search in FAISS
        top_k = min(top_k, self.index.ntotal)
        distances, indices = self.index.search(np.array([query_vector]), top_k)
        
        # Convert distances to similarity scores (0-1 range)
        # Lower distance = higher similarity
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.vector_to_id):
                memory_id = self.vector_to_id[idx]
                # Convert L2 distance to similarity score
                similarity = 1.0 / (1.0 + dist)
                results.append((memory_id, similarity))
        
        return results
    
    def size(self):
        """Return the number of vectors in the store"""
        return self.index.ntotal