from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from common.base import GenericBase


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

