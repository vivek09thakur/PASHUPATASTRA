from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import random

class BaseAction(ABC):
    """Base class for all bot actions"""
    
    def __init__(self, client, logger, timing):
        self.client = client
        self.logger = logger
        self.timing = timing
    
    @abstractmethod
    def execute(self, target, **kwargs) -> Dict[str, Any]:
        """Execute the action"""
        pass
    
    def safe_execute(self, target, max_retries=3, **kwargs) -> Optional[Dict[str, Any]]:
        """Execute action with error handling"""
        for attempt in range(max_retries):
            try:
                return self.execute(target, **kwargs)
            except Exception as e:
                self.logger.log_activity(
                    "ACTION_ERROR",
                    target,
                    {"attempt": attempt + 1, "error": str(e)}
                )
                
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    time.sleep(wait_time)
        
        return None