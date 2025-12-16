"""
Core module for multi-agent system
Contains configuration, messaging, and logging components
"""
from core.config import *
from core.message import Message
from core.logger import SystemLogger

__all__ = ['Message', 'SystemLogger']
