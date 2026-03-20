import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CENTRALIZED OSINT ENGINE CONFIGURATION
# ==========================================

# AI Models (Gemini)
# We use Pro for complex reasoning and formatting, and Flash for speed/bulk tasks.
DEFAULT_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview")
DEFAULT_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.1-flash-preview")
DEFAULT_FLASH_LITE_MODEL = os.getenv("GEMINI_FLASH_LITE_MODEL", "gemini-3.1-flash-lite-preview")

# Base Settings
DATA_DIR_NAME = "data"
