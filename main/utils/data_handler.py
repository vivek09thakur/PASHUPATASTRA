import json
import pickle
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataHandler:
    """Handle data storage and retrieval"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self.db_path = self.data_dir / "experiment.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_name TEXT,
                persona_type TEXT,
                start_time TEXT,
                end_time TEXT,
                total_actions INTEGER,
                hashtags_interacted TEXT,
                created_at TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                timestamp TEXT,
                action_type TEXT,
                target_id TEXT,
                details TEXT,
                FOREIGN KEY (session_id) REFERENCES bot_sessions (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiment_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_name TEXT,
                start_date TEXT,
                end_date TEXT,
                total_bots INTEGER,
                total_sessions INTEGER,
                total_actions INTEGER,
                results_summary TEXT,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_session(self, session_data: Dict[str, Any]) -> int:
        """Save bot session to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bot_sessions 
            (bot_name, persona_type, start_time, end_time, total_actions, hashtags_interacted, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_data['bot_name'],
            session_data['persona_type'],
            session_data['start_time'],
            session_data['end_time'],
            session_data['total_actions'],
            json.dumps(session_data.get('hashtags', [])),
            datetime.now().isoformat()
        ))
        
        session_id = cursor.lastrowid
        
        # Save activities
        for activity in session_data.get('activities', []):
            cursor.execute('''
                INSERT INTO bot_activities 
                (session_id, timestamp, action_type, target_id, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                session_id,
                activity['timestamp'],
                activity['action'],
                activity['target'],
                json.dumps(activity.get('details', {}))
            ))
        
        conn.commit()
        conn.close()
        return session_id
    
    def save_json(self, data: Any, filename: str):
        """Save data to JSON file"""
        filepath = self.data_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_json(self, filename: str) -> Any:
        """Load data from JSON file"""
        filepath = self.data_dir / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    
    def save_pickle(self, data: Any, filename: str):
        """Save data using pickle"""
        filepath = self.data_dir / filename
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load_pickle(self, filename: str) -> Any:
        """Load data using pickle"""
        filepath = self.data_dir / filename
        if filepath.exists():
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        return None
    
    def get_session_history(self, bot_name: str, limit: int = 10) -> List[Dict]:
        """Get session history for a bot"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM bot_sessions 
            WHERE bot_name = ? 
            ORDER BY start_time DESC 
            LIMIT ?
        ''', (bot_name, limit))
        
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return sessions