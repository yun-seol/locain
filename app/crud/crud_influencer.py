from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.influencer import Influencer, InfluencerPlatform, InfluencerStats
from app.schemas.influencer import InfluencerCreate, InfluencerUpdate, InfluencerStatsCreate, InfluencerStatsUpdate, InfluencerPlatformCreate, InfluencerPlatformUpdate

class CRUDInfluencer(CRUDBase[Influencer, InfluencerCreate, InfluencerUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[Influencer]:
        return db.query(Influencer).filter(Influencer.user_id == user_id).first()
    
    def get_multi_by_filters(
        self,
        db: Session,
        *,
        filters: Dict[str, Any],
        skip: int = 0,
        limit: int = 100,
    ) -> List[Influencer]:
        query = db.query(Influencer).join(InfluencerStats)
        
        if "categories" in filters:
            query = query.filter(Influencer.categories.overlap(filters["categories"]))
        
        if "preferred_regions" in filters:
            query = query.filter(Influencer.preferred_regions.overlap(filters["preferred_regions"]))
        
        if "min_followers" in filters:
            query = query.filter(InfluencerStats.followers >= filters["min_followers"])
        
        if "max_followers" in filters:
            query = query.filter(InfluencerStats.followers <= filters["max_followers"])
        
        if "min_engagement_rate" in filters:
            query = query.filter(InfluencerStats.engagement_rate >= filters["min_engagement_rate"])
        
        if "max_engagement_rate" in filters:
            query = query.filter(InfluencerStats.engagement_rate <= filters["max_engagement_rate"])
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: InfluencerCreate) -> Influencer:
        # 인플루언서 기본 정보 생성
        db_obj = Influencer(
            user_id=obj_in.user_id,
            bio=obj_in.bio,
            categories=obj_in.categories,
            preferred_brands=obj_in.preferred_brands,
            preferred_categories=obj_in.preferred_categories,
            preferred_price_range=obj_in.preferred_price_range,
            preferred_regions=obj_in.preferred_regions,
            content_style=obj_in.content_style,
            available_for_collaboration=obj_in.available_for_collaboration,
            minimum_fee=obj_in.minimum_fee,
            maximum_fee=obj_in.maximum_fee,
            preferred_payment_methods=obj_in.preferred_payment_methods,
            preferred_delivery_methods=obj_in.preferred_delivery_methods,
            preferred_communication_methods=obj_in.preferred_communication_methods,
            preferred_content_deadline=obj_in.preferred_content_deadline,
            preferred_content_review=obj_in.preferred_content_review,
            preferred_content_guidelines=obj_in.preferred_content_guidelines,
            preferred_content_format=obj_in.preferred_content_format,
            preferred_content_length=obj_in.preferred_content_length,
            preferred_content_schedule=obj_in.preferred_content_schedule,
            preferred_content_hashtags=obj_in.preferred_content_hashtags,
            preferred_content_mentions=obj_in.preferred_content_mentions,
            preferred_content_links=obj_in.preferred_content_links,
            preferred_content_images=obj_in.preferred_content_images,
            preferred_content_videos=obj_in.preferred_content_videos,
            preferred_content_audios=obj_in.preferred_content_audios,
            preferred_content_texts=obj_in.preferred_content_texts,
            preferred_content_emojis=obj_in.preferred_content_emojis,
            preferred_content_filters=obj_in.preferred_content_filters,
            preferred_content_effects=obj_in.preferred_content_effects,
            preferred_content_music=obj_in.preferred_content_music,
            preferred_content_fonts=obj_in.preferred_content_fonts,
            preferred_content_colors=obj_in.preferred_content_colors,
            preferred_content_backgrounds=obj_in.preferred_content_backgrounds,
            preferred_content_props=obj_in.preferred_content_props,
            preferred_content_locations=obj_in.preferred_content_locations,
            preferred_content_weather=obj_in.preferred_content_weather,
            preferred_content_time=obj_in.preferred_content_time,
            preferred_content_season=obj_in.preferred_content_season,
            preferred_content_occasion=obj_in.preferred_content_occasion,
            preferred_content_theme=obj_in.preferred_content_theme,
            preferred_content_mood=obj_in.preferred_content_mood,
            preferred_content_tone=obj_in.preferred_content_tone,
            preferred_content_style=obj_in.preferred_content_style,
            preferred_content_angle=obj_in.preferred_content_angle,
            preferred_content_focus=obj_in.preferred_content_focus,
            preferred_content_composition=obj_in.preferred_content_composition,
            preferred_content_lighting=obj_in.preferred_content_lighting,
            preferred_content_shadow=obj_in.preferred_content_shadow,
            preferred_content_reflection=obj_in.preferred_content_reflection,
            preferred_content_mirror=obj_in.preferred_content_mirror,
            preferred_content_window=obj_in.preferred_content_window,
            preferred_content_door=obj_in.preferred_content_door,
            preferred_content_wall=obj_in.preferred_content_wall,
            preferred_content_floor=obj_in.preferred_content_floor,
            preferred_content_ceiling=obj_in.preferred_content_ceiling,
            preferred_content_stairs=obj_in.preferred_content_stairs,
            preferred_content_elevator=obj_in.preferred_content_elevator,
            preferred_content_escalator=obj_in.preferred_content_escalator,
            preferred_content_bench=obj_in.preferred_content_bench,
            preferred_content_chair=obj_in.preferred_content_chair,
            preferred_content_table=obj_in.preferred_content_table,
            preferred_content_counter=obj_in.preferred_content_counter,
            preferred_content_bar=obj_in.preferred_content_bar,
            preferred_content_sofa=obj_in.preferred_content_sofa,
            preferred_content_bed=obj_in.preferred_content_bed,
            preferred_content_cabinet=obj_in.preferred_content_cabinet,
            preferred_content_shelf=obj_in.preferred_content_shelf,
            preferred_content_rack=obj_in.preferred_content_rack,
            preferred_content_hook=obj_in.preferred_content_hook,
            preferred_content_plant=obj_in.preferred_content_plant,
            preferred_content_flower=obj_in.preferred_content_flower,
            preferred_content_tree=obj_in.preferred_content_tree,
            preferred_content_grass=obj_in.preferred_content_grass,
            preferred_content_rock=obj_in.preferred_content_rock,
            preferred_content_sand=obj_in.preferred_content_sand,
            preferred_content_water=obj_in.preferred_content_water,
            preferred_content_fire=obj_in.preferred_content_fire,
            preferred_content_air=obj_in.preferred_content_air,
            preferred_content_earth=obj_in.preferred_content_earth,
            preferred_content_metal=obj_in.preferred_content_metal,
            preferred_content_wood=obj_in.preferred_content_wood,
            preferred_content_glass=obj_in.preferred_content_glass,
            preferred_content_plastic=obj_in.preferred_content_plastic,
            preferred_content_fabric=obj_in.preferred_content_fabric,
            preferred_content_leather=obj_in.preferred_content_leather,
            preferred_content_rubber=obj_in.preferred_content_rubber,
            preferred_content_ceramic=obj_in.preferred_content_ceramic,
            preferred_content_paper=obj_in.preferred_content_paper,
            preferred_content_cardboard=obj_in.preferred_content_cardboard,
            preferred_content_foam=obj_in.preferred_content_foam,
            preferred_content_sponge=obj_in.preferred_content_sponge,
            preferred_content_cotton=obj_in.preferred_content_cotton,
            preferred_content_wool=obj_in.preferred_content_wool,
            preferred_content_silk=obj_in.preferred_content_silk,
            preferred_content_linen=obj_in.preferred_content_linen,
            preferred_content_denim=obj_in.preferred_content_denim,
            preferred_content_corduroy=obj_in.preferred_content_corduroy,
            preferred_content_tweed=obj_in.preferred_content_tweed,
            preferred_content_flannel=obj_in.preferred_content_flannel,
            preferred_content_velvet=obj_in.preferred_content_velvet,
            preferred_content_suede=obj_in.preferred_content_suede,
            preferred_content_fur=obj_in.preferred_content_fur,
            preferred_content_feather=obj_in.preferred_content_feather,
            preferred_content_sequin=obj_in.preferred_content_sequin,
            preferred_content_rhinestone=obj_in.preferred_content_rhinestone,
            preferred_content_pearl=obj_in.preferred_content_pearl,
            preferred_content_crystal=obj_in.preferred_content_crystal,
            preferred_content_diamond=obj_in.preferred_content_diamond,
            preferred_content_gold=obj_in.preferred_content_gold,
            preferred_content_silver=obj_in.preferred_content_silver,
            preferred_content_platinum=obj_in.preferred_content_platinum,
            preferred_content_bronze=obj_in.preferred_content_bronze,
            preferred_content_copper=obj_in.preferred_content_copper,
            preferred_content_brass=obj_in.preferred_content_brass,
            preferred_content_steel=obj_in.preferred_content_steel,
            preferred_content_iron=obj_in.preferred_content_iron,
            preferred_content_aluminum=obj_in.preferred_content_aluminum,
            preferred_content_titanium=obj_in.preferred_content_titanium,
            preferred_content_zinc=obj_in.preferred_content_zinc,
            preferred_content_nickel=obj_in.preferred_content_nickel,
            preferred_content_chrome=obj_in.preferred_content_chrome,
        )
        db.add(db_obj)
        db.flush()  # ID 생성을 위해 flush

        # 통계 정보 생성
        stats = InfluencerStats(
            influencer_id=db_obj.id,
            followers=obj_in.stats.followers,
            following=obj_in.stats.following,
            total_posts=obj_in.stats.total_posts,
            average_likes=obj_in.stats.average_likes,
            average_comments=obj_in.stats.average_comments,
            engagement_rate=obj_in.stats.engagement_rate,
        )
        db.add(stats)

        # 플랫폼 정보 생성
        for platform in obj_in.platforms:
            platform_obj = InfluencerPlatform(
                influencer_id=db_obj.id,
                platform_name=platform.platform_name,
                username=platform.username,
                profile_url=platform.profile_url,
                followers=platform.followers,
                posts=platform.posts,
                engagement_rate=platform.engagement_rate,
            )
            db.add(platform_obj)

        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: Influencer,
        obj_in: Union[InfluencerUpdate, Dict[str, Any]]
    ) -> Influencer:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # 기본 정보 업데이트
        for field, value in update_data.items():
            if field not in ["stats", "platforms"]:
                setattr(db_obj, field, value)
        
        # 통계 정보 업데이트
        if "stats" in update_data:
            stats = db_obj.stats
            if not stats:
                stats = InfluencerStats(influencer_id=db_obj.id)
                db.add(stats)
            
            for field, value in update_data["stats"].items():
                setattr(stats, field, value)
        
        # 플랫폼 정보 업데이트
        if "platforms" in update_data:
            # 기존 플랫폼 정보 삭제
            db.query(InfluencerPlatform).filter(
                InfluencerPlatform.influencer_id == db_obj.id
            ).delete()
            
            # 새로운 플랫폼 정보 추가
            for platform in update_data["platforms"]:
                platform_obj = InfluencerPlatform(
                    influencer_id=db_obj.id,
                    platform_name=platform.platform_name,
                    username=platform.username,
                    profile_url=platform.profile_url,
                    followers=platform.followers,
                    posts=platform.posts,
                    engagement_rate=platform.engagement_rate,
                )
                db.add(platform_obj)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDInfluencerStats(CRUDBase[InfluencerStats, InfluencerStatsCreate, InfluencerStatsUpdate]):
    def get_by_influencer_id(self, db: Session, *, influencer_id: int) -> Optional[InfluencerStats]:
        return db.query(InfluencerStats).filter(InfluencerStats.influencer_id == influencer_id).first()

    def create(self, db: Session, *, obj_in: InfluencerStatsCreate) -> InfluencerStats:
        db_obj = InfluencerStats(
            influencer_id=obj_in.influencer_id,
            followers=obj_in.followers,
            following=obj_in.following,
            total_posts=obj_in.total_posts,
            average_likes=obj_in.average_likes,
            average_comments=obj_in.average_comments,
            engagement_rate=obj_in.engagement_rate
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: InfluencerStats, obj_in: InfluencerStatsUpdate
    ) -> InfluencerStats:
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

class CRUDInfluencerPlatform(CRUDBase[InfluencerPlatform, InfluencerPlatformCreate, InfluencerPlatformUpdate]):
    def get_by_influencer_id(self, db: Session, *, influencer_id: int) -> List[InfluencerPlatform]:
        return db.query(InfluencerPlatform).filter(InfluencerPlatform.influencer_id == influencer_id).all()

    def create(self, db: Session, *, obj_in: InfluencerPlatformCreate) -> InfluencerPlatform:
        db_obj = InfluencerPlatform(
            influencer_id=obj_in.influencer_id,
            platform_name=obj_in.platform_name,
            username=obj_in.username,
            profile_url=obj_in.profile_url,
            followers=obj_in.followers,
            posts=obj_in.posts,
            engagement_rate=obj_in.engagement_rate
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: InfluencerPlatform, obj_in: InfluencerPlatformUpdate
    ) -> InfluencerPlatform:
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

influencer = CRUDInfluencer(Influencer)
influencer_stats = CRUDInfluencerStats(InfluencerStats)
influencer_platform = CRUDInfluencerPlatform(InfluencerPlatform) 