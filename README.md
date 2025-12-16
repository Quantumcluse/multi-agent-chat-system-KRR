# Multi-Agent Chat System
## Knowledge Representation & Reasoning Assignment

A sophisticated multi-agent system demonstrating agent coordination, structured memory with vector similarity search, and autonomous reasoning for natural language query processing.

---

## 📋 Table of Contents

- [System Overview](#system-overview)
- [Architecture](#architecture)
- [Agent Roles](#agent-roles)
- [Memory Design](#memory-design)
- [Communication Protocol](#communication-protocol)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Test Scenarios](#test-scenarios)
- [Project Structure](#project-structure)
- [Design Decisions](#design-decisions)

---

## 🎯 System Overview

This multi-agent system implements a coordinated approach to answering complex natural language queries about machine learning and artificial intelligence topics. The system demonstrates:

- **Agent Orchestration**: Coordinator agent manages task decomposition and agent sequencing
- **Structured Memory**: Vector similarity search with FAISS for semantic retrieval
- **Autonomous Decision-Making**: Dynamic query analysis and execution planning
- **Traceability**: Comprehensive logging of all agent communications and decisions
- **Persistent Knowledge**: Memory reuse to avoid redundant work

### Key Features

✅ **Role Separation**: Each agent has distinct responsibilities (no overlap)  
✅ **Centralized Coordination**: All inter-agent communication through Coordinator  
✅ **Memory-Driven Adaptation**: System learns from past interactions  
✅ **Confidence Scoring**: All results include confidence/similarity metrics  
✅ **Fallback Mechanisms**: Graceful error handling and degradation  
✅ **Console-Based**: Interactive terminal interface  

---

## 🏗️ Architecture

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ Query
       ▼
┌─────────────────────────────────────┐
│      COORDINATOR AGENT              │
│  (Central Orchestrator & Manager)   │
│                                     │
│  • Analyzes query complexity        │
│  • Consults memory                  │
│  • Creates execution plan           │
│  • Routes tasks to agents           │
│  • Synthesizes final response       │
└───┬─────────┬──────────┬───────────┘
    │         │          │
    ▼         ▼          ▼
┌─────────┐ ┌──────────┐ ┌─────────────┐
│Research │ │ Analysis │ │   Memory    │
│ Agent   │ │  Agent   │ │   Agent     │
├─────────┤ ├──────────┤ ├─────────────┤
│• Search │ │• Reason  │ │• Store      │
│• Retrieve│ │• Compare │ │• Retrieve   │
│• Return │ │• Analyze │ │• Search     │
│  results│ │• Synthesize│ │  (Vector)  │
└─────────┘ └──────────┘ └─────────────┘
```

### Execution Flow

1. **Query Reception**: User submits natural language query
2. **Complexity Analysis**: Coordinator analyzes query structure and keywords
3. **Memory Consultation**: Check for relevant prior knowledge (vector search)
4. **Plan Creation**: Generate sequential execution plan
5. **Agent Coordination**: Execute plan, calling agents as needed
6. **Response Synthesis**: Merge results into coherent response
7. **Memory Storage**: Persist interaction and knowledge

---

## 🤖 Agent Roles

### 1️⃣ Coordinator Agent (Manager)

**Role**: Central controller and orchestrator

**Responsibilities**:
- Receive and analyze user queries
- Determine query complexity (simple/medium/complex)
- Consult memory for relevant prior knowledge
- Decompose complex tasks into subtasks
- Create execution plans with agent sequencing
- Route messages to appropriate agents
- Handle dependencies between agent tasks
- Synthesize final responses
- Implement fallback strategies
- Maintain conversation context
- Store interactions in memory

**Decision-Making**:
```python
Complexity Analysis:
  - Keywords: "compare", "analyze", "research and" → Complex
  - Keywords: "explain", "how", "why" → Medium
  - Keywords: "what", "list" → Simple
  - Memory queries: "earlier", "discussed" → Simple

Agent Selection:
  - Research needed? → ResearchAgent
  - Analysis required? → AnalysisAgent  
  - Memory sufficient? → Skip research
  - Comparison needed? → Research + Analysis
```

### 2️⃣ Research Agent

**Role**: Information retrieval specialist

**Responsibilities**:
- Search mock knowledge base
- Retrieve structured information
- Return results with provenance
- Provide confidence scores

**Output Format**:
```python
{
  "topic": "transformer architecture",
  "summary": "Brief description...",
  "details": "Extended information...",
  "source": "NLP Research Papers",
  "confidence": 0.92
}
```

**Constraints**:
- ❌ NO reasoning or analysis
- ❌ NO comparison or synthesis
- ❌ NO calculation

### 3️⃣ Analysis Agent

**Role**: Reasoning and synthesis specialist

**Responsibilities**:
- Perform comparisons
- Analyze trade-offs
- Synthesize information
- Identify challenges
- Analyze methodologies
- Generate recommendations

**Analysis Types**:
- `comparison`: Compare multiple approaches
- `trade_offs`: Identify advantages/disadvantages
- `methodology`: Extract research methods
- `challenges`: Identify common problems
- `synthesis`: Merge information sources

**Constraints**:
- ❌ NO information retrieval
- ❌ NO external knowledge access
- ✅ ONLY works with provided data

### 4️⃣ Memory Agent

**Role**: Knowledge and state management

**Responsibilities**:
- Store conversation history
- Manage knowledge base
- Track agent state
- Vector similarity search
- Keyword search
- Hybrid search strategies

**Memory Types**:

1. **Conversation Memory**
   - Full interaction history
   - Timestamps and metadata
   - User queries and responses

2. **Knowledge Base**
   - Learned facts and findings
   - Source provenance
   - Confidence scores
   - Topic organization

3. **Agent State Memory**
   - What each agent learned
   - Task accomplishments
   - Per-task records

**Search Strategies**:
- **Vector Search**: Semantic similarity using FAISS
- **Keyword Search**: Text matching and overlap
- **Hybrid Search**: Combines both approaches

---

## 💾 Memory Design

### Vector Store Architecture

```python
VectorStore (FAISS-based)
│
├── Text Vectorization
│   └── Word-based hashing → 384-dim vectors
│
├── Similarity Search
│   └── L2 distance → Similarity scores
│
└── Memory Records
    └── ID → Vector mapping
```

### Memory Record Structure

```python
{
  "id": "mem_0",
  "type": "conversation|knowledge|agent_state",
  "content": "Actual content...",
  "metadata": {
    "topic": "neural networks",
    "agent": "ResearchAgent",
    "source": "AI Research Database",
    "confidence": 0.95
  },
  "timestamp": "2025-12-16 10:30:45"
}
```

### Retrieval Strategy

1. **Vector Similarity**: Convert query to vector, find nearest neighbors
2. **Keyword Matching**: Extract query words, match against content
3. **Score Fusion**: Combine similarity + keyword match scores
4. **Ranking**: Sort by relevance, return top-k results

### Memory Influence on Decisions

```
High Memory Confidence (>0.8) + Simple Query
  → Skip research, use memory directly

Medium Memory Confidence (0.5-0.8)
  → Research + merge with memory

Low/No Memory
  → Full research + analysis pipeline
```

---

## 📡 Communication Protocol

### Message Structure

```python
Message {
  "msg_id": "msg_20251216_103045_123456",
  "sender": "Coordinator",
  "recipient": "ResearchAgent",
  "msg_type": "task|response|query|store|retrieve",
  "payload": {
    "query": "transformer architectures",
    "task": "Retrieve information about...",
    ...additional data...
  },
  "timestamp": "2025-12-16 10:30:45"
}
```

### Communication Rules

⚠️ **STRICT CONSTRAINT**: Agents NEVER communicate directly

```
✅ ALLOWED:  Agent → Coordinator → Agent
❌ FORBIDDEN: Agent → Agent (direct)
```

### Message Flow Example

```
User Query: "Compare CNNs and RNNs"
│
├─> Coordinator analyzes → Determines: Complex Query
│
├─> Coordinator → MemoryAgent: "Search for CNN/RNN info"
│   └─> MemoryAgent → Coordinator: [Memory results]
│
├─> Coordinator → ResearchAgent: "Retrieve CNN info"
│   └─> ResearchAgent → Coordinator: [CNN data]
│
├─> Coordinator → ResearchAgent: "Retrieve RNN info"
│   └─> ResearchAgent → Coordinator: [RNN data]
│
├─> Coordinator → AnalysisAgent: "Compare CNN and RNN"
│   └─> AnalysisAgent → Coordinator: [Comparison analysis]
│
└─> Coordinator → User: [Synthesized response]
    └─> Coordinator → MemoryAgent: "Store interaction"
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized execution)
- Git

### Local Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Assignment3
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify installation**
```bash
python --version  # Should be 3.11+
pip list | grep faiss  # Should show faiss-cpu
```

### Docker Setup

1. **Build the image**
```bash
docker-compose build
```

2. **Run interactive system**
```bash
docker-compose run --rm multi-agent-system
```

3. **Run test scenarios**
```bash
docker-compose run --rm test-scenarios
```

---

## 💻 Usage

### Interactive Mode

```bash
python main.py
```

**Example Session**:
```
User: What are the main types of neural networks?
[System processes query with full logging...]
System: [Detailed response with sources]

User: Compare transformers and RNNs
[System coordinates research + analysis...]
System: [Comparison with trade-offs]

User: What did we discuss earlier?
[System retrieves from memory...]
System: [Previous conversation summary]
```

### Available Commands

- `exit` or `quit`: End session
- `status`: View system statistics
- Any natural language query: Processed by multi-agent system

---

## 🧪 Test Scenarios

### Running All Scenarios

```bash
python run_scenarios.py
```

This executes all 5 required scenarios and saves detailed logs to `outputs/`.

### Scenario Descriptions

#### 1. Simple Query
**Query**: "What are the main types of neural networks?"

**Demonstrates**:
- Basic information retrieval
- Research agent capabilities
- Memory storage

**Expected Behavior**:
- Coordinator classifies as SIMPLE
- Calls ResearchAgent
- Returns structured list of NN types
- Stores in memory

#### 2. Complex Query
**Query**: "Research transformer architectures, analyze their computational efficiency, and summarize key trade-offs."

**Demonstrates**:
- Multi-step task decomposition
- Research → Analysis pipeline
- Trade-off analysis
- Confidence scoring

**Expected Behavior**:
- Coordinator classifies as COMPLEX
- Creates multi-step plan
- Calls ResearchAgent for transformers
- Calls AnalysisAgent for trade-offs
- Synthesizes comprehensive response

#### 3. Memory Test
**Query**: "What did we discuss about neural networks earlier?"

**Demonstrates**:
- Memory retrieval
- Vector similarity search
- Conversation history access

**Expected Behavior**:
- Coordinator recognizes memory query
- Searches conversation history
- Returns relevant past interactions
- No research needed

#### 4. Multi-step Query
**Query**: "Find recent papers on reinforcement learning, analyze their methodologies, and identify common challenges."

**Demonstrates**:
- Complex task breakdown
- Sequential agent coordination
- Methodology analysis
- Challenge identification

**Expected Behavior**:
- Research RL information
- Analyze methodologies
- Identify challenges
- Multi-agent collaboration logged

#### 5. Collaborative Decision
**Query**: "Compare convolutional neural networks and recurrent neural networks and recommend which is better for image processing."

**Demonstrates**:
- Comparison analysis
- Recommendation generation
- Decision-making with reasoning

**Expected Behavior**:
- Research both CNN and RNN
- Perform comparison analysis
- Generate reasoned recommendation
- High confidence scores

### Output Files

All scenario outputs are saved to `outputs/`:
- `simple_query.txt`
- `complex_query.txt`
- `memory_test.txt`
- `multi_step.txt`
- `collaborative.txt`

Each file contains:
- Complete message logs
- Agent call sequences
- Decision reasoning
- Memory operations
- Final responses

---

## 📁 Project Structure

```
Assignment3/
│
├── agents/                      # Agent implementations
│   ├── __init__.py
│   ├── coordinator.py          # Central orchestrator
│   ├── research_agent.py       # Information retrieval
│   ├── analysis_agent.py       # Reasoning and analysis
│   └── memory_agent.py         # Memory management
│
├── core/                       # Core system components
│   ├── __init__.py
│   ├── config.py              # Configuration constants
│   ├── message.py             # Message protocol
│   └── logger.py              # Logging system
│
├── memory/                     # Memory subsystem
│   ├── __init__.py
│   ├── knowledge_base.py      # Mock knowledge DB
│   └── vector_store.py        # FAISS vector store
│
├── outputs/                    # Test scenario outputs
│   ├── simple_query.txt
│   ├── complex_query.txt
│   ├── memory_test.txt
│   ├── multi_step.txt
│   └── collaborative.txt
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   └── test_scenarios.py
│
├── docs/                       # Additional documentation
│
├── main.py                     # Interactive entry point
├── run_scenarios.py           # Test scenario runner
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker orchestration
└── README.md                  # This file
```

---

## 🧠 Design Decisions

### 1. Centralized Coordination Pattern

**Decision**: All agent communication flows through Coordinator

**Rationale**:
- Ensures traceability of all interactions
- Simplifies debugging and logging
- Prevents circular dependencies
- Allows for global optimization

**Alternative Considered**: Peer-to-peer agent messaging
**Rejected Because**: Difficult to trace, potential deadlocks, unclear responsibility

### 2. Structured Memory with Vector Search

**Decision**: Use FAISS for semantic similarity search

**Rationale**:
- Enables semantic matching beyond keywords
- Scalable to large knowledge bases
- Industry-standard library
- Supports hybrid search strategies

**Implementation**: Simple word-hashing vectorization
**Reason**: Avoids external LLM dependency, demonstrates principle

### 3. Message-Based Communication

**Decision**: Python dict/JSON message protocol

**Rationale**:
- Language-agnostic design
- Easy to serialize and log
- Clear message boundaries
- Extensible metadata

**Alternative Considered**: Direct function calls
**Rejected Because**: Harder to log, less flexible, tight coupling

### 4. No External LLMs

**Decision**: Rule-based logic for agent decisions

**Rationale**:
- Assignment focuses on KRR concepts, not LLMs
- Deterministic behavior for testing
- No API dependencies or costs
- Clear logical rules for grading

**Fallback Strategy**: Mock knowledge base with comprehensive topics

### 5. Logging-First Architecture

**Decision**: Every decision, message, and action is logged

**Rationale**:
- Critical for assignment evaluation
- Enables debugging and analysis
- Demonstrates system reasoning
- Provides audit trail

**Implementation**: Dual output (console + file) for flexibility

### 6. Memory Influence on Planning

**Decision**: Coordinator consults memory before research

**Rationale**:
- Demonstrates adaptive behavior
- Avoids redundant work
- Shows learning capability
- Efficient resource usage

**Threshold**: >0.8 similarity → skip research (simple queries)

### 7. Confidence Scoring Throughout

**Decision**: All results include confidence/similarity scores

**Rationale**:
- Enables quality assessment
- Supports decision-making
- Demonstrates uncertainty awareness
- Required by assignment spec

**Range**: 0.0 to 1.0 (higher = more confident)

---

## 📊 Evaluation Criteria Coverage

| Criterion | Implementation | Location |
|-----------|---------------|----------|
| **System Architecture** | Coordinator + 3 workers | `agents/` |
| **Memory Design** | Vector + Structured | `memory/` |
| **Agent Coordination** | Message-based protocol | `core/message.py` |
| **Autonomous Reasoning** | Query analysis + planning | `agents/coordinator.py` |
| **Adaptive Memory** | Memory-driven decisions | `_check_memory()` |
| **Code Quality** | Documented, modular | All files |
| **Traceability** | Comprehensive logging | `core/logger.py` |
| **Repository Hygiene** | Incremental commits | Git history |

---

## 🔄 Git Commit History

The project follows a structured commit sequence:

1. ✅ `chore: document architecture and base interfaces`
2. ✅ `feat: implement coordinator agent and planner`
3. ✅ `feat: add research agent with mock knowledge base`
4. ✅ `feat: add analysis agent for reasoning and comparison`
5. ✅ `feat: implement memory agent with structured storage`
6. ✅ `feat: add vector similarity search mechanism`
7. ✅ `feat: integrate agents with coordinator and logging`
8. ✅ `test: implement required multi-agent test scenarios`
9. ✅ `chore: add outputs for all sample scenarios`
10. ✅ `chore: add dockerfile and docker-compose`
11. ✅ `docs: finalize README documentation`

Each commit leaves the project in a runnable state.

---

## 📝 Notes

### LLM Usage

This project was developed with assistance from GitHub Copilot for:
- Code structure and boilerplate
- Documentation generation
- Design pattern suggestions

**All logic and architecture decisions are original and aligned with KRR principles.**

### Fallback Behavior

- If research finds no results → Returns general ML information
- If agent call fails → Logs error, continues with degraded results
- If memory is empty → Proceeds with full research pipeline

### Performance Considerations

- Vector dimension: 384 (balance between accuracy and speed)
- Memory limit: Unlimited (in-memory only, resets on restart)
- Search top-k: 5 results (configurable)

---

## 🤝 Contributors

- **Student**: [AIR UNIVERSITY KRR Assignment]
- **Course**: Knowledge Representation & Reasoning
- **Date**: December 2025

---

## 📄 License

This project is submitted as part of a university assignment. All rights reserved.

---

## 🆘 Troubleshooting

**Q: Docker build fails**
```bash
# Try with no cache
docker-compose build --no-cache
```

**Q: FAISS import error**
```bash
# Reinstall FAISS
pip uninstall faiss-cpu
pip install faiss-cpu==1.7.4
```

**Q: Outputs not generated**
```bash
# Ensure outputs directory exists
mkdir -p outputs
python run_scenarios.py
```

**Q: Memory search returns no results**
- This is expected on first run (no conversation history)
- Run a few queries first, then test memory

---

**End of README**
