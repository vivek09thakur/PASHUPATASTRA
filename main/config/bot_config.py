import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class BehaviorParams:
    like_probability: float = 0.7
    save_probability: float = 0.3
    watch_through_probability: float = 0.8
    scroll_probability: float = 0.5
    follow_probability: float = 0.1
    daily_action_limit: int = 100
    session_duration_min: int = 30
    idle_time_max: int = 3600
    min_delay: int = 15
    max_delay: int = 45

@dataclass
class BotConfig:
    name: str
    username: str
    password: str
    persona_type: str
    target_hashtags: List[str] = field(default_factory=list)
    target_accounts: List[str] = field(default_factory=list)
    behavior_params: BehaviorParams = field(default_factory=BehaviorParams)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return {
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'persona_type': self.persona_type,
            'target_hashtags': self.target_hashtags,
            'target_accounts': self.target_accounts,
            'behavior_params': self.behavior_params.__dict__,
            'created_at': self.created_at
        }
    
    def save(self, filename: str):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
    
    @classmethod
    def load(cls, filename: str) -> 'BotConfig':
        """Load configuration from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Extract behavior params
        behavior_data = data.pop('behavior_params', {})
        behavior_params = BehaviorParams(**behavior_data)
        
        # Create config
        config = cls(**data)
        config.behavior_params = behavior_params
        return config
    
    @classmethod
    def create_persona_config(cls, persona_type: str, **kwargs):
        """Create pre-configured persona"""
        base_config = {
            'name': f"bot_{persona_type}",
            'username': '',
            'password': '',
            'persona_type': persona_type,
        }
        
        persona_configs = {
            'influencer': {
                'target_hashtags': ['fashion', 'lifestyle', 'travel', 'photography'],
                'behavior_params': BehaviorParams(
                    like_probability=0.5,
                    save_probability=0.4,
                    watch_through_probability=0.9,
                    daily_action_limit=150
                )
            },
            'enthusiast': {
                'target_hashtags': ['photography', 'nature', 'art', 'design'],
                'behavior_params': BehaviorParams(
                    like_probability=0.8,
                    save_probability=0.6,
                    watch_through_probability=0.95,
                    daily_action_limit=200
                )
            },
            'casual': {
                'target_hashtags': ['memes', 'funny', 'animals', 'food'],
                'behavior_params': BehaviorParams(
                    like_probability=0.3,
                    save_probability=0.1,
                    watch_through_probability=0.6,
                    daily_action_limit=50
                )
            }
        }
        
        if persona_type in persona_configs:
            base_config.update(persona_configs[persona_type])
        
        base_config.update(kwargs)
        return cls(**base_config)