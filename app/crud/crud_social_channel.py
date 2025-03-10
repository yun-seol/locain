from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.social_channel import SocialChannel, BlogPostRanking
from app.schemas.social_channel import SocialChannelCreate, SocialChannelUpdate, BlogPostRankingCreate, BlogPostRankingUpdate

class CRUDSocialChannel(CRUDBase[SocialChannel, SocialChannelCreate, SocialChannelUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> List[SocialChannel]:
        return db.query(SocialChannel).filter(SocialChannel.user_id == user_id).all()

    def create(self, db: Session, *, obj_in: SocialChannelCreate) -> SocialChannel:
        db_obj = SocialChannel(
            user_id=obj_in.user_id,
            platform=obj_in.platform,
            channel_url=obj_in.channel_url,
            followers=obj_in.followers,
            posts=obj_in.posts,
            engagement_rate=obj_in.engagement_rate
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: SocialChannel, obj_in: SocialChannelUpdate
    ) -> SocialChannel:
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

class CRUDBlogPostRanking(CRUDBase[BlogPostRanking, BlogPostRankingCreate, BlogPostRankingUpdate]):
    def get_by_channel_id(self, db: Session, *, channel_id: int) -> List[BlogPostRanking]:
        return db.query(BlogPostRanking).filter(BlogPostRanking.channel_id == channel_id).all()

    def create(self, db: Session, *, obj_in: BlogPostRankingCreate) -> BlogPostRanking:
        db_obj = BlogPostRanking(
            channel_id=obj_in.channel_id,
            post_url=obj_in.post_url,
            title=obj_in.title,
            views=obj_in.views,
            likes=obj_in.likes,
            comments=obj_in.comments,
            shares=obj_in.shares,
            ranking_date=obj_in.ranking_date
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: BlogPostRanking, obj_in: BlogPostRankingUpdate
    ) -> BlogPostRanking:
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

social_channel = CRUDSocialChannel(SocialChannel)
blog_post_ranking = CRUDBlogPostRanking(BlogPostRanking) 