
CREATE TABLE IF NOT EXISTS study_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_date DATE NOT NULL DEFAULT CURRENT_DATE,
    duration_minutes INTEGER NOT NULL DEFAULT 0,
    confidence_before INTEGER NOT NULL DEFAULT 5,
    confidence_after INTEGER NOT NULL DEFAULT 5,
    notes TEXT,
    session_type VARCHAR(50) DEFAULT 'study',
    completed BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    
    CONSTRAINT sessions_confidence_before_range CHECK (confidence_before >= 1 AND confidence_before <= 10),
    CONSTRAINT sessions_confidence_after_range CHECK (confidence_after >= 1 AND confidence_after <= 10),
    CONSTRAINT sessions_duration_positive CHECK (duration_minutes >= 0),
    CONSTRAINT sessions_type_valid CHECK (session_type IN ('study', 'review', 'practice', 'quiz', 'other'))
);


CREATE INDEX IF NOT EXISTS idx_sessions_topic_id ON study_sessions(topic_id);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON study_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_date ON study_sessions(session_date);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON study_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_sessions_user_topic ON study_sessions(user_id, topic_id);
CREATE INDEX IF NOT EXISTS idx_sessions_user_date ON study_sessions(user_id, session_date);
CREATE INDEX IF NOT EXISTS idx_sessions_completed ON study_sessions(completed);


ALTER TABLE study_sessions ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view own sessions" ON study_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions" ON study_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sessions" ON study_sessions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own sessions" ON study_sessions
    FOR DELETE USING (auth.uid() = user_id);


CREATE OR REPLACE FUNCTION public.set_session_user_id()
RETURNS TRIGGER AS $$
BEGIN
    
    SELECT user_id INTO NEW.user_id
    FROM topics
    WHERE id = NEW.topic_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS set_session_user_id_trigger ON study_sessions;
CREATE TRIGGER set_session_user_id_trigger
    BEFORE INSERT ON study_sessions
    FOR EACH ROW EXECUTE FUNCTION public.set_session_user_id();


GRANT ALL ON study_sessions TO authenticated;
