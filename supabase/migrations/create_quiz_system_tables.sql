
CREATE TABLE IF NOT EXISTS quizzes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    quiz_type VARCHAR(50) NOT NULL CHECK (quiz_type IN ('multiple_choice', 'flashcards', 'practice_test', 'assessment')),
    difficulty_level VARCHAR(20) DEFAULT 'medium' CHECK (difficulty_level IN ('easy', 'medium', 'hard')),
    time_limit_minutes INTEGER DEFAULT NULL,
    passing_score INTEGER DEFAULT 70,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS quiz_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quiz_id UUID NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL CHECK (question_type IN ('multiple_choice', 'true_false', 'fill_blank', 'flashcard')),
    correct_answer TEXT NOT NULL,
    explanation TEXT,
    points INTEGER DEFAULT 1,
    order_index INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS quiz_question_options (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID NOT NULL REFERENCES quiz_questions(id) ON DELETE CASCADE,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT false,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quiz_id UUID NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    score INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    time_taken_minutes INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed', 'abandoned')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS quiz_attempt_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID NOT NULL REFERENCES quiz_attempts(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES quiz_questions(id) ON DELETE CASCADE,
    user_answer TEXT,
    is_correct BOOLEAN DEFAULT false,
    time_spent_seconds INTEGER DEFAULT 0,
    answered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS flashcard_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES quiz_questions(id) ON DELETE CASCADE,
    ease_factor DECIMAL(3,2) DEFAULT 2.5,
    interval_days INTEGER DEFAULT 1,
    repetitions INTEGER DEFAULT 0,
    next_review_date DATE DEFAULT CURRENT_DATE,
    last_reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, question_id)
);


CREATE INDEX IF NOT EXISTS idx_quizzes_topic_id ON quizzes(topic_id);
CREATE INDEX IF NOT EXISTS idx_quizzes_user_id ON quizzes(user_id);
CREATE INDEX IF NOT EXISTS idx_quizzes_type ON quizzes(quiz_type);
CREATE INDEX IF NOT EXISTS idx_quiz_questions_quiz_id ON quiz_questions(quiz_id);
CREATE INDEX IF NOT EXISTS idx_quiz_question_options_question_id ON quiz_question_options(question_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_quiz_id ON quiz_attempts(quiz_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempt_answers_attempt_id ON quiz_attempt_answers(attempt_id);
CREATE INDEX IF NOT EXISTS idx_flashcard_progress_user_id ON flashcard_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_flashcard_progress_next_review ON flashcard_progress(next_review_date);


ALTER TABLE quizzes ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_question_options ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_attempt_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE flashcard_progress ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view their own quizzes" ON quizzes FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create their own quizzes" ON quizzes FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own quizzes" ON quizzes FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own quizzes" ON quizzes FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view questions for their quizzes" ON quiz_questions FOR SELECT USING (
    EXISTS (SELECT 1 FROM quizzes WHERE id = quiz_id AND user_id = auth.uid())
);
CREATE POLICY "Users can create questions for their quizzes" ON quiz_questions FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM quizzes WHERE id = quiz_id AND user_id = auth.uid())
);
CREATE POLICY "Users can update questions for their quizzes" ON quiz_questions FOR UPDATE USING (
    EXISTS (SELECT 1 FROM quizzes WHERE id = quiz_id AND user_id = auth.uid())
);
CREATE POLICY "Users can delete questions for their quizzes" ON quiz_questions FOR DELETE USING (
    EXISTS (SELECT 1 FROM quizzes WHERE id = quiz_id AND user_id = auth.uid())
);

CREATE POLICY "Users can view options for their quiz questions" ON quiz_question_options FOR SELECT USING (
    EXISTS (SELECT 1 FROM quiz_questions qq JOIN quizzes q ON qq.quiz_id = q.id WHERE qq.id = question_id AND q.user_id = auth.uid())
);
CREATE POLICY "Users can create options for their quiz questions" ON quiz_question_options FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM quiz_questions qq JOIN quizzes q ON qq.quiz_id = q.id WHERE qq.id = question_id AND q.user_id = auth.uid())
);
CREATE POLICY "Users can update options for their quiz questions" ON quiz_question_options FOR UPDATE USING (
    EXISTS (SELECT 1 FROM quiz_questions qq JOIN quizzes q ON qq.quiz_id = q.id WHERE qq.id = question_id AND q.user_id = auth.uid())
);
CREATE POLICY "Users can delete options for their quiz questions" ON quiz_question_options FOR DELETE USING (
    EXISTS (SELECT 1 FROM quiz_questions qq JOIN quizzes q ON qq.quiz_id = q.id WHERE qq.id = question_id AND q.user_id = auth.uid())
);

CREATE POLICY "Users can view their own quiz attempts" ON quiz_attempts FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create their own quiz attempts" ON quiz_attempts FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own quiz attempts" ON quiz_attempts FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view their own quiz attempt answers" ON quiz_attempt_answers FOR SELECT USING (
    EXISTS (SELECT 1 FROM quiz_attempts WHERE id = attempt_id AND user_id = auth.uid())
);
CREATE POLICY "Users can create their own quiz attempt answers" ON quiz_attempt_answers FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM quiz_attempts WHERE id = attempt_id AND user_id = auth.uid())
);
CREATE POLICY "Users can update their own quiz attempt answers" ON quiz_attempt_answers FOR UPDATE USING (
    EXISTS (SELECT 1 FROM quiz_attempts WHERE id = attempt_id AND user_id = auth.uid())
);

CREATE POLICY "Users can view their own flashcard progress" ON flashcard_progress FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create their own flashcard progress" ON flashcard_progress FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own flashcard progress" ON flashcard_progress FOR UPDATE USING (auth.uid() = user_id);


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_quizzes_updated_at BEFORE UPDATE ON quizzes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_quiz_questions_updated_at BEFORE UPDATE ON quiz_questions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
