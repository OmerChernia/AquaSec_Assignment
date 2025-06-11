class Settings:
    """Application settings and constants."""
    
    # File settings
    USERS_FILE: str = "users.json"
    
    # Validation constants
    ID_LENGTH: int = 9
    MIN_NAME_LENGTH: int = 2
    
    # API settings
    API_TITLE: str = "User Management API"
    API_DESCRIPTION: str = "A REST API for managing users with Israeli phone number and ID validation"
    API_VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 5001
    LOG_LEVEL: str = "info" # tells uvicorn what level of logs to show, can be "debug", "info", "warning", "error", "critical"


settings = Settings()