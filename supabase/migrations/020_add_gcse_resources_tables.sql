



CREATE TABLE gcse_learning_resources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    subject_id UUID NOT NULL REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    topic_area VARCHAR(255),
    difficulty_level VARCHAR(20) NOT NULL,
    format_type VARCHAR(20),
    description TEXT NOT NULL,
    content_url TEXT NOT NULL,
    thumbnail_url TEXT,
    duration_minutes INTEGER,
    file_size_mb DECIMAL(8,2),
    tags JSONB DEFAULT '[]',
    author VARCHAR(255),
    publisher VARCHAR(255),
    year_published INTEGER,
    is_free BOOLEAN DEFAULT TRUE,
    price DECIMAL(8,2),
    rating DECIMAL(3,2) CHECK (rating >= 1.0 AND rating <= 5.0),
    review_count INTEGER DEFAULT 0,
    download_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_revision_materials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    material_type VARCHAR(50) NOT NULL,
    subject_id UUID NOT NULL REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    topic_area VARCHAR(255),
    exam_board VARCHAR(100),
    specification_code VARCHAR(50),
    difficulty_level VARCHAR(20) NOT NULL,
    content_summary TEXT,
    key_points JSONB DEFAULT '[]',
    revision_notes TEXT,
    practice_questions JSONB DEFAULT '[]',
    mark_scheme TEXT,
    tips_and_tricks JSONB DEFAULT '[]',
    estimated_study_time INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_educational_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_title VARCHAR(255) NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    subject_id UUID NOT NULL REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    learning_objective TEXT,
    prerequisite_knowledge TEXT,
    content_body TEXT NOT NULL,
    examples JSONB DEFAULT '[]',
    exercises JSONB DEFAULT '[]',
    assessment_criteria TEXT,
    estimated_completion_time INTEGER,
    difficulty_progression VARCHAR(50),
    related_topics JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_resource_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    resource_id UUID NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    duration_seconds INTEGER,
    accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);


CREATE TABLE gcse_user_bookmarks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    resource_id UUID NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    bookmark_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, resource_id, resource_type)
);


CREATE TABLE gcse_resource_ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    resource_id UUID NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, resource_id, resource_type)
);


ALTER TABLE gcse_learning_resources ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access to gcse_learning_resources" ON gcse_learning_resources FOR SELECT USING (TRUE);


ALTER TABLE gcse_revision_materials ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access to gcse_revision_materials" ON gcse_revision_materials FOR SELECT USING (TRUE);


ALTER TABLE gcse_educational_content ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access to gcse_educational_content" ON gcse_educational_content FOR SELECT USING (TRUE);


ALTER TABLE gcse_resource_tracking ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own resource tracking" ON gcse_resource_tracking FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own resource tracking" ON gcse_resource_tracking FOR INSERT WITH CHECK (auth.uid() = user_id);


ALTER TABLE gcse_user_bookmarks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own bookmarks" ON gcse_user_bookmarks FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own bookmarks" ON gcse_user_bookmarks FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own bookmarks" ON gcse_user_bookmarks FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own bookmarks" ON gcse_user_bookmarks FOR DELETE USING (auth.uid() = user_id);


ALTER TABLE gcse_resource_ratings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view all resource ratings" ON gcse_resource_ratings FOR SELECT USING (TRUE);
CREATE POLICY "Users can insert own resource ratings" ON gcse_resource_ratings FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own resource ratings" ON gcse_resource_ratings FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own resource ratings" ON gcse_resource_ratings FOR DELETE USING (auth.uid() = user_id);


CREATE INDEX idx_gcse_learning_resources_subject_id ON gcse_learning_resources(subject_id);
CREATE INDEX idx_gcse_learning_resources_resource_type ON gcse_learning_resources(resource_type);
CREATE INDEX idx_gcse_learning_resources_difficulty ON gcse_learning_resources(difficulty_level);
CREATE INDEX idx_gcse_learning_resources_rating ON gcse_learning_resources(rating);
CREATE INDEX idx_gcse_learning_resources_is_free ON gcse_learning_resources(is_free);
CREATE INDEX idx_gcse_learning_resources_tags ON gcse_learning_resources USING GIN(tags);

CREATE INDEX idx_gcse_revision_materials_subject_id ON gcse_revision_materials(subject_id);
CREATE INDEX idx_gcse_revision_materials_type ON gcse_revision_materials(material_type);
CREATE INDEX idx_gcse_revision_materials_exam_board ON gcse_revision_materials(exam_board);

CREATE INDEX idx_gcse_educational_content_subject_id ON gcse_educational_content(subject_id);
CREATE INDEX idx_gcse_educational_content_type ON gcse_educational_content(content_type);

CREATE INDEX idx_gcse_resource_tracking_user_id ON gcse_resource_tracking(user_id);
CREATE INDEX idx_gcse_resource_tracking_resource_id ON gcse_resource_tracking(resource_id);
CREATE INDEX idx_gcse_resource_tracking_accessed_at ON gcse_resource_tracking(accessed_at);

CREATE INDEX idx_gcse_user_bookmarks_user_id ON gcse_user_bookmarks(user_id);
CREATE INDEX idx_gcse_user_bookmarks_resource_id ON gcse_user_bookmarks(resource_id);

CREATE INDEX idx_gcse_resource_ratings_resource_id ON gcse_resource_ratings(resource_id);
CREATE INDEX idx_gcse_resource_ratings_rating ON gcse_resource_ratings(rating);


INSERT INTO gcse_learning_resources (title, resource_type, subject_id, topic_area, difficulty_level, format_type, description, content_url, thumbnail_url, duration_minutes, tags, author, publisher, year_published, is_free, rating, review_count, download_count) VALUES
('GCSE Biology: Cell Structure and Function', 'video', (SELECT id FROM gcse_subjects WHERE name = 'Biology' LIMIT 1), 'Cell Biology', 'intermediate', 'mp4', 'Comprehensive video explaining cell structure, organelles, and their functions. Perfect for GCSE Biology revision.', 'https://example.com/biology/cell-structure.mp4', 'https://example.com/thumbnails/cell-structure.jpg', 15, '["cells", "organelles", "biology", "revision"]', 'GCSE Biology Tutor', 'EduVideos', 2023, true, 4.8, 156, 2340),

('GCSE Mathematics: Quadratic Equations', 'interactive', (SELECT id FROM gcse_subjects WHERE name = 'Mathematics' LIMIT 1), 'Algebra', 'intermediate', 'html', 'Interactive tutorial with step-by-step solutions for quadratic equations. Includes practice problems with instant feedback.', 'https://example.com/maths/quadratic-equations.html', 'https://example.com/thumbnails/quadratic.jpg', 25, '["algebra", "quadratic", "equations", "interactive"]', 'Maths Master', 'Interactive Learning', 2023, true, 4.6, 89, 1876),

('GCSE English Literature: Macbeth Analysis', 'document', (SELECT id FROM gcse_subjects WHERE name = 'English Literature' LIMIT 1), 'Shakespeare', 'advanced', 'pdf', 'Detailed analysis of Macbeth including themes, characters, and key quotes. Perfect for essay preparation.', 'https://example.com/english/macbeth-analysis.pdf', 'https://example.com/thumbnails/macbeth.jpg', 45, '["macbeth", "shakespeare", "literature", "analysis"]', 'English Literature Expert', 'Literary Guides', 2023, false, 4.9, 203, 892),

('GCSE Chemistry: Atomic Structure', 'video', (SELECT id FROM gcse_subjects WHERE name = 'Chemistry' LIMIT 1), 'Atomic Structure', 'intermediate', 'mp4', 'Clear explanation of atomic structure, electron configuration, and periodic table trends.', 'https://example.com/chemistry/atomic-structure.mp4', 'https://example.com/thumbnails/atomic-structure.jpg', 20, '["atoms", "electrons", "periodic table", "chemistry"]', 'Chemistry Teacher', 'Science Videos', 2023, true, 4.7, 124, 1567),

('GCSE Physics: Forces and Motion', 'interactive', (SELECT id FROM gcse_subjects WHERE name = 'Physics' LIMIT 1), 'Forces and Motion', 'intermediate', 'html', 'Interactive simulations demonstrating forces, motion, and Newton''s laws with real-time calculations.', 'https://example.com/physics/forces-motion.html', 'https://example.com/thumbnails/forces.jpg', 30, '["forces", "motion", "newton", "physics"]', 'Physics Pro', 'Interactive Science', 2023, true, 4.5, 78, 1234),

('GCSE History: World War I', 'document', (SELECT id FROM gcse_subjects WHERE name = 'History' LIMIT 1), 'World War I', 'intermediate', 'pdf', 'Comprehensive study guide covering causes, key events, and consequences of World War I.', 'https://example.com/history/wwi-guide.pdf', 'https://example.com/thumbnails/wwi.jpg', 60, '["world war", "history", "causes", "consequences"]', 'History Scholar', 'Historical Guides', 2023, true, 4.4, 92, 987),

('GCSE Geography: Climate Change', 'video', (SELECT id FROM gcse_subjects WHERE name = 'Geography' LIMIT 1), 'Climate Change', 'intermediate', 'mp4', 'Documentary-style video explaining climate change causes, effects, and solutions.', 'https://example.com/geography/climate-change.mp4', 'https://example.com/thumbnails/climate.jpg', 35, '["climate", "environment", "geography", "sustainability"]', 'Geography Expert', 'EcoVideos', 2023, true, 4.6, 67, 1456),

('GCSE Computer Science: Programming Basics', 'interactive', (SELECT id FROM gcse_subjects WHERE name = 'Computer Science' LIMIT 1), 'Programming', 'beginner', 'html', 'Learn programming fundamentals with interactive coding exercises and instant feedback.', 'https://example.com/computing/programming-basics.html', 'https://example.com/thumbnails/programming.jpg', 40, '["programming", "coding", "computer science", "python"]', 'Code Master', 'Programming Academy', 2023, true, 4.8, 145, 2134);


INSERT INTO gcse_revision_materials (title, material_type, subject_id, topic_area, exam_board, specification_code, difficulty_level, content_summary, key_points, tips_and_tricks, estimated_study_time) VALUES
('Biology Cell Structure Revision Guide', 'revision_guide', (SELECT id FROM gcse_subjects WHERE name = 'Biology' LIMIT 1), 'Cell Biology', 'AQA', '8461', 'intermediate', 'Complete revision guide covering all aspects of cell structure and function for GCSE Biology.', '["Plant and animal cells have different organelles", "Mitochondria are the powerhouse of the cell", "Chloroplasts contain chlorophyll for photosynthesis", "Cell membrane controls what enters and leaves the cell"]', '["Use diagrams to remember organelle locations", "Compare plant vs animal cells in a table", "Practice labeling cell diagrams", "Remember functions with acronyms"]', 60),

('Mathematics Algebra Summary Sheet', 'summary_sheet', (SELECT id FROM gcse_subjects WHERE name = 'Mathematics' LIMIT 1), 'Algebra', 'AQA', '8300', 'intermediate', 'Essential formulas and methods for GCSE Algebra topics.', '["Linear equations: y = mx + c", "Quadratic formula: x = (-b ± √(b²-4ac)) / 2a", "Factorising: find common factors", "Simultaneous equations: substitution or elimination"]', '["Always check your answers by substituting back", "Draw graphs to visualize linear equations", "Practice with negative numbers", "Use calculator efficiently for complex calculations"]', 45),

('English Literature Essay Structure Guide', 'revision_guide', (SELECT id FROM gcse_subjects WHERE name = 'English Literature' LIMIT 1), 'Essay Writing', 'AQA', '8702', 'advanced', 'Step-by-step guide to structuring essays for GCSE English Literature.', '["Use PEEL structure for paragraphs", "Include relevant quotations", "Analyze language techniques", "Link to themes and context"]', '["Plan your essay before writing", "Use topic sentences", "Analyze rather than describe", "Practice timed essays"]', 30);


INSERT INTO gcse_educational_content (content_title, content_type, subject_id, learning_objective, prerequisite_knowledge, content_body, examples, exercises, estimated_completion_time) VALUES
('Understanding Photosynthesis', 'lesson', (SELECT id FROM gcse_subjects WHERE name = 'Biology' LIMIT 1), 'Students will understand the process of photosynthesis and its importance in ecosystems', 'Basic understanding of plant cells and energy', 'Photosynthesis is the process by which plants convert light energy into chemical energy. This process occurs in the chloroplasts of plant cells and is essential for life on Earth.', '["Green plants in sunlight produce oxygen", "Leaves change color in autumn due to chlorophyll breakdown"]', '["Label the parts of a leaf involved in photosynthesis", "Explain why plants need sunlight", "Calculate the rate of photosynthesis from given data"]', 30),

('Solving Linear Equations', 'tutorial', (SELECT id FROM gcse_subjects WHERE name = 'Mathematics' LIMIT 1), 'Students will be able to solve linear equations with one unknown', 'Basic arithmetic and algebraic manipulation', 'Linear equations are equations where the highest power of the variable is 1. We solve them by isolating the variable on one side of the equation.', '["2x + 3 = 7 → x = 2", "3y - 5 = 10 → y = 5"]', '["Solve: 4x + 2 = 14", "Solve: 2y - 3 = 7", "Solve: 3z + 1 = 10"]', 25),

('Shakespeare''s Language Techniques', 'lesson', (SELECT id FROM gcse_subjects WHERE name = 'English Literature' LIMIT 1), 'Students will identify and analyze Shakespeare''s use of language techniques', 'Basic understanding of literary devices', 'Shakespeare used various language techniques to create meaning and effect in his plays. Understanding these techniques helps us analyze his work more effectively.', '["Metaphors in Romeo and Juliet", "Soliloquies in Hamlet", "Puns in Much Ado About Nothing"]', '["Identify metaphors in a Shakespeare passage", "Analyze the effect of a soliloquy", "Explain the purpose of wordplay"]', 35);


CREATE TRIGGER update_gcse_learning_resources_updated_at BEFORE UPDATE ON gcse_learning_resources FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_revision_materials_updated_at BEFORE UPDATE ON gcse_revision_materials FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_educational_content_updated_at BEFORE UPDATE ON gcse_educational_content FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_resource_ratings_updated_at BEFORE UPDATE ON gcse_resource_ratings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
