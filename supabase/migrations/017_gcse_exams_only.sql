-- Minimal migration: Just create gcse_exams table for exam scheduling

-- First, drop the table if it exists to start fresh
DROP TABLE IF EXISTS gcse_exams CASCADE;

-- Create gcse_exams table
CREATE TABLE gcse_exams (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    subject_id TEXT NOT NULL,
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

-- Create indexes
CREATE INDEX idx_gcse_exams_user_id ON gcse_exams(user_id);
CREATE INDEX idx_gcse_exams_exam_date ON gcse_exams(exam_date);

-- Enable Row Level Security
ALTER TABLE gcse_exams ENABLE ROW LEVEL SECURITY;

-- Create policies (user_id is TEXT, so compare as text)
CREATE POLICY "Users can view own exams" ON gcse_exams FOR SELECT USING (auth.uid()::text = user_id);
CREATE POLICY "Users can insert own exams" ON gcse_exams FOR INSERT WITH CHECK (auth.uid()::text = user_id);
CREATE POLICY "Users can update own exams" ON gcse_exams FOR UPDATE USING (auth.uid()::text = user_id);
CREATE POLICY "Users can delete own exams" ON gcse_exams FOR DELETE USING (auth.uid()::text = user_id);

