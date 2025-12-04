"""
Domain Repositories Package
Exports all repository interfaces
"""
from app.domain.repositories.interfaces import (
    IEntityRepository,
    IEntityInfoRepository,
    IHealthRecordRepository,
    IMapRepository,
    ISPARQLRepository,
)

__all__ = [
    "IEntityRepository",
    "IEntityInfoRepository",
    "IHealthRecordRepository",
    "IMapRepository",
    "ISPARQLRepository",
]
