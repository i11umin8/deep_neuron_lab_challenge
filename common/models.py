from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class GenericBase(DeclarativeBase):

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
            for c in self.__table__.columns 
        }

class CarMake(GenericBase):
    __tablename__ = "car_makes"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    models = relationship("CarModel", back_populates="make")

class CarModel(GenericBase):
    __tablename__ = "car_models"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    make_id = Column(Integer, ForeignKey("car_makes.id"))
    make = relationship("CarMake", back_populates="models")
    parts = relationship("CarPart", back_populates="model")

class CarPart(GenericBase):
    __tablename__ = "car_parts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    model_id = Column(Integer, ForeignKey("car_models.id"))
    model = relationship("CarModel", back_populates="parts")

