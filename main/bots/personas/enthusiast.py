from ..base_bot import BaseInstagramBot
import random
import time

class EnthusiastBot(BaseInstagramBot):
    """Enthusiast persona bot - highly engaged, passionate"""
    
    def decide_action(self) -> str:
        actions = ['like_post', 'save_post', 'browse_hashtag', 'watch_video']
        weights = [0.4, 0.3, 0.2, 0.1]  # High engagement rate
        
        return random.choices(actions, weights=weights)[0]
    
    def run_session(self, duration_minutes: int = 30) -> Dict[str, Any]:
        self.start_session()
        session_end = time.time() + (duration_minutes * 60)
        
        actions_performed = 0
        
        while time.time() < session_end and actions_performed < self.config.behavior_params.daily_action_limit:
            action = self.decide_action()
            
            if action == 'browse_hashtag' and self.config.target_hashtags:
                hashtag = random.choice(self.config.target_hashtags)
                result = self.hashtag_nav.execute(hashtag, max_posts=5)
                
                # Enthusiasts engage with multiple posts
                for post in result['interacted_posts'][:3]:
                    if random.random() < 0.7:  # 70% chance to like
                        self.like_action.execute(post['media_id'])
                        actions_performed += 1
                    
                    if random.random() < 0.4:  # 40% chance to save
                        self.save_action.execute(post['media_id'])
                        actions_performed += 1
            
            elif action == 'like_post':
                # Like from various sources
                pass
            
            elif action == 'save_post':
                # Save inspirational content
                pass
            
            elif action == 'watch_video':
                # Watch educational/learning content
                pass
            
            # Shorter delays for enthusiasts
            if time.time() < session_end - 60:
                delay = self.timing.human_delay(
                    random.uniform(20, 40)  # Quick engagement
                )
                time.sleep(delay)
        
        return self.end_session()