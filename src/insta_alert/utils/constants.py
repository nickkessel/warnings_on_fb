#stuff that remains constant across all configs
from dotenv import load_dotenv
import os
from pathlib import Path
cwd = Path(os.getcwd())
env_path = cwd / ".env"
load_dotenv(env_path)
# ---- ALERT TYPES ----
SEVERE = ['Tornado Warning', 'Severe Thunderstorm Warning', 'Flash Flood Warning']
OTHER = ['Special Weather Statement', 'Flood Advisory', 'Special Marine Warning', 'Dust Storm Warning', 'Dense Fog Advisory', 'High Wind Warning', 'Red Flag Warning', 'Wind Advisory']
WINTER = ['Winter Storm Warning', 'Frost Advisory', 'Freeze Warning', 'Snow Squall Warning', 'Winter Weather Advisory','Lake Effect Snow Warning', 'Blizzard Warning', 'Winter Storm Watch']
WATCHES = ['Tornado Watch', 'Severe Thunderstorm Watch', 'Flood Watch', 'Flash Flood Watch']

ALL = SEVERE + OTHER + WINTER + WATCHES
# --- ERRORS ----
DISCORD_PINGS_ALL = ['1427050976732254300'] #role to mention for all errors
ERROR_WEBHOOK = os.getenv("ERROR_WEBHOOK")
ALERT_COLORS = {
    "Severe Thunderstorm Warning": {
        "facecolor": "#ffff00", # yellow
        "edgecolor": "#efef00", # darker yellow for border
        "fillalpha": "50"
    },
    "Tornado Warning": {
        "facecolor": "#ff0000", # red
        "edgecolor": "#cc0000", # darker red
        "fillalpha": "50"
    },
    "Flash Flood Warning": {
        "facecolor": "#02de02", # green
        "edgecolor": "#00dc00", # darker green
        "fillalpha": "50"
    },
    "Special Weather Statement": {
        "facecolor": "#ff943d", # orange
        "edgecolor": "#e07b24", # darker orange
        "fillalpha": "50"
    },
    "Special Marine Warning": {
        "facecolor": "#00E4DD", # teal
        "edgecolor": "#00cdc6", # darker teal
        "fillalpha": "50"
    },
    "Dust Storm Warning": {
        "facecolor": "#FFE4C4",
        "edgecolor": "#968672",
        "fillalpha": "50"
    },
    'Flood Advisory': {
        'facecolor': '#00ff7f',
        'edgecolor': "#00d168",
        'fillalpha': '50'
    },
    'Severe Thunderstorm Watch': {
        'facecolor': "#DB7093", #pink because i hate nick
        'edgecolor': "#8f4a61",
        'fillalpha': '50'
    },
    'Tornado Watch': {
        'facecolor': "#FFFF00", #also yellow because i hate nick
        'edgecolor': "#b8b800",
        'fillalpha': '50'
    },
    'Flood Watch': {
        'facecolor': "#2E8B57",
        'edgecolor': "#168445",
        'fillalpha': '50'
    },
    'Flash Flood Watch': {
        'facecolor': "#2E8B57",
        'edgecolor': "#168445",
        'fillalpha': '50'
    },
    'Dense Fog Advisory': {
        'facecolor': "#708090",
        'edgecolor': "#565F68",
        'fillalpha': '50'
    },
    'Freeze Warning': {
        'facecolor': "#5E54A5",
        'edgecolor': "#483D8B",
        'fillalpha': '50'
    },
    'Frost Advisory': {
        'facecolor': "#73A0F3",
        'edgecolor': "#437DEA",
        'fillalpha': '50'
    },
    'Winter Storm Warning': {
        'facecolor': "#FF69B4",
        'edgecolor': "#FF69B4",
        'fillalpha': '50'
    },
    'High Wind Warning':{
        'facecolor': '#DAA520',
        'edgecolor': '#DAA520',
        'fillalpha': '50'
    },
    'Wind Advisory':{
        'facecolor': '#D2B48C',
        'edgecolor': '#D2B48C',
        'fillalpha': '50'
    },
    'Red Flag Warning': {
        'facecolor': '#FF1493',
        'edgecolor': '#FF1493',
        'fillalpha': '50'
    },
    'Snow Squall Warning': {
        'facecolor': "#CB3D97",
        'edgecolor': '#C71585',
        'fillalpha': '50'
    },
    'Lake Effect Snow Warning': {
        'facecolor': "#22A9A9",
        'edgecolor': '#008B8B',
        'fillalpha': '50'
    },
    'Blizzard Warning': {
        'facecolor': "#FF5F25",
        'edgecolor': "#FF4500",
        'fillalpha': '50'
    },
    'Winter Storm Watch': {
        'facecolor': "#4682B4",
        'edgecolor': '#4682B4',
        'fillalpha': '50'
    },
    'Winter Weather Advisory': {
        'facecolor': "#8875F0",
        'edgecolor': "#755EF5",
        'fillalpha': '50'
    },
    "default": {
        "facecolor": "#b7b7b7", # grey
        "edgecolor": "#414141", # dark grey
        "fillalpha": "50"
    }
}