

CREATE OR REPLACE FUNCTION public.get_topics_for_review(p_user_id UUID)
RETURNS TABLE (
    topic_id UUID,
    title VARCHAR,
    days_since_last_session INTEGER,
    mastery_level INTEGER,
    recommended_interval INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id,
        t.title,
        COALESCE(EXTRACT(DAY FROM CURRENT_DATE - ua.last_session_date)::INTEGER, 999) as days_since,
        ua.mastery_level,
        CASE ua.mastery_level
            WHEN 1 THEN 1
            WHEN 2 THEN 3
            WHEN 3 THEN 7
            WHEN 4 THEN 14
            WHEN 5 THEN 30
            ELSE 1
        END as interval_days
    FROM topics t
    LEFT JOIN user_analytics ua ON t.id = ua.topic_id
    WHERE t.user_id = p_user_id 
    AND t.is_active = TRUE
    AND (
        ua.last_session_date IS NULL 
        OR ua.last_session_date <= CURRENT_DATE - INTERVAL '1 day' * 
            CASE ua.mastery_level
                WHEN 1 THEN 1
                WHEN 2 THEN 3
                WHEN 3 THEN 7
                WHEN 4 THEN 14
                WHEN 5 THEN 30
                ELSE 1
            END
    )
    ORDER BY ua.mastery_level ASC, ua.last_session_date ASC NULLS FIRST;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.get_learning_velocity(p_user_id UUID, p_weeks INTEGER DEFAULT 4)
RETURNS TABLE (
    topic_id UUID,
    title VARCHAR,
    sessions_last_weeks INTEGER,
    target_sessions INTEGER,
    velocity_ratio DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id,
        t.title,
        COUNT(s.id)::INTEGER as sessions_count,
        t.target_sessions_per_week * p_weeks as target_total,
        ROUND(
            COUNT(s.id)::DECIMAL / (t.target_sessions_per_week * p_weeks), 
            2
        ) as ratio
    FROM topics t
    LEFT JOIN study_sessions s ON t.id = s.topic_id 
        AND s.session_date >= CURRENT_DATE - INTERVAL '1 week' * p_weeks
        AND s.completed = TRUE
    WHERE t.user_id = p_user_id AND t.is_active = TRUE
    GROUP BY t.id, t.title, t.target_sessions_per_week
    ORDER BY ratio ASC;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.get_confidence_trend(p_user_id UUID, p_topic_id UUID, p_days INTEGER DEFAULT 30)
RETURNS TABLE (
    session_date DATE,
    confidence_before INTEGER,
    confidence_after INTEGER,
    confidence_gain INTEGER,
    session_duration INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.session_date,
        s.confidence_before,
        s.confidence_after,
        (s.confidence_after - s.confidence_before) as gain,
        s.duration_minutes
    FROM study_sessions s
    WHERE s.user_id = p_user_id 
    AND s.topic_id = p_topic_id
    AND s.session_date >= CURRENT_DATE - INTERVAL '1 day' * p_days
    AND s.completed = TRUE
    ORDER BY s.session_date ASC;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.get_study_schedule(p_user_id UUID, p_days INTEGER DEFAULT 7)
RETURNS TABLE (
    study_date DATE,
    topic_id UUID,
    title VARCHAR,
    priority_score INTEGER,
    recommended_duration INTEGER,
    reason TEXT
) AS $$
BEGIN
    RETURN QUERY
    WITH topic_priorities AS (
        SELECT 
            t.id as topic_id,
            t.title,
            t.target_sessions_per_week,
            ua.mastery_level,
            ua.current_streak,
            ua.last_session_date,
            CASE 
                WHEN ua.last_session_date IS NULL THEN 100
                WHEN ua.last_session_date <= CURRENT_DATE - INTERVAL '7 days' THEN 90
                WHEN ua.last_session_date <= CURRENT_DATE - INTERVAL '3 days' THEN 70
                WHEN ua.mastery_level <= 2 THEN 60
                WHEN ua.current_streak >= 3 THEN 40
                ELSE 50
            END as priority_score,
            CASE ua.mastery_level
                WHEN 1 THEN 30
                WHEN 2 THEN 45
                WHEN 3 THEN 60
                WHEN 4 THEN 45
                WHEN 5 THEN 30
                ELSE 30
            END as recommended_duration
        FROM topics t
        LEFT JOIN user_analytics ua ON t.id = ua.topic_id
        WHERE t.user_id = p_user_id AND t.is_active = TRUE
    )
    SELECT 
        CURRENT_DATE + INTERVAL '1 day' * (ROW_NUMBER() OVER (ORDER BY priority_score DESC) - 1) as study_date,
        topic_id,
        title,
        priority_score,
        recommended_duration,
        CASE 
            WHEN priority_score >= 90 THEN 'Overdue for review'
            WHEN priority_score >= 70 THEN 'Maintaining streak'
            WHEN priority_score >= 60 THEN 'Building foundation'
            WHEN priority_score >= 40 THEN 'Advanced practice'
            ELSE 'Regular review'
        END as reason
    FROM topic_priorities
    WHERE ROW_NUMBER() OVER (ORDER BY priority_score DESC) <= p_days;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.get_mastery_insights(p_user_id UUID)
RETURNS TABLE (
    topic_id UUID,
    title VARCHAR,
    current_mastery INTEGER,
    sessions_to_next_level INTEGER,
    estimated_days_to_mastery INTEGER,
    confidence_trend DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id,
        t.title,
        COALESCE(ua.mastery_level, 1) as current_level,
        GREATEST(0, (COALESCE(ua.mastery_level, 1) * 10) - COALESCE(ua.total_sessions, 0)) as sessions_needed,
        CEIL(
            GREATEST(0, (COALESCE(ua.mastery_level, 1) * 10) - COALESCE(ua.total_sessions, 0))::DECIMAL / 
            t.target_sessions_per_week * 7
        )::INTEGER as days_estimate,
        COALESCE(ua.average_confidence_gain, 0) as trend
    FROM topics t
    LEFT JOIN user_analytics ua ON t.id = ua.topic_id
    WHERE t.user_id = p_user_id AND t.is_active = TRUE
    ORDER BY current_level ASC, sessions_needed ASC;
END;
$$ LANGUAGE plpgsql;


GRANT EXECUTE ON FUNCTION public.get_topics_for_review(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_learning_velocity(UUID, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_confidence_trend(UUID, UUID, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_study_schedule(UUID, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_mastery_insights(UUID) TO authenticated;
