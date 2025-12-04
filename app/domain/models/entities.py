"""
Domain Models following Domain-Driven Design
These are pure domain entities with business logic
"""
from dataclasses import dataclass, field
from typing import Optional, List, Literal
from datetime import datetime


EntityType = Literal["country", "region", "organization", "division"]


@dataclass
class Entity:
    """Domain entity representing countries, regions, or organizations"""
    id: str
    label: str
    type: EntityType
    iso3_code: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            raise ValueError("Entity ID cannot be empty")
        if not self.label:
            raise ValueError("Entity label cannot be empty")


@dataclass
class HealthRecord:
    """Health data record for a specific location and year"""
    id: str
    location: str  # Entity ID
    year: int
    
    # Disease Cases
    hiv_cases: Optional[float] = None
    malaria_cases: Optional[float] = None
    rabies_cases: Optional[float] = None
    tuberculosis_cases: Optional[float] = None
    cholera_cases: Optional[float] = None
    guineaworm: Optional[float] = None
    polio_cases: Optional[float] = None
    smallpox_cases: Optional[float] = None
    yaws_cases: Optional[float] = None
    
    # Vaccination Coverage (one-year-olds)
    bcg: Optional[float] = None
    dtp3: Optional[float] = None
    hepb3: Optional[float] = None
    hib3: Optional[float] = None
    measles1: Optional[float] = None
    polio3: Optional[float] = None
    rotavirus: Optional[float] = None
    rubella1: Optional[float] = None
    
    # Population
    population_age0: Optional[float] = None
    
    def __post_init__(self):
        if self.year < 1900 or self.year > 2100:
            raise ValueError(f"Invalid year: {self.year}")


@dataclass
class Property:
    """RDF Property definition"""
    id: str
    label: str
    description: Optional[str] = None


@dataclass
class HealthMetricItem:
    """Individual health metric with metadata"""
    id: str
    label: str
    value: float
    year: int
    unit: Optional[str] = None
    category: Literal["disease", "vaccination", "population"] = "disease"


@dataclass
class HealthMetrics:
    """Grouped health metrics for an entity"""
    disease_cases: List[HealthMetricItem] = field(default_factory=list)
    vaccination_coverage: List[HealthMetricItem] = field(default_factory=list)
    population: List[HealthMetricItem] = field(default_factory=list)
    available_years: List[int] = field(default_factory=list)


@dataclass
class EntityAttribute:
    """Attribute of an entity with rich metadata"""
    property: str
    property_label: str
    value: str
    value_label: Optional[str] = None
    value_type: Literal["string", "number", "date", "uri", "entity"] = "string"
    unit: Optional[str] = None


@dataclass
class RelatedEntity:
    """Related entity with relationship information"""
    id: str
    label: str
    type: EntityType
    relationship_type: str
    relationship_label: str
    description: Optional[str] = None


@dataclass
class EntitySource:
    """Data source information"""
    name: str
    url: Optional[str] = None
    date: Optional[str] = None


@dataclass
class EntityInfo:
    """Complete entity information for InfoBox"""
    id: str
    label: str
    type: EntityType
    description: Optional[str] = None
    image: Optional[str] = None
    attributes: List[EntityAttribute] = field(default_factory=list)
    health_metrics: Optional[HealthMetrics] = None
    related_entities: List[RelatedEntity] = field(default_factory=list)
    sources: List[EntitySource] = field(default_factory=list)


@dataclass
class CountryCoordinates:
    """Geographic coordinates for map display"""
    iso3_code: str
    label: str
    latitude: float
    longitude: float
    
    def __post_init__(self):
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Invalid latitude: {self.latitude}")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Invalid longitude: {self.longitude}")


@dataclass
class SPARQLBinding:
    """SPARQL query result binding"""
    var: str
    value: str
    type: Literal["uri", "literal", "bnode"]
    datatype: Optional[str] = None
    lang: Optional[str] = None


@dataclass
class SPARQLQueryResult:
    """SPARQL query result"""
    variables: List[str]
    bindings: List[dict]
    
    def to_dict(self):
        """Convert to SPARQL JSON format"""
        return {
            "head": {"vars": self.variables},
            "results": {"bindings": self.bindings}
        }
