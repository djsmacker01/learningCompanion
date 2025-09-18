-- Migration: Create User Analytics Table
-- Description: Creates the user_analytics table for AI recommendations and progress tracking

-- Create user_analytics table
CREATE TABLE IF NOT EXISTS user_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    total_study_time INTEGER DEFAULT 0, -- in minutes
    total_sessions INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    average_confidence_gain DECIMAL(3,2) DEFAULT 0.00,
    last_session_date DATE,
    next_recommended_date DATE,
    mastery_level INTEGER DEFAULT 1,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure one analytics record per user-topic combination
    UNIQUE(user_id, topic_id),
    
    -- Constraints
    CONSTRAINT analytics_mastery_range CHECK (mastery_level >= 1 AND mastery_level <= 5),
    CONSTRAINT analytics_study_time_positive CHECK (total_study_time >= 0),
    CONSTRAINT analytics_sessions_positive CHECK (total_sessions >= 0),
    CONSTRAINT analytics_streak_positive CHECK (current_streak >= 0 AND longest_streak >= 0),
    CONSTRAINT analytics_confidence_gain_range CHECK (average_confidence_gain >= -9.00 AND average_confidence_gain <= 9.00)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON user_analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_topic_id ON user_analytics(topic_id);
CREATE INDEX IF NOT EXISTS idx_analytics_next_recommended ON user_analytics(next_recommended_date);
CREATE INDEX IF NOT EXISTS idx_analytics_mastery ON user_analytics(mastery_level);
CREATE INDEX IF NOT EXISTS idx_analytics_user_topic ON user_analytics(user_id, topic_id);
CREATE INDEX IF NOT EXISTS idx_analytics_updated_at ON user_analytics(updated_at);

-- Enable Row Level Security
ALTER TABLE user_analytics ENABLE ROW LEVEL SECURITY;

-- RLS Policies: Users can only access their own analytics
CREATE POLICY "Users can view own analytics" ON user_analytics
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own analytics" ON user_analytics
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own analytics" ON user_analytics
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own analytics" ON user_analytics
    FOR DELETE USING (auth.uid() = user_id);

-- Create function to update analytics when a session is created/updated
CREATE OR REPLACE FUNCTION public.update_user_analytics()
RETURNS TRIGGER AS $$
DECLARE
    confidence_gain INTEGER;
    current_analytics RECORD;
BEGIN
    -- Calculate confidence gain
    confidence_gain := NEW.confidence_after - NEW.confidence_before;
    
    -- Get current analytics for this user-topic combination
    SELECT * INTO current_analytics
    FROM user_analytics
    WHERE user_id = NEW.user_id AND topic_id = NEW.topic_id;
    
    IF current_analytics IS NULL THEN
        -- Create new analytics record
        INSERT INTO user_analytics (
            user_id, topic_id, total_study_time, total_sessions,
            current_streak, longest_streak, average_confidence_gain,
            last_session_date, next_recommended_date, mastery_level
        ) VALUES (
            NEW.user_id, NEW.topic_id, NEW.duration_minutes, 1,
            1, 1, confidence_gain,
            NEW.session_date, NEW.session_date + INTERVAL '1 day', 1
        );
    ELSE
        -- Update existing analytics
        UPDATE user_analytics SET
            total_study_time = total_study_time + NEW.duration_minutes,
            total_sessions = total_sessions + 1,
            current_streak = CASE 
                WHEN NEW.session_date = last_session_date + INTERVAL '1 day' 
                THEN current_streak + 1 
                ELSE 1 
            END,
            longest_streak = GREATEST(longest_streak, 
                CASE 
                    WHEN NEW.session_date = last_session_date + INTERVAL '1 day' 
                    THEN current_streak + 1 
                    ELSE 1 
                END),
            average_confidence_gain = (
                (average_confidence_gain * total_sessions + confidence_gain) / 
                (total_sessions + 1)
            ),
            last_session_date = NEW.session_date,
            next_recommended_date = NEW.session_date + INTERVAL '1 day',
            mastery_level = LEAST(5, GREATEST(1, 
                ROUND((total_sessions + 1) / 10.0) + 1
            )),
            updated_at = NOW()
        WHERE user_id = NEW.user_id AND topic_id = NEW.topic_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to update analytics on session insert
DROP TRIGGER IF EXISTS update_analytics_on_session_insert ON study_sessions;
CREATE TRIGGER update_analytics_on_session_insert
    AFTER INSERT ON study_sessions
    FOR EACH ROW EXECUTE FUNCTION public.update_user_analytics();

-- Grant necessary permissions
GRANT ALL ON user_analytics TO authenticated;
