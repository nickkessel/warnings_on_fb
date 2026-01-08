## Use on personal machine for testing/messing w/ things. 
# --- API POLLING SETTINGS ---
# Define categories for alert types
from insta_alert.utils.constants import SEVERE, WATCHES, WINTER, OTHER, ALL
from dotenv import load_dotenv
import os
from pathlib import Path
cwd = Path(os.getcwd())
env_path = cwd / ".env"
load_dotenv(env_path)
ALERT_TYPES_TO_MONITOR = (
    'Winter Weather Advisory'
)
LOG_FILE = 'logs/posted_alerts_test3.log'
# --- BOUNDING ZONES --- 
#use https://api.weather.gov/zones?type=county search to find county codes. best source.

CINCY_ZONES = [
  'OHZ078', 'OHZ079', 'OHZ079', 'OHZ080', 'OHZ077', 'OHZ071', 'OHZ070', 'OHZ072', 'INZ066', 'INZ074', 'INZ075', 'KY091', 'KY092', 'KY093'
]
MMWX_ZONES = [
  'MIZ039', 'MIZ040', 'MIZ041', 'MIZ044', 'MIZ045', 'MIZ046', 'MIZ047', 'MIZ048', 'MIZ057', 'MIZ051', 'MIZ052', 'MIZ053', 'MIZ050', 'MIZ056', 'MIZ058', 'MIZ059', 'MIZ060', 'MIZ061', 'MIZ062', 'MIZ064', 'MIZ065', 'MIZ066', 'MIZ067', 'MIZ068', 'MIZ069', 'MIZ072', 'MIZ073', 'MIZ074', 'MIZ075','LMZ845', 'LMZ846', 'LMZ847', 'LMZ876', 'LMZ874', 'LMZ872', 'LHZ422', 'LHZ421'
]
EVERYWHERE = True #polls for all alerts, ignores the active_zones flag
ACTIVE_ZONES = CINCY_ZONES #counties are w/ a C, marine zones w/ a Z

# --- TARGETS ---
# Set to True to enable posting, False to disable
OUTPUT_DIR = 'graphics/live-test' #should be graphics/something
POST_TO_FACEBOOK = False
POST_TO_DISCORD = False #using tha new webhooks 
POST_TO_INSTAGRAM_GRID = False
POST_TO_INSTAGRAM_STORY = False
SEND_TO_SLIDESHOW = False 
# A list of Discord webhook URLs to send alerts to

new_logs = os.getenv("ALL_DISCORD_WEBHOOK")
WEBHOOKS = [new_logs]

# --- CAPTION ---
DEFAULT_TAGS = '#weather #weatheralert #stayalert #wx'
USE_TAGS = False
