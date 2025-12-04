"""
Unit tests for domain models
Testing business logic and validation
"""
import pytest
from app.domain.models import (
    Entity, HealthRecord, CountryCoordinates, EntityInfo
)


class TestEntity:
    """Test Entity model"""
    
    def test_create_valid_entity(self):
        """Should create entity with valid data"""
        entity = Entity(
            id="http://www.wikidata.org/entity/Q252",
            label="Indonesia",
            type="country",
            iso3_code="IDN"
        )
        assert entity.id == "http://www.wikidata.org/entity/Q252"
        assert entity.label == "Indonesia"
        assert entity.type == "country"
        assert entity.iso3_code == "IDN"
    
    def test_entity_requires_id(self):
        """Should raise error if ID is empty"""
        with pytest.raises(ValueError, match="Entity ID cannot be empty"):
            Entity(id="", label="Test", type="country")
    
    def test_entity_requires_label(self):
        """Should raise error if label is empty"""
        with pytest.raises(ValueError, match="Entity label cannot be empty"):
            Entity(id="test", label="", type="country")


class TestHealthRecord:
    """Test HealthRecord model"""
    
    def test_create_valid_health_record(self):
        """Should create health record with valid data"""
        record = HealthRecord(
            id="record1",
            location="http://www.wikidata.org/entity/Q252",
            year=2020,
            hiv_cases=1000.0,
            tuberculosis_cases=5000.0
        )
        assert record.year == 2020
        assert record.hiv_cases == 1000.0
    
    def test_invalid_year_raises_error(self):
        """Should raise error for invalid year"""
        with pytest.raises(ValueError, match="Invalid year"):
            HealthRecord(
                id="record1",
                location="test",
                year=1800
            )
    
    def test_optional_fields_can_be_none(self):
        """Optional health fields can be None"""
        record = HealthRecord(
            id="record1",
            location="test",
            year=2020
        )
        assert record.hiv_cases is None
        assert record.malaria_cases is None


class TestCountryCoordinates:
    """Test CountryCoordinates model"""
    
    def test_valid_coordinates(self):
        """Should create coordinates with valid data"""
        coords = CountryCoordinates(
            iso3_code="IDN",
            label="Indonesia",
            latitude=-0.7893,
            longitude=113.9213
        )
        assert coords.latitude == -0.7893
        assert coords.longitude == 113.9213
    
    def test_invalid_latitude_raises_error(self):
        """Should raise error for invalid latitude"""
        with pytest.raises(ValueError, match="Invalid latitude"):
            CountryCoordinates(
                iso3_code="IDN",
                label="Indonesia",
                latitude=91.0,  # Invalid
                longitude=0.0
            )
    
    def test_invalid_longitude_raises_error(self):
        """Should raise error for invalid longitude"""
        with pytest.raises(ValueError, match="Invalid longitude"):
            CountryCoordinates(
                iso3_code="IDN",
                label="Indonesia",
                latitude=0.0,
                longitude=181.0  # Invalid
            )
