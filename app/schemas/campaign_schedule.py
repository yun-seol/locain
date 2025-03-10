from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class CampaignSchedule(BaseModel):
    application_start_date: datetime = Field(..., description="신청 시작일")
    application_end_date: datetime = Field(..., description="신청 종료일")
    influencer_announcement_date: datetime = Field(..., description="인플루언서 발표일")
    content_start_date: datetime = Field(..., description="콘텐츠 등록 시작일")
    content_end_date: datetime = Field(..., description="콘텐츠 등록 종료일")
    result_announcement_date: datetime = Field(..., description="결과 발표일")
    max_applicants: int = Field(..., description="최대 신청자 수")
    selected_applicants: int = Field(..., description="선정된 신청자 수") 