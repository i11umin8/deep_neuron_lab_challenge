from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from common.db import get_session
from schemas.responses import MakeOut, ModelOut, PartOut
from services import car_service

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/makes", response_model=List[MakeOut])
async def list_makes(
    name: Optional[str] = Query(default=None, description="Filter by make name"),
    limit: Optional[int] = Query(default=None, ge=1, description="Max number of results"),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    makes = await car_service.get_all_makes(session, name=name, limit=limit, offset=offset)
    return makes


@router.get("/makes/{make_id}/models", response_model=List[ModelOut])
async def list_models_for_make(
    make_id: int,
    name: Optional[str] = Query(default=None, description="Filter by model name"),
    limit: Optional[int] = Query(default=None, ge=1),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    models = await car_service.get_models_by_make(
        make_id=make_id, session=session, name=name, limit=limit, offset=offset
    )
    if not models:
        raise HTTPException(status_code=404, detail="No models found for this make")
    return models


@router.get("/models/{model_id}/parts", response_model=List[PartOut])
async def list_parts_for_model(
    model_id: int,
    name: Optional[str] = Query(default=None, description="Filter by part name"),
    limit: Optional[int] = Query(default=None, ge=1),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    parts = await car_service.get_parts_by_model(
        model_id=model_id, session=session, name=name, limit=limit, offset=offset
    )
    if not parts:
        raise HTTPException(status_code=404, detail="No parts found for this model")
    return parts


@router.get("/parts/{part_id}", response_model=PartOut)
async def get_part(part_id: int, session: AsyncSession = Depends(get_session)):
    part = await car_service.get_part_by_id(part_id, session)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return part
