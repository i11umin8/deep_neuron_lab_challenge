from sqlalchemy import func
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base, DeclarativeBase
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class GenericBase(DeclarativeBase):
    """Base for all models"""

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: uuid.uuid4(),
        sort_order=-3,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), sort_order=-2
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), sort_order=-1
    )

    def as_dict(self) -> dict:
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns  # type: ignore
        }
