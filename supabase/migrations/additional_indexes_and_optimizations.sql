
CREATE INDEX IF NOT EXISTS idx_analytics_user_mastery ON user_analytics(user_id, mastery_level);
CREATE INDEX IF NOT EXISTS idx_analytics_user_next_recommended ON user_analytics(user_id, next_recommended_date);
CREATE INDEX IF NOT EXISTS idx_analytics_topic_mastery ON user_analytics(topic_id, mastery_level);


CREATE INDEX IF NOT EXISTS idx_sessions_topic_date ON study_sessions(topic_id, session_date);
CREATE INDEX IF NOT EXISTS idx_sessions_user_date_range ON study_sessions(user_id, session_date, completed);
CREATE INDEX IF NOT EXISTS idx_sessions_confidence_analysis ON study_sessions(topic_id, confidence_before, confidence_after);


CREATE INDEX IF NOT EXISTS idx_topics_user_difficulty ON topics(user_id, difficulty_level, is_active);
CREATE INDEX IF NOT EXISTS idx_topics_user_created ON topics(user_id, created_at DESC);


CREATE INDEX IF NOT EXISTS idx_topics_active ON topics(user_id, title) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_sessions_completed ON study_sessions(user_id, session_date) WHERE completed = TRUE;


CREATE INDEX IF NOT EXISTS idx_sessions_recent ON study_sessions(user_id, session_date DESC) WHERE session_date >= CURRENT_DATE - INTERVAL '30 days';
CREATE INDEX IF NOT EXISTS idx_analytics_recent_updates ON user_analytics(user_id, updated_at DESC) WHERE updated_at >= CURRENT_DATE - INTERVAL '7 days';


CREATE OR REPLACE FUNCTION public.calculate_streak(p_user_id UUID, p_topic_id UUID)
RETURNS INTEGER AS $$
DECLARE
    streak_count INTEGER := 0;
    current_date DATE := CURRENT_DATE;
    session_exists BOOLEAN;
BEGIN
    LOOP
       
        SELECT EXISTS(
            SELECT 1 FROM study_sessions 
            WHERE user_id = p_user_id 
            AND topic_id = p_topic_id 
            AND session_date = current_date 
            AND completed = TRUE
        ) INTO session_exists;
        
        IF session_exists THEN
            streak_count := streak_count + 1;
            current_date := current_date - INTERVAL '1 day';
        ELSE
            EXIT;
        END IF;
    END LOOP;
    
    RETURN streak_count;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.calculate_next_review_date(
    p_user_id UUID, 
    p_topic_id UUID, 
    p_mastery_level INTEGER
)
RETURNS DATE AS $$
DECLARE
    last_session_date DATE;
    interval_days INTEGER;
BEGIN
    
    SELECT MAX(session_date) INTO last_session_date
    FROM study_sessions
    WHERE user_id = p_user_id AND topic_id = p_topic_id AND completed = TRUE;
    
    
    interval_days := CASE p_mastery_level
        WHEN 1 THEN 1    
        WHEN 2 THEN 3    
        WHEN 3 THEN 7    
        WHEN 4 THEN 14   
        WHEN 5 THEN 30  
        ELSE 1
    END;
    
    RETURN COALESCE(last_session_date, CURRENT_DATE) + INTERVAL '1 day' * interval_days;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE VIEW public.user_dashboard_analytics AS
SELECT 
    u.id as user_id,
    u.email,
    u.first_name,
    u.last_name,
    COUNT(DISTINCT t.id) as total_topics,
    COUNT(DISTINCT CASE WHEN t.is_active = TRUE THEN t.id END) as active_topics,
    COUNT(DISTINCT s.id) as total_sessions,
    COALESCE(SUM(s.duration_minutes), 0) as total_study_time,
    COALESCE(AVG(s.confidence_after - s.confidence_before), 0) as avg_confidence_gain,
    MAX(s.session_date) as last_study_date,
    COUNT(DISTINCT CASE WHEN s.session_date >= CURRENT_DATE - INTERVAL '7 days' THEN s.id END) as sessions_this_week
FROM users u
LEFT JOIN topics t ON u.id = t.user_id
LEFT JOIN study_sessions s ON u.id = s.user_id AND s.completed = TRUE
GROUP BY u.id, u.email, u.first_name, u.last_name;
-- Grant permissions on the view
GRANT SELECT ON user_dashboard_analytics TO authenticated;


CREATE OR REPLACE VIEW public.topic_progress_analytics AS
SELECT 
    t.id as topic_id,
    t.user_id,
    t.title,
    t.difficulty_level,
    t.target_sessions_per_week,
    ua.total_sessions,
    ua.total_study_time,
    ua.current_streak,
    ua.longest_streak,
    ua.mastery_level,
    ua.average_confidence_gain,
    ua.last_session_date,
    ua.next_recommended_date,
    CASE 
        WHEN ua.total_sessions >= t.target_sessions_per_week THEN 'On Track'
        WHEN ua.total_sessions >= t.target_sessions_per_week * 0.5 THEN 'Behind'
        ELSE 'Needs Attention'
    END as progress_status
FROM topics t
LEFT JOIN user_analytics ua ON t.id = ua.topic_id
WHERE t.is_active = TRUE;


GRANT SELECT ON topic_progress_analytics TO authenticated;
