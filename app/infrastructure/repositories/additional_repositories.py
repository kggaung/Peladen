"""
Additional GraphDB Repository Implementations
Health Records, Map, and SPARQL repositories
"""
from typing import List, Optional, Dict, Any
from app.domain.models import HealthRecord, CountryCoordinates, Entity, SPARQLQueryResult
from app.domain.repositories import IHealthRecordRepository, IMapRepository, ISPARQLRepository
from app.infrastructure.config.settings import settings
from app.infrastructure.repositories.graphdb_repository import GraphDBClient
from app.data.country_coordinates import COUNTRY_COORDINATES
import logging

logger = logging.getLogger(__name__)


class HealthRecordRepository(IHealthRecordRepository):
    """Health record repository implementation"""
    
    def __init__(self, graphdb_client: GraphDBClient):
        self.client = graphdb_client
        self.kgr_ns = settings.kg_record_ns
        self.kgp_ns = settings.kg_property_ns
    
    async def get_by_location(
        self,
        location_id: str,
        year: Optional[int] = None
    ) -> List[HealthRecord]:
        """Get health records for a location"""
        
        year_filter = f'FILTER(?year = "{year}"^^xsd:gYear)' if year else ""
        
        sparql_query = f"""
        PREFIX kgr: <{self.kgr_ns}>
        PREFIX kgp: <{self.kgp_ns}>
        PREFIX schema: <http://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT * WHERE {{
            ?record a kgp:healthRecord ;
                    schema:location <{location_id}> ;
                    schema:year ?year .
            {year_filter}
            
            OPTIONAL {{ ?record kgp:hivCases ?hivCases . }}
            OPTIONAL {{ ?record kgp:malariaCases ?malariaCases . }}
            OPTIONAL {{ ?record kgp:rabiesCases ?rabiesCases . }}
            OPTIONAL {{ ?record kgp:tuberculosisCases ?tuberculosisCases . }}
            OPTIONAL {{ ?record kgp:choleraCases ?choleraCases . }}
            OPTIONAL {{ ?record kgp:guineaworm ?guineaworm . }}
            OPTIONAL {{ ?record kgp:polioCases ?polioCases . }}
            OPTIONAL {{ ?record kgp:smallpoxCases ?smallpoxCases . }}
            OPTIONAL {{ ?record kgp:yawsCases ?yawsCases . }}
            OPTIONAL {{ ?record kgp:bcg ?bcg . }}
            OPTIONAL {{ ?record kgp:dtp3 ?dtp3 . }}
            OPTIONAL {{ ?record kgp:hepb3 ?hepb3 . }}
            OPTIONAL {{ ?record kgp:hib3 ?hib3 . }}
            OPTIONAL {{ ?record kgp:measles1 ?measles1 . }}
            OPTIONAL {{ ?record kgp:polio3 ?polio3 . }}
            OPTIONAL {{ ?record kgp:rotavirus ?rotavirus . }}
            OPTIONAL {{ ?record kgp:rubella1 ?rubella1 . }}
            OPTIONAL {{ ?record kgp:populationAge0 ?populationAge0 . }}
        }}
        ORDER BY ?year
        """
        
        results = await self.client.query(sparql_query)
        return self._parse_health_records(results)
    
    async def get_available_years(self, location_id: str) -> List[int]:
        """Get years with available data"""
        sparql_query = f"""
        PREFIX kgp: <{self.kgp_ns}>
        PREFIX schema: <http://schema.org/>
        
        SELECT DISTINCT ?year WHERE {{
            ?record a kgp:healthRecord ;
                    schema:location <{location_id}> ;
                    schema:year ?year .
        }}
        ORDER BY ?year
        """
        
        results = await self.client.query(sparql_query)
        years = []
        for binding in results["results"]["bindings"]:
            year_str = binding["year"]["value"]
            years.append(int(year_str))
        
        return years
    
    def _parse_health_records(self, results: Dict[str, Any]) -> List[HealthRecord]:
        """Parse SPARQL results to HealthRecord objects"""
        records = []
        
        for binding in results["results"]["bindings"]:
            record = HealthRecord(
                id=binding["record"]["value"],
                location=binding.get("location", {}).get("value", ""),
                year=int(binding["year"]["value"]),
                hiv_cases=self._get_float(binding, "hivCases"),
                malaria_cases=self._get_float(binding, "malariaCases"),
                rabies_cases=self._get_float(binding, "rabiesCases"),
                tuberculosis_cases=self._get_float(binding, "tuberculosisCases"),
                cholera_cases=self._get_float(binding, "choleraCases"),
                guineaworm=self._get_float(binding, "guineaworm"),
                polio_cases=self._get_float(binding, "polioCases"),
                smallpox_cases=self._get_float(binding, "smallpoxCases"),
                yaws_cases=self._get_float(binding, "yawsCases"),
                bcg=self._get_float(binding, "bcg"),
                dtp3=self._get_float(binding, "dtp3"),
                hepb3=self._get_float(binding, "hepb3"),
                hib3=self._get_float(binding, "hib3"),
                measles1=self._get_float(binding, "measles1"),
                polio3=self._get_float(binding, "polio3"),
                rotavirus=self._get_float(binding, "rotavirus"),
                rubella1=self._get_float(binding, "rubella1"),
                population_age0=self._get_float(binding, "populationAge0")
            )
            records.append(record)
        
        return records
    
    @staticmethod
    def _get_float(binding: dict, key: str) -> Optional[float]:
        """Safely extract float value from binding"""
        if key in binding:
            try:
                return float(binding[key]["value"])
            except (ValueError, KeyError):
                return None
        return None


class MapRepository(IMapRepository):
    """Map repository implementation"""
    
    def __init__(self, graphdb_client: GraphDBClient):
        self.client = graphdb_client
        self.wdt_ns = settings.wd_property_ns
    
    async def get_all_country_coordinates(self) -> List[CountryCoordinates]:
        """Get coordinates for all countries from static data"""
        # Using static data as coordinates are not in RDF
        return COUNTRY_COORDINATES
    
    async def get_country_by_iso3(self, iso3_code: str) -> Optional[Entity]:
        """Get country entity by ISO3 code"""
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


class SPARQLRepository(ISPARQLRepository):
    """SPARQL repository for direct query execution"""
    
    def __init__(self, graphdb_client: GraphDBClient):
        self.client = graphdb_client
    
    async def execute_query(self, query: str) -> SPARQLQueryResult:
        """Execute SPARQL query"""
        results = await self.client.query(query)
        
        variables = results["head"]["vars"]
        bindings = results["results"]["bindings"]
        
        return SPARQLQueryResult(
            variables=variables,
            bindings=bindings
        )
    
    async def validate_query(self, query: str) -> tuple[bool, Optional[str]]:
        """Validate SPARQL query syntax"""
        try:
            # Try to execute query with LIMIT 1 to validate
            validation_query = f"{query.rstrip()} LIMIT 1"
            await self.client.query(validation_query)
            return True, None
        except Exception as e:
            return False, str(e)
    
    async def get_sample_queries(self) -> List[str]:
        """Get sample SPARQL queries"""
        return [
            # Query 1: Countries with health data
            """PREFIX kgp: <http://kg.gaung.org/property/>
PREFIX schema: <http://schema.org/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?country ?countryLabel (COUNT(?record) as ?recordCount)
WHERE {
    ?record a kgp:healthRecord ;
            schema:location ?country .
    ?country rdfs:label ?countryLabel .
}
GROUP BY ?country ?countryLabel
ORDER BY DESC(?recordCount)
LIMIT 10""",
            
            # Query 2: HIV cases by year
            """PREFIX kgp: <http://kg.gaung.org/property/>
PREFIX schema: <http://schema.org/>

SELECT ?year (SUM(?cases) as ?totalCases)
WHERE {
    ?record a kgp:healthRecord ;
            schema:year ?year ;
            kgp:hivCases ?cases .
}
GROUP BY ?year
ORDER BY ?year""",
            
            # Query 3: Vaccination coverage
            """PREFIX kgp: <http://kg.gaung.org/property/>
PREFIX schema: <http://schema.org/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?country ?countryLabel ?year ?bcg ?dtp3 ?measles1
WHERE {
    ?record a kgp:healthRecord ;
            schema:location ?country ;
            schema:year ?year ;
            kgp:bcg ?bcg ;
            kgp:dtp3 ?dtp3 ;
            kgp:measles1 ?measles1 .
    ?country rdfs:label ?countryLabel .
    FILTER(?year = "2020"^^xsd:gYear)
}
ORDER BY DESC(?bcg)
LIMIT 20""",
            
            # Query 4: All properties
            """PREFIX kgp: <http://kg.gaung.org/property/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?label ?description
WHERE {
    ?property a rdf:Property ;
              rdfs:label ?label .
    OPTIONAL { ?property rdfs:comment ?description . }
}
ORDER BY ?label"""
        ]
