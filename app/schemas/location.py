from typing import Optional
from pydantic import BaseModel, Field

class Location(BaseModel):
    address: str = Field(..., description="주소")
    latitude: float = Field(..., description="위도")
    longitude: float = Field(..., description="경도")
    region: str = Field(..., description="지역")
    city: str = Field(..., description="시/도")
    district: str = Field(..., description="구/군")
    street: Optional[str] = Field(None, description="도로명")
    building_name: Optional[str] = Field(None, description="건물명")
    postal_code: Optional[str] = Field(None, description="우편번호") 