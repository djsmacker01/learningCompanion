



CREATE TABLE IF NOT EXISTS gcse_subjects (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    exam_board VARCHAR(20) NOT NULL,
    specification_code VARCHAR(20),
    subject_code VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_topics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    subject_id UUID REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    topic_name VARCHAR(200) NOT NULL,
    topic_number VARCHAR(10),
    topic_description TEXT,
    learning_objectives JSONB,
    exam_weight DECIMAL(5,2),
    difficulty_level VARCHAR(20) DEFAULT 'Both',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_exams (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    subject_id UUID REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    exam_name VARCHAR(200) NOT NULL,
    exam_date DATE NOT NULL,
    paper_number INTEGER,
    duration_minutes INTEGER,
    total_marks INTEGER,
    exam_board VARCHAR(20),
    specification_code VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_past_papers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    subject_id UUID REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    paper_title VARCHAR(200) NOT NULL,
    exam_year INTEGER NOT NULL,
    exam_month VARCHAR(10) NOT NULL,
    paper_number INTEGER,
    exam_board VARCHAR(20) NOT NULL,
    specification_code VARCHAR(20),
    difficulty_level VARCHAR(20) DEFAULT 'Both',
    total_marks INTEGER,
    duration_minutes INTEGER,
    file_url TEXT,
    mark_scheme_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_past_paper_questions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    past_paper_id UUID REFERENCES gcse_past_papers(id) ON DELETE CASCADE,
    question_number VARCHAR(10) NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50),
    marks INTEGER NOT NULL,
    difficulty_level VARCHAR(20) DEFAULT 'Both',
    topic_tags JSONB,
    correct_answer TEXT,
    mark_scheme TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_grade_boundaries (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    exam_board VARCHAR(20) NOT NULL,
    subject_code VARCHAR(20) NOT NULL,
    exam_year INTEGER NOT NULL,
    exam_month VARCHAR(10) NOT NULL,
    tier VARCHAR(20),
    grade VARCHAR(5) NOT NULL,
    raw_mark INTEGER NOT NULL,
    percentage_mark DECIMAL(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_performance (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subject_id UUID REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES gcse_topics(id) ON DELETE CASCADE,
    performance_type VARCHAR(50) NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    total_marks INTEGER NOT NULL,
    achieved_marks INTEGER NOT NULL,
    grade VARCHAR(5),
    difficulty_level VARCHAR(20) DEFAULT 'Both',
    time_taken_minutes INTEGER,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_study_plans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subject_id UUID REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    plan_name VARCHAR(200) NOT NULL,
    plan_description TEXT,
    target_grade VARCHAR(5) NOT NULL,
    current_grade VARCHAR(5),
    exam_date DATE NOT NULL,
    study_hours_per_week INTEGER DEFAULT 5,
    plan_status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS gcse_study_plan_steps (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    study_plan_id UUID REFERENCES gcse_study_plans(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES gcse_topics(id) ON DELETE CASCADE,
    step_order INTEGER NOT NULL,
    step_name VARCHAR(200) NOT NULL,
    step_description TEXT,
    estimated_hours INTEGER DEFAULT 2,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    due_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


ALTER TABLE topics ADD COLUMN IF NOT EXISTS is_gcse BOOLEAN DEFAULT FALSE;
ALTER TABLE topics ADD COLUMN IF NOT EXISTS gcse_subject_id UUID REFERENCES gcse_subjects(id);
ALTER TABLE topics ADD COLUMN IF NOT EXISTS gcse_topic_id UUID REFERENCES gcse_topics(id);
ALTER TABLE topics ADD COLUMN IF NOT EXISTS gcse_exam_board VARCHAR(20);
ALTER TABLE topics ADD COLUMN IF NOT EXISTS gcse_specification_code VARCHAR(20);
ALTER TABLE topics ADD COLUMN IF NOT EXISTS exam_weight INTEGER DEFAULT 1;


ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS is_gcse BOOLEAN DEFAULT FALSE;
ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS gcse_subject_id UUID REFERENCES gcse_subjects(id);
ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS gcse_topic_id UUID REFERENCES gcse_topics(id);
ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS past_paper_id UUID REFERENCES gcse_past_papers(id);
ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS exam_year INTEGER;
ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS exam_month VARCHAR(10);
ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS paper_number INTEGER;


CREATE INDEX IF NOT EXISTS idx_gcse_subjects_exam_board ON gcse_subjects(exam_board);
CREATE INDEX IF NOT EXISTS idx_gcse_subjects_specification ON gcse_subjects(specification_code);
CREATE INDEX IF NOT EXISTS idx_gcse_topics_subject_id ON gcse_topics(subject_id);
CREATE INDEX IF NOT EXISTS idx_gcse_topics_difficulty ON gcse_topics(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_gcse_exams_subject_id ON gcse_exams(subject_id);
CREATE INDEX IF NOT EXISTS idx_gcse_exams_exam_date ON gcse_exams(exam_date);
CREATE INDEX IF NOT EXISTS idx_gcse_past_papers_subject_id ON gcse_past_papers(subject_id);
CREATE INDEX IF NOT EXISTS idx_gcse_past_papers_year ON gcse_past_papers(exam_year);
CREATE INDEX IF NOT EXISTS idx_gcse_past_paper_questions_paper_id ON gcse_past_paper_questions(past_paper_id);
CREATE INDEX IF NOT EXISTS idx_gcse_grade_boundaries_subject ON gcse_grade_boundaries(exam_board, subject_code);
CREATE INDEX IF NOT EXISTS idx_gcse_performance_user_id ON gcse_performance(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_performance_subject_id ON gcse_performance(subject_id);
CREATE INDEX IF NOT EXISTS idx_gcse_study_plans_user_id ON gcse_study_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_study_plan_steps_plan_id ON gcse_study_plan_steps(study_plan_id);


INSERT INTO gcse_subjects (subject_name, exam_board, specification_code, subject_code) VALUES
('Mathematics', 'AQA', '8300', 'MATHS'),
('Mathematics', 'Edexcel', '1MA1', 'MATHS'),
('Mathematics', 'OCR', 'J560', 'MATHS'),
('English Language', 'AQA', '8700', 'ENGLANG'),
('English Language', 'Edexcel', '1EN0', 'ENGLANG'),
('English Literature', 'AQA', '8702', 'ENGLIT'),
('English Literature', 'Edexcel', '1ET0', 'ENGLIT'),
('Biology', 'AQA', '8461', 'BIO'),
('Biology', 'Edexcel', '1BI0', 'BIO'),
('Biology', 'OCR', 'J257', 'BIO'),
('Chemistry', 'AQA', '8462', 'CHEM'),
('Chemistry', 'Edexcel', '1CH0', 'CHEM'),
('Chemistry', 'OCR', 'J258', 'CHEM'),
('Physics', 'AQA', '8463', 'PHYS'),
('Physics', 'Edexcel', '1PH0', 'PHYS'),
('Physics', 'OCR', 'J259', 'PHYS'),
('History', 'AQA', '8145', 'HIST'),
('History', 'Edexcel', '1HIO', 'HIST'),
('Geography', 'AQA', '8035', 'GEOG'),
('Geography', 'Edexcel', '1GA0', 'GEOG'),
('Computer Science', 'AQA', '8525', 'CS'),
('Computer Science', 'Edexcel', '1CP2', 'CS'),
('Business Studies', 'AQA', '8132', 'BUS'),
('Business Studies', 'Edexcel', '1BS0', 'BUS'),
('Economics', 'AQA', '8136', 'ECON'),
('Economics', 'Edexcel', '1EC0', 'ECON'),
('Psychology', 'AQA', '8182', 'PSYCH'),
('Psychology', 'Edexcel', '9PS0', 'PSYCH'),
('Sociology', 'AQA', '8192', 'SOC'),
('Sociology', 'Edexcel', '1SC0', 'SOC'),
('Art & Design', 'AQA', '8201', 'ART'),
('Art & Design', 'Edexcel', '1AD0', 'ART'),
('Design & Technology', 'AQA', '8552', 'DT'),
('Design & Technology', 'Edexcel', '1DT0', 'DT'),
('Food Preparation & Nutrition', 'AQA', '8585', 'FOOD'),
('Food Preparation & Nutrition', 'Edexcel', '1FN0', 'FOOD'),
('Physical Education', 'AQA', '8582', 'PE'),
('Physical Education', 'Edexcel', '1PE0', 'PE'),
('Religious Studies', 'AQA', '8062', 'RS'),
('Religious Studies', 'Edexcel', '1RB0', 'RS'),
('Spanish', 'AQA', '8698', 'SPAN'),
('Spanish', 'Edexcel', '1SP0', 'SPAN'),
('French', 'AQA', '8658', 'FRENCH'),
('French', 'Edexcel', '1FR0', 'FRENCH'),
('German', 'AQA', '8668', 'GERMAN'),
('German', 'Edexcel', '1GN0', 'GERMAN'),
('Music', 'AQA', '8271', 'MUSIC'),
('Music', 'Edexcel', '1MU0', 'MUSIC'),
('Drama', 'AQA', '8261', 'DRAMA'),
('Drama', 'Edexcel', '1DR0', 'DRAMA')
ON CONFLICT DO NOTHING;


INSERT INTO gcse_grade_boundaries (exam_board, subject_code, exam_year, exam_month, tier, grade, raw_mark, percentage_mark) VALUES

('AQA', '8300', 2023, 'June', 'Foundation', '5', 77, 77.0),
('AQA', '8300', 2023, 'June', 'Foundation', '4', 65, 65.0),
('AQA', '8300', 2023, 'June', 'Foundation', '3', 53, 53.0),
('AQA', '8300', 2023, 'June', 'Higher', '9', 214, 89.2),
('AQA', '8300', 2023, 'June', 'Higher', '8', 186, 77.5),
('AQA', '8300', 2023, 'June', 'Higher', '7', 158, 65.8),
('AQA', '8300', 2023, 'June', 'Higher', '6', 130, 54.2),
('AQA', '8300', 2023, 'June', 'Higher', '5', 102, 42.5),
('AQA', '8300', 2023, 'June', 'Higher', '4', 74, 30.8),

('AQA', '8461', 2023, 'June', 'Foundation', '5', 69, 69.0),
('AQA', '8461', 2023, 'June', 'Foundation', '4', 58, 58.0),
('AQA', '8461', 2023, 'June', 'Foundation', '3', 47, 47.0),
('AQA', '8461', 2023, 'June', 'Higher', '9', 131, 87.3),
('AQA', '8461', 2023, 'June', 'Higher', '8', 119, 79.3),
('AQA', '8461', 2023, 'June', 'Higher', '7', 107, 71.3),
('AQA', '8461', 2023, 'June', 'Higher', '6', 95, 63.3),
('AQA', '8461', 2023, 'June', 'Higher', '5', 83, 55.3),
('AQA', '8461', 2023, 'June', 'Higher', '4', 71, 47.3),

('AQA', '8462', 2023, 'June', 'Foundation', '5', 68, 68.0),
('AQA', '8462', 2023, 'June', 'Foundation', '4', 57, 57.0),
('AQA', '8462', 2023, 'June', 'Foundation', '3', 46, 46.0),
('AQA', '8462', 2023, 'June', 'Higher', '9', 130, 86.7),
('AQA', '8462', 2023, 'June', 'Higher', '8', 118, 78.7),
('AQA', '8462', 2023, 'June', 'Higher', '7', 106, 70.7),
('AQA', '8462', 2023, 'June', 'Higher', '6', 94, 62.7),
('AQA', '8462', 2023, 'June', 'Higher', '5', 82, 54.7),
('AQA', '8462', 2023, 'June', 'Higher', '4', 70, 46.7),

('AQA', '8463', 2023, 'June', 'Foundation', '5', 70, 70.0),
('AQA', '8463', 2023, 'June', 'Foundation', '4', 59, 59.0),
('AQA', '8463', 2023, 'June', 'Foundation', '3', 48, 48.0),
('AQA', '8463', 2023, 'June', 'Higher', '9', 132, 88.0),
('AQA', '8463', 2023, 'June', 'Higher', '8', 120, 80.0),
('AQA', '8463', 2023, 'June', 'Higher', '7', 108, 72.0),
('AQA', '8463', 2023, 'June', 'Higher', '6', 96, 64.0),
('AQA', '8463', 2023, 'June', 'Higher', '5', 84, 56.0),
('AQA', '8463', 2023, 'June', 'Higher', '4', 72, 48.0)
ON CONFLICT DO NOTHING;


ALTER TABLE gcse_subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_exams ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_past_papers ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_past_paper_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_grade_boundaries ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_performance ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_study_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_study_plan_steps ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Allow public read access to gcse_subjects" ON gcse_subjects FOR SELECT USING (true);
CREATE POLICY "Allow public read access to gcse_topics" ON gcse_topics FOR SELECT USING (true);
CREATE POLICY "Allow public read access to gcse_exams" ON gcse_exams FOR SELECT USING (true);
CREATE POLICY "Allow public read access to gcse_past_papers" ON gcse_past_papers FOR SELECT USING (true);
CREATE POLICY "Allow public read access to gcse_past_paper_questions" ON gcse_past_paper_questions FOR SELECT USING (true);
CREATE POLICY "Allow public read access to gcse_grade_boundaries" ON gcse_grade_boundaries FOR SELECT USING (true);


CREATE POLICY "Users can manage their own gcse_performance" ON gcse_performance FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can manage their own gcse_study_plans" ON gcse_study_plans FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can manage their own gcse_study_plan_steps" ON gcse_study_plan_steps FOR ALL USING (
    EXISTS (SELECT 1 FROM gcse_study_plans WHERE id = study_plan_id AND user_id = auth.uid())
);


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_gcse_subjects_updated_at BEFORE UPDATE ON gcse_subjects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_topics_updated_at BEFORE UPDATE ON gcse_topics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_exams_updated_at BEFORE UPDATE ON gcse_exams FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_past_papers_updated_at BEFORE UPDATE ON gcse_past_papers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_past_paper_questions_updated_at BEFORE UPDATE ON gcse_past_paper_questions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_grade_boundaries_updated_at BEFORE UPDATE ON gcse_grade_boundaries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_study_plans_updated_at BEFORE UPDATE ON gcse_study_plans FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_study_plan_steps_updated_at BEFORE UPDATE ON gcse_study_plan_steps FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
