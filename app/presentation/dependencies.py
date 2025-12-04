"""
Dependency Injection Container
Following Dependency Inversion Principle
Provides instances of services and repositories to controllers
"""
from functools import lru_cache
from app.infrastructure.config.settings import settings
from app.infrastructure.repositories.graphdb_repository import (
    GraphDBClient, EntityRepository, EntityInfoRepository
)
from app.infrastructure.repositories.additional_repositories import (
    HealthRecordRepository, MapRepository, SPARQLRepository
)
from app.application.services import (
    SearchService, EntityInfoService, HealthRecordService,
    MapService, SPARQLQueryService
)


# GraphDB Client (Singleton)
@lru_cache()
def get_graphdb_client() -> GraphDBClient:
    """Get GraphDB client instance"""
    return GraphDBClient(settings.sparql_endpoint)


# Repositories
@lru_cache()
def get_entity_repository() -> EntityRepository:
    """Get entity repository instance"""
    return EntityRepository(get_graphdb_client())


@lru_cache()
def get_entity_info_repository() -> EntityInfoRepository:
    """Get entity info repository instance"""
    return EntityInfoRepository(get_graphdb_client())


@lru_cache()
def get_health_record_repository() -> HealthRecordRepository:
    """Get health record repository instance"""
    return HealthRecordRepository(get_graphdb_client())


@lru_cache()
def get_map_repository() -> MapRepository:
    """Get map repository instance"""
    return MapRepository(get_graphdb_client())


@lru_cache()
def get_sparql_repository() -> SPARQLRepository:
    """Get SPARQL repository instance"""
    return SPARQLRepository(get_graphdb_client())


# Services
def get_search_service() -> SearchService:
    """Get search service instance"""
    return SearchService(get_entity_repository())


def get_entity_info_service() -> EntityInfoService:
    """Get entity info service instance"""
    return EntityInfoService(
        get_entity_info_repository(),
        get_health_record_repository()
    )


def get_health_record_service() -> HealthRecordService:
    """Get health record service instance"""
    return HealthRecordService(get_health_record_repository())


def get_map_service() -> MapService:
    """Get map service instance"""
    return MapService(get_map_repository())


def get_sparql_service() -> SPARQLQueryService:
    """Get SPARQL service instance"""
    return SPARQLQueryService(get_sparql_repository())
