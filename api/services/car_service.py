from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from common.models import CarMake, CarModel, CarPart


async def get_all_makes(
    session: AsyncSession,
    name: Optional[str] = None,
    limit: int = 0,
    offset: int = 0,
) -> List[CarMake]:
    stmt = select(CarMake)
    if name:
        stmt = stmt.where(CarMake.name.ilike(f"%{name}%"))
    if limit:
        stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_models_by_make(
    make_id: int,
    session: AsyncSession,
    name: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[CarModel]:
    stmt = select(CarModel).where(CarModel.make_id == make_id)
    if name:
        stmt = stmt.where(CarModel.name.ilike(f"%{name}%"))
    if limit:
        stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_parts_by_model(
    model_id: int,
    session: AsyncSession,
    name: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[CarPart]:
    stmt = select(CarPart).where(CarPart.model_id == model_id)
    if name:
        stmt = stmt.where(CarPart.name.ilike(f"%{name}%"))
    if limit:
        stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_part_by_id(
    part_id: int,
    session: AsyncSession
) -> Optional[CarPart]:
    result = await session.execute(
        select(CarPart).where(CarPart.id == part_id)
    )
    return result.scalar_one_or_none()
