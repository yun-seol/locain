from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class InfluencerStats(BaseModel):
    followers: int = Field(default=0, description="팔로워 수")
    following: int = Field(default=0, description="팔로잉 수")
    total_posts: int = Field(default=0, description="총 포스팅 수")
    average_likes: int = Field(default=0, description="평균 좋아요 수")
    average_comments: int = Field(default=0, description="평균 댓글 수")
    engagement_rate: float = Field(default=0.0, description="참여율")

class InfluencerPlatform(BaseModel):
    platform_name: str = Field(..., description="플랫폼 이름")
    username: str = Field(..., description="사용자명")
    profile_url: str = Field(..., description="프로필 URL")
    followers: int = Field(default=0, description="팔로워 수")
    posts: int = Field(default=0, description="포스팅 수")
    engagement_rate: float = Field(default=0.0, description="참여율")

class InfluencerBase(BaseModel):
    bio: Optional[str] = None
    categories: List[str] = []
    platforms: List[InfluencerPlatform] = Field(default=[], description="활동 플랫폼")
    stats: InfluencerStats = Field(default_factory=InfluencerStats, description="통계 정보")
    preferred_brands: List[str] = []
    preferred_categories: List[str] = []
    preferred_price_range: Optional[Dict[str, float]] = None
    preferred_regions: List[str] = []
    content_style: List[str] = []
    available_for_collaboration: bool = True
    minimum_fee: Optional[float] = None
    maximum_fee: Optional[float] = None
    preferred_payment_methods: List[str] = Field(default=[], description="선호 결제 방식")
    preferred_delivery_methods: List[str] = Field(default=[], description="선호 배송 방식")
    preferred_communication_methods: List[str] = Field(default=[], description="선호 커뮤니케이션 방식")
    preferred_content_deadline: Optional[int] = Field(None, description="선호 콘텐츠 마감일(일)")
    preferred_content_review: bool = Field(default=True, description="콘텐츠 리뷰 선호 여부")
    preferred_content_guidelines: Optional[str] = Field(None, description="선호 콘텐츠 가이드라인")
    preferred_content_format: List[str] = Field(default=[], description="선호 콘텐츠 형식")
    preferred_content_length: Optional[Dict[str, int]] = Field(None, description="선호 콘텐츠 길이")
    preferred_content_schedule: Optional[Dict[str, List[str]]] = Field(None, description="선호 콘텐츠 일정")
    preferred_content_hashtags: List[str] = Field(default=[], description="선호 해시태그")
    preferred_content_mentions: List[str] = Field(default=[], description="선호 멘션")
    preferred_content_links: List[str] = Field(default=[], description="선호 링크")
    preferred_content_images: Optional[int] = Field(None, description="선호 이미지 수")
    preferred_content_videos: Optional[int] = Field(None, description="선호 영상 수")
    preferred_content_audios: Optional[int] = Field(None, description="선호 오디오 수")
    preferred_content_texts: Optional[int] = Field(None, description="선호 텍스트 수")
    preferred_content_emojis: Optional[int] = Field(None, description="선호 이모지 수")
    preferred_content_filters: List[str] = Field(default=[], description="선호 필터")
    preferred_content_effects: List[str] = Field(default=[], description="선호 효과")
    preferred_content_music: List[str] = Field(default=[], description="선호 음악")
    preferred_content_fonts: List[str] = Field(default=[], description="선호 폰트")
    preferred_content_colors: List[str] = Field(default=[], description="선호 색상")
    preferred_content_backgrounds: List[str] = Field(default=[], description="선호 배경")
    preferred_content_props: List[str] = Field(default=[], description="선호 소품")
    preferred_content_locations: List[str] = Field(default=[], description="선호 장소")
    preferred_content_weather: List[str] = Field(default=[], description="선호 날씨")
    preferred_content_time: List[str] = Field(default=[], description="선호 시간")
    preferred_content_season: List[str] = Field(default=[], description="선호 계절")
    preferred_content_occasion: List[str] = Field(default=[], description="선호 행사")
    preferred_content_theme: List[str] = Field(default=[], description="선호 테마")
    preferred_content_mood: List[str] = Field(default=[], description="선호 분위기")
    preferred_content_tone: List[str] = Field(default=[], description="선호 톤")
    preferred_content_style: List[str] = Field(default=[], description="선호 스타일")
    preferred_content_angle: List[str] = Field(default=[], description="선호 각도")
    preferred_content_focus: List[str] = Field(default=[], description="선호 초점")
    preferred_content_composition: List[str] = Field(default=[], description="선호 구도")
    preferred_content_lighting: List[str] = Field(default=[], description="선호 조명")
    preferred_content_shadow: List[str] = Field(default=[], description="선호 그림자")
    preferred_content_reflection: List[str] = Field(default=[], description="선호 반사")
    preferred_content_mirror: List[str] = Field(default=[], description="선호 거울")
    preferred_content_window: List[str] = Field(default=[], description="선호 창")
    preferred_content_door: List[str] = Field(default=[], description="선호 문")
    preferred_content_wall: List[str] = Field(default=[], description="선호 벽")
    preferred_content_floor: List[str] = Field(default=[], description="선호 바닥")
    preferred_content_ceiling: List[str] = Field(default=[], description="선호 천장")
    preferred_content_stairs: List[str] = Field(default=[], description="선호 계단")
    preferred_content_elevator: List[str] = Field(default=[], description="선호 엘리베이터")
    preferred_content_escalator: List[str] = Field(default=[], description="선호 에스컬레이터")
    preferred_content_bench: List[str] = Field(default=[], description="선호 벤치")
    preferred_content_chair: List[str] = Field(default=[], description="선호 의자")
    preferred_content_table: List[str] = Field(default=[], description="선호 테이블")
    preferred_content_counter: List[str] = Field(default=[], description="선호 카운터")
    preferred_content_bar: List[str] = Field(default=[], description="선호 바")
    preferred_content_sofa: List[str] = Field(default=[], description="선호 소파")
    preferred_content_bed: List[str] = Field(default=[], description="선호 침대")
    preferred_content_cabinet: List[str] = Field(default=[], description="선호 캐비닛")
    preferred_content_shelf: List[str] = Field(default=[], description="선호 선반")
    preferred_content_rack: List[str] = Field(default=[], description="선호 랙")
    preferred_content_hook: List[str] = Field(default=[], description="선호 훅")
    preferred_content_plant: List[str] = Field(default=[], description="선호 식물")
    preferred_content_flower: List[str] = Field(default=[], description="선호 꽃")
    preferred_content_tree: List[str] = Field(default=[], description="선호 나무")
    preferred_content_grass: List[str] = Field(default=[], description="선호 잔디")
    preferred_content_rock: List[str] = Field(default=[], description="선호 바위")
    preferred_content_sand: List[str] = Field(default=[], description="선호 모래")
    preferred_content_water: List[str] = Field(default=[], description="선호 물")
    preferred_content_fire: List[str] = Field(default=[], description="선호 불")
    preferred_content_air: List[str] = Field(default=[], description="선호 공기")
    preferred_content_earth: List[str] = Field(default=[], description="선호 땅")
    preferred_content_metal: List[str] = Field(default=[], description="선호 금속")
    preferred_content_wood: List[str] = Field(default=[], description="선호 나무")
    preferred_content_glass: List[str] = Field(default=[], description="선호 유리")
    preferred_content_plastic: List[str] = Field(default=[], description="선호 플라스틱")
    preferred_content_fabric: List[str] = Field(default=[], description="선호 천")
    preferred_content_leather: List[str] = Field(default=[], description="선호 가죽")
    preferred_content_rubber: List[str] = Field(default=[], description="선호 고무")
    preferred_content_ceramic: List[str] = Field(default=[], description="선호 도자기")
    preferred_content_paper: List[str] = Field(default=[], description="선호 종이")
    preferred_content_cardboard: List[str] = Field(default=[], description="선호 골판지")
    preferred_content_foam: List[str] = Field(default=[], description="선호 폼")
    preferred_content_sponge: List[str] = Field(default=[], description="선호 스펀지")
    preferred_content_cotton: List[str] = Field(default=[], description="선호 면")
    preferred_content_wool: List[str] = Field(default=[], description="선호 양모")
    preferred_content_silk: List[str] = Field(default=[], description="선호 실크")
    preferred_content_linen: List[str] = Field(default=[], description="선호 린넨")
    preferred_content_denim: List[str] = Field(default=[], description="선호 데님")
    preferred_content_corduroy: List[str] = Field(default=[], description="선호 코듀로이")
    preferred_content_tweed: List[str] = Field(default=[], description="선호 트위드")
    preferred_content_flannel: List[str] = Field(default=[], description="선호 플란넬")
    preferred_content_velvet: List[str] = Field(default=[], description="선호 벨벳")
    preferred_content_suede: List[str] = Field(default=[], description="선호 스웨이드")
    preferred_content_fur: List[str] = Field(default=[], description="선호 퍼")
    preferred_content_feather: List[str] = Field(default=[], description="선호 깃털")
    preferred_content_sequin: List[str] = Field(default=[], description="선호 시퀸")
    preferred_content_rhinestone: List[str] = Field(default=[], description="선호 라인스톤")
    preferred_content_pearl: List[str] = Field(default=[], description="선호 진주")
    preferred_content_crystal: List[str] = Field(default=[], description="선호 크리스탈")
    preferred_content_diamond: List[str] = Field(default=[], description="선호 다이아몬드")
    preferred_content_gold: List[str] = Field(default=[], description="선호 금")
    preferred_content_silver: List[str] = Field(default=[], description="선호 은")
    preferred_content_platinum: List[str] = Field(default=[], description="선호 백금")
    preferred_content_bronze: List[str] = Field(default=[], description="선호 청동")
    preferred_content_copper: List[str] = Field(default=[], description="선호 구리")
    preferred_content_brass: List[str] = Field(default=[], description="선호 황동")
    preferred_content_steel: List[str] = Field(default=[], description="선호 강철")
    preferred_content_iron: List[str] = Field(default=[], description="선호 철")
    preferred_content_aluminum: List[str] = Field(default=[], description="선호 알루미늄")
    preferred_content_titanium: List[str] = Field(default=[], description="선호 티타늄")
    preferred_content_zinc: List[str] = Field(default=[], description="선호 아연")
    preferred_content_nickel: List[str] = Field(default=[], description="선호 니켈")
    preferred_content_chrome: List[str] = Field(default=[], description="선호 크롬")
    preferred_content_palladium: List[str] = Field(default=[], description="선호 팔라듐")
    preferred_content_rhodium: List[str] = Field(default=[], description="선호 로듐")
    preferred_content_iridium: List[str] = Field(default=[], description="선호 이리듐")
    preferred_content_osmium: List[str] = Field(default=[], description="선호 오스뮴")
    preferred_content_ruthenium: List[str] = Field(default=[], description="선호 루테늄")
    preferred_content_technetium: List[str] = Field(default=[], description="선호 테크네튬")
    preferred_content_rhenium: List[str] = Field(default=[], description="선호 레늄")
    preferred_content_manganese: List[str] = Field(default=[], description="선호 망간")
    preferred_content_cobalt: List[str] = Field(default=[], description="선호 코발트")
    preferred_content_gallium: List[str] = Field(default=[], description="선호 갈륨")
    preferred_content_germanium: List[str] = Field(default=[], description="선호 게르마늄")
    preferred_content_arsenic: List[str] = Field(default=[], description="선호 비소")
    preferred_content_selenium: List[str] = Field(default=[], description="선호 셀레늄")
    preferred_content_bromine: List[str] = Field(default=[], description="선호 브롬")
    preferred_content_krypton: List[str] = Field(default=[], description="선호 크립톤")
    preferred_content_rubidium: List[str] = Field(default=[], description="선호 루비듐")
    preferred_content_strontium: List[str] = Field(default=[], description="선호 스트론튬")
    preferred_content_yttrium: List[str] = Field(default=[], description="선호 이트륨")
    preferred_content_zirconium: List[str] = Field(default=[], description="선호 지르코늄")
    preferred_content_niobium: List[str] = Field(default=[], description="선호 니오븀")
    preferred_content_molybdenum: List[str] = Field(default=[], description="선호 몰리브덴")
    preferred_content_technetium: List[str] = Field(default=[], description="선호 테크네튬")
    preferred_content_ruthenium: List[str] = Field(default=[], description="선호 루테늄")
    preferred_content_rhodium: List[str] = Field(default=[], description="선호 로듐")
    preferred_content_palladium: List[str] = Field(default=[], description="선호 팔라듐")
    preferred_content_silver: List[str] = Field(default=[], description="선호 은")
    preferred_content_cadmium: List[str] = Field(default=[], description="선호 카드뮴")
    preferred_content_indium: List[str] = Field(default=[], description="선호 인듐")
    preferred_content_tin: List[str] = Field(default=[], description="선호 주석")
    preferred_content_antimony: List[str] = Field(default=[], description="선호 안티모니")
    preferred_content_tellurium: List[str] = Field(default=[], description="선호 텔루륨")
    preferred_content_iodine: List[str] = Field(default=[], description="선호 요오드")
    preferred_content_xenon: List[str] = Field(default=[], description="선호 제논")
    preferred_content_cesium: List[str] = Field(default=[], description="선호 세슘")
    preferred_content_barium: List[str] = Field(default=[], description="선호 바륨")
    preferred_content_lanthanum: List[str] = Field(default=[], description="선호 란타넘")
    preferred_content_cerium: List[str] = Field(default=[], description="선호 세륨")
    preferred_content_praseodymium: List[str] = Field(default=[], description="선호 프라세오디뮴")
    preferred_content_neodymium: List[str] = Field(default=[], description="선호 네오디뮴")
    preferred_content_promethium: List[str] = Field(default=[], description="선호 프로메튬")
    preferred_content_samarium: List[str] = Field(default=[], description="선호 사마륨")
    preferred_content_europium: List[str] = Field(default=[], description="선호 유로퓸")
    preferred_content_gadolinium: List[str] = Field(default=[], description="선호 가돌리늄")
    preferred_content_terbium: List[str] = Field(default=[], description="선호 터븀")
    preferred_content_dysprosium: List[str] = Field(default=[], description="선호 디스프로슘")
    preferred_content_holmium: List[str] = Field(default=[], description="선호 홀뮴")
    preferred_content_erbium: List[str] = Field(default=[], description="선호 어븀")
    preferred_content_thulium: List[str] = Field(default=[], description="선호 툴륨")
    preferred_content_ytterbium: List[str] = Field(default=[], description="선호 이터븀")
    preferred_content_lutetium: List[str] = Field(default=[], description="선호 루테튬")
    preferred_content_hafnium: List[str] = Field(default=[], description="선호 하프늄")
    preferred_content_tantalum: List[str] = Field(default=[], description="선호 탄탈럼")
    preferred_content_tungsten: List[str] = Field(default=[], description="선호 텅스텐")
    preferred_content_rhenium: List[str] = Field(default=[], description="선호 레늄")
    preferred_content_osmium: List[str] = Field(default=[], description="선호 오스뮴")
    preferred_content_iridium: List[str] = Field(default=[], description="선호 이리듐")
    preferred_content_platinum: List[str] = Field(default=[], description="선호 백금")
    preferred_content_gold: List[str] = Field(default=[], description="선호 금")
    preferred_content_mercury: List[str] = Field(default=[], description="선호 수은")
    preferred_content_thallium: List[str] = Field(default=[], description="선호 탈륨")
    preferred_content_lead: List[str] = Field(default=[], description="선호 납")
    preferred_content_bismuth: List[str] = Field(default=[], description="선호 비스무트")
    preferred_content_polonium: List[str] = Field(default=[], description="선호 폴로늄")
    preferred_content_astatine: List[str] = Field(default=[], description="선호 아스타틴")
    preferred_content_radon: List[str] = Field(default=[], description="선호 라돈")
    preferred_content_francium: List[str] = Field(default=[], description="선호 프랑슘")
    preferred_content_radium: List[str] = Field(default=[], description="선호 라듐")
    preferred_content_actinium: List[str] = Field(default=[], description="선호 악티늄")
    preferred_content_thorium: List[str] = Field(default=[], description="선호 토륨")
    preferred_content_protactinium: List[str] = Field(default=[], description="선호 프로탁티늄")
    preferred_content_uranium: List[str] = Field(default=[], description="선호 우라늄")
    preferred_content_neptunium: List[str] = Field(default=[], description="선호 넵투늄")
    preferred_content_plutonium: List[str] = Field(default=[], description="선호 플루토늄")
    preferred_content_americium: List[str] = Field(default=[], description="선호 아메리슘")
    preferred_content_curium: List[str] = Field(default=[], description="선호 퀴륨")
    preferred_content_berkelium: List[str] = Field(default=[], description="선호 버클륨")
    preferred_content_californium: List[str] = Field(default=[], description="선호 캘리포르늄")
    preferred_content_einsteinium: List[str] = Field(default=[], description="선호 아인슈타이늄")
    preferred_content_fermium: List[str] = Field(default=[], description="선호 페르뮴")
    preferred_content_mendelevium: List[str] = Field(default=[], description="선호 멘델레븀")
    preferred_content_nobelium: List[str] = Field(default=[], description="선호 노벨륨")
    preferred_content_lawrencium: List[str] = Field(default=[], description="선호 로렌슘")
    preferred_content_rutherfordium: List[str] = Field(default=[], description="선호 러더포듐")
    preferred_content_dubnium: List[str] = Field(default=[], description="선호 더브늄")
    preferred_content_seaborgium: List[str] = Field(default=[], description="선호 시보귬")
    preferred_content_bohrium: List[str] = Field(default=[], description="선호 보륨")
    preferred_content_hassium: List[str] = Field(default=[], description="선호 하슘")
    preferred_content_meitnerium: List[str] = Field(default=[], description="선호 마이트너륨")
    preferred_content_darmstadtium: List[str] = Field(default=[], description="선호 다름슈타튬")
    preferred_content_roentgenium: List[str] = Field(default=[], description="선호 뢴트게늄")
    preferred_content_copernicium: List[str] = Field(default=[], description="선호 코페르니슘")
    preferred_content_nihonium: List[str] = Field(default=[], description="선호 니호늄")
    preferred_content_flerovium: List[str] = Field(default=[], description="선호 플레로븀")
    preferred_content_moscovium: List[str] = Field(default=[], description="선호 모스코븀")
    preferred_content_livermorium: List[str] = Field(default=[], description="선호 리버모륨")
    preferred_content_tennessine: List[str] = Field(default=[], description="선호 테네신")
    preferred_content_oganesson: List[str] = Field(default=[], description="선호 오가네손")

class InfluencerCreate(InfluencerBase):
    user_id: int

class InfluencerUpdate(BaseModel):
    bio: Optional[str] = None
    categories: Optional[List[str]] = None
    preferred_brands: Optional[List[str]] = None
    preferred_categories: Optional[List[str]] = None
    preferred_price_range: Optional[Dict[str, float]] = None
    preferred_regions: Optional[List[str]] = None
    content_style: Optional[List[str]] = None
    available_for_collaboration: Optional[bool] = None
    minimum_fee: Optional[float] = None
    maximum_fee: Optional[float] = None

class InfluencerInDBBase(InfluencerBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Influencer(InfluencerInDBBase):
    pass

class InfluencerInDB(InfluencerInDBBase):
    pass

class InfluencerStatsBase(BaseModel):
    followers: int = 0
    following: int = 0
    total_posts: int = 0
    average_likes: int = 0
    average_comments: int = 0
    engagement_rate: float = 0.0

class InfluencerStatsCreate(InfluencerStatsBase):
    influencer_id: int

class InfluencerStatsUpdate(BaseModel):
    followers: Optional[int] = None
    following: Optional[int] = None
    total_posts: Optional[int] = None
    average_likes: Optional[int] = None
    average_comments: Optional[int] = None
    engagement_rate: Optional[float] = None

class InfluencerStats(InfluencerStatsBase):
    id: int
    influencer_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InfluencerPlatformBase(BaseModel):
    platform_name: str
    username: str
    profile_url: str
    followers: int = 0
    posts: int = 0
    engagement_rate: float = 0.0

class InfluencerPlatformCreate(InfluencerPlatformBase):
    influencer_id: int

class InfluencerPlatformUpdate(BaseModel):
    platform_name: Optional[str] = None
    username: Optional[str] = None
    profile_url: Optional[str] = None
    followers: Optional[int] = None
    posts: Optional[int] = None
    engagement_rate: Optional[float] = None

class InfluencerPlatform(InfluencerPlatformBase):
    id: int
    influencer_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 