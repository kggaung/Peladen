"""
SPARQL Router
Handles /api/sparql endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from app.application.services import SPARQLQueryService
from app.application.dto import (
    SPARQLQueryRequest, SPARQLQueryResponseDTO,
    SPARQLValidationResponseDTO, SampleQueriesResponseDTO
)
from app.presentation.dependencies import get_sparql_service

router = APIRouter(prefix="/sparql", tags=["sparql"])


@router.post("/query", response_model=SPARQLQueryResponseDTO)
async def execute_sparql_query(
    request: SPARQLQueryRequest,
    sparql_service: SPARQLQueryService = Depends(get_sparql_service)
):
    """
    Execute SPARQL query against the knowledge graph
    POST /api/sparql/query
    Body: { "query": "SELECT...", "format": "json", "limit": 100 }
    """
    try:
        result = await sparql_service.execute_query(
            query=request.query,
            limit=request.limit
        )
        
        return SPARQLQueryResponseDTO(
            head={"vars": result.variables},
            results={"bindings": result.bindings}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query execution error: {str(e)}")


@router.post("/validate", response_model=SPARQLValidationResponseDTO)
async def validate_sparql_query(
    request: dict,
    sparql_service: SPARQLQueryService = Depends(get_sparql_service)
):
    """
    Validate SPARQL query syntax
    POST /api/sparql/validate
    Body: { "query": "SELECT..." }
    """
    query = request.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    is_valid, error_message = await sparql_service.validate_query(query)
    
    return SPARQLValidationResponseDTO(
        valid=is_valid,
        error=error_message
    )


@router.get("/samples", response_model=SampleQueriesResponseDTO)
async def get_sample_queries(
    sparql_service: SPARQLQueryService = Depends(get_sparql_service)
):
    """
    Get sample SPARQL queries for user reference
    GET /api/sparql/samples
    """
    queries = await sparql_service.get_sample_queries()
    
    return SampleQueriesResponseDTO(queries=queries)


# Query history endpoints (simplified - would need database in production)
@router.get("/history", response_model=dict)
async def get_query_history():
    """
    Get query execution history
    GET /api/sparql/history
    """
    # Mock response - in production, this would query a database
    return {"history": []}


@router.post("/history")
async def save_query_to_history(request: dict):
    """
    Save query to execution history
    POST /api/sparql/history
    Body: { "query": "...", "executionTime": 123, "resultCount": 45 }
    """
    # Mock response - in production, this would save to a database
    return {"status": "ok"}
