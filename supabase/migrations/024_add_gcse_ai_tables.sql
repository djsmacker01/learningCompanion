
CREATE TABLE IF NOT EXISTS gcse_study_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    exam_board VARCHAR(50) NOT NULL,
    target_grade VARCHAR(10) NOT NULL,
    study_plan JSONB NOT NULL,
    exam_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_curriculum (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject VARCHAR(100) NOT NULL,
    exam_board VARCHAR(50) NOT NULL,
    topic_name VARCHAR(200) NOT NULL,
    topic_code VARCHAR(50),
    assessment_objectives JSONB,
    grade_descriptors JSONB,
    exam_weight DECIMAL(5,2) DEFAULT 1.0,
    difficulty_level VARCHAR(20) DEFAULT 'intermediate',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_past_paper_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    exam_board VARCHAR(50) NOT NULL,
    analysis_type VARCHAR(50) NOT NULL,
    analysis_data JSONB NOT NULL,
    question_patterns JSONB,
    topic_importance JSONB,
    exam_strategies JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_grade_boundary_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    exam_board VARCHAR(50) NOT NULL,
    current_performance JSONB NOT NULL,
    predicted_boundaries JSONB NOT NULL,
    predicted_grade VARCHAR(10) NOT NULL,
    improvement_plan JSONB,
    prediction_confidence DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_revision_schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subjects JSONB NOT NULL,
    exam_dates JSONB NOT NULL,
    target_grades JSONB NOT NULL,
    daily_schedule JSONB NOT NULL,
    subject_plans JSONB NOT NULL,
    wellbeing_plan JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_exam_techniques (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    exam_board VARCHAR(50) NOT NULL,
    exam_format JSONB NOT NULL,
    question_techniques JSONB NOT NULL,
    time_management JSONB NOT NULL,
    marking_insights JSONB NOT NULL,
    mistake_avoidance JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_performance_gap_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    curriculum_standards JSONB NOT NULL,
    performance_gaps JSONB NOT NULL,
    prioritized_gaps JSONB NOT NULL,
    improvement_strategies JSONB NOT NULL,
    practice_recommendations JSONB NOT NULL,
    progress_tracking JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_personalized_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    topic VARCHAR(200) NOT NULL,
    learning_style VARCHAR(50) NOT NULL,
    difficulty_level VARCHAR(50) NOT NULL,
    curriculum_requirements JSONB NOT NULL,
    content_data JSONB NOT NULL,
    exam_prep_elements JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_grade_boundaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject VARCHAR(100) NOT NULL,
    exam_board VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    grade_9_boundary INTEGER,
    grade_8_boundary INTEGER,
    grade_7_boundary INTEGER,
    grade_6_boundary INTEGER,
    grade_5_boundary INTEGER,
    grade_4_boundary INTEGER,
    grade_3_boundary INTEGER,
    grade_2_boundary INTEGER,
    grade_1_boundary INTEGER,
    max_mark INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE INDEX IF NOT EXISTS idx_gcse_study_plans_user_id ON gcse_study_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_study_plans_subject ON gcse_study_plans(subject);
CREATE INDEX IF NOT EXISTS idx_gcse_study_plans_exam_board ON gcse_study_plans(exam_board);
CREATE INDEX IF NOT EXISTS idx_gcse_study_plans_active ON gcse_study_plans(is_active);

CREATE INDEX IF NOT EXISTS idx_gcse_curriculum_subject ON gcse_curriculum(subject);
CREATE INDEX IF NOT EXISTS idx_gcse_curriculum_exam_board ON gcse_curriculum(exam_board);
CREATE INDEX IF NOT EXISTS idx_gcse_curriculum_topic ON gcse_curriculum(topic_name);
CREATE INDEX IF NOT EXISTS idx_gcse_curriculum_active ON gcse_curriculum(is_active);

CREATE INDEX IF NOT EXISTS idx_gcse_past_paper_analysis_user_id ON gcse_past_paper_analysis(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_past_paper_analysis_subject ON gcse_past_paper_analysis(subject);
CREATE INDEX IF NOT EXISTS idx_gcse_past_paper_analysis_type ON gcse_past_paper_analysis(analysis_type);

CREATE INDEX IF NOT EXISTS idx_gcse_grade_boundary_predictions_user_id ON gcse_grade_boundary_predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_grade_boundary_predictions_subject ON gcse_grade_boundary_predictions(subject);
CREATE INDEX IF NOT EXISTS idx_gcse_grade_boundary_predictions_grade ON gcse_grade_boundary_predictions(predicted_grade);

CREATE INDEX IF NOT EXISTS idx_gcse_revision_schedules_user_id ON gcse_revision_schedules(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_revision_schedules_active ON gcse_revision_schedules(is_active);

CREATE INDEX IF NOT EXISTS idx_gcse_exam_techniques_user_id ON gcse_exam_techniques(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_exam_techniques_subject ON gcse_exam_techniques(subject);
CREATE INDEX IF NOT EXISTS idx_gcse_exam_techniques_exam_board ON gcse_exam_techniques(exam_board);

CREATE INDEX IF NOT EXISTS idx_gcse_performance_gap_analysis_user_id ON gcse_performance_gap_analysis(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_performance_gap_analysis_subject ON gcse_performance_gap_analysis(subject);

CREATE INDEX IF NOT EXISTS idx_gcse_personalized_content_user_id ON gcse_personalized_content(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_personalized_content_subject ON gcse_personalized_content(subject);
CREATE INDEX IF NOT EXISTS idx_gcse_personalized_content_topic ON gcse_personalized_content(topic);
CREATE INDEX IF NOT EXISTS idx_gcse_personalized_content_active ON gcse_personalized_content(is_active);

CREATE INDEX IF NOT EXISTS idx_gcse_grade_boundaries_subject ON gcse_grade_boundaries(subject);
CREATE INDEX IF NOT EXISTS idx_gcse_grade_boundaries_exam_board ON gcse_grade_boundaries(exam_board);
CREATE INDEX IF NOT EXISTS idx_gcse_grade_boundaries_year ON gcse_grade_boundaries(year);


ALTER TABLE gcse_study_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_curriculum ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_past_paper_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_grade_boundary_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_revision_schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_exam_techniques ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_performance_gap_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_personalized_content ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_grade_boundaries ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view their own GCSE study plans" ON gcse_study_plans
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own GCSE study plans" ON gcse_study_plans
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own GCSE study plans" ON gcse_study_plans
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own GCSE study plans" ON gcse_study_plans
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Everyone can view GCSE curriculum" ON gcse_curriculum
    FOR SELECT USING (true);

CREATE POLICY "Users can view their own GCSE past paper analysis" ON gcse_past_paper_analysis
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own GCSE past paper analysis" ON gcse_past_paper_analysis
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own GCSE grade boundary predictions" ON gcse_grade_boundary_predictions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own GCSE grade boundary predictions" ON gcse_grade_boundary_predictions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own GCSE revision schedules" ON gcse_revision_schedules
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own GCSE revision schedules" ON gcse_revision_schedules
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own GCSE revision schedules" ON gcse_revision_schedules
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own GCSE revision schedules" ON gcse_revision_schedules
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view their own GCSE exam techniques" ON gcse_exam_techniques
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own GCSE exam techniques" ON gcse_exam_techniques
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own GCSE performance gap analysis" ON gcse_performance_gap_analysis
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own GCSE performance gap analysis" ON gcse_performance_gap_analysis
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own GCSE personalized content" ON gcse_personalized_content
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own GCSE personalized content" ON gcse_personalized_content
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own GCSE personalized content" ON gcse_personalized_content
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own GCSE personalized content" ON gcse_personalized_content
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Everyone can view GCSE grade boundaries" ON gcse_grade_boundaries
    FOR SELECT USING (true);


GRANT ALL ON gcse_study_plans TO authenticated;
GRANT ALL ON gcse_curriculum TO authenticated;
GRANT ALL ON gcse_past_paper_analysis TO authenticated;
GRANT ALL ON gcse_grade_boundary_predictions TO authenticated;
GRANT ALL ON gcse_revision_schedules TO authenticated;
GRANT ALL ON gcse_exam_techniques TO authenticated;
GRANT ALL ON gcse_performance_gap_analysis TO authenticated;
GRANT ALL ON gcse_personalized_content TO authenticated;
GRANT ALL ON gcse_grade_boundaries TO authenticated;


INSERT INTO gcse_curriculum (subject, exam_board, topic_name, topic_code, assessment_objectives, grade_descriptors, exam_weight, difficulty_level) VALUES

('Mathematics', 'AQA', 'Algebra', 'A1', '{"AO1": "Use and apply standard techniques", "AO2": "Reason, interpret and communicate mathematically", "AO3": "Solve problems within mathematics"}', '{"Grade 9": "Solve complex multi-step problems", "Grade 7": "Solve standard problems with confidence", "Grade 5": "Apply basic techniques correctly"}', 25.0, 'intermediate'),
('Mathematics', 'AQA', 'Geometry', 'G1', '{"AO1": "Use and apply standard techniques", "AO2": "Reason, interpret and communicate mathematically", "AO3": "Solve problems within mathematics"}', '{"Grade 9": "Solve complex geometrical problems", "Grade 7": "Apply geometric reasoning", "Grade 5": "Use basic geometric concepts"}', 20.0, 'intermediate'),
('Mathematics', 'AQA', 'Number', 'N1', '{"AO1": "Use and apply standard techniques", "AO2": "Reason, interpret and communicate mathematically", "AO3": "Solve problems within mathematics"}', '{"Grade 9": "Work with complex number problems", "Grade 7": "Apply number concepts confidently", "Grade 5": "Use basic number operations"}', 15.0, 'beginner'),
('Mathematics', 'AQA', 'Statistics', 'S1', '{"AO1": "Use and apply standard techniques", "AO2": "Reason, interpret and communicate mathematically", "AO3": "Solve problems within mathematics"}', '{"Grade 9": "Analyze complex statistical data", "Grade 7": "Interpret statistical information", "Grade 5": "Calculate basic statistics"}', 15.0, 'intermediate'),


('English Language', 'AQA', 'Reading Comprehension', 'R1', '{"AO1": "Identify and interpret explicit and implicit information", "AO2": "Explain, comment on and analyze how writers use language", "AO3": "Compare writers ideas and perspectives", "AO4": "Evaluate texts critically"}', '{"Grade 9": "Sophisticated analysis of language and structure", "Grade 7": "Clear analysis with supporting evidence", "Grade 5": "Basic understanding with some analysis"}', 50.0, 'intermediate'),
('English Language', 'AQA', 'Creative Writing', 'W1', '{"AO5": "Communicate clearly, effectively and imaginatively", "AO6": "Use a range of vocabulary and sentence structures"}', '{"Grade 9": "Compelling and sophisticated writing", "Grade 7": "Clear and engaging writing", "Grade 5": "Competent writing with some flair"}', 50.0, 'intermediate'),


('Biology', 'AQA', 'Cell Biology', 'B1', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Deep understanding of complex biological processes", "Grade 7": "Good understanding of key concepts", "Grade 5": "Basic understanding of biological facts"}', 12.5, 'beginner'),
('Biology', 'AQA', 'Organisation', 'B2', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Complex analysis of biological systems", "Grade 7": "Clear understanding of biological organisation", "Grade 5": "Basic knowledge of biological structures"}', 12.5, 'beginner'),
('Biology', 'AQA', 'Infection and Response', 'B3', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Sophisticated understanding of immune responses", "Grade 7": "Good understanding of infection mechanisms", "Grade 5": "Basic knowledge of disease and immunity"}', 12.5, 'intermediate'),
('Biology', 'AQA', 'Bioenergetics', 'B4', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Complex understanding of energy transfer", "Grade 7": "Clear understanding of photosynthesis and respiration", "Grade 5": "Basic knowledge of energy processes"}', 12.5, 'intermediate'),


('Chemistry', 'AQA', 'Atomic Structure', 'C1', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Sophisticated understanding of atomic theory", "Grade 7": "Good understanding of atomic structure", "Grade 5": "Basic knowledge of atoms and elements"}', 10.0, 'beginner'),
('Chemistry', 'AQA', 'Bonding', 'C2', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Complex understanding of chemical bonding", "Grade 7": "Clear understanding of bonding types", "Grade 5": "Basic knowledge of chemical bonds"}', 15.0, 'intermediate'),
('Chemistry', 'AQA', 'Quantitative Chemistry', 'C3', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Complex calculations with confidence", "Grade 7": "Accurate chemical calculations", "Grade 5": "Basic chemical calculations"}', 20.0, 'advanced'),
('Chemistry', 'AQA', 'Chemical Changes', 'C4', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Sophisticated understanding of chemical reactions", "Grade 7": "Good understanding of reaction types", "Grade 5": "Basic knowledge of chemical changes"}', 20.0, 'intermediate'),


('Physics', 'AQA', 'Energy', 'P1', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Complex understanding of energy concepts", "Grade 7": "Clear understanding of energy transfer", "Grade 5": "Basic knowledge of energy types"}', 10.0, 'beginner'),
('Physics', 'AQA', 'Electricity', 'P2', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Sophisticated understanding of electrical circuits", "Grade 7": "Good understanding of electrical principles", "Grade 5": "Basic knowledge of electricity"}', 15.0, 'intermediate'),
('Physics', 'AQA', 'Particle Model', 'P3', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Complex understanding of particle behavior", "Grade 7": "Clear understanding of particle model", "Grade 5": "Basic knowledge of matter states"}', 10.0, 'beginner'),
('Physics', 'AQA', 'Atomic Structure', 'P4', '{"AO1": "Demonstrate knowledge and understanding", "AO2": "Apply knowledge and understanding", "AO3": "Analyze information and ideas"}', '{"Grade 9": "Sophisticated understanding of atomic physics", "Grade 7": "Good understanding of atomic structure", "Grade 5": "Basic knowledge of atoms and radiation"}', 15.0, 'intermediate')
ON CONFLICT DO NOTHING;


INSERT INTO gcse_grade_boundaries (subject, exam_board, year, grade_9_boundary, grade_8_boundary, grade_7_boundary, grade_6_boundary, grade_5_boundary, grade_4_boundary, grade_3_boundary, grade_2_boundary, grade_1_boundary, max_mark) VALUES
('Mathematics', 'AQA', 2023, 85, 75, 65, 55, 45, 35, 25, 15, 5, 240),
('Mathematics', 'AQA', 2022, 83, 73, 63, 53, 43, 33, 23, 13, 3, 240),
('Mathematics', 'AQA', 2021, 87, 77, 67, 57, 47, 37, 27, 17, 7, 240),
('English Language', 'AQA', 2023, 82, 72, 62, 52, 42, 32, 22, 12, 2, 160),
('English Language', 'AQA', 2022, 80, 70, 60, 50, 40, 30, 20, 10, 0, 160),
('English Language', 'AQA', 2021, 84, 74, 64, 54, 44, 34, 24, 14, 4, 160),
('Biology', 'AQA', 2023, 78, 68, 58, 48, 38, 28, 18, 8, 0, 200),
('Biology', 'AQA', 2022, 76, 66, 56, 46, 36, 26, 16, 6, 0, 200),
('Biology', 'AQA', 2021, 80, 70, 60, 50, 40, 30, 20, 10, 0, 200),
('Chemistry', 'AQA', 2023, 79, 69, 59, 49, 39, 29, 19, 9, 0, 200),
('Chemistry', 'AQA', 2022, 77, 67, 57, 47, 37, 27, 17, 7, 0, 200),
('Chemistry', 'AQA', 2021, 81, 71, 61, 51, 41, 31, 21, 11, 1, 200),
('Physics', 'AQA', 2023, 77, 67, 57, 47, 37, 27, 17, 7, 0, 200),
('Physics', 'AQA', 2022, 75, 65, 55, 45, 35, 25, 15, 5, 0, 200),
('Physics', 'AQA', 2021, 79, 69, 59, 49, 39, 29, 19, 9, 0, 200)
ON CONFLICT DO NOTHING;
