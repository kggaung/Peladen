"""
GraphDB Repository Implementation using SPARQLWrapper
Implements repository interfaces from domain layer (Dependency Inversion Principle)
"""
from typing import List, Optional, Dict, Any
from SPARQLWrapper import SPARQLWrapper, JSON
import asyncio
from functools import partial
from app.domain.models import (
    Entity, EntityInfo, HealthRecord, CountryCoordinates,
    SPARQLQueryResult, EntityType, HealthMetrics, HealthMetricItem,
    EntityAttribute, RelatedEntity, EntitySource
)
from app.domain.repositories import (
    IEntityRepository, IEntityInfoRepository, IHealthRecordRepository,
    IMapRepository, ISPARQLRepository
)
from app.infrastructure.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class GraphDBClient:
    """SPARQL client wrapper for GraphDB"""
    
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)
    
    def _execute_query(self, sparql_query: str) -> Dict[str, Any]:
        """Synchronous query execution"""
        self.sparql.setQuery(sparql_query)
        return self.sparql.query().convert()
    
    async def query(self, sparql_query: str) -> Dict[str, Any]:
        """Execute SPARQL query asynchronously in thread pool"""
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                partial(self._execute_query, sparql_query)
            )
            return results
        except Exception as e:
            logger.error(f"SPARQL query error: {e}")
            logger.error(f"Query: {sparql_query}")
            raise


class EntityRepository(IEntityRepository):
    """Entity repository implementation using SPARQL"""
    
    def __init__(self, graphdb_client: GraphDBClient):
        self.client = graphdb_client
        self.kge_ns = settings.kg_entity_ns
        self.wd_ns = settings.wd_entity_ns
        self.wdt_ns = settings.wd_property_ns
    
    async def search(
        self,
        query: str,
        entity_type: Optional[EntityType] = None,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Entity], int]:
        """Search entities by query string with optional type filter"""
        
        # Build type filter
        type_filter = ""
        if entity_type == "country":
            type_filter = "?entity wdt:P31/wdt:P279* wd:Q6256 ."
        elif entity_type == "region":
            type_filter = """
                ?entity wdt:P31/wdt:P279* ?regionType .
                FILTER(?regionType IN (wd:Q82794, wd:Q5107, wd:Q2418896))
            """
        elif entity_type == "organization":
            type_filter = "?entity wdt:P31/wdt:P279* wd:Q43229 ."
        
        sparql_query = f"""
        PREFIX wd: <{self.wd_ns}>
        PREFIX wdt: <{self.wdt_ns}>
        PREFIX kge: <{self.kge_ns}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?entity ?label ?iso3Code WHERE {{
            {{
                ?entity rdfs:label ?label .
                FILTER(CONTAINS(LCASE(?label), LCASE("{query}")))
                {type_filter}
                OPTIONAL {{ ?entity wdt:P298 ?iso3Code . }}
            }}
            UNION
            {{
                ?entity rdfs:label ?label .
                FILTER(CONTAINS(LCASE(STR(?entity)), LCASE("{query}")))
                {type_filter}
                OPTIONAL {{ ?entity wdt:P298 ?iso3Code . }}
            }}
        }}
        LIMIT {limit}
        OFFSET {offset}
        """
        
        # Count query
        count_query = f"""
        PREFIX wd: <{self.wd_ns}>
        PREFIX wdt: <{self.wdt_ns}>
        PREFIX kge: <{self.kge_ns}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT (COUNT(DISTINCT ?entity) AS ?count) WHERE {{
            {{
                ?entity rdfs:label ?label .
                FILTER(CONTAINS(LCASE(?label), LCASE("{query}")))
                {type_filter}
            }}
            UNION
            {{
                ?entity rdfs:label ?label .
                FILTER(CONTAINS(LCASE(STR(?entity)), LCASE("{query}")))
                {type_filter}
            }}
        }}
        """
        
        results = await self.client.query(sparql_query)
        count_results = await self.client.query(count_query)
        
        entities = self._parse_entities(results)
        total = int(count_results["results"]["bindings"][0]["count"]["value"]) if count_results["results"]["bindings"] else 0
        
        return entities, total
    
    async def get_by_id(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID"""
        sparql_query = f"""
        PREFIX wdt: <{self.wdt_ns}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?label ?iso3Code WHERE {{
            <{entity_id}> rdfs:label ?label .
            OPTIONAL {{ <{entity_id}> wdt:P298 ?iso3Code . }}
        }}
        """
        
        results = await self.client.query(sparql_query)
        bindings = results["results"]["bindings"]
        
        if not bindings:
            return None
        
        binding = bindings[0]
        entity_type = self._determine_entity_type(entity_id)
        
        return Entity(
            id=entity_id,
            label=binding["label"]["value"],
            type=entity_type,
            iso3_code=binding.get("iso3Code", {}).get("value")
        )
    
    async def get_suggestions(self, query: str, limit: int = 10) -> List[Entity]:
        """Get autocomplete suggestions"""
        entities, _ = await self.search(query, limit=limit)
        return entities
    
    async def get_by_iso3_code(self, iso3_code: str) -> Optional[Entity]:
        """Get entity by ISO 3166-1 alpha-3 code"""
        sparql_query = f"""
        PREFIX wdt: <{self.wdt_ns}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?entity ?label WHERE {{
            ?entity wdt:P298 "{iso3_code}" ;
                    rdfs:label ?label .
        }}
        """
        
        results = await self.client.query(sparql_query)
        bindings = results["results"]["bindings"]
        
        if not bindings:
            return None
        
        binding = bindings[0]
        return Entity(
            id=binding["entity"]["value"],
            label=binding["label"]["value"],
            type="country",
            iso3_code=iso3_code
        )
    
    def _parse_entities(self, results: Dict[str, Any]) -> List[Entity]:
        """Parse SPARQL results to Entity objects"""
        entities = []
        for binding in results["results"]["bindings"]:
            entity_id = binding["entity"]["value"]
            entity_type = self._determine_entity_type(entity_id)
            
            entities.append(Entity(
                id=entity_id,
                label=binding["label"]["value"],
                type=entity_type,
                iso3_code=binding.get("iso3Code", {}).get("value")
            ))
        
        return entities
    
    def _determine_entity_type(self, entity_id: str) -> EntityType:
        """Determine entity type from ID"""
        if entity_id.startswith(self.kge_ns):
            # Custom entities are regions
            return "region"
        elif "Q" in entity_id:
            # Default to country for Wikidata entities
            # In production, you'd query for actual type
            return "country"
        return "organization"


class EntityInfoRepository(IEntityInfoRepository):
    """Entity info repository for detailed entity information"""
    
    def __init__(self, graphdb_client: GraphDBClient):
        self.client = graphdb_client
        self.kge_ns = settings.kg_entity_ns
        self.wd_ns = settings.wd_entity_ns
        self.wdt_ns = settings.wd_property_ns
    
    async def get_entity_info(self, entity_id: str) -> Optional[EntityInfo]:
        """Get complete entity information"""
        
        # Get basic entity info
        basic_query = f"""
        PREFIX wdt: <{self.wdt_ns}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX schema: <http://schema.org/>
        
        SELECT ?label ?description ?image WHERE {{
            <{entity_id}> rdfs:label ?label .
            OPTIONAL {{ <{entity_id}> schema:description ?description . }}
            OPTIONAL {{ <{entity_id}> wdt:P18 ?image . }}
        }}
        """
        
        results = await self.client.query(basic_query)
        if not results["results"]["bindings"]:
            return None
        
        binding = results["results"]["bindings"][0]
        
        # Get attributes
        attributes = await self._get_attributes(entity_id)
        
        # Get related entities
        related = await self.get_related_entities(entity_id)
        
        entity_type = self._determine_entity_type(entity_id)
        
        return EntityInfo(
            id=entity_id,
            label=binding["label"]["value"],
            type=entity_type,
            description=binding.get("description", {}).get("value"),
            image=binding.get("image", {}).get("value"),
            attributes=attributes,
            health_metrics=None,  # Will be populated by service layer
            related_entities=[
                RelatedEntity(
                    id=e.id,
                    label=e.label,
                    type=e.type,
                    relationship_type="partOf",
                    relationship_label="Part of"
                ) for e in related
            ],
            sources=[
                EntitySource(
                    name="Wikidata",
                    url=entity_id if entity_id.startswith("http://www.wikidata.org") else None
                )
            ]
        )
    
    async def get_related_entities(self, entity_id: str, limit: int = 10) -> List[Entity]:
        """Get related entities"""
        sparql_query = f"""
        PREFIX wdt: <{self.wdt_ns}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?related ?label ?iso3Code WHERE {{
            {{
                <{entity_id}> wdt:P361 ?related .
            }}
            UNION
            {{
                ?related wdt:P361 <{entity_id}> .
            }}
            ?related rdfs:label ?label .
            OPTIONAL {{ ?related wdt:P298 ?iso3Code . }}
        }}
        LIMIT {limit}
        """
        
        results = await self.client.query(sparql_query)
        entities = []
        
        for binding in results["results"]["bindings"]:
            entity_type = self._determine_entity_type(binding["related"]["value"])
            entities.append(Entity(
                id=binding["related"]["value"],
                label=binding["label"]["value"],
                type=entity_type,
                iso3_code=binding.get("iso3Code", {}).get("value")
            ))
        
        return entities
    
    async def _get_attributes(self, entity_id: str) -> List[EntityAttribute]:
        """Get entity attributes"""
        # Get specific important properties with known labels
        sparql_query = f"""
        PREFIX wdt: <{self.wdt_ns}>
        PREFIX wd: <{self.wd_ns}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?iso3Code ?population ?area ?capital ?inception WHERE {{
            OPTIONAL {{ <{entity_id}> wdt:P298 ?iso3Code . }}
            OPTIONAL {{ <{entity_id}> wdt:P1082 ?population . }}
            OPTIONAL {{ <{entity_id}> wdt:P2046 ?area . }}
            OPTIONAL {{ <{entity_id}> wdt:P36 ?capital . }}
            OPTIONAL {{ <{entity_id}> wdt:P571 ?inception . }}
        }}
        LIMIT 1
        """
        
        results = await self.client.query(sparql_query)
        attributes = []
        
        if results["results"]["bindings"]:
            binding = results["results"]["bindings"][0]
            
            # ISO 3166-1 alpha-3 code
            if "iso3Code" in binding:
                attributes.append(EntityAttribute(
                    property="http://www.wikidata.org/prop/direct/P298",
                    property_label="ISO 3166-1 alpha-3 code",
                    value=binding["iso3Code"]["value"],
                    value_type="string"
                ))
            
            # Population
            if "population" in binding:
                pop_value = binding["population"]["value"]
                attributes.append(EntityAttribute(
                    property="http://www.wikidata.org/prop/direct/P1082",
                    property_label="Population",
                    value=pop_value,
                    value_type="number",
                    unit="inhabitants"
                ))
            
            # Capital - fetch label separately if not available
            if "capital" in binding:
                capital_uri = binding["capital"]["value"]
                capital_label = await self._get_entity_label(capital_uri)
                
                attributes.append(EntityAttribute(
                    property="http://www.wikidata.org/prop/direct/P36",
                    property_label="Capital",
                    value=capital_uri,
                    value_label=capital_label,
                    value_type="entity"
                ))
            
            # Inception date
            if "inception" in binding:
                inception_value = binding["inception"]["value"]
                # Extract just the date part (YYYY-MM-DD)
                if "T" in inception_value:
                    inception_value = inception_value.split("T")[0]
                attributes.append(EntityAttribute(
                    property="http://www.wikidata.org/prop/direct/P571",
                    property_label="Inception",
                    value=inception_value,
                    value_type="date"
                ))
            
            # Area
            if "area" in binding:
                area_value = binding["area"]["value"]
                attributes.append(EntityAttribute(
                    property="http://www.wikidata.org/prop/direct/P2046",
                    property_label="Area",
                    value=area_value,
                    value_type="number",
                    unit="km²"
                ))
        
        return attributes
    
    async def _get_entity_label(self, entity_uri: str) -> Optional[str]:
        """Get label for an entity URI"""
        sparql_query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?label WHERE {{
            <{entity_uri}> rdfs:label ?label .
        }}
        LIMIT 1
        """
        
        results = await self.client.query(sparql_query)
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]["label"]["value"]
        
        # Fallback: extract Wikidata ID from URI
        if "/entity/" in entity_uri:
            return entity_uri.split("/entity/")[-1]
        
        return None
    
    def _determine_entity_type(self, entity_id: str) -> EntityType:
        """Determine entity type from ID"""
        if entity_id.startswith(self.kge_ns):
            return "region"
        return "country"


# Continue in next file due to length...
