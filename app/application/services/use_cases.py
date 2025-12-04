"""
Application Services (Use Cases)
Following Single Responsibility Principle
Each service handles one specific business capability
"""
from typing import List, Optional, Tuple
from app.domain.models import (
    Entity, EntityInfo, HealthRecord, CountryCoordinates, 
    SPARQLQueryResult, EntityType, HealthMetrics, HealthMetricItem
)
from app.domain.repositories import (
    IEntityRepository, IEntityInfoRepository, IHealthRecordRepository,
    IMapRepository, ISPARQLRepository
)
import logging

logger = logging.getLogger(__name__)


class SearchService:
    """
    Search service following Single Responsibility Principle
    Handles search-related business logic
    """
    
    def __init__(self, entity_repo: IEntityRepository):
        self.entity_repo = entity_repo
    
    async def search_entities(
        self,
        query: str,
        entity_type: Optional[EntityType] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Entity], int, int]:
        """
        Search entities with pagination
        Returns: (entities, total_count, current_page)
        """
        offset = (page - 1) * page_size
        entities, total = await self.entity_repo.search(
            query=query,
            entity_type=entity_type,
            limit=page_size,
            offset=offset
        )
        return entities, total, page
    
    async def get_entity_by_id(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID"""
        return await self.entity_repo.get_by_id(entity_id)
    
    async def get_suggestions(self, query: str, limit: int = 10) -> List[Entity]:
        """Get autocomplete suggestions"""
        if len(query) < 2:
            return []
        return await self.entity_repo.get_suggestions(query, limit)


class EntityInfoService:
    """
    Entity information service
    Handles retrieval and enrichment of entity details
    """
    
    def __init__(
        self,
        entity_info_repo: IEntityInfoRepository,
        health_record_repo: IHealthRecordRepository
    ):
        self.entity_info_repo = entity_info_repo
        self.health_record_repo = health_record_repo
    
    async def get_entity_info(self, entity_id: str) -> Optional[EntityInfo]:
        """Get complete entity information with health metrics"""
        entity_info = await self.entity_info_repo.get_entity_info(entity_id)
        
        if not entity_info:
            return None
        
        # Enrich with health metrics
        health_metrics = await self._get_health_metrics(entity_id)
        entity_info.health_metrics = health_metrics
        
        return entity_info
    
    async def get_entity_info_by_label(self, label: str) -> Optional[EntityInfo]:
        """Get entity info by label (search-based)"""
        # Implementation would search and return first match
        # For simplicity, we'll skip this for now
        return None
    
    async def get_related_entities(
        self,
        entity_id: str,
        limit: int = 10
    ) -> List[Entity]:
        """Get related entities"""
        return await self.entity_info_repo.get_related_entities(entity_id, limit)
    
    async def _get_health_metrics(self, entity_id: str) -> Optional[HealthMetrics]:
        """Get and organize health metrics for entity"""
        try:
            records = await self.health_record_repo.get_by_location(entity_id)
            
            if not records:
                return None
            
            disease_cases = []
            vaccination_coverage = []
            population_metrics = []
            years = set()
            
            for record in records:
                years.add(record.year)
                
                # Disease cases
                if record.hiv_cases is not None:
                    disease_cases.append(HealthMetricItem(
                        id="hivCases",
                        label="HIV/AIDS Cases",
                        value=record.hiv_cases,
                        year=record.year,
                        unit="cases",
                        category="disease"
                    ))
                
                if record.malaria_cases is not None:
                    disease_cases.append(HealthMetricItem(
                        id="malariaCases",
                        label="Malaria Cases",
                        value=record.malaria_cases,
                        year=record.year,
                        unit="cases",
                        category="disease"
                    ))
                
                if record.tuberculosis_cases is not None:
                    disease_cases.append(HealthMetricItem(
                        id="tuberculosisCases",
                        label="Tuberculosis Cases",
                        value=record.tuberculosis_cases,
                        year=record.year,
                        unit="cases",
                        category="disease"
                    ))
                
                if record.rabies_cases is not None:
                    disease_cases.append(HealthMetricItem(
                        id="rabiesCases",
                        label="Rabies Cases",
                        value=record.rabies_cases,
                        year=record.year,
                        unit="cases",
                        category="disease"
                    ))
                
                if record.cholera_cases is not None:
                    disease_cases.append(HealthMetricItem(
                        id="choleraCases",
                        label="Cholera Cases",
                        value=record.cholera_cases,
                        year=record.year,
                        unit="cases",
                        category="disease"
                    ))
                
                # Vaccination coverage
                if record.bcg is not None:
                    vaccination_coverage.append(HealthMetricItem(
                        id="bcg",
                        label="BCG",
                        value=record.bcg,
                        year=record.year,
                        unit="children",
                        category="vaccination"
                    ))
                
                if record.dtp3 is not None:
                    vaccination_coverage.append(HealthMetricItem(
                        id="dtp3",
                        label="DTP3",
                        value=record.dtp3,
                        year=record.year,
                        unit="children",
                        category="vaccination"
                    ))
                
                if record.hepb3 is not None:
                    vaccination_coverage.append(HealthMetricItem(
                        id="hepb3",
                        label="HepB3",
                        value=record.hepb3,
                        year=record.year,
                        unit="children",
                        category="vaccination"
                    ))
                
                if record.hib3 is not None:
                    vaccination_coverage.append(HealthMetricItem(
                        id="hib3",
                        label="Hib3",
                        value=record.hib3,
                        year=record.year,
                        unit="children",
                        category="vaccination"
                    ))
                
                if record.measles1 is not None:
                    vaccination_coverage.append(HealthMetricItem(
                        id="measles1",
                        label="Measles (1st dose)",
                        value=record.measles1,
                        year=record.year,
                        unit="children",
                        category="vaccination"
                    ))
                
                if record.polio3 is not None:
                    vaccination_coverage.append(HealthMetricItem(
                        id="polio3",
                        label="Polio (3rd dose)",
                        value=record.polio3,
                        year=record.year,
                        unit="children",
                        category="vaccination"
                    ))
                
                if record.rotavirus is not None:
                    vaccination_coverage.append(HealthMetricItem(
                        id="rotavirus",
                        label="Rotavirus (last dose)",
                        value=record.rotavirus,
                        year=record.year,
                        unit="children",
                        category="vaccination"
                    ))
                
                if record.rubella1 is not None:
                    vaccination_coverage.append(HealthMetricItem(
                        id="rubella1",
                        label="Rubella (1st dose)",
                        value=record.rubella1,
                        year=record.year,
                        unit="children",
                        category="vaccination"
                    ))
                
                # Population
                if record.population_age0 is not None:
                    population_metrics.append(HealthMetricItem(
                        id="populationAge0",
                        label="Population Age 0",
                        value=record.population_age0,
                        year=record.year,
                        unit="people",
                        category="population"
                    ))
            
            return HealthMetrics(
                disease_cases=disease_cases,
                vaccination_coverage=vaccination_coverage,
                population=population_metrics,
                available_years=sorted(list(years))
            )
        
        except Exception as e:
            logger.error(f"Error getting health metrics: {e}")
            return None


class HealthRecordService:
    """Health record service"""
    
    def __init__(self, health_record_repo: IHealthRecordRepository):
        self.health_record_repo = health_record_repo
    
    async def get_health_records(
        self,
        location_id: str,
        year: Optional[int] = None
    ) -> List[HealthRecord]:
        """Get health records for a location"""
        return await self.health_record_repo.get_by_location(location_id, year)
    
    async def get_available_years(self, location_id: str) -> List[int]:
        """Get available years for a location"""
        return await self.health_record_repo.get_available_years(location_id)


class MapService:
    """Map service for geographic data"""
    
    def __init__(self, map_repo: IMapRepository):
        self.map_repo = map_repo
    
    async def get_all_country_coordinates(self) -> List[CountryCoordinates]:
        """Get coordinates for all countries"""
        return await self.map_repo.get_all_country_coordinates()
    
    async def get_country_info(self, iso3_code: str) -> Optional[Entity]:
        """Get country information by ISO3 code"""
        return await self.map_repo.get_country_by_iso3(iso3_code)


class SPARQLQueryService:
    """SPARQL query service"""
    
    def __init__(self, sparql_repo: ISPARQLRepository):
        self.sparql_repo = sparql_repo
    
    async def execute_query(
        self,
        query: str,
        limit: Optional[int] = None
    ) -> SPARQLQueryResult:
        """Execute SPARQL query"""
        # Apply limit if specified
        if limit:
            query = f"{query.rstrip()} LIMIT {limit}"
        
        return await self.sparql_repo.execute_query(query)
    
    async def validate_query(self, query: str) -> Tuple[bool, Optional[str]]:
        """Validate SPARQL query"""
        return await self.sparql_repo.validate_query(query)
    
    async def get_sample_queries(self) -> List[str]:
        """Get sample queries"""
        return await self.sparql_repo.get_sample_queries()
