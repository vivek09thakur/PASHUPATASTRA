import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class ExperimentLogger:
    """Custom logger for experiment data"""
    
    def __init__(self, bot_name: str, log_dir: str = "logs"):
        self.bot_name = bot_name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup file logger
        self.log_file = self.log_dir / f"{bot_name}_{datetime.now().strftime('%Y%m%d')}.log"
        self.setup_logging()
        
        # Activity log
        self.activity_log = []
    
    def setup_logging(self):
        """Configure logging"""
        logger = logging.getLogger(self.bot_name)
        logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        self.logger = logger
    
    def log_activity(self, action_type: str, target_id: str, details: Dict[str, Any] = None):
        """Log bot activity"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'bot': self.bot_name,
            'action': action_type,
            'target': target_id,
            'details': details or {}
        }
        
        self.activity_log.append(log_entry)
        self.logger.info(f"{action_type}: {target_id} - {details}")
        
        # Save to JSON file periodically
        if len(self.activity_log) % 10 == 0:
            self.save_activity_log()
    
    def save_activity_log(self):
        """Save activity log to file"""
        log_file = self.log_dir / f"{self.bot_name}_activity_{datetime.now().strftime('%Y%m%d')}.json"
        with open(log_file, 'w') as f:
            json.dump(self.activity_log, f, indent=4)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get activity summary"""
        if not self.activity_log:
            return {}
        
        actions = {}
        for entry in self.activity_log:
            action = entry['action']
            actions[action] = actions.get(action, 0) + 1
        
        return {
            'total_actions': len(self.activity_log),
            'action_breakdown': actions,
            'first_action': self.activity_log[0]['timestamp'] if self.activity_log else None,
            'last_action': self.activity_log[-1]['timestamp'] if self.activity_log else None
        }