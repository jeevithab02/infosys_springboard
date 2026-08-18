# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict, EmailStr


class OperatorCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    shift: str


class OperatorUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    shift: str | None = None


class OperatorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    shift: str

    model_config = ConfigDict(from_attributes=True)
