from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional


class URLRequest(BaseModel):
    original_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None


class URLResponse(BaseModel):
    id: int
    original_url: HttpUrl
    short_key: str
    clicks: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
