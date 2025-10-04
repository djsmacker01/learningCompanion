
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total_xp INTEGER DEFAULT 0,
    current_level INTEGER DEFAULT 1,
    study_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    total_study_time_minutes INTEGER DEFAULT 0,
    badges_earned INTEGER DEFAULT 0,
    achievements_unlocked INTEGER DEFAULT 0,
    quizzes_completed INTEGER DEFAULT 0,
    topics_mastered INTEGER DEFAULT 0,
    last_activity_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);


CREATE TABLE IF NOT EXISTS badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('study', 'quiz', 'streak', 'achievement', 'special')),
    rarity VARCHAR(20) DEFAULT 'common' CHECK (rarity IN ('common', 'rare', 'epic', 'legendary')),
    xp_reward INTEGER DEFAULT 10,
    requirements JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS user_badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_id UUID NOT NULL REFERENCES badges(id) ON DELETE CASCADE,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, badge_id)
);


CREATE TABLE IF NOT EXISTS achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('study', 'quiz', 'streak', 'time', 'mastery', 'social')),
    xp_reward INTEGER DEFAULT 25,
    requirements JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS user_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    achievement_id UUID NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    progress JSONB DEFAULT '{}',
    UNIQUE(user_id, achievement_id)
);


CREATE TABLE IF NOT EXISTS xp_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    source VARCHAR(50) NOT NULL CHECK (source IN ('study_session', 'quiz_completion', 'badge_earned', 'achievement_unlocked', 'streak_milestone', 'daily_login')),
    source_id UUID,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS leaderboards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL CHECK (category IN ('total_xp', 'study_streak', 'quizzes_completed', 'study_time', 'topics_mastered')),
    rank INTEGER NOT NULL,
    value INTEGER NOT NULL,
    period VARCHAR(20) DEFAULT 'all_time' CHECK (period IN ('daily', 'weekly', 'monthly', 'all_time')),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, category, period)
);


CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_total_xp ON user_profiles(total_xp DESC);
CREATE INDEX IF NOT EXISTS idx_user_profiles_study_streak ON user_profiles(study_streak DESC);
CREATE INDEX IF NOT EXISTS idx_user_badges_user_id ON user_badges(user_id);
CREATE INDEX IF NOT EXISTS idx_user_badges_badge_id ON user_badges(badge_id);
CREATE INDEX IF NOT EXISTS idx_user_achievements_user_id ON user_achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_user_achievements_achievement_id ON user_achievements(achievement_id);
CREATE INDEX IF NOT EXISTS idx_xp_transactions_user_id ON xp_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_xp_transactions_created_at ON xp_transactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leaderboards_category_period ON leaderboards(category, period);
CREATE INDEX IF NOT EXISTS idx_leaderboards_rank ON leaderboards(category, period, rank);


ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE xp_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE leaderboards ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view their own profile" ON user_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update their own profile" ON user_profiles FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own profile" ON user_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Anyone can view badges" ON badges FOR SELECT USING (is_active = true);
CREATE POLICY "Users can view their own badges" ON user_badges FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own badges" ON user_badges FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Anyone can view achievements" ON achievements FOR SELECT USING (is_active = true);
CREATE POLICY "Users can view their own achievements" ON user_achievements FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update their own achievements" ON user_achievements FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own achievements" ON user_achievements FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own XP transactions" ON xp_transactions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own XP transactions" ON xp_transactions FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Anyone can view leaderboards" ON leaderboards FOR SELECT USING (true);
CREATE POLICY "Users can update their own leaderboard entries" ON leaderboards FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own leaderboard entries" ON leaderboards FOR INSERT WITH CHECK (auth.uid() = user_id);


CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_leaderboards_updated_at BEFORE UPDATE ON leaderboards FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


INSERT INTO badges (name, description, icon, category, rarity, xp_reward, requirements) VALUES

('First Steps', 'Complete your first study session', 'fas fa-baby', 'study', 'common', 10, '{"study_sessions": 1}'),
('Dedicated Learner', 'Complete 10 study sessions', 'fas fa-graduation-cap', 'study', 'common', 25, '{"study_sessions": 10}'),
('Study Master', 'Complete 50 study sessions', 'fas fa-crown', 'study', 'rare', 50, '{"study_sessions": 50}'),
('Study Legend', 'Complete 100 study sessions', 'fas fa-trophy', 'study', 'epic', 100, '{"study_sessions": 100}'),


('Getting Started', 'Maintain a 3-day study streak', 'fas fa-fire', 'streak', 'common', 15, '{"study_streak": 3}'),
('On Fire', 'Maintain a 7-day study streak', 'fas fa-fire', 'streak', 'common', 30, '{"study_streak": 7}'),
('Streak Master', 'Maintain a 30-day study streak', 'fas fa-fire', 'streak', 'rare', 75, '{"study_streak": 30}'),
('Unstoppable', 'Maintain a 100-day study streak', 'fas fa-fire', 'streak', 'legendary', 200, '{"study_streak": 100}'),


('Quiz Novice', 'Complete your first quiz', 'fas fa-question-circle', 'quiz', 'common', 15, '{"quizzes_completed": 1}'),
('Quiz Enthusiast', 'Complete 10 quizzes', 'fas fa-brain', 'quiz', 'common', 35, '{"quizzes_completed": 10}'),
('Quiz Master', 'Complete 25 quizzes', 'fas fa-medal', 'quiz', 'rare', 60, '{"quizzes_completed": 25}'),
('Quiz Legend', 'Complete 50 quizzes', 'fas fa-trophy', 'quiz', 'epic', 125, '{"quizzes_completed": 50}'),


('Speed Learner', 'Complete a quiz in under 5 minutes', 'fas fa-bolt', 'achievement', 'rare', 40, '{"quiz_time_under": 300}'),
('Perfectionist', 'Score 100% on a quiz', 'fas fa-star', 'achievement', 'rare', 50, '{"quiz_score": 100}'),
('Marathon Studier', 'Study for 2 hours in one session', 'fas fa-clock', 'achievement', 'epic', 75, '{"session_duration": 120}'),
('Topic Master', 'Master 5 different topics', 'fas fa-book', 'achievement', 'rare', 60, '{"topics_mastered": 5}'),


('Early Bird', 'Study before 6 AM', 'fas fa-sun', 'special', 'rare', 30, '{"study_time_before": "06:00"}'),
('Night Owl', 'Study after 10 PM', 'fas fa-moon', 'special', 'rare', 30, '{"study_time_after": "22:00"}'),
('Weekend Warrior', 'Study on both weekend days', 'fas fa-calendar-weekend', 'special', 'common', 25, '{"weekend_study": true}');


INSERT INTO achievements (name, description, icon, category, xp_reward, requirements) VALUES

('Study Habit', 'Study for 7 consecutive days', 'fas fa-calendar-check', 'study', 50, '{"consecutive_days": 7}'),
('Study Marathon', 'Study for 30 consecutive days', 'fas fa-calendar-alt', 'study', 150, '{"consecutive_days": 30}'),
('Time Master', 'Accumulate 100 hours of study time', 'fas fa-hourglass-half', 'time', 100, '{"total_hours": 100}'),
('Speed Reader', 'Complete 10 study sessions in one day', 'fas fa-tachometer-alt', 'study', 75, '{"sessions_per_day": 10}'),


('Quiz Champion', 'Score 90% or higher on 10 quizzes', 'fas fa-medal', 'quiz', 80, '{"high_scores": 10}'),
('Perfect Score', 'Score 100% on 5 different quizzes', 'fas fa-star', 'quiz', 100, '{"perfect_scores": 5}'),
('Quiz Marathon', 'Complete 20 quizzes in one week', 'fas fa-running', 'quiz', 120, '{"quizzes_per_week": 20}'),


('Subject Expert', 'Master 10 different topics', 'fas fa-graduation-cap', 'mastery', 150, '{"topics_mastered": 10}'),
('Knowledge Seeker', 'Create 25 quizzes', 'fas fa-plus-circle', 'mastery', 100, '{"quizzes_created": 25}'),
('Flashcard Master', 'Review 1000 flashcards', 'fas fa-lightbulb', 'mastery', 80, '{"flashcards_reviewed": 1000}'),


('Consistency King', 'Maintain a 14-day study streak', 'fas fa-fire', 'streak', 100, '{"study_streak": 14}'),
('Iron Will', 'Maintain a 60-day study streak', 'fas fa-dumbbell', 'streak', 250, '{"study_streak": 60}');
