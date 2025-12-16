"""
Research Agent - Simulates information retrieval
"""
from core.message import Message
from core.config import MSG_TYPE_RESPONSE, MSG_TYPE_RESEARCH
from memory.knowledge_base import search_knowledge, KNOWLEDGE_DB

class ResearchAgent:
    """
    Agent responsible for retrieving information from knowledge base
    """
    
    def __init__(self, name="ResearchAgent", logger=None):
        """
        Initialize the Research Agent
        
        Args:
            name (str): Agent name
            logger: System logger instance
        """
        self.name = name
        self.logger = logger
    
    def process_message(self, message):
        """
        Process incoming message and perform research
        
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
        
        query = message.payload.get("query", "")
        task_description = message.payload.get("task", query)
        
        # Perform research
        results = self._research(query)
        
        # Log response
        if self.logger:
            summary = f"Found {len(results)} results for '{query}'"
            confidence = results[0]["confidence"] if results else 0.0
            self.logger.log_agent_response(self.name, summary, confidence)
        
        # Create response
        response = Message(
            sender=self.name,
            recipient=message.sender,
            msg_type=MSG_TYPE_RESPONSE,
            payload={
                "query": query,
                "results": results,
                "task": task_description,
                "status": "completed" if results else "no_results"
            }
        )
        
        return response
    
    def _research(self, query):
        """
        Perform research in knowledge base
        
        Args:
            query (str): Research query
            
        Returns:
            list: List of research results
        """
        results = []
        query_lower = query.lower()
        
        # Search for direct and partial matches
        matched_topics = []
        
        for topic in KNOWLEDGE_DB.keys():
            if topic in query_lower or any(word in topic for word in query_lower.split()):
                matched_topics.append(topic)
        
        # If no matches, search more broadly
        if not matched_topics:
            # Try finding any keyword match
            query_words = set(query_lower.split())
            for topic in KNOWLEDGE_DB.keys():
                topic_words = set(topic.split())
                if query_words.intersection(topic_words):
                    matched_topics.append(topic)
        
        # Get knowledge for matched topics
        for topic in matched_topics:
            knowledge = KNOWLEDGE_DB[topic]
            results.append({
                "topic": topic,
                "summary": knowledge["summary"],
                "details": knowledge.get("details", knowledge["summary"]),
                "source": knowledge["source"],
                "confidence": knowledge["confidence"]
            })
        
        # If still no results, return general info
        if not results and "machine learning" in KNOWLEDGE_DB:
            knowledge = KNOWLEDGE_DB["machine learning"]
            results.append({
                "topic": "machine learning (general)",
                "summary": "General machine learning information as fallback.",
                "details": knowledge["summary"],
                "source": knowledge["source"],
                "confidence": 0.6
            })
        
        return results
    
    def get_capabilities(self):
        """
        Return agent capabilities
        
        Returns:
            dict: Agent capabilities
        """
        return {
            "name": self.name,
            "role": "Information Retrieval",
            "capabilities": [
                "Search knowledge base",
                "Retrieve information on ML/AI topics",
                "Provide structured research results",
                "Return source provenance and confidence scores"
            ],
            "no_capabilities": [
                "Cannot perform analysis or reasoning",
                "Cannot compare or synthesize information",
                "Cannot perform calculations"
            ]
        }
