


DROP TABLE IF EXISTS gcse_exams CASCADE;

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

CREATE INDEX idx_gcse_exams_user_id ON gcse_exams(user_id);
CREATE INDEX idx_gcse_exams_exam_date ON gcse_exams(exam_date);

