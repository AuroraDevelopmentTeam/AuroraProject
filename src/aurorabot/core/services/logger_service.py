import logging
import os
from datetime import datetime
from typing import Optional


class LoggerService:
    """Service for handling logging."""
    
    _instance: Optional['LoggerService'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'LoggerService':
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        """Initialize logger if not already initialized."""
        if self._logger is None:
            self._initialize_logger()
            
    def _initialize_logger(self) -> None:
        """Initialize the logger with proper configuration."""
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create logger
        logger = logging.getLogger("AuroraBot")
        logger.setLevel(logging.INFO)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Create file handler
        log_file = os.path.join(
            logs_dir,
            f"bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        self._logger = logger
        
    def get_logger(self) -> logging.Logger:
        """Get the logger instance."""
        return self._logger 