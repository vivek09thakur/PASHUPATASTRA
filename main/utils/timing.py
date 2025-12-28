import time
import random
from typing import Tuple

class HumanTiming:
    """Simulate human-like timing patterns"""
    
    @staticmethod
    def random_delay(min_seconds: float, max_seconds: float) -> float:
        """Generate random delay with normal distribution"""
        delay = random.uniform(min_seconds, max_seconds)
        return delay
    
    @staticmethod
    def human_delay(base_delay: float, variability: float = 0.3) -> float:
        """
        Create human-like delay with micro-pauses
        
        Args:
            base_delay: Base delay in seconds
            variability: How much to vary the delay (±percentage)
        """
        # Add random variation
        variation = base_delay * random.uniform(-variability, variability)
        actual_delay = max(0.5, base_delay + variation)
        
        # Split into chunks with micro-pauses
        chunks = random.randint(2, 6)
        chunk_delay = actual_delay / chunks
        
        for i in range(chunks):
            time.sleep(chunk_delay)
            
            # Simulate human micro-interactions
            if random.random() < 0.15:  # 15% chance
                micro_pause = random.uniform(0.3, 1.5)
                time.sleep(micro_pause)
        
        return actual_delay
    
    @staticmethod
    def session_break(session_length_minutes: int) -> float:
        """Calculate appropriate break between sessions"""
        # Longer sessions need longer breaks
        base_break = session_length_minutes * 1.5
        
        # Add randomness
        break_time = base_break * random.uniform(0.8, 1.5)
        
        # Convert to minutes
        return max(5, break_time)  # Minimum 5 minutes
    
    @staticmethod
    def get_time_of_day_multiplier() -> float:
        """Get timing multiplier based on time of day"""
        import datetime
        hour = datetime.datetime.now().hour
        
        if 8 <= hour <= 10:    # Morning
            return random.uniform(0.8, 1.2)
        elif 12 <= hour <= 14:  # Lunch
            return random.uniform(1.0, 1.5)
        elif 18 <= hour <= 22:  # Evening
            return random.uniform(1.2, 1.8)
        else:                   # Night
            return random.uniform(0.5, 1.0)