from typing import Dict, Type
from .base_bot import BaseInstagramBot
from .personas.influencer import InfluencerBot
from .personas.enthusiast import EnthusiastBot
from .personas.casual import CasualBot
from config.bot_config import BotConfig

class BotFactory:
    """Factory for creating bot instances"""
    
    _bot_classes: Dict[str, Type[BaseInstagramBot]] = {
        'influencer': InfluencerBot,
        'enthusiast': EnthusiastBot,
        'casual': CasualBot
    }
    
    @classmethod
    def create_bot(cls, config: BotConfig) -> BaseInstagramBot:
        """Create bot instance based on persona"""
        bot_class = cls._bot_classes.get(config.persona_type)
        
        if not bot_class:
            raise ValueError(f"Unknown persona type: {config.persona_type}")
        
        return bot_class(config)
    
    @classmethod
    def create_bot_from_config_file(cls, config_file: str) -> BaseInstagramBot:
        """Create bot from configuration file"""
        config = BotConfig.load(config_file)
        return cls.create_bot(config)
    
    @classmethod
    def create_multiple_bots(cls, configs: list) -> list:
        """Create multiple bots from configurations"""
        bots = []
        for config in configs:
            try:
                bot = cls.create_bot(config)
                bots.append(bot)
            except Exception as e:
                print(f"Error creating bot {config.name}: {e}")
        
        return bots