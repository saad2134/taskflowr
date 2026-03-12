"""
TaskFlowr Multi-Agent System
"""

__version__ = "1.0.0"
__author__ = "TaskFlowr Team"

from .coordinator import create_coordinator
from .automation_agent import create_automation_agent
from .communication_agent import create_communication_agent

__all__ = [
    'create_coordinator',
    'create_automation_agent', 
    'create_communication_agent'
]