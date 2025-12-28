from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import time
import random
from instagrapi import Client

from config.bot_config import BotConfig
from utils.logger import ExperimentLogger
from utils.timing import HumanTiming
from actions.engagement import LikeAction, SaveAction, WatchAction
from actions.navigation import HashtagNavigation, ProfileNavigation

class BaseInstagramBot(ABC):
    """Base Instagram bot with common functionality"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.client = Client()
        self.setup_client()
        
        # Initialize utilities
        self.logger = ExperimentLogger(config.name)
        self.timing = HumanTiming()
        
        # Initialize actions
        self.like_action = LikeAction(self.client, self.logger, self.timing)
        self.save_action = SaveAction(self.client, self.logger, self.timing)
        self.watch_action = WatchAction(self.client, self.logger, self.timing)
        self.hashtag_nav = HashtagNavigation(self.client, self.logger, self.timing)
        self.profile_nav = ProfileNavigation(self.client, self.logger, self.timing)
        
        # Session data
        self.session_actions = []
        self.session_start = None
        
    def setup_client(self):
        """Configure Instagram client"""
        from config.settings import USER_AGENTS, DEFAULT_DELAY_RANGE
        
        self.client.set_user_agent(random.choice(USER_AGENTS))
        self.client.delay_range = DEFAULT_DELAY_RANGE
        
        # Load session if exists
        session_file = f"sessions/{self.config.name}_session.json"
        try:
            self.client.load_settings(session_file)
            self.logger.logger.info("Loaded existing session")
        except:
            pass
    
    def login(self) -> bool:
        """Login to Instagram"""
        try:
            self.client.login(self.config.username, self.config.password)
            
            # Save session
            session_file = f"sessions/{self.config.name}_session.json"
            self.client.dump_settings(session_file)
            
            self.logger.logger.info("Login successful")
            return True
        except Exception as e:
            self.logger.logger.error(f"Login failed: {e}")
            return False
    
    def start_session(self):
        """Start a new session"""
        self.session_start = time.time()
        self.session_actions = []
        
        self.logger.log_activity(
            "SESSION_START",
            "system",
            {"persona": self.config.persona_type}
        )
    
    def end_session(self):
        """End current session"""
        session_duration = time.time() - self.session_start
        
        summary = {
            "duration_seconds": session_duration,
            "total_actions": len(self.session_actions),
            "persona": self.config.persona_type
        }
        
        self.logger.log_activity(
            "SESSION_END",
            "system",
            summary
        )
        
        # Save activity log
        self.logger.save_activity_log()
        
        return summary
    
    @abstractmethod
    def decide_action(self) -> str:
        """Decide next action based on persona"""
        pass
    
    @abstractmethod
    def run_session(self, duration_minutes: int = 30) -> Dict[str, Any]:
        """Run a complete session"""
        pass