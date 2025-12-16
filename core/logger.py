"""
Centralized logging system for multi-agent system
"""
import os
from datetime import datetime
from core.config import LOG_TIMESTAMP_FORMAT

class SystemLogger:
    """
    Handles logging for agent communications and decisions
    """
    
    def __init__(self, log_file=None, console_output=True):
        """
        Initialize the logger
        
        Args:
            log_file (str): Optional file path for logging
            console_output (bool): Whether to print to console
        """
        self.log_file = log_file
        self.console_output = console_output
        self.logs = []
        
        if self.log_file and os.path.exists(self.log_file):
            os.remove(self.log_file)
    
    def _format_timestamp(self):
        """Get formatted timestamp"""
        return datetime.now().strftime(LOG_TIMESTAMP_FORMAT)
    
    def _write_log(self, message):
        """
        Write log message to file and/or console
        
        Args:
            message (str): Log message
        """
        self.logs.append(message)
        
        if self.console_output:
            print(message)
        
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
    
    def log_message(self, sender, recipient, msg_type, payload):
        """
        Log an agent message
        
        Args:
            sender (str): Sending agent
            recipient (str): Receiving agent
            msg_type (str): Message type
            payload (dict): Message payload
        """
        timestamp = self._format_timestamp()
        message = f"[{timestamp}] MESSAGE: {sender} -> {recipient} | Type: {msg_type}"
        self._write_log(message)
        self._write_log(f"  Payload: {payload}")
    
    def log_decision(self, agent, decision, reasoning):
        """
        Log a coordinator decision
        
        Args:
            agent (str): Agent making decision
            decision (str): Decision description
            reasoning (str): Reasoning behind decision
        """
        timestamp = self._format_timestamp()
        message = f"[{timestamp}] DECISION ({agent}): {decision}"
        self._write_log(message)
        self._write_log(f"  Reasoning: {reasoning}")
    
    def log_agent_call(self, coordinator, agent, task):
        """
        Log an agent being called by coordinator
        
        Args:
            coordinator (str): Coordinator name
            agent (str): Agent being called
            task (str): Task description
        """
        timestamp = self._format_timestamp()
        message = f"[{timestamp}] AGENT_CALL: {coordinator} invokes {agent}"
        self._write_log(message)
        self._write_log(f"  Task: {task}")
    
    def log_agent_response(self, agent, response_summary, confidence):
        """
        Log an agent's response
        
        Args:
            agent (str): Agent name
            response_summary (str): Summary of response
            confidence (float): Confidence score
        """
        timestamp = self._format_timestamp()
        message = f"[{timestamp}] AGENT_RESPONSE ({agent}): Confidence={confidence:.2f}"
        self._write_log(message)
        self._write_log(f"  Summary: {response_summary}")
    
    def log_memory_operation(self, operation, details):
        """
        Log a memory operation
        
        Args:
            operation (str): Operation type (store/retrieve)
            details (str): Operation details
        """
        timestamp = self._format_timestamp()
        message = f"[{timestamp}] MEMORY: {operation}"
        self._write_log(message)
        self._write_log(f"  Details: {details}")
    
    def log_query(self, query):
        """
        Log a user query
        
        Args:
            query (str): User query
        """
        timestamp = self._format_timestamp()
        self._write_log("=" * 80)
        self._write_log(f"[{timestamp}] NEW USER QUERY: {query}")
        self._write_log("=" * 80)
    
    def log_final_response(self, response):
        """
        Log the final system response
        
        Args:
            response (str): Final response
        """
        timestamp = self._format_timestamp()
        self._write_log(f"\n[{timestamp}] FINAL RESPONSE:")
        self._write_log("-" * 80)
        self._write_log(response)
        self._write_log("=" * 80)
        self._write_log("")
    
    def get_all_logs(self):
        """
        Get all logged messages
        
        Returns:
            list: All log messages
        """
        return self.logs.copy()
    
    def clear_logs(self):
        """Clear all logs"""
        self.logs = []
