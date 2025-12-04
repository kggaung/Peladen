"""
Mappers to convert between domain models and DTOs
Following Single Responsibility Principle
"""
from typing import List, Optional
from app.domain.models import (
    Entity, EntityInfo, HealthRecord, CountryCoordinates,
    HealthMetrics, HealthMetricItem, EntityAttribute,
    RelatedEntity, EntitySource
)
from app.application.dto import (
    EntityDTO, EntityInfoDTO, HealthRecordDTO, CountryCoordinatesDTO,
    HealthMetricsDTO, HealthMetricItemDTO, EntityAttributeDTO,
    RelatedEntityDTO, EntitySourceDTO, SearchResponseDTO,
    EntityDetailResponseDTO, InfoBoxResponseDTO
)


class EntityMapper:
    """Maps Entity domain model to DTO"""
    
    @staticmethod
    def to_dto(entity: Entity) -> EntityDTO:
        """Convert Entity to EntityDTO"""
        return EntityDTO(
            id=entity.id,
            label=entity.label,
            type=entity.type,
            iso3Code=entity.iso3_code
        )
    
    @staticmethod
    def to_dto_list(entities: List[Entity]) -> List[EntityDTO]:
        """Convert list of Entities to DTOs"""
        return [EntityMapper.to_dto(e) for e in entities]


class HealthRecordMapper:
    """Maps HealthRecord domain model to DTO"""
    
    @staticmethod
    def to_dto(record: HealthRecord) -> HealthRecordDTO:
        """Convert HealthRecord to HealthRecordDTO"""
        return HealthRecordDTO(
            id=record.id,
            location=record.location,
            year=record.year,
            hivCases=record.hiv_cases,
            malariaCases=record.malaria_cases,
            rabiesCases=record.rabies_cases,
            tuberculosisCases=record.tuberculosis_cases,
            choleraCases=record.cholera_cases,
            guineaworm=record.guineaworm,
            polioCases=record.polio_cases,
            smallpoxCases=record.smallpox_cases,
            yawsCases=record.yaws_cases,
            bcg=record.bcg,
            dtp3=record.dtp3,
            hepb3=record.hepb3,
            hib3=record.hib3,
            measles1=record.measles1,
            polio3=record.polio3,
            rotavirus=record.rotavirus,
            rubella1=record.rubella1,
            populationAge0=record.population_age0
        )
    
    @staticmethod
    def to_dto_list(records: List[HealthRecord]) -> List[HealthRecordDTO]:
        """Convert list of HealthRecords to DTOs"""
        return [HealthRecordMapper.to_dto(r) for r in records]


class HealthMetricsMapper:
    """Maps HealthMetrics domain model to DTO"""
    
    @staticmethod
    def to_dto(metrics: Optional[HealthMetrics]) -> Optional[HealthMetricsDTO]:
        """Convert HealthMetrics to HealthMetricsDTO"""
        if not metrics:
            return None
        
        return HealthMetricsDTO(
            diseaseCases=[
                HealthMetricItemDTO(
                    id=item.id,
                    label=item.label,
                    value=item.value,
                    year=item.year,
                    unit=item.unit,
                    category=item.category
                ) for item in metrics.disease_cases
            ],
            vaccinationCoverage=[
                HealthMetricItemDTO(
                    id=item.id,
                    label=item.label,
                    value=item.value,
                    year=item.year,
                    unit=item.unit,
                    category=item.category
                ) for item in metrics.vaccination_coverage
            ],
            population=[
                HealthMetricItemDTO(
                    id=item.id,
                    label=item.label,
                    value=item.value,
                    year=item.year,
                    unit=item.unit,
                    category=item.category
                ) for item in metrics.population
            ],
            availableYears=metrics.available_years
        )


class EntityInfoMapper:
    """Maps EntityInfo domain model to DTO"""
    
    @staticmethod
    def to_dto(entity_info: EntityInfo) -> EntityInfoDTO:
        """Convert EntityInfo to EntityInfoDTO"""
        return EntityInfoDTO(
            id=entity_info.id,
            label=entity_info.label,
            type=entity_info.type,
            description=entity_info.description,
            image=entity_info.image,
            attributes=[
                EntityAttributeDTO(
                    property=attr.property,
                    propertyLabel=attr.property_label,
                    value=attr.value,
                    valueLabel=attr.value_label,
                    valueType=attr.value_type,
                    unit=attr.unit
                ) for attr in entity_info.attributes
            ],
            healthMetrics=HealthMetricsMapper.to_dto(entity_info.health_metrics),
            relatedEntities=[
                RelatedEntityDTO(
                    id=rel.id,
                    label=rel.label,
                    type=rel.type,
                    relationshipType=rel.relationship_type,
                    relationshipLabel=rel.relationship_label,
                    description=rel.description
                ) for rel in entity_info.related_entities
            ],
            sources=[
                EntitySourceDTO(
                    name=src.name,
                    url=src.url,
                    date=src.date
                ) for src in entity_info.sources
            ]
        )


class CountryCoordinatesMapper:
    """Maps CountryCoordinates domain model to DTO"""
    
    @staticmethod
    def to_dto(coords: CountryCoordinates) -> CountryCoordinatesDTO:
        """Convert CountryCoordinates to CountryCoordinatesDTO"""
        return CountryCoordinatesDTO(
            iso3Code=coords.iso3_code,
            label=coords.label,
            latitude=coords.latitude,
            longitude=coords.longitude
        )
    
    @staticmethod
    def to_dto_list(coords_list: List[CountryCoordinates]) -> List[CountryCoordinatesDTO]:
        """Convert list of CountryCoordinates to DTOs"""
        return [CountryCoordinatesMapper.to_dto(c) for c in coords_list]
