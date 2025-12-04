"""
Integration tests for API endpoints
Testing the complete stack
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self):
        """Should return API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Knowledge Graph Health Data API"
        assert data["status"] == "running"
    
    def test_health_check(self):
        """Should return healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestSearchEndpoints:
    """Test search endpoints"""
    
    def test_search_requires_query(self):
        """Should return 422 if query is missing"""
        response = client.get("/api/search")
        assert response.status_code == 422
    
    def test_search_validates_page_number(self):
        """Should validate page number >= 1"""
        response = client.get("/api/search?query=test&page=0")
        assert response.status_code == 422


class TestSPARQLEndpoints:
    """Test SPARQL endpoints"""
    
    def test_get_sample_queries(self):
        """Should return sample queries"""
        response = client.get("/api/sparql/samples")
        assert response.status_code == 200
        data = response.json()
        assert "queries" in data
        assert isinstance(data["queries"], list)
    
    def test_validate_query_requires_query(self):
        """Should return error if query is missing"""
        response = client.post("/api/sparql/validate", json={})
        assert response.status_code == 400


class TestMapEndpoints:
    """Test map endpoints"""
    
    def test_get_country_coordinates(self):
        """Should return list of country coordinates"""
        response = client.get("/api/map/countries")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        if len(data) > 0:
            country = data[0]
            assert "iso3Code" in country
            assert "label" in country
            assert "latitude" in country
            assert "longitude" in country
