-- Add social features functionality
-- This migration adds friend connections, study groups, challenges, and social features

-- Create friends table for friend connections
CREATE TABLE IF NOT EXISTS friends (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    friend_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending', -- pending, accepted, blocked
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, friend_id)
);

-- Create study_groups table
CREATE TABLE IF NOT EXISTS study_groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    creator_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_public BOOLEAN DEFAULT TRUE,
    max_members INTEGER DEFAULT 50,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create study_group_members table
CREATE TABLE IF NOT EXISTS study_group_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member', -- member, moderator, admin
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'active', -- active, inactive, banned
    UNIQUE(group_id, user_id)
);

-- Create study_group_topics table (topics shared in groups)
CREATE TABLE IF NOT EXISTS study_group_topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    shared_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    shared_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_pinned BOOLEAN DEFAULT FALSE,
    UNIQUE(group_id, topic_id)
);

-- Create social_challenges table
CREATE TABLE IF NOT EXISTS social_challenges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    challenge_type VARCHAR(50) NOT NULL, -- study_time, streak, quiz_score, topic_completion
    target_value INTEGER NOT NULL, -- e.g., 120 (minutes), 7 (days), 85 (score), 5 (topics)
    target_unit VARCHAR(20), -- minutes, days, score, topics
    creator_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    group_id UUID REFERENCES study_groups(id) ON DELETE CASCADE, -- NULL for global challenges
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create challenge_participants table
CREATE TABLE IF NOT EXISTS challenge_participants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    challenge_id UUID NOT NULL REFERENCES social_challenges(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    current_progress INTEGER DEFAULT 0,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(challenge_id, user_id)
);

-- Create social_achievements table (for sharing achievements)
CREATE TABLE IF NOT EXISTS social_achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    achievement_type VARCHAR(50) NOT NULL, -- badge_earned, level_up, streak_milestone, challenge_completed
    achievement_data JSONB, -- stores specific achievement details
    is_shared BOOLEAN DEFAULT FALSE,
    shared_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create social_activity table (activity feed)
CREATE TABLE IF NOT EXISTS social_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL, -- friend_request, group_join, challenge_join, achievement_shared, study_session
    activity_data JSONB, -- stores activity-specific data
    target_user_id UUID REFERENCES users(id) ON DELETE CASCADE, -- for activities involving other users
    group_id UUID REFERENCES study_groups(id) ON DELETE CASCADE, -- for group activities
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create study_sessions_social table (for study with friends)
CREATE TABLE IF NOT EXISTS study_sessions_social (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES study_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_public BOOLEAN DEFAULT FALSE,
    shared_with_friends BOOLEAN DEFAULT FALSE,
    shared_with_group_id UUID REFERENCES study_groups(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_friends_user_id ON friends(user_id);
CREATE INDEX IF NOT EXISTS idx_friends_friend_id ON friends(friend_id);
CREATE INDEX IF NOT EXISTS idx_friends_status ON friends(status);
CREATE INDEX IF NOT EXISTS idx_study_groups_creator ON study_groups(creator_id);
CREATE INDEX IF NOT EXISTS idx_study_groups_public ON study_groups(is_public);
CREATE INDEX IF NOT EXISTS idx_study_group_members_group ON study_group_members(group_id);
CREATE INDEX IF NOT EXISTS idx_study_group_members_user ON study_group_members(user_id);
CREATE INDEX IF NOT EXISTS idx_study_group_members_role ON study_group_members(role);
CREATE INDEX IF NOT EXISTS idx_study_group_topics_group ON study_group_topics(group_id);
CREATE INDEX IF NOT EXISTS idx_study_group_topics_topic ON study_group_topics(topic_id);
CREATE INDEX IF NOT EXISTS idx_social_challenges_creator ON social_challenges(creator_id);
CREATE INDEX IF NOT EXISTS idx_social_challenges_group ON social_challenges(group_id);
CREATE INDEX IF NOT EXISTS idx_social_challenges_active ON social_challenges(is_active);
CREATE INDEX IF NOT EXISTS idx_social_challenges_dates ON social_challenges(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_challenge_participants_challenge ON challenge_participants(challenge_id);
CREATE INDEX IF NOT EXISTS idx_challenge_participants_user ON challenge_participants(user_id);
CREATE INDEX IF NOT EXISTS idx_challenge_participants_completed ON challenge_participants(is_completed);
CREATE INDEX IF NOT EXISTS idx_social_achievements_user ON social_achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_social_achievements_shared ON social_achievements(is_shared);
CREATE INDEX IF NOT EXISTS idx_social_activity_user ON social_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_social_activity_type ON social_activity(activity_type);
CREATE INDEX IF NOT EXISTS idx_social_activity_created ON social_activity(created_at);
CREATE INDEX IF NOT EXISTS idx_study_sessions_social_session ON study_sessions_social(session_id);
CREATE INDEX IF NOT EXISTS idx_study_sessions_social_user ON study_sessions_social(user_id);

-- Enable RLS on all tables
ALTER TABLE friends ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_group_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_group_topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_challenges ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_activity ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_sessions_social ENABLE ROW LEVEL SECURITY;

-- RLS policies for friends
CREATE POLICY "Users can view their own friend relationships" ON friends
    FOR SELECT USING (auth.uid() = user_id OR auth.uid() = friend_id);

CREATE POLICY "Users can create friend requests" ON friends
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own friend relationships" ON friends
    FOR UPDATE USING (auth.uid() = user_id OR auth.uid() = friend_id);

CREATE POLICY "Users can delete their own friend relationships" ON friends
    FOR DELETE USING (auth.uid() = user_id OR auth.uid() = friend_id);

-- RLS policies for study_groups
CREATE POLICY "Anyone can view public study groups" ON study_groups
    FOR SELECT USING (is_public = TRUE OR auth.uid() = creator_id);

CREATE POLICY "Users can create study groups" ON study_groups
    FOR INSERT WITH CHECK (auth.uid() = creator_id);

CREATE POLICY "Group creators can update their groups" ON study_groups
    FOR UPDATE USING (auth.uid() = creator_id);

CREATE POLICY "Group creators can delete their groups" ON study_groups
    FOR DELETE USING (auth.uid() = creator_id);

-- RLS policies for study_group_members
CREATE POLICY "Users can view group memberships" ON study_group_members
    FOR SELECT USING (
        auth.uid() = user_id OR 
        EXISTS (SELECT 1 FROM study_groups WHERE id = group_id AND (is_public = TRUE OR creator_id = auth.uid()))
    );

CREATE POLICY "Users can join groups" ON study_group_members
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own memberships" ON study_group_members
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can leave groups" ON study_group_members
    FOR DELETE USING (auth.uid() = user_id);

-- RLS policies for study_group_topics
CREATE POLICY "Group members can view shared topics" ON study_group_topics
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM study_group_members WHERE group_id = study_group_topics.group_id AND user_id = auth.uid())
    );

CREATE POLICY "Group members can share topics" ON study_group_topics
    FOR INSERT WITH CHECK (
        auth.uid() = shared_by AND
        EXISTS (SELECT 1 FROM study_group_members WHERE group_id = study_group_topics.group_id AND user_id = auth.uid())
    );

CREATE POLICY "Topic sharers can remove their shares" ON study_group_topics
    FOR DELETE USING (auth.uid() = shared_by);

-- RLS policies for social_challenges
CREATE POLICY "Anyone can view active challenges" ON social_challenges
    FOR SELECT USING (is_active = TRUE);

CREATE POLICY "Users can create challenges" ON social_challenges
    FOR INSERT WITH CHECK (auth.uid() = creator_id);

CREATE POLICY "Challenge creators can update their challenges" ON social_challenges
    FOR UPDATE USING (auth.uid() = creator_id);

CREATE POLICY "Challenge creators can delete their challenges" ON social_challenges
    FOR DELETE USING (auth.uid() = creator_id);

-- RLS policies for challenge_participants
CREATE POLICY "Users can view their own participation" ON challenge_participants
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can join challenges" ON challenge_participants
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own participation" ON challenge_participants
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can leave challenges" ON challenge_participants
    FOR DELETE USING (auth.uid() = user_id);

-- RLS policies for social_achievements
CREATE POLICY "Users can view their own achievements" ON social_achievements
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create achievements" ON social_achievements
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own achievements" ON social_achievements
    FOR UPDATE USING (auth.uid() = user_id);

-- RLS policies for social_activity
CREATE POLICY "Users can view their own activity" ON social_activity
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create activity" ON social_activity
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- RLS policies for study_sessions_social
CREATE POLICY "Users can view their own social sessions" ON study_sessions_social
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create social sessions" ON study_sessions_social
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own social sessions" ON study_sessions_social
    FOR UPDATE USING (auth.uid() = user_id);

-- Functions for social features
CREATE OR REPLACE FUNCTION send_friend_request(p_friend_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    -- Check if friend request already exists
    IF EXISTS (SELECT 1 FROM friends WHERE user_id = auth.uid() AND friend_id = p_friend_id) THEN
        RAISE EXCEPTION 'Friend request already exists';
    END IF;
    
    -- Check if reverse friend request exists
    IF EXISTS (SELECT 1 FROM friends WHERE user_id = p_friend_id AND friend_id = auth.uid()) THEN
        RAISE EXCEPTION 'Friend request already exists from this user';
    END IF;
    
    -- Create friend request
    INSERT INTO friends (user_id, friend_id, status) VALUES (auth.uid(), p_friend_id, 'pending');
    
    -- Log activity
    INSERT INTO social_activity (user_id, activity_type, activity_data, target_user_id)
    VALUES (auth.uid(), 'friend_request', jsonb_build_object('friend_id', p_friend_id), p_friend_id);
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION accept_friend_request(p_user_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    -- Update the friend request
    UPDATE friends 
    SET status = 'accepted', updated_at = NOW()
    WHERE user_id = p_user_id AND friend_id = auth.uid() AND status = 'pending';
    
    -- Create reverse friendship
    INSERT INTO friends (user_id, friend_id, status) 
    VALUES (auth.uid(), p_user_id, 'accepted')
    ON CONFLICT (user_id, friend_id) DO NOTHING;
    
    -- Log activity
    INSERT INTO social_activity (user_id, activity_type, activity_data, target_user_id)
    VALUES (auth.uid(), 'friend_accepted', jsonb_build_object('friend_id', p_user_id), p_user_id);
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION join_study_group(p_group_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    group_data RECORD;
    member_count INTEGER;
BEGIN
    -- Get group info
    SELECT * INTO group_data FROM study_groups WHERE id = p_group_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Study group not found';
    END IF;
    
    -- Check if group is full
    SELECT COUNT(*) INTO member_count FROM study_group_members WHERE group_id = p_group_id AND status = 'active';
    
    IF member_count >= group_data.max_members THEN
        RAISE EXCEPTION 'Study group is full';
    END IF;
    
    -- Add user to group
    INSERT INTO study_group_members (group_id, user_id, role) 
    VALUES (p_group_id, auth.uid(), 'member')
    ON CONFLICT (group_id, user_id) DO UPDATE SET status = 'active';
    
    -- Log activity
    INSERT INTO social_activity (user_id, activity_type, activity_data, group_id)
    VALUES (auth.uid(), 'group_join', jsonb_build_object('group_id', p_group_id), p_group_id);
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION join_challenge(p_challenge_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    challenge_data RECORD;
BEGIN
    -- Get challenge info
    SELECT * INTO challenge_data FROM social_challenges WHERE id = p_challenge_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Challenge not found';
    END IF;
    
    IF NOT challenge_data.is_active THEN
        RAISE EXCEPTION 'Challenge is not active';
    END IF;
    
    IF NOW() > challenge_data.end_date THEN
        RAISE EXCEPTION 'Challenge has ended';
    END IF;
    
    -- Add user to challenge
    INSERT INTO challenge_participants (challenge_id, user_id) 
    VALUES (p_challenge_id, auth.uid())
    ON CONFLICT (challenge_id, user_id) DO NOTHING;
    
    -- Log activity
    INSERT INTO social_activity (user_id, activity_type, activity_data)
    VALUES (auth.uid(), 'challenge_join', jsonb_build_object('challenge_id', p_challenge_id));
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION update_challenge_progress(p_challenge_id UUID, p_progress INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    challenge_data RECORD;
    is_completed BOOLEAN := FALSE;
BEGIN
    -- Get challenge info
    SELECT * INTO challenge_data FROM social_challenges WHERE id = p_challenge_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Challenge not found';
    END IF;
    
    -- Check if progress meets target
    IF p_progress >= challenge_data.target_value THEN
        is_completed := TRUE;
    END IF;
    
    -- Update progress
    UPDATE challenge_participants 
    SET 
        current_progress = p_progress,
        is_completed = is_completed,
        completed_at = CASE WHEN is_completed AND completed_at IS NULL THEN NOW() ELSE completed_at END
    WHERE challenge_id = p_challenge_id AND user_id = auth.uid();
    
    -- Log completion activity
    IF is_completed THEN
        INSERT INTO social_activity (user_id, activity_type, activity_data)
        VALUES (auth.uid(), 'challenge_completed', jsonb_build_object('challenge_id', p_challenge_id, 'progress', p_progress));
    END IF;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant permissions
GRANT EXECUTE ON FUNCTION send_friend_request(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION accept_friend_request(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION join_study_group(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION join_challenge(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION update_challenge_progress(UUID, INTEGER) TO authenticated;

-- Create triggers for updated_at
CREATE TRIGGER update_friends_updated_at 
    BEFORE UPDATE ON friends 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_study_groups_updated_at 
    BEFORE UPDATE ON study_groups 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments
COMMENT ON TABLE friends IS 'Friend connections between users';
COMMENT ON TABLE study_groups IS 'Study groups for collaborative learning';
COMMENT ON TABLE study_group_members IS 'Membership in study groups';
COMMENT ON TABLE study_group_topics IS 'Topics shared within study groups';
COMMENT ON TABLE social_challenges IS 'Social challenges for motivation';
COMMENT ON TABLE challenge_participants IS 'User participation in challenges';
COMMENT ON TABLE social_achievements IS 'Shared achievements and milestones';
COMMENT ON TABLE social_activity IS 'Social activity feed';
COMMENT ON TABLE study_sessions_social IS 'Social study session sharing';
