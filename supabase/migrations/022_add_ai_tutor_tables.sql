-
CREATE TABLE IF NOT EXISTS ai_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recommendations JSONB NOT NULL,
    recommendation_type VARCHAR(50) DEFAULT 'general',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Study Plans Table
CREATE TABLE IF NOT EXISTS ai_study_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    study_plan JSONB NOT NULL,
    target_grade VARCHAR(10),
    time_available_minutes INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Explanations Table
CREATE TABLE IF NOT EXISTS ai_explanations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    concept VARCHAR(255) NOT NULL,
    explanation TEXT NOT NULL,
    explanation_level VARCHAR(20) DEFAULT 'intermediate',
    learning_style VARCHAR(20) DEFAULT 'visual',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Grade Predictions Table
CREATE TABLE IF NOT EXISTS ai_grade_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    predicted_grade VARCHAR(10) NOT NULL,
    confidence_score INTEGER CHECK (confidence_score >= 0 AND confidence_score <= 100),
    recommendations JSONB,
    performance_analysis JSONB,
    learning_velocity DECIMAL(5,2),
    exam_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Learning Styles Table
CREATE TABLE IF NOT EXISTS ai_learning_styles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    learning_style VARCHAR(50) NOT NULL,
    confidence_score INTEGER CHECK (confidence_score >= 0 AND confidence_score <= 100),
    recommendations JSONB,
    study_patterns JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- AI Tutor Conversations Table
CREATE TABLE IF NOT EXISTS ai_tutor_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conversation_id UUID NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    context JSONB,
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    message_type VARCHAR(50) DEFAULT 'general',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Adaptive Quiz Recommendations Table
CREATE TABLE IF NOT EXISTS ai_adaptive_quiz_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    recommendations JSONB NOT NULL,
    weak_areas JSONB,
    performance_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_user_id ON ai_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_type ON ai_recommendations(recommendation_type);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_created_at ON ai_recommendations(created_at);

CREATE INDEX IF NOT EXISTS idx_ai_study_plans_user_id ON ai_study_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_study_plans_topic_id ON ai_study_plans(topic_id);
CREATE INDEX IF NOT EXISTS idx_ai_study_plans_active ON ai_study_plans(is_active);

CREATE INDEX IF NOT EXISTS idx_ai_explanations_user_id ON ai_explanations(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_explanations_topic_id ON ai_explanations(topic_id);
CREATE INDEX IF NOT EXISTS idx_ai_explanations_concept ON ai_explanations(concept);

CREATE INDEX IF NOT EXISTS idx_ai_grade_predictions_user_id ON ai_grade_predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_grade_predictions_topic_id ON ai_grade_predictions(topic_id);
CREATE INDEX IF NOT EXISTS idx_ai_grade_predictions_exam_date ON ai_grade_predictions(exam_date);

CREATE INDEX IF NOT EXISTS idx_ai_learning_styles_user_id ON ai_learning_styles(user_id);

CREATE INDEX IF NOT EXISTS idx_ai_tutor_conversations_user_id ON ai_tutor_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_tutor_conversations_conversation_id ON ai_tutor_conversations(conversation_id);
CREATE INDEX IF NOT EXISTS idx_ai_tutor_conversations_created_at ON ai_tutor_conversations(created_at);

CREATE INDEX IF NOT EXISTS idx_ai_adaptive_quiz_user_id ON ai_adaptive_quiz_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_adaptive_quiz_topic_id ON ai_adaptive_quiz_recommendations(topic_id);

-- Enable RLS
ALTER TABLE ai_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_study_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_explanations ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_grade_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_learning_styles ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_tutor_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_adaptive_quiz_recommendations ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view their own AI recommendations" ON ai_recommendations
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own AI recommendations" ON ai_recommendations
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own study plans" ON ai_study_plans
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own study plans" ON ai_study_plans
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own study plans" ON ai_study_plans
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view their own explanations" ON ai_explanations
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own explanations" ON ai_explanations
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own grade predictions" ON ai_grade_predictions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own grade predictions" ON ai_grade_predictions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own grade predictions" ON ai_grade_predictions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view their own learning styles" ON ai_learning_styles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own learning styles" ON ai_learning_styles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own learning styles" ON ai_learning_styles
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view their own tutor conversations" ON ai_tutor_conversations
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own tutor conversations" ON ai_tutor_conversations
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own adaptive quiz recommendations" ON ai_adaptive_quiz_recommendations
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own adaptive quiz recommendations" ON ai_adaptive_quiz_recommendations
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Grant permissions
GRANT ALL ON ai_recommendations TO authenticated;
GRANT ALL ON ai_study_plans TO authenticated;
GRANT ALL ON ai_explanations TO authenticated;
GRANT ALL ON ai_grade_predictions TO authenticated;
GRANT ALL ON ai_learning_styles TO authenticated;
GRANT ALL ON ai_tutor_conversations TO authenticated;
GRANT ALL ON ai_adaptive_quiz_recommendations TO authenticated;
