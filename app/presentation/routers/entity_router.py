"""
Entity Router
Handles /api/entities and /api/entity endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import Optional
from app.application.services import EntityInfoService, SearchService, HealthRecordService
from app.application.dto import (
    InfoBoxResponseDTO, EntityDetailResponseDTO, EntityDTO
)
from app.application.mappers import EntityInfoMapper, EntityMapper, HealthRecordMapper
from app.presentation.dependencies import (
    get_entity_info_service, get_search_service, get_health_record_service
)

router = APIRouter(tags=["entities"])


@router.get("/entity/by-label", response_model=InfoBoxResponseDTO)
async def get_entity_by_label(
    label: str = Query(..., description="Entity label"),
    entity_info_service: EntityInfoService = Depends(get_entity_info_service)
):
    """
    Get entity information by label
    GET /api/entity/by-label?label={label}
    """
    entity_info = await entity_info_service.get_entity_info_by_label(label)
    
    if not entity_info:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return InfoBoxResponseDTO(
        entity=EntityInfoMapper.to_dto(entity_info),
        sparqlQuery=None
    )


@router.get("/entity/related", response_model=dict)
async def get_related_entities(
    entityId: str = Query(..., description="Entity ID", alias="entityId"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of related entities"),
    entity_info_service: EntityInfoService = Depends(get_entity_info_service)
):
    """
    Get related entities for an entity
    GET /api/entity/related?entityId={entityId}&limit={limit}
    """
    related = await entity_info_service.get_related_entities(entityId, limit)
    
    return {
        "entities": EntityMapper.to_dto_list(related)
    }


@router.get("/entities/{entity_id}", response_model=EntityDetailResponseDTO)
async def get_entity_by_id(
    entity_id: str = Path(..., description="Entity ID"),
    search_service: SearchService = Depends(get_search_service),
    health_record_service: HealthRecordService = Depends(get_health_record_service),
    entity_info_service: EntityInfoService = Depends(get_entity_info_service)
):
    """
    Get detailed information about a specific entity
    GET /api/entities/{id}
    """
    # Get basic entity
    entity = await search_service.get_entity_by_id(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    # Get health records
    health_records = await health_record_service.get_health_records(entity_id)
    
    # Get related entities
    related_entities = await entity_info_service.get_related_entities(entity_id, limit=5)
    
    return EntityDetailResponseDTO(
        entity=EntityMapper.to_dto(entity),
        healthRecords=HealthRecordMapper.to_dto_list(health_records),
        relatedEntities=EntityMapper.to_dto_list(related_entities) if related_entities else None
    )


@router.get("/entity/{entity_id:path}", response_model=InfoBoxResponseDTO)
async def get_entity_info(
    entity_id: str = Path(..., description="Entity ID or URI"),
    entity_info_service: EntityInfoService = Depends(get_entity_info_service)
):
    """
    Get complete entity information for InfoBox
    GET /api/entity/{id}
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Getting entity info for: {entity_id}")
    
    entity_info = await entity_info_service.get_entity_info(entity_id)
    
    if not entity_info:
        logger.warning(f"Entity not found: {entity_id}")
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return InfoBoxResponseDTO(
        entity=EntityInfoMapper.to_dto(entity_info),
        sparqlQuery=None  # Could include the SPARQL query used
    )
