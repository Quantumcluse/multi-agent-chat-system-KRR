"""
Mock knowledge base for ResearchAgent
"""

KNOWLEDGE_DB = {
    "neural networks": {
        "summary": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers.",
        "details": "Main types include: Feedforward Neural Networks (FNN) for basic pattern recognition, Convolutional Neural Networks (CNN) for image processing, Recurrent Neural Networks (RNN) for sequential data, and Transformers for natural language processing.",
        "source": "AI Research Database",
        "confidence": 0.95
    },
    
    "transformers": {
        "summary": "Transformers are a type of neural network architecture that uses self-attention mechanisms to process sequential data in parallel, rather than sequentially.",
        "details": "Key components include multi-head attention layers, positional encodings, and feed-forward networks. Trade-offs: excellent performance on NLP tasks but computationally expensive and require large amounts of training data. Examples include BERT, GPT, and T5.",
        "source": "NLP Research Papers",
        "confidence": 0.92
    },
    
    "transformer architecture": {
        "summary": "Transformer architecture revolutionized NLP by introducing self-attention mechanisms that allow the model to weigh the importance of different words in a sequence.",
        "details": "Architecture consists of encoder and decoder stacks. Each layer has multi-head self-attention and position-wise feed-forward networks. Computational efficiency trade-off: parallel processing enables faster training but requires more memory and compute resources than RNNs.",
        "source": "Deep Learning Research",
        "confidence": 0.90
    },
    
    "reinforcement learning": {
        "summary": "Reinforcement learning is a machine learning paradigm where agents learn to make decisions by interacting with an environment and receiving rewards or penalties.",
        "details": "Key concepts include states, actions, rewards, and policies. Recent methods include Deep Q-Networks (DQN), Policy Gradients, Actor-Critic methods, and Proximal Policy Optimization (PPO). Challenges include sample efficiency, exploration vs exploitation trade-off, and credit assignment problem.",
        "source": "RL Research Database",
        "confidence": 0.88
    },
    
    "machine learning": {
        "summary": "Machine learning enables computers to learn from data without being explicitly programmed. It includes supervised, unsupervised, and reinforcement learning approaches.",
        "details": "Supervised learning uses labeled data for classification and regression. Unsupervised learning finds patterns in unlabeled data through clustering and dimensionality reduction. Common algorithms include decision trees, SVMs, k-means, and neural networks.",
        "source": "ML Textbooks",
        "confidence": 0.93
    },
    
    "convolutional neural networks": {
        "summary": "CNNs are specialized neural networks designed for processing grid-like data such as images. They use convolutional layers to automatically learn spatial hierarchies of features.",
        "details": "Key components include convolutional layers, pooling layers, and fully connected layers. Trade-offs: excellent for image tasks but require large datasets and significant computational resources. Applications include image classification, object detection, and image segmentation.",
        "source": "Computer Vision Research",
        "confidence": 0.91
    },
    
    "recurrent neural networks": {
        "summary": "RNNs are neural networks designed for sequential data by maintaining hidden states that capture information about previous inputs.",
        "details": "Variants include LSTM (Long Short-Term Memory) and GRU (Gated Recurrent Unit) which solve the vanishing gradient problem. Trade-offs: good for sequential data but slower to train than Transformers and can struggle with long-range dependencies.",
        "source": "Sequence Modeling Research",
        "confidence": 0.89
    },
    
    "deep learning": {
        "summary": "Deep learning is a subset of machine learning using neural networks with multiple layers to learn hierarchical representations of data.",
        "details": "Enabled by increased computational power (GPUs), large datasets, and improved training techniques. Applications span computer vision, NLP, speech recognition, and game playing. Challenges include interpretability, data requirements, and computational cost.",
        "source": "Deep Learning Literature",
        "confidence": 0.94
    }
}

def search_knowledge(query):
    """
    Search the knowledge base for relevant information
    
    Args:
        query (str): Search query
        
    Returns:
        dict: Knowledge entry if found, None otherwise
    """
    query_lower = query.lower()
    
    # Direct match
    if query_lower in KNOWLEDGE_DB:
        return KNOWLEDGE_DB[query_lower]
    
    # Partial match
    for key, value in KNOWLEDGE_DB.items():
        if query_lower in key or key in query_lower:
            return value
    
    # No match found
    return None