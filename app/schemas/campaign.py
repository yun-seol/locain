from datetime import date
from typing import Optional, List
from pydantic import BaseModel
from app.schemas.campaign_status import CampaignStatus

class CampaignBase(BaseModel):
    title: str
    description: str
    status: CampaignStatus
    start_date: date
    end_date: date
    budget: int
    max_participants: int
    requirements: str
    is_active: bool = True

class CampaignCreate(CampaignBase):
    user_id: int

class CampaignUpdate(CampaignBase):
    pass

class CampaignResponse(CampaignBase):
    id: int
    user_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class CampaignList(BaseModel):
    total: int
    items: List[CampaignResponse]

    class Config:
        from_attributes = True

class CampaignInDBBase(CampaignBase):
    id: int
    user_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class Campaign(CampaignInDBBase):
    pass

class CampaignInDB(CampaignInDBBase):
    pass

class CampaignApplicationBase(BaseModel):
    campaign_id: int
    user_id: int
    status: str = "PENDING"
    application_text: Optional[str] = None

class CampaignApplicationCreate(CampaignApplicationBase):
    pass

class CampaignApplicationUpdate(BaseModel):
    status: Optional[str] = None
    application_text: Optional[str] = None

class CampaignApplicationResponse(CampaignApplicationBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class CampaignApplicationList(BaseModel):
    total: int
    items: List[CampaignApplicationResponse]

    class Config:
        from_attributes = True

class CampaignApplicationInDBBase(CampaignApplicationBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class CampaignApplication(CampaignApplicationInDBBase):
    pass

class CampaignApplicationInDB(CampaignApplicationInDBBase):
    pass 