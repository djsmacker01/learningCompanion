
CREATE TABLE learning_velocity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    velocity_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    learning_rate DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    time_to_mastery INTEGER, -- days to reach mastery
    difficulty_level VARCHAR(20) NOT NULL DEFAULT 'beginner',
    measurement_period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    measurement_period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Knowledge retention tracking
CREATE TABLE knowledge_retention (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    retention_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    forgetting_curve_slope DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    retention_period_days INTEGER NOT NULL,
    last_reviewed TIMESTAMP WITH TIME ZONE,
    next_review_due TIMESTAMP WITH TIME ZONE,
    mastery_level VARCHAR(20) NOT NULL DEFAULT 'novice',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Learning efficiency metrics
CREATE TABLE learning_efficiency (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    efficiency_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    time_invested_minutes INTEGER NOT NULL DEFAULT 0,
    knowledge_gained_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    focus_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    distraction_count INTEGER NOT NULL DEFAULT 0,
    session_quality DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    measurement_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Personalized learning paths
CREATE TABLE learning_paths (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    path_name VARCHAR(100) NOT NULL,
    path_description TEXT,
    target_skill_level VARCHAR(20) NOT NULL DEFAULT 'intermediate',
    estimated_duration_days INTEGER NOT NULL,
    current_step INTEGER NOT NULL DEFAULT 0,
    total_steps INTEGER NOT NULL,
    completion_percentage DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    ai_generated BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Learning path steps
CREATE TABLE learning_path_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    path_id UUID NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
    step_order INTEGER NOT NULL,
    step_title VARCHAR(200) NOT NULL,
    step_description TEXT,
    step_type VARCHAR(50) NOT NULL, -- 'study', 'practice', 'quiz', 'review'
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    estimated_time_minutes INTEGER NOT NULL DEFAULT 30,
    difficulty_level VARCHAR(20) NOT NULL DEFAULT 'beginner',
    prerequisites TEXT[], -- Array of prerequisite step IDs
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Knowledge gaps and weaknesses
CREATE TABLE knowledge_gaps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    gap_type VARCHAR(50) NOT NULL, -- 'conceptual', 'practical', 'theoretical'
    gap_severity VARCHAR(20) NOT NULL DEFAULT 'medium', -- 'low', 'medium', 'high', 'critical'
    gap_description TEXT NOT NULL,
    detected_through VARCHAR(50) NOT NULL, -- 'quiz', 'session', 'ai_analysis'
    confidence_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    suggested_remediation TEXT,
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Predictive learning analytics
CREATE TABLE predictive_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    prediction_type VARCHAR(50) NOT NULL, -- 'success_probability', 'optimal_time', 'burnout_risk', 'goal_achievement'
    prediction_value DECIMAL(5,2) NOT NULL,
    confidence_level DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    prediction_horizon_days INTEGER NOT NULL DEFAULT 7,
    factors_considered TEXT[], -- Array of factors used in prediction
    prediction_date TIMESTAMP WITH TIME ZONE NOT NULL,
    actual_outcome DECIMAL(5,2), -- For validation
    accuracy_score DECIMAL(5,2), -- How accurate the prediction was
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Study time optimization
CREATE TABLE study_time_optimization (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    optimal_hour INTEGER NOT NULL, -- 0-23
    optimal_day_of_week INTEGER NOT NULL, -- 0-6 (Sunday-Saturday)
    productivity_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    focus_duration_minutes INTEGER NOT NULL DEFAULT 25,
    break_duration_minutes INTEGER NOT NULL DEFAULT 5,
    session_frequency_per_week INTEGER NOT NULL DEFAULT 3,
    measurement_period_days INTEGER NOT NULL DEFAULT 30,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Burnout risk tracking
CREATE TABLE burnout_risk (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    risk_level VARCHAR(20) NOT NULL DEFAULT 'low', -- 'low', 'medium', 'high', 'critical'
    risk_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    contributing_factors TEXT[], -- Array of factors
    study_intensity_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    rest_adequacy_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    stress_indicators TEXT[], -- Array of stress indicators
    recommended_actions TEXT[], -- Array of recommended actions
    is_monitored BOOLEAN NOT NULL DEFAULT TRUE,
    last_assessment TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Goal achievement forecasting
CREATE TABLE goal_forecasting (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    goal_id UUID, -- Reference to user goals (if separate table exists)
    goal_description TEXT NOT NULL,
    target_completion_date DATE NOT NULL,
    predicted_completion_date DATE NOT NULL,
    confidence_percentage DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    current_progress_percentage DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    required_velocity DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    current_velocity DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    is_on_track BOOLEAN NOT NULL DEFAULT TRUE,
    risk_factors TEXT[], -- Array of risk factors
    mitigation_strategies TEXT[], -- Array of mitigation strategies
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_learning_velocity_user_topic ON learning_velocity(user_id, topic_id);
CREATE INDEX idx_learning_velocity_created ON learning_velocity(created_at);
CREATE INDEX idx_knowledge_retention_user_topic ON knowledge_retention(user_id, topic_id);
CREATE INDEX idx_knowledge_retention_next_review ON knowledge_retention(next_review_due);
CREATE INDEX idx_learning_efficiency_user_date ON learning_efficiency(user_id, measurement_date);
CREATE INDEX idx_learning_paths_user_active ON learning_paths(user_id, is_active);
CREATE INDEX idx_learning_path_steps_path_order ON learning_path_steps(path_id, step_order);
CREATE INDEX idx_knowledge_gaps_user_resolved ON knowledge_gaps(user_id, is_resolved);
CREATE INDEX idx_predictive_analytics_user_type ON predictive_analytics(user_id, prediction_type);
CREATE INDEX idx_study_time_optimization_user ON study_time_optimization(user_id);
CREATE INDEX idx_burnout_risk_user_level ON burnout_risk(user_id, risk_level);
CREATE INDEX idx_goal_forecasting_user_track ON goal_forecasting(user_id, is_on_track);

-- Row Level Security (RLS) policies
ALTER TABLE learning_velocity ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_retention ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_efficiency ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_paths ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_path_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_gaps ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictive_analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_time_optimization ENABLE ROW LEVEL SECURITY;
ALTER TABLE burnout_risk ENABLE ROW LEVEL SECURITY;
ALTER TABLE goal_forecasting ENABLE ROW LEVEL SECURITY;

-- RLS Policies for learning_velocity
CREATE POLICY "Users can view own learning velocity" ON learning_velocity
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own learning velocity" ON learning_velocity
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own learning velocity" ON learning_velocity
    FOR UPDATE USING (auth.uid() = user_id);

-- RLS Policies for knowledge_retention
CREATE POLICY "Users can view own knowledge retention" ON knowledge_retention
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own knowledge retention" ON knowledge_retention
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own knowledge retention" ON knowledge_retention
    FOR UPDATE USING (auth.uid() = user_id);

-- RLS Policies for learning_efficiency
CREATE POLICY "Users can view own learning efficiency" ON learning_efficiency
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own learning efficiency" ON learning_efficiency
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- RLS Policies for learning_paths
CREATE POLICY "Users can view own learning paths" ON learning_paths
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own learning paths" ON learning_paths
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own learning paths" ON learning_paths
    FOR UPDATE USING (auth.uid() = user_id);

-- RLS Policies for learning_path_steps
CREATE POLICY "Users can view own learning path steps" ON learning_path_steps
    FOR SELECT USING (auth.uid() = (SELECT user_id FROM learning_paths WHERE id = path_id));
CREATE POLICY "Users can insert own learning path steps" ON learning_path_steps
    FOR INSERT WITH CHECK (auth.uid() = (SELECT user_id FROM learning_paths WHERE id = path_id));
CREATE POLICY "Users can update own learning path steps" ON learning_path_steps
    FOR UPDATE USING (auth.uid() = (SELECT user_id FROM learning_paths WHERE id = path_id));

-- RLS Policies for knowledge_gaps
CREATE POLICY "Users can view own knowledge gaps" ON knowledge_gaps
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own knowledge gaps" ON knowledge_gaps
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own knowledge gaps" ON knowledge_gaps
    FOR UPDATE USING (auth.uid() = user_id);

-- RLS Policies for predictive_analytics
CREATE POLICY "Users can view own predictive analytics" ON predictive_analytics
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own predictive analytics" ON predictive_analytics
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- RLS Policies for study_time_optimization
CREATE POLICY "Users can view own study time optimization" ON study_time_optimization
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own study time optimization" ON study_time_optimization
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own study time optimization" ON study_time_optimization
    FOR UPDATE USING (auth.uid() = user_id);

-- RLS Policies for burnout_risk
CREATE POLICY "Users can view own burnout risk" ON burnout_risk
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own burnout risk" ON burnout_risk
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own burnout risk" ON burnout_risk
    FOR UPDATE USING (auth.uid() = user_id);

-- RLS Policies for goal_forecasting
CREATE POLICY "Users can view own goal forecasting" ON goal_forecasting
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own goal forecasting" ON goal_forecasting
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own goal forecasting" ON goal_forecasting
    FOR UPDATE USING (auth.uid() = user_id);

-- Functions for advanced analytics calculations
CREATE OR REPLACE FUNCTION calculate_learning_velocity(
    p_user_id UUID,
    p_topic_id UUID,
    p_days_back INTEGER DEFAULT 30
)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    velocity_score DECIMAL(5,2);
    total_sessions INTEGER;
    total_time_minutes INTEGER;
    knowledge_gained DECIMAL(5,2);
BEGIN
    -- Calculate learning velocity based on sessions and knowledge gained
    SELECT 
        COUNT(*),
        COALESCE(SUM(duration_minutes), 0),
        COALESCE(AVG(progress_percentage), 0)
    INTO total_sessions, total_time_minutes, knowledge_gained
    FROM study_sessions 
    WHERE user_id = p_user_id 
    AND topic_id = p_topic_id 
    AND created_at >= NOW() - INTERVAL '1 day' * p_days_back;
    
    IF total_sessions = 0 THEN
        RETURN 0.0;
    END IF;
    
    -- Velocity = knowledge gained per hour of study
    velocity_score := (knowledge_gained * 60.0) / GREATEST(total_time_minutes, 1);
    
    RETURN LEAST(velocity_score, 100.0); -- Cap at 100
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calculate_retention_curve(
    p_user_id UUID,
    p_topic_id UUID
)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    retention_score DECIMAL(5,2);
    last_review TIMESTAMP WITH TIME ZONE;
    days_since_review INTEGER;
    forgetting_factor DECIMAL(5,2);
BEGIN
    -- Get last review date
    SELECT MAX(created_at) INTO last_review
    FROM study_sessions 
    WHERE user_id = p_user_id AND topic_id = p_topic_id;
    
    IF last_review IS NULL THEN
        RETURN 0.0;
    END IF;
    
    days_since_review := EXTRACT(EPOCH FROM (NOW() - last_review)) / 86400;
    
    -- Ebbinghaus forgetting curve: R = e^(-t/S)
    -- Where R is retention, t is time, S is strength of memory
    forgetting_factor := EXP(-days_since_review / 7.0); -- 7 days half-life
    
    retention_score := forgetting_factor * 100.0;
    
    RETURN GREATEST(retention_score, 0.0);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calculate_learning_efficiency(
    p_user_id UUID,
    p_topic_id UUID,
    p_session_id UUID
)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    efficiency_score DECIMAL(5,2);
    session_duration INTEGER;
    session_progress DECIMAL(5,2);
    focus_score DECIMAL(5,2);
BEGIN
    -- Get session data
    SELECT duration_minutes, progress_percentage, focus_score
    INTO session_duration, session_progress, focus_score
    FROM study_sessions 
    WHERE id = p_session_id AND user_id = p_user_id;
    
    IF session_duration IS NULL OR session_duration = 0 THEN
        RETURN 0.0;
    END IF;
    
    -- Efficiency = (progress * focus) / time
    efficiency_score := (session_progress * COALESCE(focus_score, 50.0)) / session_duration;
    
    RETURN LEAST(efficiency_score, 100.0);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION detect_knowledge_gaps(
    p_user_id UUID,
    p_topic_id UUID
)
RETURNS TABLE(
    gap_type VARCHAR(50),
    gap_severity VARCHAR(20),
    gap_description TEXT,
    confidence_score DECIMAL(5,2)
) AS $$
BEGIN
    -- Analyze quiz results, session performance, and retention
    RETURN QUERY
    WITH performance_analysis AS (
        SELECT 
            AVG(score) as avg_score,
            COUNT(*) as total_attempts,
            MAX(score) as best_score,
            MIN(score) as worst_score
        FROM quiz_attempts qa
        JOIN quizzes q ON qa.quiz_id = q.id
        WHERE qa.user_id = p_user_id AND q.topic_id = p_topic_id
    ),
    session_analysis AS (
        SELECT 
            AVG(progress_percentage) as avg_progress,
            COUNT(*) as total_sessions,
            AVG(focus_score) as avg_focus
        FROM study_sessions 
        WHERE user_id = p_user_id AND topic_id = p_topic_id
    )
    SELECT 
        CASE 
            WHEN pa.avg_score < 60 THEN 'conceptual'
            WHEN pa.avg_score < 80 THEN 'practical'
            ELSE 'theoretical'
        END as gap_type,
        CASE 
            WHEN pa.avg_score < 40 THEN 'critical'
            WHEN pa.avg_score < 60 THEN 'high'
            WHEN pa.avg_score < 80 THEN 'medium'
            ELSE 'low'
        END as gap_severity,
        CASE 
            WHEN pa.avg_score < 40 THEN 'Critical knowledge gaps detected. Immediate remediation needed.'
            WHEN pa.avg_score < 60 THEN 'Significant knowledge gaps. Focused study required.'
            WHEN pa.avg_score < 80 THEN 'Minor knowledge gaps. Review recommended.'
            ELSE 'Strong understanding. Continue current approach.'
        END as gap_description,
        CASE 
            WHEN pa.total_attempts >= 3 THEN 0.9
            WHEN pa.total_attempts >= 1 THEN 0.7
            ELSE 0.5
        END as confidence_score
    FROM performance_analysis pa, session_analysis sa
    WHERE pa.avg_score IS NOT NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION predict_success_probability(
    p_user_id UUID,
    p_topic_id UUID,
    p_exam_date DATE
)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    success_probability DECIMAL(5,2);
    current_progress DECIMAL(5,2);
    study_velocity DECIMAL(5,2);
    days_remaining INTEGER;
    required_velocity DECIMAL(5,2);
BEGIN
    -- Get current progress
    SELECT AVG(progress_percentage) INTO current_progress
    FROM study_sessions 
    WHERE user_id = p_user_id AND topic_id = p_topic_id
    AND created_at >= NOW() - INTERVAL '7 days';
    
    -- Calculate study velocity
    SELECT calculate_learning_velocity(p_user_id, p_topic_id, 14) INTO study_velocity;
    
    -- Calculate days remaining
    days_remaining := p_exam_date - CURRENT_DATE;
    
    IF days_remaining <= 0 THEN
        RETURN CASE WHEN current_progress >= 80 THEN 90.0 ELSE 20.0 END;
    END IF;
    
    -- Calculate required velocity to reach 80% by exam date
    required_velocity := (80.0 - COALESCE(current_progress, 0)) / days_remaining;
    
    -- Success probability based on velocity comparison
    IF study_velocity >= required_velocity THEN
        success_probability := 85.0 + (study_velocity - required_velocity) * 2;
    ELSE
        success_probability := 20.0 + (study_velocity / required_velocity) * 60;
    END IF;
    
    RETURN GREATEST(LEAST(success_probability, 95.0), 5.0);
END;
$$ LANGUAGE plpgsql;

-- Triggers for automatic analytics updates
CREATE OR REPLACE FUNCTION update_learning_analytics()
RETURNS TRIGGER AS $$
BEGIN
    -- Update learning velocity when study session is completed
    IF NEW.status = 'completed' THEN
        INSERT INTO learning_velocity (
            user_id, topic_id, velocity_score, learning_rate,
            measurement_period_start, measurement_period_end
        )
        VALUES (
            NEW.user_id, NEW.topic_id,
            calculate_learning_velocity(NEW.user_id, NEW.topic_id, 30),
            calculate_learning_velocity(NEW.user_id, NEW.topic_id, 7),
            NEW.created_at - INTERVAL '30 days',
            NEW.created_at
        )
        ON CONFLICT (user_id, topic_id, measurement_period_start) 
        DO UPDATE SET 
            velocity_score = EXCLUDED.velocity_score,
            learning_rate = EXCLUDED.learning_rate,
            updated_at = NOW();
        
        -- Update knowledge retention
        INSERT INTO knowledge_retention (
            user_id, topic_id, retention_score, forgetting_curve_slope,
            retention_period_days, last_reviewed, next_review_due
        )
        VALUES (
            NEW.user_id, NEW.topic_id,
            calculate_retention_curve(NEW.user_id, NEW.topic_id),
            -0.1, -- Default forgetting curve slope
            7, -- 7 days retention period
            NEW.created_at,
            NEW.created_at + INTERVAL '7 days'
        )
        ON CONFLICT (user_id, topic_id) 
        DO UPDATE SET 
            retention_score = EXCLUDED.retention_score,
            last_reviewed = EXCLUDED.last_reviewed,
            next_review_due = EXCLUDED.next_review_due,
            updated_at = NOW();
        
        -- Update learning efficiency
        INSERT INTO learning_efficiency (
            user_id, topic_id, efficiency_score, time_invested_minutes,
            knowledge_gained_score, focus_score, session_quality,
            measurement_date
        )
        VALUES (
            NEW.user_id, NEW.topic_id,
            calculate_learning_efficiency(NEW.user_id, NEW.topic_id, NEW.id),
            NEW.duration_minutes,
            NEW.progress_percentage,
            COALESCE(NEW.focus_score, 50.0),
            NEW.progress_percentage * COALESCE(NEW.focus_score, 50.0) / 100.0,
            NEW.created_at
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_learning_analytics
    AFTER UPDATE ON study_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_learning_analytics();

-- Insert sample data for testing
INSERT INTO learning_velocity (user_id, topic_id, velocity_score, learning_rate, difficulty_level, measurement_period_start, measurement_period_end)
SELECT 
    u.id,
    t.id,
    ROUND((RANDOM() * 50 + 25)::numeric, 2),
    ROUND((RANDOM() * 30 + 15)::numeric, 2),
    CASE 
        WHEN RANDOM() < 0.3 THEN 'beginner'
        WHEN RANDOM() < 0.7 THEN 'intermediate'
        ELSE 'advanced'
    END,
    NOW() - INTERVAL '30 days',
    NOW()
FROM users u
CROSS JOIN topics t
WHERE u.id IN (SELECT id FROM users LIMIT 3)
AND t.id IN (SELECT id FROM topics LIMIT 5);

INSERT INTO knowledge_retention (user_id, topic_id, retention_score, forgetting_curve_slope, retention_period_days, last_reviewed, next_review_due, mastery_level)
SELECT 
    u.id,
    t.id,
    ROUND((RANDOM() * 40 + 30)::numeric, 2),
    ROUND((RANDOM() * -0.2 - 0.1)::numeric, 3),
    FLOOR(RANDOM() * 14 + 7),
    NOW() - INTERVAL '3 days',
    NOW() + INTERVAL '4 days',
    CASE 
        WHEN RANDOM() < 0.2 THEN 'novice'
        WHEN RANDOM() < 0.5 THEN 'beginner'
        WHEN RANDOM() < 0.8 THEN 'intermediate'
        ELSE 'advanced'
    END
FROM users u
CROSS JOIN topics t
WHERE u.id IN (SELECT id FROM users LIMIT 3)
AND t.id IN (SELECT id FROM topics LIMIT 5);

INSERT INTO study_time_optimization (user_id, optimal_hour, optimal_day_of_week, productivity_score, focus_duration_minutes, break_duration_minutes, session_frequency_per_week, measurement_period_days)
SELECT 
    u.id,
    FLOOR(RANDOM() * 12 + 8), -- 8 AM to 8 PM
    FLOOR(RANDOM() * 7), -- 0-6 (Sunday-Saturday)
    ROUND((RANDOM() * 30 + 60)::numeric, 2),
    FLOOR(RANDOM() * 30 + 25), -- 25-55 minutes
    FLOOR(RANDOM() * 10 + 5), -- 5-15 minutes
    FLOOR(RANDOM() * 4 + 3), -- 3-7 sessions per week
    30
FROM users u
WHERE u.id IN (SELECT id FROM users LIMIT 3);

INSERT INTO burnout_risk (user_id, risk_level, risk_score, contributing_factors, study_intensity_score, rest_adequacy_score, stress_indicators, recommended_actions, last_assessment)
SELECT 
    u.id,
    CASE 
        WHEN RANDOM() < 0.1 THEN 'critical'
        WHEN RANDOM() < 0.3 THEN 'high'
        WHEN RANDOM() < 0.6 THEN 'medium'
        ELSE 'low'
    END,
    ROUND((RANDOM() * 40 + 20)::numeric, 2),
    ARRAY['long_study_sessions', 'insufficient_breaks', 'high_difficulty_topics'],
    ROUND((RANDOM() * 30 + 50)::numeric, 2),
    ROUND((RANDOM() * 40 + 40)::numeric, 2),
    ARRAY['fatigue', 'decreased_focus', 'irritability'],
    ARRAY['take_breaks', 'reduce_intensity', 'get_adequate_sleep'],
    NOW() - INTERVAL '1 day'
FROM users u
WHERE u.id IN (SELECT id FROM users LIMIT 3);
