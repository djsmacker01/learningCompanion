
CREATE TABLE IF NOT EXISTS topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    difficulty_level INTEGER NOT NULL DEFAULT 1,
    target_sessions_per_week INTEGER NOT NULL DEFAULT 3,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    color_tag VARCHAR(7) DEFAULT '#3B82F6',
    
    CONSTRAINT topics_difficulty_range CHECK (difficulty_level >= 1 AND difficulty_level <= 5),
    CONSTRAINT topics_sessions_per_week CHECK (target_sessions_per_week >= 1 AND target_sessions_per_week <= 14),
    CONSTRAINT topics_title_length CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 200),
    CONSTRAINT topics_color_format CHECK (color_tag ~* '^#[0-9A-Fa-f]{6}$')
);

CREATE INDEX IF NOT EXISTS idx_topics_user_id ON topics(user_id);
CREATE INDEX IF NOT EXISTS idx_topics_created_at ON topics(created_at);
CREATE INDEX IF NOT EXISTS idx_topics_is_active ON topics(is_active);
CREATE INDEX IF NOT EXISTS idx_topics_difficulty ON topics(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_topics_user_active ON topics(user_id, is_active);

ALTER TABLE topics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own topics" ON topics
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own topics" ON topics
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own topics" ON topics
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own topics" ON topics
    FOR DELETE USING (auth.uid() = user_id);

GRANT ALL ON topics TO authenticated;
