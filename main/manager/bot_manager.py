import concurrent.futures
import threading
import time
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from queue import Queue

from bots.bot_factory import BotFactory
from config.bot_config import BotConfig
from utils.data_handler import DataHandler

class BotManager:
    """Manage multiple bot instances"""
    
    def __init__(self, max_workers: int = 5):
        self.bots = []
        self.max_workers = max_workers
        self.data_handler = DataHandler()
        self.experiment_results = []
        self._stop_event = threading.Event()
    
    def add_bot(self, bot):
        """Add bot to manager"""
        self.bots.append(bot)
    
    def add_bot_from_config(self, config: BotConfig):
        """Add bot from configuration"""
        bot = BotFactory.create_bot(config)
        self.add_bot(bot)
    
    def load_bots_from_configs(self, config_files: List[str]):
        """Load bots from configuration files"""
        for config_file in config_files:
            try:
                bot = BotFactory.create_bot_from_config_file(config_file)
                self.add_bot(bot)
                print(f"Loaded bot: {bot.config.name}")
            except Exception as e:
                print(f"Error loading {config_file}: {e}")
    
    def run_single_session(self, bot, delay: int = 0) -> Optional[Dict[str, Any]]:
        """Run a single bot session"""
        if delay > 0:
            time.sleep(delay)
        
        try:
            # Login
            if not bot.login():
                return None
            
            # Run session
            session_result = bot.run_session(duration_minutes=30)
            
            # Save session data
            session_data = {
                'bot_name': bot.config.name,
                'persona_type': bot.config.persona_type,
                'start_time': datetime.fromtimestamp(bot.session_start).isoformat(),
                'end_time': datetime.now().isoformat(),
                'total_actions': len(bot.session_actions),
                'hashtags': bot.config.target_hashtags,
                'activities': bot.logger.activity_log[-session_result['total_actions']:] if session_result['total_actions'] > 0 else []
            }
            
            session_id = self.data_handler.save_session(session_data)
            
            # Logout
            bot.client.logout()
            
            result = {
                'bot': bot.config.name,
                'persona': bot.config.persona_type,
                'session_id': session_id,
                'actions': session_result['total_actions'],
                'hashtags': bot.config.target_hashtags,
                'timestamp': datetime.now().isoformat(),
                'success': True
            }
            
            self.experiment_results.append(result)
            return result
            
        except Exception as e:
            print(f"[{bot.config.name}] Session failed: {e}")
            return {
                'bot': bot.config.name,
                'success': False,
                'error': str(e)
            }
    
    def run_parallel_sessions(self, stagger_minutes: int = 3) -> List[Dict[str, Any]]:
        """Run all bot sessions in parallel"""
        print(f"\n{'='*60}")
        print(f"Starting parallel bot sessions")
        print(f"Total bots: {len(self.bots)}")
        print(f"Max workers: {self.max_workers}")
        print(f"Stagger: {stagger_minutes} minutes")
        print(f"{'='*60}\n")
        
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Prepare futures with staggered delays
            futures = []
            for i, bot in enumerate(self.bots):
                delay = i * stagger_minutes * 60  # Convert to seconds
                future = executor.submit(self.run_single_session, bot, delay)
                futures.append((bot.config.name, future))
            
            # Collect results
            for bot_name, future in futures:
                try:
                    result = future.result(timeout=3600)  # 1 hour timeout
                    if result:
                        results.append(result)
                        print(f"Completed: {bot_name} - {result.get('actions', 0)} actions")
                except concurrent.futures.TimeoutError:
                    print(f"{bot_name}: Session timed out")
                except Exception as e:
                    print(f"{bot_name}: Error - {e}")
        
        # Save experiment results
        self.save_experiment_summary()
        
        print(f"\n{'='*60}")
        print(f"All sessions completed")
        print(f"Successful: {len([r for r in results if r.get('success', False)])}/{len(self.bots)}")
        print(f"{'='*60}")
        
        return results
    
    