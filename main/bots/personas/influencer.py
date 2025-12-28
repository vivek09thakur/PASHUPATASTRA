from ..base_bot import BaseInstagramBot
import random
import time

class InfluencerBot(BaseInstagramBot):
    """Influencer persona bot - selective, high-quality engagement"""
    
    def decide_action(self) -> str:
        actions = ['browse_hashtag', 'view_profile', 'like_post', 'save_post', 'watch_video']
        weights = [0.2, 0.3, 0.3, 0.15, 0.05]  # More profile viewing, selective liking
        
        return random.choices(actions, weights=weights)[0]
    
    def run_session(self, duration_minutes: int = 30) -> Dict[str, Any]:
        self.start_session()
        session_end = time.time() + (duration_minutes * 60)
        
        actions_performed = 0
        
        while time.time() < session_end and actions_performed < self.config.behavior_params.daily_action_limit:
            action = self.decide_action()
            
            if action == 'browse_hashtag' and self.config.target_hashtags:
                hashtag = random.choice(self.config.target_hashtags)
                result = self.hashtag_nav.execute(hashtag, max_posts=3)
                
                # Influencers are selective - only like 1 in 3 posts
                if result['success'] and random.random() < 0.3:
                    for post in result['interacted_posts'][:1]:
                        self.like_action.execute(post['media_id'])
                        actions_performed += 1
            
            elif action == 'view_profile':
                # Influencers check out other influencers
                if self.config.target_accounts:
                    account = random.choice(self.config.target_accounts)
                    self.profile_nav.execute(account)
                    actions_performed += 1
            
            elif action == 'like_post':
                # Like from feed or explore
                pass
            
            elif action == 'save_post':
                if self.config.target_hashtags:
                    hashtag = random.choice(self.config.target_hashtags)
                    medias = self.client.hashtag_medias_recent(hashtag, amount=5)
                    if medias:
                        media = random.choice(medias)
                        self.save_action.execute(media.id)
                        actions_performed += 1
            
            elif action == 'watch_video':
                # Watch reels
                pass
            
            # Delay between actions
            if time.time() < session_end - 60:
                delay = self.timing.human_delay(
                    random.uniform(30, 60)  # Longer delays for influencers
                )
                time.sleep(delay)
        
        return self.end_session()