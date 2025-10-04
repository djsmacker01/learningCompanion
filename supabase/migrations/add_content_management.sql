



ALTER TABLE topics ADD COLUMN IF NOT EXISTS notes TEXT;
ALTER TABLE topics ADD COLUMN IF NOT EXISTS tags TEXT[];
ALTER TABLE topics ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;
ALTER TABLE topics ADD COLUMN IF NOT EXISTS last_modified TIMESTAMP WITH TIME ZONE DEFAULT NOW();


CREATE TABLE IF NOT EXISTS topic_attachments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    mime_type VARCHAR(100),
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS topic_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    note_type VARCHAR(50) DEFAULT 'general',
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS topic_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    notes TEXT,
    tags TEXT[],
    change_summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(topic_id, version_number)
);


CREATE TABLE IF NOT EXISTS topic_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL UNIQUE,
    color VARCHAR(7) DEFAULT '#3B82F6',
    description TEXT,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE INDEX IF NOT EXISTS idx_topics_tags ON topics USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_topics_version ON topics(version);
CREATE INDEX IF NOT EXISTS idx_topics_last_modified ON topics(last_modified);
CREATE INDEX IF NOT EXISTS idx_topic_attachments_topic_id ON topic_attachments(topic_id);
CREATE INDEX IF NOT EXISTS idx_topic_attachments_user_id ON topic_attachments(user_id);
CREATE INDEX IF NOT EXISTS idx_topic_attachments_file_type ON topic_attachments(file_type);
CREATE INDEX IF NOT EXISTS idx_topic_notes_topic_id ON topic_notes(topic_id);
CREATE INDEX IF NOT EXISTS idx_topic_notes_user_id ON topic_notes(user_id);
CREATE INDEX IF NOT EXISTS idx_topic_notes_type ON topic_notes(note_type);
CREATE INDEX IF NOT EXISTS idx_topic_versions_topic_id ON topic_versions(topic_id);
CREATE INDEX IF NOT EXISTS idx_topic_versions_version ON topic_versions(topic_id, version_number);
CREATE INDEX IF NOT EXISTS idx_topic_tags_name ON topic_tags(name);
CREATE INDEX IF NOT EXISTS idx_topic_tags_usage ON topic_tags(usage_count);


ALTER TABLE topic_attachments ENABLE ROW LEVEL SECURITY;
ALTER TABLE topic_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE topic_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE topic_tags ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view their own topic attachments" ON topic_attachments
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create attachments for their topics" ON topic_attachments
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own topic attachments" ON topic_attachments
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own topic attachments" ON topic_attachments
    FOR DELETE USING (auth.uid() = user_id);


CREATE POLICY "Users can view their own topic notes" ON topic_notes
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create notes for their topics" ON topic_notes
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own topic notes" ON topic_notes
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own topic notes" ON topic_notes
    FOR DELETE USING (auth.uid() = user_id);


CREATE POLICY "Users can view their own topic versions" ON topic_versions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create versions for their topics" ON topic_versions
    FOR INSERT WITH CHECK (auth.uid() = user_id);


CREATE POLICY "Anyone can view topic tags" ON topic_tags
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can create topic tags" ON topic_tags
    FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "Authenticated users can update topic tags" ON topic_tags
    FOR UPDATE USING (auth.uid() IS NOT NULL);


CREATE OR REPLACE FUNCTION create_topic_version(
    p_topic_id UUID,
    p_change_summary TEXT DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    new_version INTEGER;
    topic_data RECORD;
BEGIN

    SELECT title, description, notes, tags, version
    INTO topic_data
    FROM topics 
    WHERE id = p_topic_id AND user_id = auth.uid();
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Topic not found or access denied';
    END IF;
    

    new_version := topic_data.version + 1;
    

    INSERT INTO topic_versions (
        topic_id, user_id, version_number, title, description, 
        notes, tags, change_summary
    ) VALUES (
        p_topic_id, auth.uid(), new_version, topic_data.title, 
        topic_data.description, topic_data.notes, topic_data.tags, p_change_summary
    );
    

    UPDATE topics 
    SET version = new_version, last_modified = NOW()
    WHERE id = p_topic_id;
    
    RETURN new_version;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


CREATE OR REPLACE FUNCTION restore_topic_version(
    p_topic_id UUID,
    p_version_number INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    version_data RECORD;
BEGIN

    SELECT title, description, notes, tags
    INTO version_data
    FROM topic_versions 
    WHERE topic_id = p_topic_id AND version_number = p_version_number AND user_id = auth.uid();
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Version not found or access denied';
    END IF;
    

    PERFORM create_topic_version(p_topic_id, 'Restored from version ' || p_version_number);
    

    UPDATE topics 
    SET 
        title = version_data.title,
        description = version_data.description,
        notes = version_data.notes,
        tags = version_data.tags,
        last_modified = NOW()
    WHERE id = p_topic_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


CREATE OR REPLACE FUNCTION update_tag_usage()
RETURNS TRIGGER AS $$
BEGIN

    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN

        UPDATE topic_tags 
        SET usage_count = usage_count + 1 
        WHERE name = ANY(NEW.tags) AND name != ALL(COALESCE(OLD.tags, ARRAY[]::TEXT[]));
        

        UPDATE topic_tags 
        SET usage_count = GREATEST(usage_count - 1, 0) 
        WHERE name = ANY(COALESCE(OLD.tags, ARRAY[]::TEXT[])) AND name != ALL(NEW.tags);
    ELSIF TG_OP = 'DELETE' THEN

        UPDATE topic_tags 
        SET usage_count = GREATEST(usage_count - 1, 0) 
        WHERE name = ANY(COALESCE(OLD.tags, ARRAY[]::TEXT[]));
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_tag_usage_trigger
    AFTER INSERT OR UPDATE OR DELETE ON topics
    FOR EACH ROW EXECUTE FUNCTION update_tag_usage();


CREATE TRIGGER update_topic_attachments_updated_at 
    BEFORE UPDATE ON topic_attachments 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_topic_notes_updated_at 
    BEFORE UPDATE ON topic_notes 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


GRANT EXECUTE ON FUNCTION create_topic_version(UUID, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION restore_topic_version(UUID, INTEGER) TO authenticated;


INSERT INTO topic_tags (name, color, description) VALUES
('programming', '#3B82F6', 'Programming and coding topics'),
('mathematics', '#10B981', 'Math and quantitative subjects'),
('science', '#F59E0B', 'Scientific subjects and research'),
('language', '#EF4444', 'Language learning and linguistics'),
('history', '#8B5CF6', 'Historical topics and events'),
('art', '#EC4899', 'Art, design, and creative subjects'),
('business', '#06B6D4', 'Business and economics topics'),
('health', '#84CC16', 'Health and medical subjects')
ON CONFLICT (name) DO NOTHING;


COMMENT ON TABLE topic_attachments IS 'File attachments for topics';
COMMENT ON TABLE topic_notes IS 'Detailed notes for topics';
COMMENT ON TABLE topic_versions IS 'Version history for topics';
COMMENT ON TABLE topic_tags IS 'Available tags for categorizing topics';
COMMENT ON COLUMN topics.notes IS 'Quick notes for the topic';
COMMENT ON COLUMN topics.tags IS 'Tags for categorizing the topic';
COMMENT ON COLUMN topics.version IS 'Current version number';
COMMENT ON COLUMN topics.last_modified IS 'When the topic was last modified';
