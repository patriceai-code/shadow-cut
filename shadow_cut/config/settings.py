from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    google_cloud_project: str = "shadow-cut-hackathon"
    gemini_api_key: str = ""
    google_application_credentials: str = ".\\service-account.json"
    firestore_project_id: str = "shadow-cut-hackathon"
    firestore_database: str = "(default)"
    gcs_bucket: str = "shadow-cut-proxies"
    confluent_bootstrap_servers: str = "localhost:9092"
    confluent_api_key: str = "local-key"
    confluent_api_secret: str = "local-secret"
    confluent_topic: str = "shadow-cut.takes.uploaded"
    use_confluent_fallback: bool = True
    pro_escalation_budget: int = 50
    env: str = "development"
    log_level: str = "INFO"
    yolo_device: str = "cpu"
    yolo_model_path: str = ".\\models\\yolo-world"
    ibm_watsonx_api_key: Optional[str] = None
    ibm_watsonx_url: Optional[str] = "https://eu-gb.ml.cloud.ibm.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
