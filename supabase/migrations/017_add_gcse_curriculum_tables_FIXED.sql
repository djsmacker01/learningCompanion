



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
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
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


CREATE INDEX IF NOT EXISTS idx_gcse_subjects_exam_board ON gcse_subjects(exam_board);
CREATE INDEX IF NOT EXISTS idx_gcse_subjects_specification ON gcse_subjects(specification_code);
CREATE INDEX IF NOT EXISTS idx_gcse_topics_subject_id ON gcse_topics(subject_id);
CREATE INDEX IF NOT EXISTS idx_gcse_exams_user_id ON gcse_exams(user_id);
CREATE INDEX IF NOT EXISTS idx_gcse_exams_subject_id ON gcse_exams(subject_id);
CREATE INDEX IF NOT EXISTS idx_gcse_exams_exam_date ON gcse_exams(exam_date);
CREATE INDEX IF NOT EXISTS idx_gcse_past_papers_subject_id ON gcse_past_papers(subject_id);


ALTER TABLE gcse_subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_exams ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_past_papers ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_past_paper_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE gcse_grade_boundaries ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Allow public read access to gcse_subjects" ON gcse_subjects FOR SELECT USING (true);
CREATE POLICY "Allow public read access to gcse_topics" ON gcse_topics FOR SELECT USING (true);


CREATE POLICY "Users can view own exams" ON gcse_exams FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own exams" ON gcse_exams FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own exams" ON gcse_exams FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own exams" ON gcse_exams FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Allow public read access to gcse_past_papers" ON gcse_past_papers FOR SELECT USING (true);
CREATE POLICY "Allow public read access to gcse_past_paper_questions" ON gcse_past_paper_questions FOR SELECT USING (true);
CREATE POLICY "Allow public read access to gcse_grade_boundaries" ON gcse_grade_boundaries FOR SELECT USING (true);

