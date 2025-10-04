



CREATE TABLE gcse_grade_boundaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exam_board VARCHAR(100) NOT NULL,
    subject_code VARCHAR(50) NOT NULL,
    exam_year INTEGER NOT NULL,
    exam_month VARCHAR(20),
    tier VARCHAR(20),
    grade VARCHAR(5) NOT NULL,
    raw_mark INTEGER NOT NULL,
    percentage_mark DECIMAL(5,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    subject_id UUID NOT NULL REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    assessment_type VARCHAR(50) NOT NULL,
    assessment_id UUID,
    score DECIMAL(5,2) NOT NULL,
    grade VARCHAR(5),
    total_marks INTEGER NOT NULL,
    achieved_marks INTEGER NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_exam_schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    subject_id UUID NOT NULL REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    exam_name VARCHAR(255) NOT NULL,
    exam_date DATE NOT NULL,
    paper_number INTEGER,
    duration_minutes INTEGER,
    exam_board VARCHAR(100),
    specification_code VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_revision_schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    subject_id UUID NOT NULL REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    revision_date DATE NOT NULL,
    duration_minutes INTEGER NOT NULL,
    revision_type VARCHAR(50) NOT NULL,
    priority_level VARCHAR(20) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_study_reminders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    reminder_type VARCHAR(50) NOT NULL,
    subject_id UUID REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    reminder_date DATE NOT NULL,
    reminder_time TIME NOT NULL,
    message TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


ALTER TABLE gcse_grade_boundaries ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access to gcse_grade_boundaries" ON gcse_grade_boundaries FOR SELECT USING (TRUE);


ALTER TABLE gcse_performance ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own performance" ON gcse_performance FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own performance" ON gcse_performance FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own performance" ON gcse_performance FOR UPDATE USING (auth.uid() = user_id);


ALTER TABLE gcse_exam_schedules ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own exam schedules" ON gcse_exam_schedules FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own exam schedules" ON gcse_exam_schedules FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own exam schedules" ON gcse_exam_schedules FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own exam schedules" ON gcse_exam_schedules FOR DELETE USING (auth.uid() = user_id);


ALTER TABLE gcse_revision_schedules ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own revision schedules" ON gcse_revision_schedules FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own revision schedules" ON gcse_revision_schedules FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own revision schedules" ON gcse_revision_schedules FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own revision schedules" ON gcse_revision_schedules FOR DELETE USING (auth.uid() = user_id);


ALTER TABLE gcse_study_reminders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own study reminders" ON gcse_study_reminders FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own study reminders" ON gcse_study_reminders FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own study reminders" ON gcse_study_reminders FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own study reminders" ON gcse_study_reminders FOR DELETE USING (auth.uid() = user_id);


CREATE INDEX idx_gcse_grade_boundaries_exam_board_subject ON gcse_grade_boundaries(exam_board, subject_code);
CREATE INDEX idx_gcse_grade_boundaries_year_tier ON gcse_grade_boundaries(exam_year, tier);
CREATE INDEX idx_gcse_performance_user_subject ON gcse_performance(user_id, subject_id);
CREATE INDEX idx_gcse_performance_completed_at ON gcse_performance(completed_at);
CREATE INDEX idx_gcse_exam_schedules_user_date ON gcse_exam_schedules(user_id, exam_date);
CREATE INDEX idx_gcse_revision_schedules_user_date ON gcse_revision_schedules(user_id, revision_date);
CREATE INDEX idx_gcse_study_reminders_user_date ON gcse_study_reminders(user_id, reminder_date);


INSERT INTO gcse_grade_boundaries (exam_board, subject_code, exam_year, exam_month, tier, grade, raw_mark, percentage_mark) VALUES

('AQA', '8300', 2023, 'May/June', 'Higher', '9', 214, 89.2),
('AQA', '8300', 2023, 'May/June', 'Higher', '8', 186, 77.5),
('AQA', '8300', 2023, 'May/June', 'Higher', '7', 158, 65.8),
('AQA', '8300', 2023, 'May/June', 'Higher', '6', 130, 54.2),
('AQA', '8300', 2023, 'May/June', 'Higher', '5', 102, 42.5),
('AQA', '8300', 2023, 'May/June', 'Higher', '4', 74, 30.8),

('AQA', '8300', 2023, 'May/June', 'Foundation', '5', 77, 77.0),
('AQA', '8300', 2023, 'May/June', 'Foundation', '4', 65, 65.0),
('AQA', '8300', 2023, 'May/June', 'Foundation', '3', 53, 53.0);


INSERT INTO gcse_grade_boundaries (exam_board, subject_code, exam_year, exam_month, tier, grade, raw_mark, percentage_mark) VALUES

('AQA', '8461', 2023, 'May/June', 'Higher', '9', 131, 87.3),
('AQA', '8461', 2023, 'May/June', 'Higher', '8', 119, 79.3),
('AQA', '8461', 2023, 'May/June', 'Higher', '7', 107, 71.3),
('AQA', '8461', 2023, 'May/June', 'Higher', '6', 95, 63.3),
('AQA', '8461', 2023, 'May/June', 'Higher', '5', 83, 55.3),
('AQA', '8461', 2023, 'May/June', 'Higher', '4', 71, 47.3),

('AQA', '8461', 2023, 'May/June', 'Foundation', '5', 69, 69.0),
('AQA', '8461', 2023, 'May/June', 'Foundation', '4', 58, 58.0),
('AQA', '8461', 2023, 'May/June', 'Foundation', '3', 47, 47.0);


INSERT INTO gcse_grade_boundaries (exam_board, subject_code, exam_year, exam_month, tier, grade, raw_mark, percentage_mark) VALUES

('Edexcel', '1MA1', 2023, 'May/June', 'Higher', '9', 198, 82.5),
('Edexcel', '1MA1', 2023, 'May/June', 'Higher', '8', 171, 71.3),
('Edexcel', '1MA1', 2023, 'May/June', 'Higher', '7', 144, 60.0),
('Edexcel', '1MA1', 2023, 'May/June', 'Higher', '6', 117, 48.8),
('Edexcel', '1MA1', 2023, 'May/June', 'Higher', '5', 90, 37.5),
('Edexcel', '1MA1', 2023, 'May/June', 'Higher', '4', 63, 26.3),

('Edexcel', '1MA1', 2023, 'May/June', 'Foundation', '5', 75, 75.0),
('Edexcel', '1MA1', 2023, 'May/June', 'Foundation', '4', 63, 63.0),
('Edexcel', '1MA1', 2023, 'May/June', 'Foundation', '3', 51, 51.0);


INSERT INTO gcse_grade_boundaries (exam_board, subject_code, exam_year, exam_month, tier, grade, raw_mark, percentage_mark) VALUES

('OCR', 'J560', 2023, 'May/June', 'Higher', '9', 205, 85.4),
('OCR', 'J560', 2023, 'May/June', 'Higher', '8', 178, 74.2),
('OCR', 'J560', 2023, 'May/June', 'Higher', '7', 151, 62.9),
('OCR', 'J560', 2023, 'May/June', 'Higher', '6', 124, 51.7),
('OCR', 'J560', 2023, 'May/June', 'Higher', '5', 97, 40.4),
('OCR', 'J560', 2023, 'May/June', 'Higher', '4', 70, 29.2),

('OCR', 'J560', 2023, 'May/June', 'Foundation', '5', 78, 78.0),
('OCR', 'J560', 2023, 'May/June', 'Foundation', '4', 66, 66.0),
('OCR', 'J560', 2023, 'May/June', 'Foundation', '3', 54, 54.0);


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_gcse_grade_boundaries_updated_at BEFORE UPDATE ON gcse_grade_boundaries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_exam_schedules_updated_at BEFORE UPDATE ON gcse_exam_schedules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_revision_schedules_updated_at BEFORE UPDATE ON gcse_revision_schedules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
