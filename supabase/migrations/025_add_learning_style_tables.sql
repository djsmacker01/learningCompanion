
CREATE TABLE IF NOT EXISTS learning_style_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    primary_learning_style VARCHAR(50) NOT NULL,
    secondary_learning_styles JSONB,
    behavioral_patterns JSONB NOT NULL,
    confidence_scores JSONB NOT NULL,
    recommendations JSONB NOT NULL,
    assessment_data JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Adaptive Learning Paths Table
CREATE TABLE IF NOT EXISTS adaptive_learning_paths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    current_level VARCHAR(50) NOT NULL,
    target_level VARCHAR(50) NOT NULL,
    learning_style VARCHAR(50) NOT NULL,
    learning_gaps JSONB NOT NULL,
    learning_modules JSONB NOT NULL,
    adaptive_progression JSONB NOT NULL,
    personalized_assessments JSONB NOT NULL,
    learning_milestones JSONB NOT NULL,
    estimated_completion_time VARCHAR(50),
    completion_percentage DECIMAL(5,2) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Personalized Content Delivery Table
CREATE TABLE IF NOT EXISTS personalized_content_delivery (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content_id UUID NOT NULL,
    original_content JSONB NOT NULL,
    adapted_content JSONB NOT NULL,
    content_analysis JSONB NOT NULL,
    delivery_timing JSONB NOT NULL,
    interactive_elements JSONB NOT NULL,
    comprehension_checks JSONB NOT NULL,
    reinforcement_activities JSONB NOT NULL,
    personalization_score DECIMAL(5,2) NOT NULL,
    learning_style VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Learning Progress Analysis Table
CREATE TABLE IF NOT EXISTS learning_progress_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    time_period VARCHAR(50) NOT NULL,
    learning_data JSONB NOT NULL,
    progress_patterns JSONB NOT NULL,
    style_evolution JSONB NOT NULL,
    learning_velocity DECIMAL(5,2) NOT NULL,
    optimization_opportunities JSONB NOT NULL,
    progress_insights JSONB NOT NULL,
    improvement_recommendations JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Intelligent Study Schedules Table
CREATE TABLE IF NOT EXISTS intelligent_study_schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    learning_style VARCHAR(50) NOT NULL,
    available_time JSONB NOT NULL,
    subjects JSONB NOT NULL,
    priorities JSONB NOT NULL,
    optimal_times JSONB NOT NULL,
    subject_schedules JSONB NOT NULL,
    optimized_sessions JSONB NOT NULL,
    break_recommendations JSONB NOT NULL,
    intensity_patterns JSONB NOT NULL,
    revision_schedule JSONB NOT NULL,
    motivation_triggers JSONB NOT NULL,
    schedule_effectiveness_score DECIMAL(5,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Learning Insights Table
CREATE TABLE IF NOT EXISTS learning_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    analysis_depth VARCHAR(50) NOT NULL,
    learning_patterns JSONB NOT NULL,
    learning_preferences JSONB NOT NULL,
    strengths_weaknesses JSONB NOT NULL,
    learning_efficiency JSONB NOT NULL,
    personalized_insights JSONB NOT NULL,
    action_plan JSONB NOT NULL,
    success_predictions JSONB NOT NULL,
    insights_confidence DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Learning Style Assessments Table
CREATE TABLE IF NOT EXISTS learning_style_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assessment_type VARCHAR(50) NOT NULL,
    assessment_responses JSONB NOT NULL,
    style_scores JSONB NOT NULL,
    primary_learning_style VARCHAR(50) NOT NULL,
    secondary_learning_styles JSONB,
    assessment_confidence DECIMAL(5,2) NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Adaptive Learning Modules Table
CREATE TABLE IF NOT EXISTS adaptive_learning_modules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    learning_path_id UUID NOT NULL REFERENCES adaptive_learning_paths(id) ON DELETE CASCADE,
    module_name VARCHAR(200) NOT NULL,
    module_type VARCHAR(50) NOT NULL,
    difficulty_level VARCHAR(50) NOT NULL,
    learning_objectives JSONB NOT NULL,
    content_data JSONB NOT NULL,
    assessment_criteria JSONB NOT NULL,
    completion_requirements JSONB NOT NULL,
    estimated_time_minutes INTEGER NOT NULL,
    prerequisites JSONB,
    learning_style_adaptations JSONB NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    completion_percentage DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Learning Analytics Table
CREATE TABLE IF NOT EXISTS learning_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    analytics_type VARCHAR(50) NOT NULL,
    analytics_data JSONB NOT NULL,
    performance_metrics JSONB NOT NULL,
    learning_efficiency_score DECIMAL(5,2) NOT NULL,
    improvement_suggestions JSONB NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_learning_style_profiles_user_id ON learning_style_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_style_profiles_primary_style ON learning_style_profiles(primary_learning_style);
CREATE INDEX IF NOT EXISTS idx_learning_style_profiles_active ON learning_style_profiles(is_active);

CREATE INDEX IF NOT EXISTS idx_adaptive_learning_paths_user_id ON adaptive_learning_paths(user_id);
CREATE INDEX IF NOT EXISTS idx_adaptive_learning_paths_subject ON adaptive_learning_paths(subject);
CREATE INDEX IF NOT EXISTS idx_adaptive_learning_paths_learning_style ON adaptive_learning_paths(learning_style);
CREATE INDEX IF NOT EXISTS idx_adaptive_learning_paths_active ON adaptive_learning_paths(is_active);

CREATE INDEX IF NOT EXISTS idx_personalized_content_delivery_user_id ON personalized_content_delivery(user_id);
CREATE INDEX IF NOT EXISTS idx_personalized_content_delivery_content_id ON personalized_content_delivery(content_id);
CREATE INDEX IF NOT EXISTS idx_personalized_content_delivery_learning_style ON personalized_content_delivery(learning_style);

CREATE INDEX IF NOT EXISTS idx_learning_progress_analysis_user_id ON learning_progress_analysis(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_progress_analysis_time_period ON learning_progress_analysis(time_period);

CREATE INDEX IF NOT EXISTS idx_intelligent_study_schedules_user_id ON intelligent_study_schedules(user_id);
CREATE INDEX IF NOT EXISTS idx_intelligent_study_schedules_learning_style ON intelligent_study_schedules(learning_style);
CREATE INDEX IF NOT EXISTS idx_intelligent_study_schedules_active ON intelligent_study_schedules(is_active);

CREATE INDEX IF NOT EXISTS idx_learning_insights_user_id ON learning_insights(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_insights_analysis_depth ON learning_insights(analysis_depth);

CREATE INDEX IF NOT EXISTS idx_learning_style_assessments_user_id ON learning_style_assessments(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_style_assessments_primary_style ON learning_style_assessments(primary_learning_style);
CREATE INDEX IF NOT EXISTS idx_learning_style_assessments_completed_at ON learning_style_assessments(completed_at);

CREATE INDEX IF NOT EXISTS idx_adaptive_learning_modules_learning_path_id ON adaptive_learning_modules(learning_path_id);
CREATE INDEX IF NOT EXISTS idx_adaptive_learning_modules_module_type ON adaptive_learning_modules(module_type);
CREATE INDEX IF NOT EXISTS idx_adaptive_learning_modules_difficulty_level ON adaptive_learning_modules(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_adaptive_learning_modules_completed ON adaptive_learning_modules(is_completed);

CREATE INDEX IF NOT EXISTS idx_learning_analytics_user_id ON learning_analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_analytics_type ON learning_analytics(analytics_type);
CREATE INDEX IF NOT EXISTS idx_learning_analytics_generated_at ON learning_analytics(generated_at);

-- Enable RLS
ALTER TABLE learning_style_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE adaptive_learning_paths ENABLE ROW LEVEL SECURITY;
ALTER TABLE personalized_content_delivery ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_progress_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE intelligent_study_schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_style_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE adaptive_learning_modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_analytics ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
-- Note: Using more permissive policies for initial setup - can be tightened later
CREATE POLICY "Enable read access for all users" ON learning_style_profiles
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON learning_style_profiles
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update for all users" ON learning_style_profiles
    FOR UPDATE USING (true);

CREATE POLICY "Enable delete for all users" ON learning_style_profiles
    FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON adaptive_learning_paths
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON adaptive_learning_paths
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update for all users" ON adaptive_learning_paths
    FOR UPDATE USING (true);

CREATE POLICY "Enable delete for all users" ON adaptive_learning_paths
    FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON personalized_content_delivery
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON personalized_content_delivery
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON learning_progress_analysis
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON learning_progress_analysis
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON intelligent_study_schedules
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON intelligent_study_schedules
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update for all users" ON intelligent_study_schedules
    FOR UPDATE USING (true);

CREATE POLICY "Enable delete for all users" ON intelligent_study_schedules
    FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON learning_insights
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON learning_insights
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON learning_style_assessments
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON learning_style_assessments
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON adaptive_learning_modules
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON adaptive_learning_modules
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update for all users" ON adaptive_learning_modules
    FOR UPDATE USING (true);

CREATE POLICY "Enable read access for all users" ON learning_analytics
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON learning_analytics
    FOR INSERT WITH CHECK (true);

-- Grant permissions
GRANT ALL ON learning_style_profiles TO authenticated;
GRANT ALL ON adaptive_learning_paths TO authenticated;
GRANT ALL ON personalized_content_delivery TO authenticated;
GRANT ALL ON learning_progress_analysis TO authenticated;
GRANT ALL ON intelligent_study_schedules TO authenticated;
GRANT ALL ON learning_insights TO authenticated;
GRANT ALL ON learning_style_assessments TO authenticated;
GRANT ALL ON adaptive_learning_modules TO authenticated;
GRANT ALL ON learning_analytics TO authenticated;

-- Note: Sample data can be inserted manually after migration if needed
-- INSERT INTO learning_style_assessments (user_id, assessment_type, assessment_responses, style_scores, primary_learning_style, secondary_learning_styles, assessment_confidence) VALUES
-- ('00000000-0000-0000-0000-000000000000', 'comprehensive', 
--  '{"answers": [{"question_id": 1, "style": "visual"}, {"question_id": 2, "style": "visual"}, {"question_id": 3, "style": "kinesthetic"}]}', 
--  '{"visual": 2, "auditory": 0, "kinesthetic": 1, "reading_writing": 0}', 
--  'visual', '["kinesthetic", "auditory"]', 85.5)
-- ON CONFLICT DO NOTHING;
