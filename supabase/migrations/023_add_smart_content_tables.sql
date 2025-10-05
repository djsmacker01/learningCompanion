
CREATE TABLE IF NOT EXISTS generated_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    content_type VARCHAR(50) NOT NULL,
    content_subtype VARCHAR(50) NOT NULL,
    content_data JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Content Templates Table
CREATE TABLE IF NOT EXISTS content_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    template_name VARCHAR(100) NOT NULL,
    template_type VARCHAR(50) NOT NULL,
    template_data JSONB NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Content Generation History Table
CREATE TABLE IF NOT EXISTS content_generation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    generation_type VARCHAR(50) NOT NULL,
    generation_params JSONB,
    content_id UUID REFERENCES generated_content(id) ON DELETE SET NULL,
    generation_time_seconds INTEGER,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Content Ratings Table
CREATE TABLE IF NOT EXISTS content_ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content_id UUID NOT NULL REFERENCES generated_content(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, content_id)
);


CREATE TABLE IF NOT EXISTS content_usage_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL REFERENCES generated_content(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    usage_type VARCHAR(50) NOT NULL,
    usage_duration_seconds INTEGER,
    interaction_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE INDEX IF NOT EXISTS idx_generated_content_user_id ON generated_content(user_id);
CREATE INDEX IF NOT EXISTS idx_generated_content_topic_id ON generated_content(topic_id);
CREATE INDEX IF NOT EXISTS idx_generated_content_type ON generated_content(content_type);
CREATE INDEX IF NOT EXISTS idx_generated_content_active ON generated_content(is_active);
CREATE INDEX IF NOT EXISTS idx_generated_content_created_at ON generated_content(created_at);

CREATE INDEX IF NOT EXISTS idx_content_templates_type ON content_templates(template_type);
CREATE INDEX IF NOT EXISTS idx_content_templates_default ON content_templates(is_default);

CREATE INDEX IF NOT EXISTS idx_content_generation_history_user_id ON content_generation_history(user_id);
CREATE INDEX IF NOT EXISTS idx_content_generation_history_topic_id ON content_generation_history(topic_id);
CREATE INDEX IF NOT EXISTS idx_content_generation_history_type ON content_generation_history(generation_type);
CREATE INDEX IF NOT EXISTS idx_content_generation_history_success ON content_generation_history(success);

CREATE INDEX IF NOT EXISTS idx_content_ratings_content_id ON content_ratings(content_id);
CREATE INDEX IF NOT EXISTS idx_content_ratings_user_id ON content_ratings(user_id);
CREATE INDEX IF NOT EXISTS idx_content_ratings_rating ON content_ratings(rating);

CREATE INDEX IF NOT EXISTS idx_content_usage_analytics_content_id ON content_usage_analytics(content_id);
CREATE INDEX IF NOT EXISTS idx_content_usage_analytics_user_id ON content_usage_analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_content_usage_analytics_type ON content_usage_analytics(usage_type);


ALTER TABLE generated_content ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_generation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_ratings ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_usage_analytics ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view their own generated content" ON generated_content
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own generated content" ON generated_content
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own generated content" ON generated_content
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own generated content" ON generated_content
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Everyone can view content templates" ON content_templates
    FOR SELECT USING (true);

CREATE POLICY "Users can view their own content generation history" ON content_generation_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own content generation history" ON content_generation_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own content ratings" ON content_ratings
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own content ratings" ON content_ratings
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own content ratings" ON content_ratings
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view their own content usage analytics" ON content_usage_analytics
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own content usage analytics" ON content_usage_analytics
    FOR INSERT WITH CHECK (auth.uid() = user_id);


GRANT ALL ON generated_content TO authenticated;
GRANT ALL ON content_templates TO authenticated;
GRANT ALL ON content_generation_history TO authenticated;
GRANT ALL ON content_ratings TO authenticated;
GRANT ALL ON content_usage_analytics TO authenticated;


INSERT INTO content_templates (template_name, template_type, template_data, is_default) VALUES
('Comprehensive Study Notes', 'study_notes', '{"sections": ["introduction", "key_concepts", "examples", "practice_questions"], "format": "structured"}', true),
('Quick Summary', 'summary', '{"sections": ["overview", "key_points", "quick_facts"], "format": "bullet_points"}', true),
('Interactive Quiz', 'interactive_content', '{"question_types": ["multiple_choice", "true_false", "fill_blank"], "difficulty": "adaptive"}', true),
('Mind Map', 'visual_aids', '{"layout": "radial", "elements": ["central_concept", "main_branches", "sub_branches"], "style": "color_coded"}', true),
('Learning Path', 'learning_path', '{"steps": ["foundation", "practice", "application", "assessment"], "progression": "gradual"}', true)
ON CONFLICT DO NOTHING;
