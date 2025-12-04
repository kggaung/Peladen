"""
Map Router
Handles /api/map endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from app.application.services import MapService
from app.application.dto import CountryCoordinatesDTO, EntityDTO
from app.application.mappers import CountryCoordinatesMapper, EntityMapper
from app.presentation.dependencies import get_map_service

router = APIRouter(prefix="/map", tags=["map"])


@router.get("/countries", response_model=List[CountryCoordinatesDTO])
async def get_all_country_coordinates(
    map_service: MapService = Depends(get_map_service)
):
    """
    Get coordinates for all countries to display on map
    GET /api/map/countries
    """
    coordinates = await map_service.get_all_country_coordinates()
    return CountryCoordinatesMapper.to_dto_list(coordinates)


@router.get("/countries/{iso3_code}", response_model=EntityDTO)
async def get_country_info(
    iso3_code: str = Path(..., description="ISO 3166-1 alpha-3 country code"),
    map_service: MapService = Depends(get_map_service)
):
    """
    Get detailed country information by ISO code
    GET /api/map/countries/{iso3Code}
    """
    country = await map_service.get_country_info(iso3_code)
    
    if not country:
        raise HTTPException(status_code=404, detail=f"Country with ISO3 code '{iso3_code}' not found")
    
    return EntityMapper.to_dto(country)
