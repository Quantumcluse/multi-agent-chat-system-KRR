"""
Coordinator Agent - Central controller and orchestrator
"""
from core.message import Message
from core.config import (
    MSG_TYPE_TASK, MSG_TYPE_RESPONSE, MSG_TYPE_RESEARCH, 
    MSG_TYPE_ANALYZE, MSG_TYPE_RETRIEVE, MSG_TYPE_STORE,
    COMPLEXITY_SIMPLE, COMPLEXITY_MEDIUM, COMPLEXITY_COMPLEX
)
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.memory_agent import MemoryAgent

class Coordinator:
    """
    Central coordinator agent that orchestrates multi-agent system
    """
    
    def __init__(self, logger=None):
        """
        Initialize the Coordinator
        
        Args:
            logger: System logger instance
        """
        self.name = "Coordinator"
        self.logger = logger
        
        # Initialize worker agents
        self.research_agent = ResearchAgent(logger=logger)
        self.analysis_agent = AnalysisAgent(logger=logger)
        self.memory_agent = MemoryAgent(logger=logger)
        
        # Execution state
        self.current_query = None
        self.query_context = {}
        self.execution_plan = []
    
    def process_query(self, user_query):
        """
        Process user query through multi-agent system
        
        Args:
            user_query (str): User's natural language query
            
        Returns:
            str: Final synthesized response
        """
        if self.logger:
            self.logger.log_query(user_query)
        
        self.current_query = user_query
        self.query_context = {
            "query": user_query,
            "complexity": None,
            "required_agents": [],
            "execution_steps": []
        }
        
        # Step 1: Analyze query complexity and intent
        complexity = self._analyze_complexity(user_query)
        self.query_context["complexity"] = complexity
        
        if self.logger:
            self.logger.log_decision(
                self.name,
                f"Query complexity: {complexity}",
                f"Based on keywords and structure analysis"
            )
        
        # Step 2: Check memory for relevant prior knowledge
        memory_results = self._check_memory(user_query)
        
        # Step 3: Determine required agents and create execution plan
        plan = self._create_execution_plan(user_query, complexity, memory_results)
        self.execution_plan = plan
        
        if self.logger:
            plan_summary = " -> ".join([step["agent"] for step in plan])
            self.logger.log_decision(
                self.name,
                f"Execution plan created: {plan_summary}",
                f"Plan includes {len(plan)} steps based on query requirements"
            )
        
        # Step 4: Execute plan
        execution_results = self._execute_plan(plan)
        
        # Step 5: Synthesize final response
        final_response = self._synthesize_response(execution_results, memory_results)
        
        # Step 6: Store interaction in memory
        self._store_interaction(user_query, final_response, execution_results)
        
        if self.logger:
            self.logger.log_final_response(final_response)
        
        return final_response
    
    def _analyze_complexity(self, query):
        """
        Analyze query complexity
        
        Args:
            query (str): User query
            
        Returns:
            str: Complexity level
        """
        query_lower = query.lower()
        
        # Keywords indicating complexity
        complex_keywords = [
            "compare", "analyze", "evaluate", "research and",
            "find and", "identify and", "synthesize", "trade-offs",
            "trade-off", "advantages and disadvantages", "pros and cons"
        ]
        
        medium_keywords = [
            "explain", "describe", "how", "why", "relationship",
            "difference", "similarity", "methodology"
        ]
        
        memory_keywords = [
            "earlier", "previous", "before", "discussed", 
            "we talked", "mentioned", "said"
        ]
        
        # Check for memory queries
        if any(keyword in query_lower for keyword in memory_keywords):
            return COMPLEXITY_SIMPLE
        
        # Check for complex queries
        if any(keyword in query_lower for keyword in complex_keywords):
            return COMPLEXITY_COMPLEX
        
        # Check for medium queries
        if any(keyword in query_lower for keyword in medium_keywords):
            return COMPLEXITY_MEDIUM
        
        # Check for multiple clauses or questions
        if query.count("?") > 1 or query.count(",") > 2:
            return COMPLEXITY_COMPLEX
        
        # Default to simple
        return COMPLEXITY_SIMPLE
    
    def _check_memory(self, query):
        """
        Check memory for relevant information
        
        Args:
            query (str): User query
            
        Returns:
            dict: Memory search results
        """
        if self.logger:
            self.logger.log_agent_call(
                self.name,
                self.memory_agent.name,
                "Search for relevant prior knowledge"
            )
        
        message = Message(
            sender=self.name,
            recipient=self.memory_agent.name,
            msg_type=MSG_TYPE_RETRIEVE,
            payload={
                "operation": "search",
                "query": query,
                "search_type": "hybrid",
                "limit": 5
            }
        )
        
        response = self.memory_agent.process_message(message)
        results = response.payload.get("result", {})
        
        memory_count = results.get("count", 0)
        if memory_count > 0 and self.logger:
            self.logger.log_decision(
                self.name,
                f"Found {memory_count} relevant memories",
                "Will incorporate prior knowledge into response"
            )
        
        return results
    
    def _create_execution_plan(self, query, complexity, memory_results):
        """
        Create execution plan based on query analysis
        
        Args:
            query (str): User query
            complexity (str): Query complexity
            memory_results (dict): Results from memory search
            
        Returns:
            list: Execution plan steps
        """
        plan = []
        query_lower = query.lower()
        
        # Check if this is a memory-only query
        memory_keywords = ["earlier", "previous", "before", "discussed", "we talked"]
        if any(keyword in query_lower for keyword in memory_keywords):
            # Memory retrieval only
            plan.append({
                "step": 1,
                "agent": "MemoryAgent",
                "action": "retrieve_conversation",
                "reason": "Query asks about previous conversation"
            })
            return plan
        
        # Determine if research is needed
        needs_research = True
        research_topics = self._extract_research_topics(query)
        
        # Check if memory has sufficient information
        if memory_results.get("count", 0) > 0:
            memory_confidence = sum(
                m.get("similarity_score", 0) 
                for m in memory_results.get("results", [])
            ) / max(memory_results.get("count", 1), 1)
            
            if memory_confidence > 0.8 and complexity == COMPLEXITY_SIMPLE:
                needs_research = False
                if self.logger:
                    self.logger.log_decision(
                        self.name,
                        "Skipping research - sufficient memory",
                        f"Memory confidence: {memory_confidence:.2f}"
                    )
        
        step_num = 1
        
        # Research step
        if needs_research and research_topics:
            for topic in research_topics:
                plan.append({
                    "step": step_num,
                    "agent": "ResearchAgent",
                    "action": "research",
                    "topic": topic,
                    "reason": f"Retrieve information about {topic}"
                })
                step_num += 1
        
        # Analysis step (for medium and complex queries)
        if complexity in [COMPLEXITY_MEDIUM, COMPLEXITY_COMPLEX]:
            analysis_type = self._determine_analysis_type(query)
            
            plan.append({
                "step": step_num,
                "agent": "AnalysisAgent",
                "action": "analyze",
                "analysis_type": analysis_type,
                "reason": f"Perform {analysis_type} analysis on research results",
                "depends_on": list(range(1, step_num))
            })
            step_num += 1
        
        return plan
    
    def _extract_research_topics(self, query):
        """
        Extract research topics from query
        
        Args:
            query (str): User query
            
        Returns:
            list: Research topics
        """
        query_lower = query.lower()
        topics = []
        
        # Key topics to search for
        topic_keywords = {
            "neural networks": ["neural network", "neural net"],
            "transformers": ["transformer", "transformer architecture"],
            "reinforcement learning": ["reinforcement learning", "rl", "reinforcement"],
            "machine learning": ["machine learning", "ml"],
            "deep learning": ["deep learning"],
            "cnn": ["cnn", "convolutional"],
            "rnn": ["rnn", "recurrent"],
        }
        
        # Extract topics
        for topic, keywords in topic_keywords.items():
            if any(kw in query_lower for kw in keywords):
                topics.append(topic)
        
        # If no specific topics, extract general topic
        if not topics:
            words = query_lower.split()
            # Remove common words
            stop_words = {"what", "are", "the", "is", "a", "an", "how", "why", "about"}
            meaningful_words = [w for w in words if w not in stop_words and len(w) > 3]
            if meaningful_words:
                topics.append(" ".join(meaningful_words[:3]))
        
        return topics[:2]  # Limit to 2 topics
    
    def _determine_analysis_type(self, query):
        """
        Determine type of analysis needed
        
        Args:
            query (str): User query
            
        Returns:
            str: Analysis type
        """
        query_lower = query.lower()
        
        if "compare" in query_lower or "comparison" in query_lower:
            return "comparison"
        elif "trade-off" in query_lower or "tradeoffs" in query_lower:
            return "trade_offs"
        elif "methodology" in query_lower or "methods" in query_lower:
            return "methodology"
        elif "challenge" in query_lower or "challenges" in query_lower:
            return "challenges"
        elif "analyze" in query_lower or "analysis" in query_lower:
            return "synthesis"
        else:
            return "general"
    
    def _execute_plan(self, plan):
        """
        Execute the planned steps
        
        Args:
            plan (list): Execution plan
            
        Returns:
            list: Execution results
        """
        results = []
        research_data = []
        
        for step in plan:
            agent_name = step["agent"]
            action = step["action"]
            
            if self.logger:
                self.logger.log_agent_call(
                    self.name,
                    agent_name,
                    step["reason"]
                )
            
            if agent_name == "ResearchAgent":
                result = self._call_research_agent(step, research_data)
                if result:
                    research_data.extend(result.get("results", []))
                results.append({
                    "agent": agent_name,
                    "action": action,
                    "result": result
                })
            
            elif agent_name == "AnalysisAgent":
                result = self._call_analysis_agent(step, research_data)
                results.append({
                    "agent": agent_name,
                    "action": action,
                    "result": result
                })
            
            elif agent_name == "MemoryAgent":
                result = self._call_memory_agent(step)
                results.append({
                    "agent": agent_name,
                    "action": action,
                    "result": result
                })
        
        return results
    
    def _call_research_agent(self, step, existing_data):
        """Call research agent with retry logic"""
        topic = step.get("topic", "")
        
        message = Message(
            sender=self.name,
            recipient=self.research_agent.name,
            msg_type=MSG_TYPE_RESEARCH,
            payload={
                "query": topic,
                "task": step["reason"]
            }
        )
        
        try:
            response = self.research_agent.process_message(message)
            return response.payload
        except Exception as e:
            if self.logger:
                self.logger.log_decision(
                    self.name,
                    "Research agent error - applying fallback",
                    f"Error: {str(e)}"
                )
            return {"results": [], "status": "error"}
    
    def _call_analysis_agent(self, step, research_data):
        """Call analysis agent"""
        analysis_type = step.get("analysis_type", "general")
        
        message = Message(
            sender=self.name,
            recipient=self.analysis_agent.name,
            msg_type=MSG_TYPE_ANALYZE,
            payload={
                "task": step["reason"],
                "data": research_data,
                "analysis_type": analysis_type
            }
        )
        
        try:
            response = self.analysis_agent.process_message(message)
            return response.payload
        except Exception as e:
            if self.logger:
                self.logger.log_decision(
                    self.name,
                    "Analysis agent error - applying fallback",
                    f"Error: {str(e)}"
                )
            return {"analysis": {"type": "error"}, "status": "error"}
    
    def _call_memory_agent(self, step):
        """Call memory agent"""
        action = step.get("action", "retrieve")
        
        if action == "retrieve_conversation":
            message = Message(
                sender=self.name,
                recipient=self.memory_agent.name,
                msg_type=MSG_TYPE_RETRIEVE,
                payload={
                    "operation": "retrieve",
                    "memory_type": "conversation",
                    "limit": 10
                }
            )
        else:
            message = Message(
                sender=self.name,
                recipient=self.memory_agent.name,
                msg_type=MSG_TYPE_RETRIEVE,
                payload={
                    "operation": "retrieve",
                    "memory_type": "all",
                    "limit": 5
                }
            )
        
        try:
            response = self.memory_agent.process_message(message)
            return response.payload
        except Exception as e:
            if self.logger:
                self.logger.log_decision(
                    self.name,
                    "Memory agent error - applying fallback",
                    f"Error: {str(e)}"
                )
            return {"result": {"memories": []}, "status": "error"}
    
    def _synthesize_response(self, execution_results, memory_results):
        """
        Synthesize final response from execution results
        
        Args:
            execution_results (list): Results from plan execution
            memory_results (dict): Results from memory search
            
        Returns:
            str: Final response
        """
        response_parts = []
        
        # Check for memory-only queries
        if len(execution_results) == 1 and execution_results[0]["agent"] == "MemoryAgent":
            memories = execution_results[0]["result"].get("result", {}).get("memories", [])
            if memories:
                response_parts.append("Based on our previous conversation:\n")
                for i, mem in enumerate(memories[:3], 1):
                    content = mem.get("content", "")
                    metadata = mem.get("metadata", {})
                    topic = metadata.get("topic", "")
                    if topic:
                        response_parts.append(f"\n{i}. Regarding {topic}:")
                    response_parts.append(f"   {content[:200]}")
            else:
                response_parts.append("I don't have any relevant information from our previous conversations.")
            
            return "\n".join(response_parts)
        
        # Synthesize from research and analysis
        research_results = []
        analysis_results = []
        
        for exec_result in execution_results:
            if exec_result["agent"] == "ResearchAgent":
                results = exec_result["result"].get("results", [])
                research_results.extend(results)
            elif exec_result["agent"] == "AnalysisAgent":
                analysis_results.append(exec_result["result"].get("analysis", {}))
        
        # Build response
        if research_results:
            # Check if we have memory context
            if memory_results.get("count", 0) > 0:
                response_parts.append("Building on our previous discussion and new research:\n")
            
            # Add research findings
            for i, result in enumerate(research_results, 1):
                topic = result.get("topic", "")
                summary = result.get("summary", "")
                details = result.get("details", "")
                
                response_parts.append(f"\n{i}. {topic.title()}:")
                response_parts.append(f"   {summary}")
                if details and details != summary:
                    response_parts.append(f"   {details}")
        
        # Add analysis if present
        if analysis_results:
            for analysis in analysis_results:
                analysis_type = analysis.get("type", "")
                
                response_parts.append(f"\n\nAnalysis ({analysis_type}):")
                
                if analysis_type == "comparison":
                    comparisons = analysis.get("comparisons", [])
                    for comp in comparisons:
                        approach = comp.get("approach", "")
                        description = comp.get("description", "")
                        response_parts.append(f"\n- {approach}: {description}")
                    
                    recommendation = analysis.get("recommendation", "")
                    if recommendation:
                        response_parts.append(f"\nRecommendation: {recommendation}")
                
                elif analysis_type == "trade_off_analysis":
                    tradeoffs = analysis.get("tradeoffs", [])
                    for to in tradeoffs:
                        approach = to.get("approach", "")
                        response_parts.append(f"\n- {approach}:")
                        response_parts.append(f"  Advantages: {', '.join(to.get('advantages', []))}")
                        response_parts.append(f"  Disadvantages: {', '.join(to.get('disadvantages', []))}")
                
                elif analysis_type == "challenge_identification":
                    challenges_by_area = analysis.get("challenges_by_area", [])
                    for area_challenges in challenges_by_area:
                        area = area_challenges.get("area", "")
                        challenges = area_challenges.get("challenges", [])
                        response_parts.append(f"\n- {area}: {', '.join(challenges)}")
                    
                    common = analysis.get("common_challenges", [])
                    if common:
                        response_parts.append(f"\nCommon challenges: {', '.join(common)}")
                
                else:
                    # General analysis
                    summary = analysis.get("summary", "")
                    if summary:
                        response_parts.append(f"\n{summary}")
        
        if not response_parts:
            response_parts.append("I don't have enough information to provide a comprehensive answer to your query.")
        
        return "\n".join(response_parts)
    
    def _store_interaction(self, query, response, execution_results):
        """
        Store interaction in memory
        
        Args:
            query (str): User query
            response (str): System response
            execution_results (list): Execution results
        """
        # Store conversation
        self.memory_agent.store_conversation(
            user_query=query,
            agent_name=self.name,
            response=response,
            metadata={"complexity": self.query_context.get("complexity")}
        )
        
        # Store knowledge from research
        for exec_result in execution_results:
            if exec_result["agent"] == "ResearchAgent":
                results = exec_result["result"].get("results", [])
                for result in results:
                    topic = result.get("topic", "")
                    summary = result.get("summary", "")
                    source = result.get("source", "")
                    confidence = result.get("confidence", 0.8)
                    
                    self.memory_agent.store_knowledge(
                        topic=topic,
                        content=summary,
                        source=source,
                        confidence=confidence,
                        agent_name="ResearchAgent"
                    )
        
        if self.logger:
            stats = self.memory_agent.get_statistics()
            self.logger.log_memory_operation(
                "STORE_INTERACTION",
                f"Stored interaction. Memory stats: {stats}"
            )
    
    def get_system_status(self):
        """
        Get current system status
        
        Returns:
            dict: System status
        """
        return {
            "coordinator": self.name,
            "agents": {
                "research": self.research_agent.get_capabilities(),
                "analysis": self.analysis_agent.get_capabilities(),
                "memory": self.memory_agent.get_capabilities()
            },
            "memory_stats": self.memory_agent.get_statistics(),
            "current_query": self.current_query,
            "query_context": self.query_context
        }
