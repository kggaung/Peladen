"""
Unit tests for services
Testing business logic in application layer
"""
import pytest
from unittest.mock import Mock, AsyncMock
from app.application.services import SearchService, EntityInfoService
from app.domain.models import Entity, EntityInfo, HealthRecord


@pytest.fixture
def mock_entity_repository():
    """Mock entity repository"""
    repo = Mock()
    repo.search = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_suggestions = AsyncMock()
    return repo


@pytest.fixture
def mock_entity_info_repository():
    """Mock entity info repository"""
    repo = Mock()
    repo.get_entity_info = AsyncMock()
    repo.get_related_entities = AsyncMock()
    return repo


@pytest.fixture
def mock_health_record_repository():
    """Mock health record repository"""
    repo = Mock()
    repo.get_by_location = AsyncMock()
    repo.get_available_years = AsyncMock()
    return repo


class TestSearchService:
    """Test SearchService"""
    
    @pytest.mark.asyncio
    async def test_search_entities_returns_results(self, mock_entity_repository):
        """Should return search results with pagination"""
        # Arrange
        mock_entities = [
            Entity(id="1", label="Indonesia", type="country"),
            Entity(id="2", label="India", type="country")
        ]
        mock_entity_repository.search.return_value = (mock_entities, 2)
        
        service = SearchService(mock_entity_repository)
        
        # Act
        entities, total, page = await service.search_entities(
            query="ind",
            page=1,
            page_size=20
        )
        
        # Assert
        assert len(entities) == 2
        assert total == 2
        assert page == 1
        mock_entity_repository.search.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_suggestions_filters_short_queries(self, mock_entity_repository):
        """Should return empty list for queries shorter than 2 characters"""
        service = SearchService(mock_entity_repository)
        
        # Act
        results = await service.get_suggestions("a")
        
        # Assert
        assert results == []
        mock_entity_repository.get_suggestions.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_suggestions_calls_repository(self, mock_entity_repository):
        """Should call repository for valid query"""
        mock_entity_repository.get_suggestions.return_value = [
            Entity(id="1", label="Indonesia", type="country")
        ]
        
        service = SearchService(mock_entity_repository)
        
        # Act
        results = await service.get_suggestions("ind")
        
        # Assert
        assert len(results) == 1
        mock_entity_repository.get_suggestions.assert_called_once_with("ind", 10)


class TestEntityInfoService:
    """Test EntityInfoService"""
    
    @pytest.mark.asyncio
    async def test_get_entity_info_returns_enriched_data(
        self, mock_entity_info_repository, mock_health_record_repository
    ):
        """Should return entity info with health metrics"""
        # Arrange
        mock_entity_info = EntityInfo(
            id="1",
            label="Indonesia",
            type="country",
            attributes=[],
            related_entities=[],
            sources=[]
        )
        mock_entity_info_repository.get_entity_info.return_value = mock_entity_info
        mock_health_record_repository.get_by_location.return_value = [
            HealthRecord(id="r1", location="1", year=2020, hiv_cases=1000)
        ]
        
        service = EntityInfoService(
            mock_entity_info_repository,
            mock_health_record_repository
        )
        
        # Act
        result = await service.get_entity_info("1")
        
        # Assert
        assert result is not None
        assert result.id == "1"
        assert result.health_metrics is not None
        mock_entity_info_repository.get_entity_info.assert_called_once_with("1")
    
    @pytest.mark.asyncio
    async def test_get_entity_info_returns_none_if_not_found(
        self, mock_entity_info_repository, mock_health_record_repository
    ):
        """Should return None if entity not found"""
        mock_entity_info_repository.get_entity_info.return_value = None
        
        service = EntityInfoService(
            mock_entity_info_repository,
            mock_health_record_repository
        )
        
        # Act
        result = await service.get_entity_info("nonexistent")
        
        # Assert
        assert result is None
