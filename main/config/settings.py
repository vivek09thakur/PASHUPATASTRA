import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
SESSIONS_DIR = DATA_DIR / 'sessions'
LOGS_DIR = DATA_DIR / 'logs'
CONFIGS_DIR = DATA_DIR / 'configs'

# Create directories
for dir_path in [DATA_DIR, SESSIONS_DIR, LOGS_DIR, CONFIGS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Instagram API settings
USER_AGENTS = [
    "Instagram 219.0.0.12.117 Android (29/10; 480dpi; 1080x1920; samsung; SM-G973F; beyond1; exynos9820; en_US; 301826283)",
    "Instagram 263.1.0.19.301 iOS (15_4_1; iPhone13,4; en_US; en; scale=3.00; 1284x2778; 386449684)",
    "Instagram 285.0.0.27.91 Android (30/11; 420dpi; 1080x2260; Google; Pixel 6; oriole; oriole; en_US; 457333356)",
]

# Rate limiting
DEFAULT_DELAY_RANGE = [1, 4]
MAX_REQUESTS_PER_HOUR = 200

# Experiment settings
DEFAULT_SESSION_DURATION = 30  # minutes
DEFAULT_POSTS_PER_HASHTAG = 10
DEFAULT_ACTIONS_PER_SESSION = 50