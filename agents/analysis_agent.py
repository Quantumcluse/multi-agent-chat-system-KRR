"""
Analysis Agent - Performs reasoning and analysis on data
"""
from core.message import Message
from core.config import MSG_TYPE_RESPONSE, MSG_TYPE_ANALYZE

class AnalysisAgent:
    """
    Agent responsible for analysis, reasoning, and synthesis
    """
    
    def __init__(self, name="AnalysisAgent", logger=None):
        """
        Initialize the Analysis Agent
        
        Args:
            name (str): Agent name
            logger: System logger instance
        """
        self.name = name
        self.logger = logger
    
    def process_message(self, message):
        """
        Process incoming message and perform analysis
        
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
        
        task = message.payload.get("task", "")
        data = message.payload.get("data", [])
        analysis_type = message.payload.get("analysis_type", "general")
        
        # Perform analysis
        analysis_result = self._analyze(data, analysis_type, task)
        
        # Log response
        if self.logger:
            summary = f"Completed {analysis_type} analysis"
            confidence = analysis_result.get("confidence", 0.8)
            self.logger.log_agent_response(self.name, summary, confidence)
        
        # Create response
        response = Message(
            sender=self.name,
            recipient=message.sender,
            msg_type=MSG_TYPE_RESPONSE,
            payload={
                "task": task,
                "analysis": analysis_result,
                "status": "completed"
            }
        )
        
        return response
    
    def _analyze(self, data, analysis_type, task):
        """
        Perform analysis on provided data
        
        Args:
            data (list): Data to analyze (typically from ResearchAgent)
            analysis_type (str): Type of analysis
            task (str): Task description
            
        Returns:
            dict: Analysis results
        """
        if analysis_type == "comparison":
            return self._compare_data(data, task)
        elif analysis_type == "synthesis":
            return self._synthesize_data(data, task)
        elif analysis_type == "trade_offs":
            return self._analyze_tradeoffs(data, task)
        elif analysis_type == "methodology":
            return self._analyze_methodology(data, task)
        elif analysis_type == "challenges":
            return self._identify_challenges(data, task)
        else:
            return self._general_analysis(data, task)
    
    def _compare_data(self, data, task):
        """Compare different approaches or concepts"""
        if len(data) < 2:
            return {
                "comparison": "Insufficient data for comparison",
                "confidence": 0.3
            }
        
        comparisons = []
        for i, item in enumerate(data):
            topic = item.get("topic", f"Item {i+1}")
            summary = item.get("summary", "")
            details = item.get("details", "")
            
            comparisons.append({
                "approach": topic,
                "description": summary,
                "analysis": details
            })
        
        # Generate recommendation
        recommendation = self._generate_recommendation(data, task)
        
        return {
            "type": "comparison",
            "items_compared": len(data),
            "comparisons": comparisons,
            "recommendation": recommendation,
            "confidence": 0.85
        }
    
    def _synthesize_data(self, data, task):
        """Synthesize multiple pieces of information"""
        key_points = []
        sources = []
        
        for item in data:
            topic = item.get("topic", "")
            summary = item.get("summary", "")
            source = item.get("source", "Unknown")
            
            key_points.append(f"{topic}: {summary}")
            if source not in sources:
                sources.append(source)
        
        synthesis = " ".join(key_points)
        
        return {
            "type": "synthesis",
            "key_points": key_points,
            "synthesis": synthesis,
            "sources_consulted": sources,
            "confidence": 0.82
        }
    
    def _analyze_tradeoffs(self, data, task):
        """Analyze trade-offs in approaches"""
        tradeoffs = []
        
        for item in data:
            topic = item.get("topic", "")
            details = item.get("details", "")
            
            # Extract trade-offs from details
            advantages = []
            disadvantages = []
            
            if "trade-off" in details.lower() or "trade-offs" in details.lower():
                parts = details.split("Trade-offs:")
                if len(parts) > 1:
                    tradeoff_text = parts[1]
                    
                    if "but" in tradeoff_text.lower():
                        pros_cons = tradeoff_text.split("but")
                        advantages.append(pros_cons[0].strip())
                        disadvantages.append(pros_cons[1].strip())
                    else:
                        disadvantages.append(tradeoff_text.strip())
            
            # General extraction
            if "excellent" in details.lower() or "good" in details.lower():
                advantages.append(f"{topic} shows strong performance in specific areas")
            if "expensive" in details.lower() or "require" in details.lower():
                disadvantages.append(f"{topic} has resource requirements")
            
            tradeoffs.append({
                "approach": topic,
                "advantages": advantages if advantages else ["Specific strengths in domain"],
                "disadvantages": disadvantages if disadvantages else ["Resource considerations"],
                "summary": item.get("summary", "")
            })
        
        return {
            "type": "trade_off_analysis",
            "tradeoffs": tradeoffs,
            "overall_conclusion": self._conclude_tradeoffs(tradeoffs),
            "confidence": 0.80
        }
    
    def _analyze_methodology(self, data, task):
        """Analyze methodologies in research"""
        methodologies = []
        
        for item in data:
            topic = item.get("topic", "")
            details = item.get("details", "")
            
            # Extract methodology information
            methods = []
            if "methods" in details.lower() or "algorithms" in details.lower():
                # Extract key methods mentioned
                for method_keyword in ["DQN", "PPO", "Q-Learning", "Policy Gradient", 
                                      "LSTM", "GRU", "CNN", "RNN", "Transformer"]:
                    if method_keyword.lower() in details.lower():
                        methods.append(method_keyword)
            
            methodologies.append({
                "topic": topic,
                "methods_identified": methods if methods else ["Domain-specific approaches"],
                "description": item.get("summary", "")
            })
        
        return {
            "type": "methodology_analysis",
            "methodologies": methodologies,
            "common_approaches": self._find_common_approaches(methodologies),
            "confidence": 0.78
        }
    
    def _identify_challenges(self, data, task):
        """Identify challenges from research data"""
        all_challenges = []
        
        for item in data:
            topic = item.get("topic", "")
            details = item.get("details", "")
            
            challenges = []
            
            # Extract challenges
            if "challenge" in details.lower():
                parts = details.split("Challenges")
                if len(parts) > 1:
                    challenge_text = parts[1]
                    # Extract individual challenges
                    if "include" in challenge_text.lower():
                        challenge_parts = challenge_text.split("include")
                        if len(challenge_parts) > 1:
                            challenge_list = challenge_parts[1].split(",")
                            challenges = [c.strip().rstrip(".") for c in challenge_list[:3]]
            
            # Generic challenges if none found
            if not challenges:
                if "data" in details.lower():
                    challenges.append("Data requirements and availability")
                if "computational" in details.lower() or "compute" in details.lower():
                    challenges.append("Computational resource requirements")
                if "complex" in details.lower():
                    challenges.append("System complexity and implementation")
            
            all_challenges.append({
                "area": topic,
                "challenges": challenges if challenges else ["Implementation considerations"]
            })
        
        return {
            "type": "challenge_identification",
            "challenges_by_area": all_challenges,
            "common_challenges": self._find_common_challenges(all_challenges),
            "confidence": 0.83
        }
    
    def _general_analysis(self, data, task):
        """Perform general analysis"""
        insights = []
        
        for item in data:
            topic = item.get("topic", "")
            summary = item.get("summary", "")
            confidence = item.get("confidence", 0.8)
            
            insights.append({
                "topic": topic,
                "insight": summary,
                "confidence": confidence
            })
        
        return {
            "type": "general_analysis",
            "insights": insights,
            "summary": f"Analyzed {len(data)} information sources",
            "confidence": 0.80
        }
    
    def _generate_recommendation(self, data, task):
        """Generate recommendation based on comparison"""
        if not data:
            return "Insufficient data for recommendation"
        
        # Find highest confidence item
        best_item = max(data, key=lambda x: x.get("confidence", 0))
        topic = best_item.get("topic", "")
        
        return f"Based on the analysis, {topic} appears most suitable due to its strong foundation and proven effectiveness in the domain."
    
    def _conclude_tradeoffs(self, tradeoffs):
        """Generate conclusion from trade-offs"""
        return f"Analysis of {len(tradeoffs)} approaches reveals that each has specific strengths and limitations. Selection should be based on specific use case requirements and available resources."
    
    def _find_common_approaches(self, methodologies):
        """Find common approaches across methodologies"""
        all_methods = []
        for m in methodologies:
            all_methods.extend(m.get("methods_identified", []))
        
        # Count occurrences
        method_counts = {}
        for method in all_methods:
            method_counts[method] = method_counts.get(method, 0) + 1
        
        # Return most common
        common = sorted(method_counts.items(), key=lambda x: x[1], reverse=True)
        return [m[0] for m in common[:3]] if common else ["Various domain-specific methods"]
    
    def _find_common_challenges(self, all_challenges):
        """Find common challenges across areas"""
        challenge_list = []
        for area in all_challenges:
            challenge_list.extend(area.get("challenges", []))
        
        # Count occurrences
        challenge_counts = {}
        for challenge in challenge_list:
            challenge_counts[challenge] = challenge_counts.get(challenge, 0) + 1
        
        # Return most common
        common = sorted(challenge_counts.items(), key=lambda x: x[1], reverse=True)
        return [c[0] for c in common[:3]] if common else ["Implementation and resource considerations"]
    
    def get_capabilities(self):
        """
        Return agent capabilities
        
        Returns:
            dict: Agent capabilities
        """
        return {
            "name": self.name,
            "role": "Analysis and Reasoning",
            "capabilities": [
                "Compare different approaches",
                "Analyze trade-offs",
                "Synthesize information",
                "Identify challenges and methodologies",
                "Generate recommendations",
                "Perform calculations and reasoning"
            ],
            "no_capabilities": [
                "Cannot retrieve new information",
                "Cannot access external knowledge bases"
            ]
        }
