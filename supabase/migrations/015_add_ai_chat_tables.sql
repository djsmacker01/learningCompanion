
-- AI Conversations table
CREATE TABLE IF NOT EXISTS ai_conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS ai_chat_settings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    response_style VARCHAR(20) DEFAULT 'detailed' CHECK (response_style IN ('detailed', 'concise', 'beginner', 'advanced')),
    context_length VARCHAR(20) DEFAULT 'medium' CHECK (context_length IN ('short', 'medium', 'long')),
    include_examples BOOLEAN DEFAULT TRUE,
    auto_save_conversations BOOLEAN DEFAULT TRUE,
    preferred_model VARCHAR(50) DEFAULT 'gpt-3.5-turbo',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- AI Chat Templates table
CREATE TABLE IF NOT EXISTS ai_chat_templates (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    template_type VARCHAR(50) NOT NULL CHECK (template_type IN ('summarize', 'explain', 'questions', 'study_guide', 'custom')),
    content TEXT NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT check_user_or_public CHECK (
        (user_id IS NOT NULL AND is_public = FALSE) OR 
        (user_id IS NULL AND is_public = TRUE)
    )
);

-- AI Chat Analytics table
CREATE TABLE IF NOT EXISTS ai_chat_analytics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES ai_conversations(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    interaction_type VARCHAR(50) NOT NULL CHECK (interaction_type IN ('chat', 'summarize', 'explain', 'questions', 'study_guide')),
    tokens_used INTEGER DEFAULT 0,
    response_time_ms INTEGER DEFAULT 0,
    user_satisfaction INTEGER CHECK (user_satisfaction >= 1 AND user_satisfaction <= 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_ai_conversations_user_id ON ai_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_conversations_topic_id ON ai_conversations(topic_id);
CREATE INDEX IF NOT EXISTS idx_ai_conversations_created_at ON ai_conversations(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_ai_chat_settings_user_id ON ai_chat_settings(user_id);

CREATE INDEX IF NOT EXISTS idx_ai_chat_templates_user_id ON ai_chat_templates(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_chat_templates_type ON ai_chat_templates(template_type);
CREATE INDEX IF NOT EXISTS idx_ai_chat_templates_public ON ai_chat_templates(is_public);

CREATE INDEX IF NOT EXISTS idx_ai_chat_analytics_user_id ON ai_chat_analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_chat_analytics_conversation_id ON ai_chat_analytics(conversation_id);
CREATE INDEX IF NOT EXISTS idx_ai_chat_analytics_topic_id ON ai_chat_analytics(topic_id);
CREATE INDEX IF NOT EXISTS idx_ai_chat_analytics_type ON ai_chat_analytics(interaction_type);

-- Enable Row Level Security (RLS)
ALTER TABLE ai_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_chat_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_chat_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_chat_analytics ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
-- AI Conversations policies
CREATE POLICY "Users can view their own conversations" ON ai_conversations
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own conversations" ON ai_conversations
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own conversations" ON ai_conversations
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own conversations" ON ai_conversations
    FOR DELETE USING (auth.uid() = user_id);

-- AI Chat Settings policies
CREATE POLICY "Users can view their own settings" ON ai_chat_settings
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own settings" ON ai_chat_settings
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own settings" ON ai_chat_settings
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own settings" ON ai_chat_settings
    FOR DELETE USING (auth.uid() = user_id);

-- AI Chat Templates policies
CREATE POLICY "Users can view their own templates and public templates" ON ai_chat_templates
    FOR SELECT USING (auth.uid() = user_id OR is_public = TRUE);

CREATE POLICY "Users can insert their own templates" ON ai_chat_templates
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own templates" ON ai_chat_templates
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own templates" ON ai_chat_templates
    FOR DELETE USING (auth.uid() = user_id);


CREATE POLICY "Users can view their own analytics" ON ai_chat_analytics
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own analytics" ON ai_chat_analytics
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own analytics" ON ai_chat_analytics
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own analytics" ON ai_chat_analytics
    FOR DELETE USING (auth.uid() = user_id);


CREATE OR REPLACE FUNCTION get_user_ai_conversations(p_user_id UUID, p_limit INTEGER DEFAULT 50)
RETURNS TABLE (
    id UUID,
    user_message TEXT,
    ai_response TEXT,
    topic_id UUID,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ac.id,
        ac.user_message,
        ac.ai_response,
        ac.topic_id,
        ac.created_at
    FROM ai_conversations ac
    WHERE ac.user_id = p_user_id
    ORDER BY ac.created_at DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION get_ai_chat_stats(p_user_id UUID)
RETURNS TABLE (
    total_conversations BIGINT,
    total_tokens_used BIGINT,
    avg_response_time NUMERIC,
    most_used_topic_id UUID,
    most_used_topic_title TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(ac.id) as total_conversations,
        COALESCE(SUM(aca.tokens_used), 0) as total_tokens_used,
        COALESCE(AVG(aca.response_time_ms), 0) as avg_response_time,
        ac.topic_id as most_used_topic_id,
        t.title as most_used_topic_title
    FROM ai_conversations ac
    LEFT JOIN ai_chat_analytics aca ON ac.id = aca.conversation_id
    LEFT JOIN topics t ON ac.topic_id = t.id
    WHERE ac.user_id = p_user_id
    GROUP BY ac.topic_id, t.title
    ORDER BY COUNT(ac.id) DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_ai_conversations_updated_at
    BEFORE UPDATE ON ai_conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_chat_settings_updated_at
    BEFORE UPDATE ON ai_chat_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_chat_templates_updated_at
    BEFORE UPDATE ON ai_chat_templates
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert default AI chat settings for existing users
INSERT INTO ai_chat_settings (user_id, response_style, context_length, include_examples, auto_save_conversations)
SELECT 
    u.id,
    'detailed',
    'medium',
    TRUE,
    TRUE
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM ai_chat_settings acs WHERE acs.user_id = u.id
);

-- Insert some default public templates
INSERT INTO ai_chat_templates (user_id, name, template_type, content, is_public)
VALUES 
    (NULL, 'Summarize Key Points', 'summarize', 'Please summarize the key points of this topic in a clear and concise way.', TRUE),
    (NULL, 'Explain Concept', 'explain', 'Can you explain this concept in simple terms with examples?', TRUE),
    (NULL, 'Generate Study Questions', 'questions', 'Generate 5 practice questions for this topic with varying difficulty levels.', TRUE),
    (NULL, 'Create Study Guide', 'study_guide', 'Create a comprehensive study guide for this topic with main concepts, examples, and practice exercises.', TRUE);

-- Add comments for documentation
COMMENT ON TABLE ai_conversations IS 'Stores AI chat conversations between users and the AI assistant';
COMMENT ON TABLE ai_chat_settings IS 'Stores user preferences for AI chat functionality';
COMMENT ON TABLE ai_chat_templates IS 'Stores reusable chat templates for common AI interactions';
COMMENT ON TABLE ai_chat_analytics IS 'Stores analytics data for AI chat usage and performance';

COMMENT ON COLUMN ai_conversations.user_message IS 'The message sent by the user to the AI';
COMMENT ON COLUMN ai_conversations.ai_response IS 'The response generated by the AI';
COMMENT ON COLUMN ai_conversations.topic_id IS 'Optional reference to a topic if the conversation is topic-specific';

COMMENT ON COLUMN ai_chat_settings.response_style IS 'Preferred style of AI responses (detailed, concise, beginner, advanced)';
COMMENT ON COLUMN ai_chat_settings.context_length IS 'Preferred length of context to include (short, medium, long)';
COMMENT ON COLUMN ai_chat_settings.include_examples IS 'Whether to include examples in AI responses';
COMMENT ON COLUMN ai_chat_settings.preferred_model IS 'Preferred AI model to use for responses';

COMMENT ON COLUMN ai_chat_templates.template_type IS 'Type of template (summarize, explain, questions, study_guide, custom)';
COMMENT ON COLUMN ai_chat_templates.content IS 'The template content/prompt';
COMMENT ON COLUMN ai_chat_templates.is_public IS 'Whether the template is available to all users';

COMMENT ON COLUMN ai_chat_analytics.tokens_used IS 'Number of tokens used in the AI request';
COMMENT ON COLUMN ai_chat_analytics.response_time_ms IS 'Response time in milliseconds';
COMMENT ON COLUMN ai_chat_analytics.user_satisfaction IS 'User satisfaction rating (1-5)';
