import logging
import sys
from pathlib import Path

def setup_logger(name: str = "WeeklyReport") -> logging.Logger:
    """Configures and returns a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File Handler (Optional, strictly for debugging if needed, but keeping it simple for now)
        # logs_dir = Path("logs")
        # logs_dir.mkdir(exist_ok=True)
        # file_handler = logging.FileHandler(logs_dir / "app.log")
        # ...

    return logger
