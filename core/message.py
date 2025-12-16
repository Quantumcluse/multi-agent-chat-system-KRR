"""
Message class for inter-agent communication
"""
from datetime import datetime
from core.config import LOG_TIMESTAMP_FORMAT

class Message:
    """
    Standardized message format for agent communication
    """
    
    def __init__(self, sender, recipient, msg_type, payload):
        """
        Initialize a message
        
        Args:
            sender (str): Name of the sending agent
            recipient (str): Name of the receiving agent
            msg_type (str): Type of message (task, response, query, etc.)
            payload (dict): The actual data being sent
        """
        self.msg_id = self._generate_id()
        self.sender = sender
        self.recipient = recipient
        self.msg_type = msg_type
        self.payload = payload
        self.timestamp = datetime.now().strftime(LOG_TIMESTAMP_FORMAT)
    
    def _generate_id(self):
        """Generate a unique message ID"""
        return f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            "msg_id": self.msg_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "msg_type": self.msg_type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create message from dictionary"""
        msg = cls(
            sender=data["sender"],
            recipient=data["recipient"],
            msg_type=data["msg_type"],
            payload=data["payload"]
        )
        msg.msg_id = data["msg_id"]
        msg.timestamp = data["timestamp"]
        return msg
    
    def __str__(self):
        """String representation for logging"""
        return (f"[{self.timestamp}] {self.sender} -> {self.recipient} "
                f"({self.msg_type}): {self.payload}")