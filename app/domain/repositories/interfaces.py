"""
Repository Interfaces following Dependency Inversion Principle
These are abstractions that domain/application layers depend on
Infrastructure layer provides concrete implementations
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.domain.models import (
    Entity, EntityInfo, HealthRecord, CountryCoordinates,
    SPARQLQueryResult, EntityType
)


class IEntityRepository(ABC):
    """
    Interface for entity operations
    Following Interface Segregation Principle - focused interface
    """
    
    @abstractmethod
    async def search(
        self, 
        query: str, 
        entity_type: Optional[EntityType] = None,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Entity], int]:
        """
        Search entities by query string
        Returns: (entities, total_count)
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    async def get_suggestions(self, query: str, limit: int = 10) -> List[Entity]:
        """Get autocomplete suggestions"""
        pass
    
    @abstractmethod
    async def get_by_iso3_code(self, iso3_code: str) -> Optional[Entity]:
        """Get entity by ISO 3166-1 alpha-3 code"""
        pass


class IEntityInfoRepository(ABC):
    """Interface for detailed entity information"""
    
    @abstractmethod
    async def get_entity_info(self, entity_id: str) -> Optional[EntityInfo]:
        """Get complete entity information for InfoBox"""
        pass
    
    @abstractmethod
    async def get_related_entities(
        self, 
        entity_id: str, 
        limit: int = 10
    ) -> List[Entity]:
        """Get entities related to given entity"""
        pass


class IHealthRecordRepository(ABC):
    """Interface for health record operations"""
    
    @abstractmethod
    async def get_by_location(
        self, 
        location_id: str, 
        year: Optional[int] = None
    ) -> List[HealthRecord]:
        """Get health records for a location, optionally filtered by year"""
        pass
    
    @abstractmethod
    async def get_available_years(self, location_id: str) -> List[int]:
        """Get years with available data for a location"""
        pass


class IMapRepository(ABC):
    """Interface for map-related operations"""
    
    @abstractmethod
    async def get_all_country_coordinates(self) -> List[CountryCoordinates]:
        """Get coordinates for all countries"""
        pass
    
    @abstractmethod
    async def get_country_by_iso3(self, iso3_code: str) -> Optional[Entity]:
        """Get country entity by ISO3 code"""
        pass


class ISPARQLRepository(ABC):
    """Interface for SPARQL query execution"""
    
    @abstractmethod
    async def execute_query(self, query: str) -> SPARQLQueryResult:
        """Execute SPARQL query against the knowledge graph"""
        pass
    
    @abstractmethod
    async def validate_query(self, query: str) -> tuple[bool, Optional[str]]:
        """
        Validate SPARQL query syntax
        Returns: (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    async def get_sample_queries(self) -> List[str]:
        """Get sample SPARQL queries"""
        pass
