from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OperationSchema(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str

    model_config = ConfigDict(from_attributes=True)


class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str


class OperationEdit(BaseModel):
    quantity: str = Field(min_length=1)
    figi: str = Field(min_length=4)
    instrument_type: str = Field(min_length=4)
    type: str = Field(min_length=15)


class OperationPartialEdit(BaseModel):
    quantity: str | None
    figi: str | None
    instrument_type: str | None
    type: str | None
