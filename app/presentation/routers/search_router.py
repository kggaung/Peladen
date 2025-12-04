"""
Search Router
Handles /api/search endpoints
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from app.application.services import SearchService
from app.application.dto import SearchResponseDTO, EntityDTO, EntityDetailResponseDTO
from app.application.mappers import EntityMapper, HealthRecordMapper
from app.presentation.dependencies import get_search_service, get_health_record_service
from app.application.services import HealthRecordService

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponseDTO)
async def search_entities(
    query: str = Query(..., min_length=1, description="Search query string"),
    type: Optional[str] = Query(None, description="Entity type filter"),
    page: int = Query(1, ge=1, description="Page number"),
    pageSize: int = Query(20, ge=1, le=100, description="Items per page"),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Search entities in the knowledge graph
    GET /api/search?query={query}&type={type}&page={page}&pageSize={pageSize}
    """
    entities, total, current_page = await search_service.search_entities(
        query=query,
        entity_type=type,  # type: ignore
        page=page,
        page_size=pageSize
    )
    
    return SearchResponseDTO(
        results=EntityMapper.to_dto_list(entities),
        total=total,
        page=current_page,
        pageSize=pageSize
    )


@router.get("/suggestions", response_model=list[EntityDTO])
async def get_suggestions(
    query: str = Query(..., min_length=2, description="Query string"),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Get search suggestions for autocomplete
    GET /api/search/suggestions?query={query}
    """
    entities = await search_service.get_suggestions(query)
    return EntityMapper.to_dto_list(entities)
