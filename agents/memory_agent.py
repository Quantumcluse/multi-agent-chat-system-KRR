"""
Memory Agent - Manages system memory and knowledge storage
"""
from datetime import datetime
from core.message import Message
from core.config import MSG_TYPE_RESPONSE, MSG_TYPE_STORE, MSG_TYPE_RETRIEVE
from memory.vector_store import VectorStore

class MemoryAgent:
    """
    Agent responsible for managing long-term memory
    """
    
    def __init__(self, name="MemoryAgent", logger=None):
        """
        Initialize the Memory Agent
        
        Args:
            name (str): Agent name
            logger: System logger instance
        """
        self.name = name
        self.logger = logger
        
        # Initialize memory stores
        self.vector_store = VectorStore()
        self.conversation_memory = []
        self.knowledge_base = {}
        self.agent_state_memory = {}
        self.memory_id_counter = 0
    
    def process_message(self, message):
        """
        Process incoming message for memory operations
        
        Args:
            message (Message): Incoming message
            
        Returns:
            Message: Response message
        """
        if self.logger:
            self.logger.log_message(
                message.sender, 
                self.name, 
                message.msg_type, 
                message.payload
            )
        
        operation = message.payload.get("operation", "retrieve")
        
        if operation == "store":
            result = self._store_memory(message.payload)
            status = "stored"
        elif operation == "retrieve":
            result = self._retrieve_memory(message.payload)
            status = "retrieved"
        elif operation == "search":
            result = self._search_memory(message.payload)
            status = "searched"
        else:
            result = {"error": f"Unknown operation: {operation}"}
            status = "error"
        
        # Log response
        if self.logger:
            summary = f"Memory operation: {operation} - {status}"
            confidence = 0.95 if status != "error" else 0.0
            self.logger.log_agent_response(self.name, summary, confidence)
        
        # Create response
        response = Message(
            sender=self.name,
            recipient=message.sender,
            msg_type=MSG_TYPE_RESPONSE,
            payload={
                "operation": operation,
                "result": result,
                "status": status
            }
        )
        
        return response
    
    def _store_memory(self, payload):
        """
        Store information in memory
        
        Args:
            payload (dict): Storage request payload
            
        Returns:
            dict: Storage result
        """
        memory_type = payload.get("memory_type", "conversation")
        content = payload.get("content", "")
        metadata = payload.get("metadata", {})
        
        memory_id = f"mem_{self.memory_id_counter}"
        self.memory_id_counter += 1
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        memory_record = {
            "id": memory_id,
            "type": memory_type,
            "content": content,
            "metadata": metadata,
            "timestamp": timestamp
        }
        
        # Store in appropriate memory
        if memory_type == "conversation":
            self.conversation_memory.append(memory_record)
        elif memory_type == "knowledge":
            topic = metadata.get("topic", "general")
            if topic not in self.knowledge_base:
                self.knowledge_base[topic] = []
            self.knowledge_base[topic].append(memory_record)
        elif memory_type == "agent_state":
            agent_name = metadata.get("agent", "unknown")
            if agent_name not in self.agent_state_memory:
                self.agent_state_memory[agent_name] = []
            self.agent_state_memory[agent_name].append(memory_record)
        
        # Add to vector store for similarity search
        search_text = f"{metadata.get('topic', '')} {content}"
        self.vector_store.add(memory_id, search_text)
        
        if self.logger:
            self.logger.log_memory_operation(
                "STORE",
                f"Stored {memory_type} memory (ID: {memory_id})"
            )
        
        return {
            "memory_id": memory_id,
            "status": "stored",
            "memory_type": memory_type
        }
    
    def _retrieve_memory(self, payload):
        """
        Retrieve specific memory by ID or criteria
        
        Args:
            payload (dict): Retrieval request payload
            
        Returns:
            dict: Retrieved memories
        """
        memory_type = payload.get("memory_type", "all")
        limit = payload.get("limit", 10)
        
        results = []
        
        if memory_type == "conversation" or memory_type == "all":
            results.extend(self.conversation_memory[-limit:])
        
        if memory_type == "knowledge" or memory_type == "all":
            for topic_memories in self.knowledge_base.values():
                results.extend(topic_memories)
        
        if memory_type == "agent_state" or memory_type == "all":
            for agent_memories in self.agent_state_memory.values():
                results.extend(agent_memories)
        
        # Sort by timestamp and limit
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        results = results[:limit]
        
        if self.logger:
            self.logger.log_memory_operation(
                "RETRIEVE",
                f"Retrieved {len(results)} memories of type {memory_type}"
            )
        
        return {
            "memories": results,
            "count": len(results)
        }
    
    def _search_memory(self, payload):
        """
        Search memory using keywords or vector similarity
        
        Args:
            payload (dict): Search request payload
            
        Returns:
            dict: Search results
        """
        query = payload.get("query", "")
        search_type = payload.get("search_type", "hybrid")
        limit = payload.get("limit", 5)
        
        results = []
        
        # Vector similarity search
        if search_type in ["vector", "hybrid"]:
            similar_ids = self.vector_store.search(query, top_k=limit)
            
            # Retrieve full memory records
            for memory_id, similarity in similar_ids:
                # Find memory in stores
                memory_record = self._find_memory_by_id(memory_id)
                if memory_record:
                    memory_record["similarity_score"] = similarity
                    results.append(memory_record)
        
        # Keyword search
        if search_type in ["keyword", "hybrid"]:
            keyword_results = self._keyword_search(query, limit)
            
            # Merge results (avoid duplicates)
            existing_ids = {r["id"] for r in results}
            for kr in keyword_results:
                if kr["id"] not in existing_ids:
                    kr["similarity_score"] = 0.7  # Default score for keyword match
                    results.append(kr)
        
        # Sort by similarity score
        results.sort(key=lambda x: x.get("similarity_score", 0), reverse=True)
        results = results[:limit]
        
        if self.logger:
            self.logger.log_memory_operation(
                "SEARCH",
                f"Found {len(results)} memories for query: '{query}'"
            )
        
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    
    def _find_memory_by_id(self, memory_id):
        """Find memory record by ID"""
        # Search in all memory stores
        for memory in self.conversation_memory:
            if memory["id"] == memory_id:
                return memory.copy()
        
        for topic_memories in self.knowledge_base.values():
            for memory in topic_memories:
                if memory["id"] == memory_id:
                    return memory.copy()
        
        for agent_memories in self.agent_state_memory.values():
            for memory in agent_memories:
                if memory["id"] == memory_id:
                    return memory.copy()
        
        return None
    
    def _keyword_search(self, query, limit):
        """
        Perform keyword-based search
        
        Args:
            query (str): Search query
            limit (int): Maximum results
            
        Returns:
            list: Matching memories
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        results = []
        
        # Search all memories
        all_memories = []
        all_memories.extend(self.conversation_memory)
        for topic_memories in self.knowledge_base.values():
            all_memories.extend(topic_memories)
        for agent_memories in self.agent_state_memory.values():
            all_memories.extend(agent_memories)
        
        for memory in all_memories:
            content = memory.get("content", "").lower()
            metadata = memory.get("metadata", {})
            topic = metadata.get("topic", "").lower()
            
            # Check for keyword matches
            content_words = set(content.split())
            topic_words = set(topic.split())
            
            match_score = 0
            if query_lower in content or query_lower in topic:
                match_score = 1.0
            else:
                # Calculate word overlap
                overlap = query_words.intersection(content_words.union(topic_words))
                if overlap:
                    match_score = len(overlap) / len(query_words)
            
            if match_score > 0:
                memory_copy = memory.copy()
                memory_copy["match_score"] = match_score
                results.append(memory_copy)
        
        # Sort by match score
        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        return results[:limit]
    
    def store_conversation(self, user_query, agent_name, response, metadata=None):
        """
        Convenience method to store conversation
        
        Args:
            user_query (str): User query
            agent_name (str): Agent that processed it
            response (str): Response given
            metadata (dict): Additional metadata
        """
        meta = metadata or {}
        meta.update({
            "query": user_query,
            "agent": agent_name
        })
        
        payload = {
            "memory_type": "conversation",
            "content": response,
            "metadata": meta
        }
        
        return self._store_memory(payload)
    
    def store_knowledge(self, topic, content, source, confidence, agent_name):
        """
        Convenience method to store knowledge
        
        Args:
            topic (str): Knowledge topic
            content (str): Knowledge content
            source (str): Information source
            confidence (float): Confidence score
            agent_name (str): Agent that produced it
        """
        payload = {
            "memory_type": "knowledge",
            "content": content,
            "metadata": {
                "topic": topic,
                "source": source,
                "confidence": confidence,
                "agent": agent_name
            }
        }
        
        return self._store_memory(payload)
    
    def get_statistics(self):
        """
        Get memory statistics
        
        Returns:
            dict: Memory statistics
        """
        return {
            "conversation_count": len(self.conversation_memory),
            "knowledge_topics": len(self.knowledge_base),
            "total_knowledge": sum(len(v) for v in self.knowledge_base.values()),
            "agent_states": len(self.agent_state_memory),
            "vector_store_size": self.vector_store.size()
        }
    
    def get_capabilities(self):
        """
        Return agent capabilities
        
        Returns:
            dict: Agent capabilities
        """
        return {
            "name": self.name,
            "role": "Memory Management",
            "capabilities": [
                "Store conversation history",
                "Store knowledge with provenance",
                "Store agent state information",
                "Vector similarity search",
                "Keyword search",
                "Hybrid search strategies",
                "Memory retrieval by type and criteria"
            ],
            "memory_types": ["conversation", "knowledge", "agent_state"]
        }
