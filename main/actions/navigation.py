from .base_actions import BaseAction
import time
import random

class HashtagNavigation(BaseAction):
    """Navigate and explore hashtags"""
    
    def execute(self, hashtag, max_posts=10, **kwargs):
        # Get posts from hashtag
        medias = self.client.hashtag_medias_recent(hashtag, amount=max_posts * 2)
        random.shuffle(medias)
        
        interacted_posts = []
        
        for media in medias[:max_posts]:
            # Simulate scrolling/delay
            scroll_time = random.uniform(1, 3)
            time.sleep(scroll_time)
            
            interacted_posts.append({
                "media_id": media.id,
                "user": media.user.username if hasattr(media.user, 'username') else 'unknown'
            })
        
        return {
            "action": "hashtag_navigation",
            "hashtag": hashtag,
            "posts_found": len(medias),
            "posts_interacted": len(interacted_posts),
            "interacted_posts": interacted_posts,
            "success": True
        }

class ProfileNavigation(BaseAction):
    """Navigate user profiles"""
    
    def execute(self, username, **kwargs):
        # Get user info
        user_id = self.client.user_id_from_username(username)
        user_info = self.client.user_info(user_id)
        
        # Get user's posts
        user_medias = self.client.user_medias(user_id, amount=10)
        
        # Simulate profile browsing
        browse_time = random.uniform(5, 15)
        time.sleep(browse_time)
        
        return {
            "action": "profile_navigation",
            "username": username,
            "user_id": user_id,
            "follower_count": user_info.follower_count,
            "posts_count": len(user_medias),
            "browse_time": browse_time,
            "success": True
        }