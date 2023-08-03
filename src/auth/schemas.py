from typing import Optional

from fastapi_users import schemas, models
from pydantic import VERSION as PYDANTIC_VERSION, EmailStr, ConfigDict

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    username: str
    email: EmailStr
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
