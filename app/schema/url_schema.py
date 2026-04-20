from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional


class URLRequest(BaseModel):
    original_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None

    @field_validator("original_url", mode="after")
    @classmethod
    def convert_to_str(cls, v):
        return str(v)


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_key: str
    clicks: int
    is_active: bool

    model_config = {"from_attributes": True}
