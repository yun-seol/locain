-- 기존 테이블 삭제 (외래 키 제약조건 고려)
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS blog_post_rankings;
DROP TABLE IF EXISTS influencer_platforms;
DROP TABLE IF EXISTS influencer_stats;
DROP TABLE IF EXISTS influencers;
DROP TABLE IF EXISTS social_channels;
DROP TABLE IF EXISTS campaign_applications;
DROP TABLE IF EXISTS campaigns;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

-- 사용자 테이블
CREATE TABLE users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 캠페인 테이블
CREATE TABLE campaigns (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('DRAFT', 'ACTIVE', 'PAUSED', 'COMPLETED', 'CANCELLED') DEFAULT 'DRAFT',
    start_date DATETIME,
    end_date DATETIME,
    budget INT,
    max_participants INT,
    requirements TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_campaigns_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 캠페인 신청 테이블
CREATE TABLE campaign_applications (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    campaign_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    status ENUM('PENDING', 'APPROVED', 'REJECTED', 'WITHDRAWN') DEFAULT 'PENDING',
    application_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_campaign_applications_campaigns FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    CONSTRAINT fk_campaign_applications_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 소셜 채널 테이블
CREATE TABLE social_channels (
    channel_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    platform VARCHAR(50) NOT NULL,
    channel_url VARCHAR(255) NOT NULL,
    followers INT DEFAULT 0,
    posts INT DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_social_channels_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 블로그 포스트 순위 테이블
CREATE TABLE blog_post_rankings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    channel_id BIGINT NOT NULL,
    post_url VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    comments INT DEFAULT 0,
    shares INT DEFAULT 0,
    ranking_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_blog_post_rankings_social_channels FOREIGN KEY (channel_id) REFERENCES social_channels(channel_id) ON DELETE CASCADE
);

-- 인플루언서 테이블
CREATE TABLE influencers (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    bio TEXT,
    categories JSON DEFAULT ('[]'),
    preferred_brands JSON DEFAULT ('[]'),
    preferred_categories JSON DEFAULT ('[]'),
    preferred_price_range JSON,
    preferred_regions JSON DEFAULT ('[]'),
    content_style JSON DEFAULT ('[]'),
    available_for_collaboration BOOLEAN DEFAULT true,
    minimum_fee DECIMAL(10,2),
    maximum_fee DECIMAL(10,2),
    preferred_payment_methods JSON DEFAULT ('[]'),
    preferred_delivery_methods JSON DEFAULT ('[]'),
    preferred_communication_methods JSON DEFAULT ('[]'),
    preferred_content_deadline INT,
    preferred_content_review BOOLEAN DEFAULT true,
    preferred_content_guidelines TEXT,
    preferred_content_format JSON DEFAULT ('[]'),
    preferred_content_length JSON,
    preferred_content_schedule JSON,
    preferred_content_hashtags JSON DEFAULT ('[]'),
    preferred_content_mentions JSON DEFAULT ('[]'),
    preferred_content_links JSON DEFAULT ('[]'),
    preferred_content_images INT,
    preferred_content_videos INT,
    preferred_content_audios INT,
    preferred_content_texts INT,
    preferred_content_emojis INT,
    preferred_content_filters JSON DEFAULT ('[]'),
    preferred_content_effects JSON DEFAULT ('[]'),
    preferred_content_music JSON DEFAULT ('[]'),
    preferred_content_fonts JSON DEFAULT ('[]'),
    preferred_content_colors JSON DEFAULT ('[]'),
    preferred_content_backgrounds JSON DEFAULT ('[]'),
    preferred_content_props JSON DEFAULT ('[]'),
    preferred_content_locations JSON DEFAULT ('[]'),
    preferred_content_weather JSON DEFAULT ('[]'),
    preferred_content_time JSON DEFAULT ('[]'),
    preferred_content_season JSON DEFAULT ('[]'),
    preferred_content_occasion JSON DEFAULT ('[]'),
    preferred_content_theme JSON DEFAULT ('[]'),
    preferred_content_mood JSON DEFAULT ('[]'),
    preferred_content_tone JSON DEFAULT ('[]'),
    preferred_content_style JSON DEFAULT ('[]'),
    preferred_content_angle JSON DEFAULT ('[]'),
    preferred_content_focus JSON DEFAULT ('[]'),
    preferred_content_composition JSON DEFAULT ('[]'),
    preferred_content_lighting JSON DEFAULT ('[]'),
    preferred_content_shadow JSON DEFAULT ('[]'),
    preferred_content_reflection JSON DEFAULT ('[]'),
    preferred_content_mirror JSON DEFAULT ('[]'),
    preferred_content_window JSON DEFAULT ('[]'),
    preferred_content_door JSON DEFAULT ('[]'),
    preferred_content_wall JSON DEFAULT ('[]'),
    preferred_content_floor JSON DEFAULT ('[]'),
    preferred_content_ceiling JSON DEFAULT ('[]'),
    preferred_content_stairs JSON DEFAULT ('[]'),
    preferred_content_elevator JSON DEFAULT ('[]'),
    preferred_content_escalator JSON DEFAULT ('[]'),
    preferred_content_bench JSON DEFAULT ('[]'),
    preferred_content_chair JSON DEFAULT ('[]'),
    preferred_content_table JSON DEFAULT ('[]'),
    preferred_content_counter JSON DEFAULT ('[]'),
    preferred_content_bar JSON DEFAULT ('[]'),
    preferred_content_sofa JSON DEFAULT ('[]'),
    preferred_content_bed JSON DEFAULT ('[]'),
    preferred_content_cabinet JSON DEFAULT ('[]'),
    preferred_content_shelf JSON DEFAULT ('[]'),
    preferred_content_rack JSON DEFAULT ('[]'),
    preferred_content_hook JSON DEFAULT ('[]'),
    preferred_content_plant JSON DEFAULT ('[]'),
    preferred_content_flower JSON DEFAULT ('[]'),
    preferred_content_tree JSON DEFAULT ('[]'),
    preferred_content_grass JSON DEFAULT ('[]'),
    preferred_content_rock JSON DEFAULT ('[]'),
    preferred_content_sand JSON DEFAULT ('[]'),
    preferred_content_water JSON DEFAULT ('[]'),
    preferred_content_fire JSON DEFAULT ('[]'),
    preferred_content_air JSON DEFAULT ('[]'),
    preferred_content_earth JSON DEFAULT ('[]'),
    preferred_content_metal JSON DEFAULT ('[]'),
    preferred_content_wood JSON DEFAULT ('[]'),
    preferred_content_glass JSON DEFAULT ('[]'),
    preferred_content_plastic JSON DEFAULT ('[]'),
    preferred_content_fabric JSON DEFAULT ('[]'),
    preferred_content_leather JSON DEFAULT ('[]'),
    preferred_content_rubber JSON DEFAULT ('[]'),
    preferred_content_ceramic JSON DEFAULT ('[]'),
    preferred_content_paper JSON DEFAULT ('[]'),
    preferred_content_cardboard JSON DEFAULT ('[]'),
    preferred_content_foam JSON DEFAULT ('[]'),
    preferred_content_sponge JSON DEFAULT ('[]'),
    preferred_content_cotton JSON DEFAULT ('[]'),
    preferred_content_wool JSON DEFAULT ('[]'),
    preferred_content_silk JSON DEFAULT ('[]'),
    preferred_content_linen JSON DEFAULT ('[]'),
    preferred_content_denim JSON DEFAULT ('[]'),
    preferred_content_corduroy JSON DEFAULT ('[]'),
    preferred_content_tweed JSON DEFAULT ('[]'),
    preferred_content_flannel JSON DEFAULT ('[]'),
    preferred_content_velvet JSON DEFAULT ('[]'),
    preferred_content_suede JSON DEFAULT ('[]'),
    preferred_content_fur JSON DEFAULT ('[]'),
    preferred_content_feather JSON DEFAULT ('[]'),
    preferred_content_sequin JSON DEFAULT ('[]'),
    preferred_content_rhinestone JSON DEFAULT ('[]'),
    preferred_content_pearl JSON DEFAULT ('[]'),
    preferred_content_crystal JSON DEFAULT ('[]'),
    preferred_content_diamond JSON DEFAULT ('[]'),
    preferred_content_gold JSON DEFAULT ('[]'),
    preferred_content_silver JSON DEFAULT ('[]'),
    preferred_content_platinum JSON DEFAULT ('[]'),
    preferred_content_bronze JSON DEFAULT ('[]'),
    preferred_content_copper JSON DEFAULT ('[]'),
    preferred_content_brass JSON DEFAULT ('[]'),
    preferred_content_steel JSON DEFAULT ('[]'),
    preferred_content_iron JSON DEFAULT ('[]'),
    preferred_content_aluminum JSON DEFAULT ('[]'),
    preferred_content_titanium JSON DEFAULT ('[]'),
    preferred_content_zinc JSON DEFAULT ('[]'),
    preferred_content_nickel JSON DEFAULT ('[]'),
    preferred_content_chrome JSON DEFAULT ('[]'),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_influencers_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 인플루언서 통계 테이블
CREATE TABLE influencer_stats (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    influencer_id BIGINT NOT NULL UNIQUE,
    followers INT DEFAULT 0,
    following INT DEFAULT 0,
    total_posts INT DEFAULT 0,
    average_likes INT DEFAULT 0,
    average_comments INT DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_influencer_stats_influencers FOREIGN KEY (influencer_id) REFERENCES influencers(id) ON DELETE CASCADE
);

-- 인플루언서 플랫폼 테이블
CREATE TABLE influencer_platforms (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    influencer_id BIGINT NOT NULL,
    platform_name VARCHAR(50) NOT NULL,
    username VARCHAR(100) NOT NULL,
    profile_url TEXT NOT NULL,
    followers INT DEFAULT 0,
    posts INT DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_influencer_platforms_influencers FOREIGN KEY (influencer_id) REFERENCES influencers(id) ON DELETE CASCADE
);

-- 인덱스 생성
CREATE INDEX idx_influencers_user_id ON influencers(user_id);
CREATE INDEX idx_influencer_stats_influencer_id ON influencer_stats(influencer_id);
CREATE INDEX idx_influencer_platforms_influencer_id ON influencer_platforms(influencer_id);
CREATE INDEX idx_influencer_platforms_platform_name ON influencer_platforms(platform_name);
CREATE INDEX idx_social_channels_user_id ON social_channels(user_id);
CREATE INDEX idx_social_channels_platform ON social_channels(platform);
CREATE INDEX idx_campaigns_user_id ON campaigns(user_id);
CREATE INDEX idx_campaign_applications_campaign_id ON campaign_applications(campaign_id);
CREATE INDEX idx_campaign_applications_user_id ON campaign_applications(user_id);
CREATE INDEX idx_blog_post_rankings_channel_id ON blog_post_rankings(channel_id); 