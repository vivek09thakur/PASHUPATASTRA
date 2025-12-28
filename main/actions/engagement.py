from .base_actions import BaseAction
import time
import random

class LikeAction(BaseAction):
    """Handle post liking"""
    
    def execute(self, media_id, view_time=None, **kwargs):
        if view_time is None:
            view_time = random.uniform(2, 8)
        
        # Simulate viewing before liking
        time.sleep(view_time)
        
        # Like the post
        self.client.media_like(media_id)
        
        return {
            "action": "like",
            "media_id": media_id,
            "view_time": view_time,
            "success": True
        }

class SaveAction(BaseAction):
    """Handle post saving"""
    
    def execute(self, media_id, view_time=None, **kwargs):
        if view_time is None:
            view_time = random.uniform(3, 12)
        
        # Simulate viewing before saving
        time.sleep(view_time)
        
        # Save the post
        self.client.media_save(media_id)
        
        return {
            "action": "save",
            "media_id": media_id,
            "view_time": view_time,
            "success": True
        }

class WatchAction(BaseAction):
    """Handle video watching"""
    
    def execute(self, media_id, **kwargs):
        # Get media info to estimate duration
        media_info = self.client.media_info(media_id)
        
        # Estimate watch time
        if hasattr(media_info, 'video_duration'):
            estimated_duration = media_info.video_duration
        else:
            estimated_duration = random.uniform(8, 30)
        
        # Simulate watching with pauses
        actual_watch = estimated_duration * random.uniform(0.7, 1.3)
        
        # Watch in chunks
        chunks = random.randint(2, 5)
        for i in range(chunks):
            chunk_time = actual_watch / chunks
            time.sleep(chunk_time)
            
            # Sometimes pause
            if random.random() < 0.2:
                time.sleep(random.uniform(0.5, 3))
        
        return {
            "action": "watch",
            "media_id": media_id,
            "estimated_duration": estimated_duration,
            "actual_watch_time": actual_watch,
            "success": True
        }