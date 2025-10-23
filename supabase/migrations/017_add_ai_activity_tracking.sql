
CREATE TABLE IF NOT EXISTS ai_activity (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL, 
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    activity_data JSONB, 
    result_summary TEXT, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE INDEX IF NOT EXISTS idx_ai_activity_user_id ON ai_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_activity_created_at ON ai_activity(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_activity_type ON ai_activity(activity_type);


CREATE OR REPLACE FUNCTION update_ai_activity_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_ai_activity_updated_at
    BEFORE UPDATE ON ai_activity
    FOR EACH ROW
    EXECUTE FUNCTION update_ai_activity_updated_at();


ALTER TABLE ai_activity ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view their own AI activity" ON ai_activity
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own AI activity" ON ai_activity
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own AI activity" ON ai_activity
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own AI activity" ON ai_activity
    FOR DELETE USING (auth.uid() = user_id);


INSERT INTO ai_activity (user_id, activity_type, topic_id, activity_data, result_summary)
SELECT 
    u.id,
    'concept_explanation',
    t.id,
    '{"concept": "Photosynthesis", "level": "intermediate"}'::jsonb,
    'Explained photosynthesis process and its importance in plant biology'
FROM users u
CROSS JOIN topics t
WHERE u.email = 'test@example.com'
LIMIT 1;

INSERT INTO ai_activity (user_id, activity_type, topic_id, activity_data, result_summary)
SELECT 
    u.id,
    'grade_prediction',
    t.id,
    '{"target_grade": "A", "current_performance": 75}'::jsonb,
    'Predicted grade A for Mathematics with 85% confidence'
FROM users u
CROSS JOIN topics t
WHERE u.email = 'test@example.com'
LIMIT 1;

INSERT INTO ai_activity (user_id, activity_type, topic_id, activity_data, result_summary)
SELECT 
    u.id,
    'study_plan',
    t.id,
    '{"time_available": 10, "target_grade": "A"}'::jsonb,
    'Generated 4-week study plan for Physics with daily practice schedule'
FROM users u
CROSS JOIN topics t
WHERE u.email = 'test@example.com'
LIMIT 1;
