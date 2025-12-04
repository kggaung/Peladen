"""
Data Transfer Objects (DTOs) for API layer
Following Interface Segregation Principle - separate request/response models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# Request DTOs
class SearchQueryParams(BaseModel):
    """Search query parameters"""
    query: str = Field(..., min_length=1, description="Search query string")
    type: Optional[Literal["country", "region", "organization"]] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100, alias="pageSize")


class SPARQLQueryRequest(BaseModel):
    """SPARQL query request"""
    query: str = Field(..., min_length=1)
    format: Literal["json", "xml", "csv"] = "json"
    limit: Optional[int] = Field(None, ge=1, le=10000)


# Response DTOs
class EntityDTO(BaseModel):
    """Entity response model"""
    id: str
    label: str
    type: Literal["country", "region", "organization"]
    iso3Code: Optional[str] = Field(None, alias="iso3Code")
    
    class Config:
        populate_by_name = True


class SearchResponseDTO(BaseModel):
    """Search response model"""
    results: List[EntityDTO]
    total: int
    page: int
    pageSize: int = Field(alias="pageSize")
    
    class Config:
        populate_by_name = True


class HealthRecordDTO(BaseModel):
    """Health record response model"""
    id: str
    location: str
    year: int
    
    # Disease cases
    hivCases: Optional[float] = None
    malariaCases: Optional[float] = None
    rabiesCases: Optional[float] = None
    tuberculosisCases: Optional[float] = None
    choleraCases: Optional[float] = None
    guineaworm: Optional[float] = None
    polioCases: Optional[float] = None
    smallpoxCases: Optional[float] = None
    yawsCases: Optional[float] = None
    
    # Vaccination coverage
    bcg: Optional[float] = None
    dtp3: Optional[float] = None
    hepb3: Optional[float] = None
    hib3: Optional[float] = None
    measles1: Optional[float] = None
    polio3: Optional[float] = None
    rotavirus: Optional[float] = None
    rubella1: Optional[float] = None
    
    # Population
    populationAge0: Optional[float] = None


class HealthMetricItemDTO(BaseModel):
    """Health metric item"""
    id: str
    label: str
    value: float
    year: int
    unit: Optional[str] = None
    category: Literal["disease", "vaccination", "population"]


class HealthMetricsDTO(BaseModel):
    """Grouped health metrics"""
    diseaseCases: List[HealthMetricItemDTO] = []
    vaccinationCoverage: List[HealthMetricItemDTO] = []
    population: List[HealthMetricItemDTO] = []
    availableYears: List[int] = []


class EntityAttributeDTO(BaseModel):
    """Entity attribute"""
    property: str
    propertyLabel: str
    value: str
    valueLabel: Optional[str] = None
    valueType: Literal["string", "number", "date", "uri", "entity"] = "string"
    unit: Optional[str] = None


class RelatedEntityDTO(BaseModel):
    """Related entity"""
    id: str
    label: str
    type: Literal["country", "region", "organization"]
    relationshipType: str
    relationshipLabel: str
    description: Optional[str] = None


class EntitySourceDTO(BaseModel):
    """Entity source"""
    name: str
    url: Optional[str] = None
    date: Optional[str] = None


class EntityInfoDTO(BaseModel):
    """Complete entity information"""
    id: str
    label: str
    type: Literal["country", "region", "organization"]
    description: Optional[str] = None
    image: Optional[str] = None
    attributes: List[EntityAttributeDTO] = []
    healthMetrics: Optional[HealthMetricsDTO] = None
    relatedEntities: List[RelatedEntityDTO] = []
    sources: List[EntitySourceDTO] = []


class InfoBoxResponseDTO(BaseModel):
    """InfoBox response"""
    entity: EntityInfoDTO
    sparqlQuery: Optional[str] = None


class EntityDetailResponseDTO(BaseModel):
    """Entity detail response with health records"""
    entity: EntityDTO
    healthRecords: List[HealthRecordDTO] = []
    relatedEntities: Optional[List[EntityDTO]] = None


class CountryCoordinatesDTO(BaseModel):
    """Country coordinates"""
    iso3Code: str
    label: str
    latitude: float
    longitude: float


class SPARQLValueDTO(BaseModel):
    """SPARQL result value"""
    type: Literal["uri", "literal", "bnode"]
    value: str
    datatype: Optional[str] = None
    lang: Optional[str] = Field(None, alias="xml:lang")
    
    class Config:
        populate_by_name = True


class SPARQLQueryResponseDTO(BaseModel):
    """SPARQL query response"""
    head: dict
    results: dict


class SPARQLValidationResponseDTO(BaseModel):
    """SPARQL validation response"""
    valid: bool
    error: Optional[str] = None


class SampleQueriesResponseDTO(BaseModel):
    """Sample queries response"""
    queries: List[str]


class ErrorResponseDTO(BaseModel):
    """Error response"""
    message: str
    code: Optional[str] = None
    details: Optional[dict] = None
