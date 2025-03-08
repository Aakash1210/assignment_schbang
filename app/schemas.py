from pydantic import BaseModel,Field
from datetime import date
from typing import Optional
from decimal import Decimal



class AdMetricsResponse(BaseModel):
    date: date
    region_name: str
    age_range: str
    gender_name: str
    platform_name: str
    placement_name: str
    device_type_name: str
    impressions: int
    clicks: int
    cost: float
    conversions: int
    likes: int

    class Config:
        from_attributes = True
