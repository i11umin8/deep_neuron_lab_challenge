from pydantic import BaseModel

class MakeOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ModelOut(BaseModel):
    id: int
    name: str
    make_id: int

    class Config:
        from_attributes = True

class PartOut(BaseModel):
    id: int
    name: str
    model_id: int

    class Config:
        from_attributes = True
