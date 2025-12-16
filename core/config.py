"""
Configuration constants for the multi-agent system
"""

# Memory Configuration
VECTOR_DIMENSION = 384
SIMILARITY_THRESHOLD = 0.75
MAX_SEARCH_RESULTS = 5

# Agent Configuration
AGENTS = {
    "coordinator": "Coordinator",
    "research": "ResearchAgent",
    "analysis": "AnalysisAgent",
    "memory": "MemoryAgent"
}

# Confidence Thresholds
MIN_CONFIDENCE = 0.5
HIGH_CONFIDENCE = 0.8

# Query Complexity Levels
COMPLEXITY_SIMPLE = "simple"
COMPLEXITY_MEDIUM = "medium"
COMPLEXITY_COMPLEX = "complex"

# Message Types
MSG_TYPE_TASK = "task"
MSG_TYPE_RESPONSE = "response"
MSG_TYPE_QUERY = "query"
MSG_TYPE_STORE = "store"
MSG_TYPE_RETRIEVE = "retrieve"
MSG_TYPE_RESEARCH = "research"
MSG_TYPE_ANALYZE = "analyze"
MSG_TYPE_MEMORY_QUERY = "memory_query"

# Logging
LOG_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "system.log"

# Task Types
TASK_RESEARCH = "research"
TASK_ANALYSIS = "analysis"
TASK_MEMORY = "memory"
TASK_SYNTHESIS = "synthesis"