from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator, ConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Solicitudes Service"
    VERSION: str = "0.2.0"
    DESCRIPTION: str = "API para gestión de solicitudes de donación de sangre con soporte para imágenes y MongoDB"
    
    # MongoDB - Atlas por defecto, local como fallback
    MONGODB_URL: str = "mongodb+srv://username:password@cluster.mongodb.net/solicitudes?retryWrites=true&w=majority"
    MONGODB_DATABASE: str = "solicitudes"
    
    # MongoDB Testing (base de datos separada para tests)
    MONGODB_TEST_URL: str = "mongodb+srv://username:password@cluster.mongodb.net/solicitudes_test?retryWrites=true&w=majority"
    MONGODB_TEST_DATABASE: str = "solicitudes_test"
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    

    
    # Application Configuration
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    BASE_URL: str = "http://127.0.0.1:8000"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = ConfigDict(case_sensitive=True, env_file=".env")

settings = Settings() 