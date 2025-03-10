-- 테스트 데이터 삽입

-- 1. 사용자 데이터
INSERT INTO users (email, password, full_name, role, is_active) VALUES
('admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyDAg1YxQwqK6', '관리자', 'admin', true),
('brand@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyDAg1YxQwqK6', '브랜드사', 'brand', true),
('influencer1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyDAg1YxQwqK6', '인플루언서1', 'influencer', true),
('influencer2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyDAg1YxQwqK6', '인플루언서2', 'influencer', true);

-- 2. 소셜 채널 데이터
INSERT INTO social_channels (user_id, platform, channel_url, followers, posts, engagement_rate) VALUES
(3, 'instagram', 'https://instagram.com/influencer1', 10000, 500, 3.5),
(3, 'youtube', 'https://youtube.com/influencer1', 5000, 200, 4.2),
(4, 'blog', 'https://blog.naver.com/influencer2', 8000, 300, 2.8),
(4, 'instagram', 'https://instagram.com/influencer2', 15000, 800, 3.8);

-- 3. 블로그 포스트 순위 데이터
INSERT INTO blog_post_rankings (channel_id, post_url, title, views, likes, comments, shares, ranking_date) VALUES
(3, 'https://blog.naver.com/influencer2/post1', '맛있는 레시피 공유', 1000, 100, 50, 30, CURRENT_DATE),
(3, 'https://blog.naver.com/influencer2/post2', '일상 브이로그', 800, 80, 40, 20, CURRENT_DATE);

-- 4. 인플루언서 프로필 데이터
INSERT INTO influencers (user_id, bio, categories, preferred_brands, preferred_categories, preferred_price_range, preferred_regions, content_style) VALUES
(3, '패션과 뷰티 전문 인플루언서', '["fashion", "beauty"]', '["nike", "zara"]', '["clothing", "cosmetics"]', '{"min": 50000, "max": 200000}', '["seoul", "busan"]', '["casual", "elegant"]'),
(4, '요리와 라이프스타일 전문가', '["food", "lifestyle"]', '["cookware", "kitchen"]', '["cooking", "home"]', '{"min": 30000, "max": 150000}', '["seoul", "incheon"]', '["warm", "cozy"]');

-- 5. 인플루언서 통계 데이터
INSERT INTO influencer_stats (influencer_id, followers, following, total_posts, average_likes, average_comments, engagement_rate) VALUES
(1, 15000, 500, 700, 500, 50, 3.7),
(2, 23000, 800, 1100, 800, 80, 3.8);

-- 6. 인플루언서 플랫폼 데이터
INSERT INTO influencer_platforms (influencer_id, platform_name, username, profile_url, followers, posts, engagement_rate) VALUES
(1, 'instagram', 'influencer1', 'https://instagram.com/influencer1', 10000, 500, 3.5),
(1, 'youtube', 'influencer1', 'https://youtube.com/influencer1', 5000, 200, 4.2),
(2, 'blog', 'influencer2', 'https://blog.naver.com/influencer2', 8000, 300, 2.8),
(2, 'instagram', 'influencer2', 'https://instagram.com/influencer2', 15000, 800, 3.8);

-- 7. 캠페인 데이터
INSERT INTO campaigns (user_id, title, description, status, start_date, end_date, budget, max_participants, requirements, is_active) VALUES
(2, '여름 패션 캠페인', '여름 시즌 신상품 홍보', 'ACTIVE', date('now', '+1 day'), date('now', '+30 days'), 1000000, 5, '인스타그램 3개, 유튜브 1개', true),
(2, '주방용품 리뷰', '주방용품 사용 후기', 'DRAFT', date('now', '+5 days'), date('now', '+45 days'), 800000, 3, '블로그 2개, 인스타그램 2개', true);

-- 8. 캠페인 신청 데이터
INSERT INTO campaign_applications (campaign_id, user_id, status, application_text) VALUES
(1, 3, 'PENDING', '패션 전문 인플루언서로서 참여하고 싶습니다.'),
(1, 4, 'PENDING', '라이프스타일 전문가로서 참여하고 싶습니다.'),
(2, 4, 'APPROVED', '주방용품 리뷰 전문가로서 참여하고 싶습니다.'); 