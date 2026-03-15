from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Mini SOC Platform"
    app_env: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./soc.db"
    brute_force_threshold: int = 5
    suspicious_ip_threshold: int = 10
    alert_cooldown_seconds: int = 60
    log_file_path: str = "logs/sample_auth.log"
    log_poll_interval: int = 2
    geoip_enabled: bool = False
    geoip_db_path: str = "GeoLite2-City.mmdb"

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()