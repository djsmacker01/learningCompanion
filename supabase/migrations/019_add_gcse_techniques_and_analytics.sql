



CREATE TABLE gcse_study_techniques (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    technique_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subject_applicability VARCHAR(50) NOT NULL,
    difficulty_level VARCHAR(20) NOT NULL,
    time_required VARCHAR(20) NOT NULL,
    effectiveness_rating INTEGER CHECK (effectiveness_rating >= 1 AND effectiveness_rating <= 5),
    description TEXT NOT NULL,
    step_by_step_guide JSONB,
    tips_and_tricks JSONB,
    when_to_use TEXT,
    examples JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_exam_strategies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    strategy_name VARCHAR(255) NOT NULL,
    exam_type VARCHAR(50) NOT NULL,
    subject_applicability VARCHAR(50) NOT NULL,
    strategy_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    step_by_step_guide JSONB,
    time_management_tips JSONB,
    common_mistakes JSONB,
    success_tips JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_user_techniques (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    technique_id UUID NOT NULL REFERENCES gcse_study_techniques(id) ON DELETE CASCADE,
    subject_id UUID REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    notes TEXT,
    is_favorite BOOLEAN DEFAULT FALSE,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, technique_id, subject_id)
);


CREATE TABLE gcse_study_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    subject_id UUID REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    session_type VARCHAR(50) NOT NULL,
    technique_used VARCHAR(255),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    duration_minutes INTEGER,
    productivity_score INTEGER CHECK (productivity_score >= 1 AND productivity_score <= 10),
    difficulty_level VARCHAR(20),
    notes TEXT,
    distractions_count INTEGER DEFAULT 0,
    breaks_taken INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE gcse_learning_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    learning_style VARCHAR(50),
    preferred_study_times VARCHAR(100),
    study_duration_preference VARCHAR(20),
    difficulty_preference VARCHAR(20),
    group_study_preference BOOLEAN DEFAULT FALSE,
    quiet_environment_preference BOOLEAN DEFAULT TRUE,
    music_preference BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);


CREATE TABLE gcse_analytics_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    subject_id UUID REFERENCES gcse_subjects(id) ON DELETE CASCADE,
    analytics_type VARCHAR(50) NOT NULL,
    cache_key VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    computed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '1 hour'),
    UNIQUE(user_id, subject_id, analytics_type, cache_key)
);


ALTER TABLE gcse_study_techniques ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access to gcse_study_techniques" ON gcse_study_techniques FOR SELECT USING (TRUE);


ALTER TABLE gcse_exam_strategies ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access to gcse_exam_strategies" ON gcse_exam_strategies FOR SELECT USING (TRUE);


ALTER TABLE gcse_user_techniques ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own techniques" ON gcse_user_techniques FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own techniques" ON gcse_user_techniques FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own techniques" ON gcse_user_techniques FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own techniques" ON gcse_user_techniques FOR DELETE USING (auth.uid() = user_id);


ALTER TABLE gcse_study_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own study sessions" ON gcse_study_sessions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own study sessions" ON gcse_study_sessions FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own study sessions" ON gcse_study_sessions FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own study sessions" ON gcse_study_sessions FOR DELETE USING (auth.uid() = user_id);


ALTER TABLE gcse_learning_preferences ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own preferences" ON gcse_learning_preferences FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own preferences" ON gcse_learning_preferences FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own preferences" ON gcse_learning_preferences FOR UPDATE USING (auth.uid() = user_id);


ALTER TABLE gcse_analytics_cache ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own analytics cache" ON gcse_analytics_cache FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own analytics cache" ON gcse_analytics_cache FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own analytics cache" ON gcse_analytics_cache FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own analytics cache" ON gcse_analytics_cache FOR DELETE USING (auth.uid() = user_id);


CREATE INDEX idx_gcse_study_techniques_category ON gcse_study_techniques(category);
CREATE INDEX idx_gcse_study_techniques_subject_applicability ON gcse_study_techniques(subject_applicability);
CREATE INDEX idx_gcse_study_techniques_difficulty ON gcse_study_techniques(difficulty_level);
CREATE INDEX idx_gcse_exam_strategies_exam_type ON gcse_exam_strategies(exam_type);
CREATE INDEX idx_gcse_exam_strategies_strategy_type ON gcse_exam_strategies(strategy_type);
CREATE INDEX idx_gcse_user_techniques_user_id ON gcse_user_techniques(user_id);
CREATE INDEX idx_gcse_study_sessions_user_id ON gcse_study_sessions(user_id);
CREATE INDEX idx_gcse_study_sessions_start_time ON gcse_study_sessions(start_time);
CREATE INDEX idx_gcse_analytics_cache_user_subject ON gcse_analytics_cache(user_id, subject_id);
CREATE INDEX idx_gcse_analytics_cache_expires ON gcse_analytics_cache(expires_at);


INSERT INTO gcse_study_techniques (technique_name, category, subject_applicability, difficulty_level, time_required, effectiveness_rating, description, step_by_step_guide, tips_and_tricks, when_to_use, examples) VALUES
('Active Recall', 'memorization', 'all', 'intermediate', 'medium', 5, 'Test yourself on information without looking at notes to strengthen memory', 
 '["Write down everything you remember about a topic", "Check against your notes for accuracy", "Identify gaps in your knowledge", "Focus study time on the gaps", "Repeat the process regularly"]',
 '["Use flashcards for quick active recall", "Try to explain concepts out loud", "Test yourself at increasing intervals", "Don''t just re-read notes - actively test knowledge"]',
 'Best for memorizing facts, formulas, and key concepts',
 '["Testing yourself on biology definitions", "Recalling mathematical formulas", "Remembering historical dates"]'),

('Spaced Repetition', 'memorization', 'all', 'beginner', 'long', 5, 'Review information at increasing intervals to improve long-term retention',
 '["Learn new material thoroughly", "Review after 1 day", "Review after 3 days", "Review after 1 week", "Review after 2 weeks", "Review after 1 month"]',
 '["Use apps like Anki for automated scheduling", "Be consistent with review sessions", "Adjust intervals based on difficulty", "Focus more time on difficult material"]',
 'Perfect for long-term retention of facts and concepts',
 '["Learning vocabulary", "Memorizing scientific formulas", "Remembering historical facts"]'),

('Mind Mapping', 'understanding', 'all', 'beginner', 'medium', 4, 'Create visual diagrams to organize and connect information',
 '["Start with main topic in center", "Add major subtopics as branches", "Add details to each branch", "Use colors and symbols", "Review and refine connections"]',
 '["Use different colors for different topics", "Keep branches short with key words", "Add images and symbols for visual memory", "Review maps regularly to reinforce connections"]',
 'Great for understanding relationships between concepts',
 '["Biology: ecosystem relationships", "History: causes of World War I", "Literature: character relationships"]'),

('Past Paper Practice', 'practice', 'all', 'intermediate', 'long', 5, 'Practice with real exam questions under timed conditions',
 '["Complete past paper under exam conditions", "Mark your answers honestly", "Identify areas of weakness", "Study weak areas thoroughly", "Repeat with different past papers"]',
 '["Time yourself to practice exam technique", "Focus on question command words", "Practice different question types", "Review mark schemes for key points"]',
 'Essential for exam preparation and technique',
 '["Math: solving equations under time pressure", "English: essay writing practice", "Science: practical questions"]'),

('Feynman Technique', 'understanding', 'sciences', 'advanced', 'medium', 4, 'Explain complex concepts in simple terms to deepen understanding',
 '["Choose a concept to learn", "Explain it in simple terms", "Identify gaps in your explanation", "Return to source material", "Simplify and clarify", "Teach someone else"]',
 '["Use analogies and examples", "Avoid jargon and technical terms", "Focus on the ''why'' not just the ''what''", "Practice explaining to different audiences"]',
 'Best for understanding complex scientific concepts',
 '["Physics: explaining gravity", "Chemistry: understanding chemical bonds", "Biology: explaining photosynthesis"]'),

('Pomodoro Technique', 'exam_technique', 'all', 'beginner', 'quick', 4, 'Study in focused 25-minute intervals with short breaks',
 '["Set timer for 25 minutes", "Focus entirely on one task", "Take 5-minute break", "Repeat cycle 4 times", "Take longer 15-30 minute break"]',
 '["Eliminate distractions during focus time", "Use breaks for physical movement", "Track completed pomodoros", "Adjust intervals based on attention span"]',
 'Great for maintaining focus during long study sessions',
 '["Reading textbooks", "Writing essays", "Solving math problems", "Reviewing notes"]');


INSERT INTO gcse_exam_strategies (strategy_name, exam_type, subject_applicability, strategy_type, description, step_by_step_guide, time_management_tips, common_mistakes, success_tips) VALUES
('Read All Questions First', 'all', 'all', 'question_approach', 'Read through all questions before starting to plan your time effectively',
 '["Quickly scan all questions in the paper", "Identify easy questions you can answer quickly", "Note difficult questions that need more time", "Allocate time based on marks per question", "Start with questions you''re most confident about"]',
 '["Spend 5-10 minutes reading through the paper", "Allocate 1.5-2 minutes per mark", "Leave 10-15 minutes at the end for checking", "Don''t spend too long on any single question"]',
 '["Starting with the first question without planning", "Spending too much time on difficult questions early", "Running out of time for easier questions", "Not leaving time for checking answers"]',
 '["Answer easy questions first to build confidence", "Show your working even for simple calculations", "If stuck, move on and return later", "Use the full time allocated"]'),

('Command Word Recognition', 'all', 'all', 'question_approach', 'Understand what each command word requires to answer questions correctly',
 '["Identify the command word in the question", "Understand what the command word requires", "Structure your answer accordingly", "Check you''ve addressed the command word", "Ensure your answer matches the mark allocation"]',
 '["Command words indicate time needed: ''explain'' needs more time than ''state''", "Higher mark questions usually need more detailed answers", "Plan your answer structure before writing"]',
 '["Confusing ''describe'' with ''explain''", "Not providing enough detail for ''evaluate'' questions", "Listing when asked to ''compare''", "Not addressing all parts of multi-part questions"]',
 '["Learn command word meanings thoroughly", "Practice identifying command words in past papers", "Structure answers to match command requirements", "Use command words in your answer structure"]'),

('Show Your Working', 'calculation', 'maths', 'question_approach', 'Always show clear working for mathematical and scientific calculations',
 '["Write down the formula or equation you''re using", "Substitute values clearly", "Show each step of your calculation", "Write your final answer clearly", "Check your answer makes sense"]',
 '["Don''t rush calculations - accuracy is more important", "Use rough working space effectively", "Double-check calculations before moving on"]',
 '["Not showing working steps", "Using incorrect units", "Rounding errors", "Not checking if answer is reasonable"]',
 '["Even if you get the wrong answer, you can get marks for correct method", "Use standard mathematical notation", "Check units are consistent", "Estimate answers to check reasonableness"]'),

('PEEL Paragraph Structure', 'essay', 'humanities', 'question_approach', 'Use Point, Evidence, Explanation, Link structure for essay questions',
 '["Make a clear Point in your opening sentence", "Provide Evidence to support your point", "Explain how the evidence supports your point", "Link back to the question or next point", "Repeat for each paragraph"]',
 '["Plan your essay structure before writing", "Allocate time per paragraph based on marks", "Leave time for introduction and conclusion"]',
 '["Making points without evidence", "Not explaining how evidence supports the point", "Writing in a narrative style instead of analytical", "Not linking paragraphs together"]',
 '["Use specific examples and evidence", "Analyze rather than just describe", "Link each paragraph to the question", "Use topic sentences to introduce each point"]'),

('Elimination Method', 'multiple_choice', 'all', 'question_approach', 'Use process of elimination for multiple choice questions',
 '["Read the question carefully", "Identify obviously wrong answers", "Consider each remaining option", "Use knowledge to eliminate incorrect choices", "Make an educated guess if necessary"]',
 '["Don''t spend too long on difficult multiple choice questions", "Answer all questions - there''s no penalty for wrong answers", "Mark difficult questions to return to later"]',
 '["Not reading all options before choosing", "Getting distracted by similar-sounding options", "Changing correct answers unnecessarily", "Leaving questions blank"]',
 '["Read questions and options carefully", "Use elimination to narrow down choices", "Trust your first instinct unless you have a good reason to change", "Answer all questions even if unsure"]');


CREATE TRIGGER update_gcse_study_techniques_updated_at BEFORE UPDATE ON gcse_study_techniques FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_exam_strategies_updated_at BEFORE UPDATE ON gcse_exam_strategies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_gcse_learning_preferences_updated_at BEFORE UPDATE ON gcse_learning_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
