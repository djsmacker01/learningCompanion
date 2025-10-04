



ALTER TABLE topics ADD COLUMN IF NOT EXISTS is_gcse BOOLEAN DEFAULT FALSE;
ALTER TABLE topics ADD COLUMN IF NOT EXISTS gcse_subject_id UUID;
ALTER TABLE topics ADD COLUMN IF NOT EXISTS gcse_topic_id UUID;
ALTER TABLE topics ADD COLUMN IF NOT EXISTS gcse_exam_board VARCHAR(100);
ALTER TABLE topics ADD COLUMN IF NOT EXISTS gcse_specification_code VARCHAR(50);
ALTER TABLE topics ADD COLUMN IF NOT EXISTS exam_weight INTEGER DEFAULT 1;
ALTER TABLE topics ADD COLUMN IF NOT EXISTS parent_topic_id UUID;



DO $$
BEGIN

    BEGIN
        ALTER TABLE topics ADD CONSTRAINT fk_topics_gcse_subject_id 
        FOREIGN KEY (gcse_subject_id) REFERENCES gcse_subjects(id) ON DELETE SET NULL;
    EXCEPTION
        WHEN undefined_table THEN

            NULL;
    END;
    

    BEGIN
        ALTER TABLE topics ADD CONSTRAINT fk_topics_gcse_topic_id 
        FOREIGN KEY (gcse_topic_id) REFERENCES gcse_topics(id) ON DELETE SET NULL;
    EXCEPTION
        WHEN undefined_table THEN

            NULL;
    END;
    

    BEGIN
        ALTER TABLE topics ADD CONSTRAINT fk_topics_parent_topic_id 
        FOREIGN KEY (parent_topic_id) REFERENCES topics(id) ON DELETE SET NULL;
    EXCEPTION
        WHEN duplicate_object THEN

            NULL;
    END;
END $$;


CREATE INDEX IF NOT EXISTS idx_topics_is_gcse ON topics(is_gcse);
CREATE INDEX IF NOT EXISTS idx_topics_gcse_subject_id ON topics(gcse_subject_id);
CREATE INDEX IF NOT EXISTS idx_topics_gcse_topic_id ON topics(gcse_topic_id);
CREATE INDEX IF NOT EXISTS idx_topics_parent_topic_id ON topics(parent_topic_id);
