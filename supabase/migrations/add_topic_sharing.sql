
ALTER TABLE topics ADD COLUMN IF NOT EXISTS share_code VARCHAR(20) UNIQUE;
ALTER TABLE topics ADD COLUMN IF NOT EXISTS is_shared BOOLEAN DEFAULT FALSE;
ALTER TABLE topics ADD COLUMN IF NOT EXISTS shared_at TIMESTAMP WITH TIME ZONE;


CREATE TABLE IF NOT EXISTS topic_shares (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    share_code VARCHAR(20) NOT NULL UNIQUE,
    created_by UUID NOT NULL REFERENCES users(id),
    expires_at TIMESTAMP WITH TIME ZONE,
    max_uses INTEGER,
    use_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS shared_topic_access (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    share_code VARCHAR(20) NOT NULL,
    accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(topic_id, user_id)
);


CREATE INDEX IF NOT EXISTS idx_topics_share_code ON topics(share_code);
CREATE INDEX IF NOT EXISTS idx_topics_is_shared ON topics(is_shared);
CREATE INDEX IF NOT EXISTS idx_topic_shares_topic_id ON topic_shares(topic_id);
CREATE INDEX IF NOT EXISTS idx_topic_shares_share_code ON topic_shares(share_code);
CREATE INDEX IF NOT EXISTS idx_topic_shares_created_by ON topic_shares(created_by);
CREATE INDEX IF NOT EXISTS idx_shared_topic_access_topic_id ON shared_topic_access(topic_id);
CREATE INDEX IF NOT EXISTS idx_shared_topic_access_user_id ON shared_topic_access(user_id);
CREATE INDEX IF NOT EXISTS idx_shared_topic_access_share_code ON shared_topic_access(share_code);


ALTER TABLE topic_shares ENABLE ROW LEVEL SECURITY;
ALTER TABLE shared_topic_access ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view their own topic shares" ON topic_shares
    FOR SELECT USING (auth.uid() = created_by);

CREATE POLICY "Users can create topic shares for their topics" ON topic_shares
    FOR INSERT WITH CHECK (auth.uid() = created_by);

CREATE POLICY "Users can update their own topic shares" ON topic_shares
    FOR UPDATE USING (auth.uid() = created_by);

CREATE POLICY "Users can delete their own topic shares" ON topic_shares
    FOR DELETE USING (auth.uid() = created_by);

CREATE POLICY "Users can view their own shared topic access" ON shared_topic_access
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create shared topic access" ON shared_topic_access
    FOR INSERT WITH CHECK (auth.uid() = user_id);


DROP POLICY IF EXISTS "Users can view own topics" ON topics;
CREATE POLICY "Users can view own and shared topics" ON topics
    FOR SELECT USING (
        auth.uid() = user_id OR 
        EXISTS (
            SELECT 1 FROM shared_topic_access sta 
            WHERE sta.topic_id = topics.id AND sta.user_id = auth.uid()
        )
    );


CREATE OR REPLACE FUNCTION generate_share_code()
RETURNS VARCHAR(20) AS $$
DECLARE
    code VARCHAR(20);
    exists_count INTEGER;
BEGIN
    LOOP
     
        code := upper(substring(md5(random()::text) from 1 for 8));
        
        
        SELECT COUNT(*) INTO exists_count 
        FROM topic_shares 
        WHERE share_code = code;
        
       
        IF exists_count = 0 THEN
            RETURN code;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION share_topic(
    p_topic_id UUID,
    p_expires_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    p_max_uses INTEGER DEFAULT NULL
)
RETURNS VARCHAR(20) AS $$
DECLARE
    share_code VARCHAR(20);
    topic_owner UUID;
BEGIN
    
    SELECT user_id INTO topic_owner 
    FROM topics 
    WHERE id = p_topic_id AND is_active = TRUE;
    
    IF topic_owner != auth.uid() THEN
        RAISE EXCEPTION 'You can only share your own topics';
    END IF;
    
   
    share_code := generate_share_code();
    
    
    INSERT INTO topic_shares (topic_id, share_code, created_by, expires_at, max_uses)
    VALUES (p_topic_id, share_code, auth.uid(), p_expires_at, p_max_uses);
    
    UPDATE topics 
    SET is_shared = TRUE, share_code = share_code, shared_at = NOW()
    WHERE id = p_topic_id;
    
    RETURN share_code;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


CREATE OR REPLACE FUNCTION join_topic_with_code(p_share_code VARCHAR(20))
RETURNS UUID AS $$
DECLARE
    topic_id UUID;
    share_record RECORD;
BEGIN
  
    SELECT ts.*, t.id as topic_id
    INTO share_record
    FROM topic_shares ts
    JOIN topics t ON ts.topic_id = t.id
    WHERE ts.share_code = p_share_code 
    AND ts.is_active = TRUE 
    AND t.is_active = TRUE;
    
   
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Invalid or expired share code';
    END IF;
    
    
    IF share_record.expires_at IS NOT NULL AND share_record.expires_at < NOW() THEN
        RAISE EXCEPTION 'Share code has expired';
    END IF;
    
   
    IF share_record.max_uses IS NOT NULL AND share_record.use_count >= share_record.max_uses THEN
        RAISE EXCEPTION 'Share code has reached maximum uses';
    END IF;
    
    -
    IF EXISTS (
        SELECT 1 FROM shared_topic_access 
        WHERE topic_id = share_record.topic_id AND user_id = auth.uid()
    ) THEN
        RAISE EXCEPTION 'You already have access to this topic';
    END IF;
    
   
    INSERT INTO shared_topic_access (topic_id, user_id, share_code)
    VALUES (share_record.topic_id, auth.uid(), p_share_code);
    
   
    UPDATE topic_shares 
    SET use_count = use_count + 1, updated_at = NOW()
    WHERE id = share_record.id;
    
    RETURN share_record.topic_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


CREATE OR REPLACE FUNCTION revoke_topic_sharing(p_topic_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    topic_owner UUID;
BEGIN
    
    SELECT user_id INTO topic_owner 
    FROM topics 
    WHERE id = p_topic_id;
    
   
    IF topic_owner != auth.uid() THEN
        RAISE EXCEPTION 'You can only revoke sharing for your own topics';
    END IF;
    
   
    UPDATE topic_shares 
    SET is_active = FALSE, updated_at = NOW()
    WHERE topic_id = p_topic_id;
    
    
    UPDATE topics 
    SET is_shared = FALSE, share_code = NULL, shared_at = NULL
    WHERE id = p_topic_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION generate_share_code() TO authenticated;
GRANT EXECUTE ON FUNCTION share_topic(UUID, TIMESTAMP WITH TIME ZONE, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION join_topic_with_code(VARCHAR) TO authenticated;
GRANT EXECUTE ON FUNCTION revoke_topic_sharing(UUID) TO authenticated;


CREATE TRIGGER update_topic_shares_updated_at 
    BEFORE UPDATE ON topic_shares 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


COMMENT ON TABLE topic_shares IS 'Tracks shared topics with share codes';
COMMENT ON TABLE shared_topic_access IS 'Tracks which users have access to shared topics';
COMMENT ON COLUMN topics.share_code IS 'Unique code for sharing this topic';
COMMENT ON COLUMN topics.is_shared IS 'Whether this topic is currently shared';
COMMENT ON COLUMN topics.shared_at IS 'When this topic was first shared';
