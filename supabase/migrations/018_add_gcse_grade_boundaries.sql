

DROP TABLE IF EXISTS gcse_grade_boundaries CASCADE;

CREATE TABLE gcse_grade_boundaries (
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


INSERT INTO gcse_grade_boundaries (exam_board, subject_code, exam_year, exam_month, tier, grade, raw_mark, percentage_mark) VALUES

('AQA', '8300', 2023, 'June', 'Foundation', '5', 77, 77.0),
('AQA', '8300', 2023, 'June', 'Foundation', '4', 65, 65.0),
('AQA', '8300', 2023, 'June', 'Foundation', '3', 53, 53.0),

('AQA', '8300', 2023, 'June', 'Higher', '9', 214, 89.2),
('AQA', '8300', 2023, 'June', 'Higher', '8', 186, 77.5),
('AQA', '8300', 2023, 'June', 'Higher', '7', 158, 65.8),
('AQA', '8300', 2023, 'June', 'Higher', '6', 130, 54.2),
('AQA', '8300', 2023, 'June', 'Higher', '5', 102, 42.5),
('AQA', '8300', 2023, 'June', 'Higher', '4', 74, 30.8);

CREATE INDEX idx_gcse_grade_boundaries ON gcse_grade_boundaries(exam_board, subject_code, exam_year);

