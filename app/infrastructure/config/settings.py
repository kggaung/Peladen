"""
Application Configuration following Single Responsibility Principle
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # GraphDB Configuration
    graphdb_url: str = "http://localhost:7200"
    graphdb_repository: str = "knowledge-graph"
    sparql_endpoint: str = "http://localhost:7200/repositories/knowledge-graph"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 3000
    api_reload: bool = True
    
    # CORS Configuration
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    cors_allow_credentials: bool = True
    cors_allow_methods: str = "*"
    cors_allow_headers: str = "*"
    
    # Logging
    log_level: str = "INFO"
    
    # RDF Namespaces
    kg_entity_ns: str = "http://kg.gaung.org/entity/"
    kg_property_ns: str = "http://kg.gaung.org/property/"
    kg_record_ns: str = "http://kg.gaung.org/record/"
    wd_entity_ns: str = "http://www.wikidata.org/entity/"
    wd_property_ns: str = "http://www.wikidata.org/prop/direct/"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Singleton instance
settings = Settings()
