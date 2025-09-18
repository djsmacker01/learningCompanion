-- Migration: Create Reminder System Tables
-- Description: Tables for smart study reminders and scheduling

-- Study reminder preferences
CREATE TABLE IF NOT EXISTS study_reminder_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    is_enabled BOOLEAN DEFAULT true,
    reminder_methods TEXT[] DEFAULT ARRAY['email'], -- email, sms, push
    preferred_times TIME[] DEFAULT ARRAY[TIME '09:00', TIME '18:00'], -- Preferred reminder times
    timezone VARCHAR(50) DEFAULT 'UTC',
    frequency VARCHAR(20) DEFAULT 'daily', -- daily, weekly, custom
    days_of_week INTEGER[] DEFAULT ARRAY[1,2,3,4,5], -- 1=Monday, 7=Sunday
    study_goal_minutes INTEGER DEFAULT 30, -- Daily study goal
    advance_notice_minutes INTEGER DEFAULT 15, -- How far in advance to remind
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Study reminders (scheduled reminders)
CREATE TABLE IF NOT EXISTS study_reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL,
    reminder_type VARCHAR(50) DEFAULT 'study', -- study, quiz, review, custom
    reminder_method VARCHAR(20) DEFAULT 'email', -- email, sms, push
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, failed, cancelled
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    session_type VARCHAR(20), -- review, practice, quiz
    priority VARCHAR(10) DEFAULT 'medium', -- low, medium, high
    is_recurring BOOLEAN DEFAULT false,
    recurrence_pattern JSONB, -- For recurring reminders
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Study schedule (user's planned study sessions)
CREATE TABLE IF NOT EXISTS study_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    scheduled_start TIMESTAMP WITH TIME ZONE NOT NULL,
    scheduled_end TIMESTAMP WITH TIME ZONE NOT NULL,
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    session_type VARCHAR(20) DEFAULT 'review', -- review, practice, quiz
    priority VARCHAR(10) DEFAULT 'medium', -- low, medium, high
    is_recurring BOOLEAN DEFAULT false,
    recurrence_pattern JSONB, -- For recurring schedules
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, in_progress, completed, cancelled
    actual_start TIMESTAMP WITH TIME ZONE,
    actual_end TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Optimal study time suggestions (AI-generated)
CREATE TABLE IF NOT EXISTS optimal_study_times (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    suggested_time TIMESTAMP WITH TIME ZONE NOT NULL,
    confidence_score DECIMAL(3,2) DEFAULT 0.5, -- 0.0 to 1.0
    reasoning TEXT, -- Why this time is optimal
    factors JSONB, -- Factors considered (energy_level, past_performance, etc.)
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    session_type VARCHAR(20) DEFAULT 'review',
    is_accepted BOOLEAN DEFAULT false,
    accepted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Study patterns (for AI analysis)
CREATE TABLE IF NOT EXISTS study_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    pattern_type VARCHAR(50) NOT NULL, -- peak_hours, best_days, topic_preferences, etc.
    pattern_data JSONB NOT NULL, -- The actual pattern data
    confidence_score DECIMAL(3,2) DEFAULT 0.5,
    sample_size INTEGER DEFAULT 1, -- Number of sessions used to determine pattern
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, pattern_type) -- Each user can have only one pattern of each type
);

-- Reminder delivery logs
CREATE TABLE IF NOT EXISTS reminder_delivery_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reminder_id UUID NOT NULL REFERENCES study_reminders(id) ON DELETE CASCADE,
    delivery_method VARCHAR(20) NOT NULL, -- email, sms, push
    delivery_status VARCHAR(20) NOT NULL, -- sent, failed, bounced
    delivery_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    error_message TEXT,
    external_id VARCHAR(255), -- ID from email/SMS service
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_study_reminder_preferences_user_id ON study_reminder_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_study_reminders_user_id ON study_reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_study_reminders_scheduled_time ON study_reminders(scheduled_time);
CREATE INDEX IF NOT EXISTS idx_study_reminders_status ON study_reminders(status);
CREATE INDEX IF NOT EXISTS idx_study_schedules_user_id ON study_schedules(user_id);
CREATE INDEX IF NOT EXISTS idx_study_schedules_scheduled_start ON study_schedules(scheduled_start);
CREATE INDEX IF NOT EXISTS idx_study_schedules_status ON study_schedules(status);
CREATE INDEX IF NOT EXISTS idx_optimal_study_times_user_id ON optimal_study_times(user_id);
CREATE INDEX IF NOT EXISTS idx_optimal_study_times_suggested_time ON optimal_study_times(suggested_time);
CREATE INDEX IF NOT EXISTS idx_study_patterns_user_id ON study_patterns(user_id);
CREATE INDEX IF NOT EXISTS idx_study_patterns_pattern_type ON study_patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_reminder_delivery_logs_reminder_id ON reminder_delivery_logs(reminder_id);

-- RLS Policies
ALTER TABLE study_reminder_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE optimal_study_times ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_patterns ENABLE ROW LEVEL SECURITY;
ALTER TABLE reminder_delivery_logs ENABLE ROW LEVEL SECURITY;

-- RLS Policies for study_reminder_preferences
CREATE POLICY "Users can view their own reminder preferences" ON study_reminder_preferences
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own reminder preferences" ON study_reminder_preferences
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own reminder preferences" ON study_reminder_preferences
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own reminder preferences" ON study_reminder_preferences
    FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for study_reminders
CREATE POLICY "Users can view their own reminders" ON study_reminders
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own reminders" ON study_reminders
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own reminders" ON study_reminders
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own reminders" ON study_reminders
    FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for study_schedules
CREATE POLICY "Users can view their own schedules" ON study_schedules
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own schedules" ON study_schedules
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own schedules" ON study_schedules
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own schedules" ON study_schedules
    FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for optimal_study_times
CREATE POLICY "Users can view their own optimal study times" ON optimal_study_times
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own optimal study times" ON optimal_study_times
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own optimal study times" ON optimal_study_times
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own optimal study times" ON optimal_study_times
    FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for study_patterns
CREATE POLICY "Users can view their own study patterns" ON study_patterns
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own study patterns" ON study_patterns
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own study patterns" ON study_patterns
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own study patterns" ON study_patterns
    FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for reminder_delivery_logs
CREATE POLICY "Users can view their own reminder delivery logs" ON reminder_delivery_logs
    FOR SELECT USING (auth.uid() = (SELECT user_id FROM study_reminders WHERE id = reminder_id));

CREATE POLICY "Users can insert their own reminder delivery logs" ON reminder_delivery_logs
    FOR INSERT WITH CHECK (auth.uid() = (SELECT user_id FROM study_reminders WHERE id = reminder_id));

-- Sample data for testing
INSERT INTO study_reminder_preferences (user_id, is_enabled, reminder_methods, preferred_times, timezone, frequency, days_of_week, study_goal_minutes, advance_notice_minutes)
SELECT 
    u.id,
    true,
    ARRAY['email'],
    ARRAY[TIME '09:00', TIME '18:00'],
    'UTC',
    'daily',
    ARRAY[1,2,3,4,5],
    30,
    15
FROM users u
WHERE u.email = 'flask-test@example.com'
ON CONFLICT (user_id) DO NOTHING;

-- Sample study patterns
INSERT INTO study_patterns (user_id, pattern_type, pattern_data, confidence_score, sample_size)
SELECT 
    u.id,
    'peak_hours',
    '{"peak_hours": [9, 14, 20], "low_hours": [1, 2, 3, 4, 5, 6, 7, 8]}',
    0.7,
    5
FROM users u
WHERE u.email = 'flask-test@example.com'
ON CONFLICT (user_id, pattern_type) DO NOTHING;

INSERT INTO study_patterns (user_id, pattern_type, pattern_data, confidence_score, sample_size)
SELECT 
    u.id,
    'best_days',
    '{"best_days": ["Monday", "Wednesday", "Friday"], "worst_days": ["Sunday"]}',
    0.6,
    5
FROM users u
WHERE u.email = 'flask-test@example.com'
ON CONFLICT (user_id, pattern_type) DO NOTHING;
