from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.campaign import Campaign, CampaignApplication
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignApplicationCreate, CampaignApplicationUpdate

class CRUDCampaign(CRUDBase[Campaign, CampaignCreate, CampaignUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> List[Campaign]:
        return db.query(Campaign).filter(Campaign.user_id == user_id).all()

    def create(self, db: Session, *, obj_in: CampaignCreate) -> Campaign:
        db_obj = Campaign(
            user_id=obj_in.user_id,
            title=obj_in.title,
            description=obj_in.description,
            status=obj_in.status,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            budget=obj_in.budget,
            max_participants=obj_in.max_participants,
            requirements=obj_in.requirements,
            is_active=obj_in.is_active
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Campaign, obj_in: CampaignUpdate
    ) -> Campaign:
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

class CRUDCampaignApplication(CRUDBase[CampaignApplication, CampaignApplicationCreate, CampaignApplicationUpdate]):
    def get_by_campaign_id(self, db: Session, *, campaign_id: int) -> List[CampaignApplication]:
        return db.query(CampaignApplication).filter(CampaignApplication.campaign_id == campaign_id).all()

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[CampaignApplication]:
        return db.query(CampaignApplication).filter(CampaignApplication.user_id == user_id).all()

    def create(self, db: Session, *, obj_in: CampaignApplicationCreate) -> CampaignApplication:
        db_obj = CampaignApplication(
            campaign_id=obj_in.campaign_id,
            user_id=obj_in.user_id,
            status=obj_in.status,
            application_text=obj_in.application_text
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: CampaignApplication, obj_in: CampaignApplicationUpdate
    ) -> CampaignApplication:
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

campaign = CRUDCampaign(Campaign)
campaign_application = CRUDCampaignApplication(CampaignApplication) 