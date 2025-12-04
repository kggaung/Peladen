"""
Application DTO Package
Exports all data transfer objects (schemas)
"""
from app.application.dto.schemas import (
    # Request DTOs
    SearchQueryParams,
    SPARQLQueryRequest,
    
    # Response DTOs
    EntityDTO,
    SearchResponseDTO,
    HealthRecordDTO,
    HealthMetricItemDTO,
    HealthMetricsDTO,
    EntityAttributeDTO,
    RelatedEntityDTO,
    EntitySourceDTO,
    EntityInfoDTO,
    InfoBoxResponseDTO,
    EntityDetailResponseDTO,
    CountryCoordinatesDTO,
    SPARQLValueDTO,
    SPARQLQueryResponseDTO,
    SPARQLValidationResponseDTO,
    SampleQueriesResponseDTO,
    ErrorResponseDTO,
)

__all__ = [
    # Request DTOs
    "SearchQueryParams",
    "SPARQLQueryRequest",
    
    # Response DTOs
    "EntityDTO",
    "SearchResponseDTO",
    "HealthRecordDTO",
    "HealthMetricItemDTO",
    "HealthMetricsDTO",
    "EntityAttributeDTO",
    "RelatedEntityDTO",
    "EntitySourceDTO",
    "EntityInfoDTO",
    "InfoBoxResponseDTO",
    "EntityDetailResponseDTO",
    "CountryCoordinatesDTO",
    "SPARQLValueDTO",
    "SPARQLQueryResponseDTO",
    "SPARQLValidationResponseDTO",
    "SampleQueriesResponseDTO",
    "ErrorResponseDTO",
]
