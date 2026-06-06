from typing import List

from fastapi import APIRouter, HTTPException
from shared.db.session import SessionLocal
from shared.repository import SourceRepo
from .schemas import SourceResponse

router = APIRouter(prefix="/sources", tags=["sources"])
source_repo = SourceRepo()

@router.get("/{source_id}", response_model=SourceResponse)
def get_source(source_id: int):
    with SessionLocal() as db:
        source = source_repo.get_by_id(source_id, db)

        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

        return source
    
@router.get("/", response_model=List[SourceResponse])
def get_all_sources():
    with SessionLocal() as db:
        sources = source_repo.get_all(db)

        if not sources:
            raise HTTPException(status_code=404, detail="No sources found")

        return sources