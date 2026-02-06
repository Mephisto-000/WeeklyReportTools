import sys
import os
from pathlib import Path

# Add project root to sys.path to allow imports from src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import customtkinter as ctk
from src.gui.app import App
from src.utils.logger import setup_logger

logger = setup_logger("Main")

def main():
    # Redirect stderr to log file to capture C-level warnings (e.g. macOS IMK/TSM logs)
    # and silence the terminal as requested.
    try:
        log_file = open("app_log.txt", "a")
        os.dup2(log_file.fileno(), sys.stderr.fileno())
    except Exception as e:
        logger.warning(f"Failed to redirect stderr: {e}")

    logger.info("Starting Weekly Report Tool...")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Application crashed: {e}", exc_info=True)

if __name__ == "__main__":
    main()
