"""
Quick test of basic components
"""
from core.config import VECTOR_DIMENSION, SIMILARITY_THRESHOLD
from core.message import Message
from memory.vector_store import VectorStore
from memory.knowledge_base import search_knowledge

# Test 1: Config
print("Test 1: Config")
print(f"Vector dimension: {VECTOR_DIMENSION}")
print(f"Similarity threshold: {SIMILARITY_THRESHOLD}")
print()

# Test 2: Message
print("Test 2: Message")
msg = Message("Coordinator", "ResearchAgent", "task", {"query": "neural networks"})
print(msg)
print()

# Test 3: Knowledge Base
print("Test 3: Knowledge Base")
result = search_knowledge("transformers")
if result:
    print(f"Found: {result['summary'][:100]}...")
print()

# Test 4: Vector Store
print("Test 4: Vector Store")
vs = VectorStore()
vs.add("mem1", "What are neural networks?")
vs.add("mem2", "Explain transformers in AI")
vs.add("mem3", "What is the weather today?")

results = vs.search("Tell me about neural nets", top_k=2)
print(f"Search results: {results}")
print()

print("✅ All basic tests passed!")