
CREATE TABLE IF NOT EXISTS user_accessibility_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    screen_reader_enabled BOOLEAN DEFAULT FALSE,
    high_contrast_mode BOOLEAN DEFAULT FALSE,
    text_size VARCHAR(20) DEFAULT 'medium', -- small, medium, large, extra-large
    keyboard_navigation BOOLEAN DEFAULT TRUE,
    reduced_motion BOOLEAN DEFAULT FALSE,
    color_blind_friendly BOOLEAN DEFAULT FALSE,
    focus_indicators BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Create user_mobile_preferences table
CREATE TABLE IF NOT EXISTS user_mobile_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    offline_mode BOOLEAN DEFAULT FALSE,
    auto_sync BOOLEAN DEFAULT TRUE,
    sync_frequency INTEGER DEFAULT 15, -- minutes
    data_usage_limit INTEGER DEFAULT 100, -- MB per day
    push_notifications BOOLEAN DEFAULT TRUE,
    vibration_enabled BOOLEAN DEFAULT TRUE,
    haptic_feedback BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Create offline_data table for caching
CREATE TABLE IF NOT EXISTS offline_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    data_type VARCHAR(50) NOT NULL, -- topics, sessions, notes, attachments
    data_id UUID NOT NULL,
    data_content JSONB NOT NULL,
    last_synced TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_dirty BOOLEAN DEFAULT FALSE, -- has local changes not synced
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create device_sync table for cross-device synchronization
CREATE TABLE IF NOT EXISTS device_sync (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id VARCHAR(255) NOT NULL,
    device_name VARCHAR(255),
    device_type VARCHAR(50), -- mobile, tablet, desktop
    last_sync TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sync_token VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, device_id)
);

-- Create accessibility_audit_log table
CREATE TABLE IF NOT EXISTS accessibility_audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL, -- screen_reader_used, keyboard_navigation, high_contrast_toggle
    action_data JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_accessibility_preferences_user ON user_accessibility_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_user_mobile_preferences_user ON user_mobile_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_offline_data_user ON offline_data(user_id);
CREATE INDEX IF NOT EXISTS idx_offline_data_type ON offline_data(data_type);
CREATE INDEX IF NOT EXISTS idx_offline_data_dirty ON offline_data(is_dirty);
CREATE INDEX IF NOT EXISTS idx_device_sync_user ON device_sync(user_id);
CREATE INDEX IF NOT EXISTS idx_device_sync_device ON device_sync(device_id);
CREATE INDEX IF NOT EXISTS idx_accessibility_audit_user ON accessibility_audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_accessibility_audit_timestamp ON accessibility_audit_log(timestamp);

-- Enable RLS on all tables
ALTER TABLE user_accessibility_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_mobile_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE offline_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE device_sync ENABLE ROW LEVEL SECURITY;
ALTER TABLE accessibility_audit_log ENABLE ROW LEVEL SECURITY;

-- RLS policies for user_accessibility_preferences
CREATE POLICY "Users can view their own accessibility preferences" ON user_accessibility_preferences
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own accessibility preferences" ON user_accessibility_preferences
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own accessibility preferences" ON user_accessibility_preferences
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own accessibility preferences" ON user_accessibility_preferences
    FOR DELETE USING (auth.uid() = user_id);

-- RLS policies for user_mobile_preferences
CREATE POLICY "Users can view their own mobile preferences" ON user_mobile_preferences
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own mobile preferences" ON user_mobile_preferences
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own mobile preferences" ON user_mobile_preferences
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own mobile preferences" ON user_mobile_preferences
    FOR DELETE USING (auth.uid() = user_id);

-- RLS policies for offline_data
CREATE POLICY "Users can view their own offline data" ON offline_data
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own offline data" ON offline_data
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own offline data" ON offline_data
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own offline data" ON offline_data
    FOR DELETE USING (auth.uid() = user_id);

-- RLS policies for device_sync
CREATE POLICY "Users can view their own device sync data" ON device_sync
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own device sync data" ON device_sync
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own device sync data" ON device_sync
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own device sync data" ON device_sync
    FOR DELETE USING (auth.uid() = user_id);

-- RLS policies for accessibility_audit_log
CREATE POLICY "Users can view their own accessibility audit log" ON accessibility_audit_log
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own accessibility audit log" ON accessibility_audit_log
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Functions for mobile and accessibility features
CREATE OR REPLACE FUNCTION get_user_accessibility_preferences(p_user_id UUID)
RETURNS JSONB AS $$
DECLARE
    preferences RECORD;
BEGIN
    SELECT * INTO preferences FROM user_accessibility_preferences WHERE user_id = p_user_id;
    
    IF NOT FOUND THEN
        -- Create default preferences
        INSERT INTO user_accessibility_preferences (user_id) VALUES (p_user_id);
        SELECT * INTO preferences FROM user_accessibility_preferences WHERE user_id = p_user_id;
    END IF;
    
    RETURN jsonb_build_object(
        'screen_reader_enabled', preferences.screen_reader_enabled,
        'high_contrast_mode', preferences.high_contrast_mode,
        'text_size', preferences.text_size,
        'keyboard_navigation', preferences.keyboard_navigation,
        'reduced_motion', preferences.reduced_motion,
        'color_blind_friendly', preferences.color_blind_friendly,
        'focus_indicators', preferences.focus_indicators
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION update_user_accessibility_preferences(
    p_user_id UUID,
    p_screen_reader_enabled BOOLEAN DEFAULT NULL,
    p_high_contrast_mode BOOLEAN DEFAULT NULL,
    p_text_size VARCHAR DEFAULT NULL,
    p_keyboard_navigation BOOLEAN DEFAULT NULL,
    p_reduced_motion BOOLEAN DEFAULT NULL,
    p_color_blind_friendly BOOLEAN DEFAULT NULL,
    p_focus_indicators BOOLEAN DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Insert or update preferences
    INSERT INTO user_accessibility_preferences (
        user_id, screen_reader_enabled, high_contrast_mode, text_size,
        keyboard_navigation, reduced_motion, color_blind_friendly, focus_indicators
    ) VALUES (
        p_user_id, 
        COALESCE(p_screen_reader_enabled, FALSE),
        COALESCE(p_high_contrast_mode, FALSE),
        COALESCE(p_text_size, 'medium'),
        COALESCE(p_keyboard_navigation, TRUE),
        COALESCE(p_reduced_motion, FALSE),
        COALESCE(p_color_blind_friendly, FALSE),
        COALESCE(p_focus_indicators, TRUE)
    )
    ON CONFLICT (user_id) DO UPDATE SET
        screen_reader_enabled = COALESCE(p_screen_reader_enabled, user_accessibility_preferences.screen_reader_enabled),
        high_contrast_mode = COALESCE(p_high_contrast_mode, user_accessibility_preferences.high_contrast_mode),
        text_size = COALESCE(p_text_size, user_accessibility_preferences.text_size),
        keyboard_navigation = COALESCE(p_keyboard_navigation, user_accessibility_preferences.keyboard_navigation),
        reduced_motion = COALESCE(p_reduced_motion, user_accessibility_preferences.reduced_motion),
        color_blind_friendly = COALESCE(p_color_blind_friendly, user_accessibility_preferences.color_blind_friendly),
        focus_indicators = COALESCE(p_focus_indicators, user_accessibility_preferences.focus_indicators),
        updated_at = NOW();
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION get_user_mobile_preferences(p_user_id UUID)
RETURNS JSONB AS $$
DECLARE
    preferences RECORD;
BEGIN
    SELECT * INTO preferences FROM user_mobile_preferences WHERE user_id = p_user_id;
    
    IF NOT FOUND THEN
        -- Create default preferences
        INSERT INTO user_mobile_preferences (user_id) VALUES (p_user_id);
        SELECT * INTO preferences FROM user_mobile_preferences WHERE user_id = p_user_id;
    END IF;
    
    RETURN jsonb_build_object(
        'offline_mode', preferences.offline_mode,
        'auto_sync', preferences.auto_sync,
        'sync_frequency', preferences.sync_frequency,
        'data_usage_limit', preferences.data_usage_limit,
        'push_notifications', preferences.push_notifications,
        'vibration_enabled', preferences.vibration_enabled,
        'haptic_feedback', preferences.haptic_feedback
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION update_user_mobile_preferences(
    p_user_id UUID,
    p_offline_mode BOOLEAN DEFAULT NULL,
    p_auto_sync BOOLEAN DEFAULT NULL,
    p_sync_frequency INTEGER DEFAULT NULL,
    p_data_usage_limit INTEGER DEFAULT NULL,
    p_push_notifications BOOLEAN DEFAULT NULL,
    p_vibration_enabled BOOLEAN DEFAULT NULL,
    p_haptic_feedback BOOLEAN DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Insert or update preferences
    INSERT INTO user_mobile_preferences (
        user_id, offline_mode, auto_sync, sync_frequency, data_usage_limit,
        push_notifications, vibration_enabled, haptic_feedback
    ) VALUES (
        p_user_id,
        COALESCE(p_offline_mode, FALSE),
        COALESCE(p_auto_sync, TRUE),
        COALESCE(p_sync_frequency, 15),
        COALESCE(p_data_usage_limit, 100),
        COALESCE(p_push_notifications, TRUE),
        COALESCE(p_vibration_enabled, TRUE),
        COALESCE(p_haptic_feedback, TRUE)
    )
    ON CONFLICT (user_id) DO UPDATE SET
        offline_mode = COALESCE(p_offline_mode, user_mobile_preferences.offline_mode),
        auto_sync = COALESCE(p_auto_sync, user_mobile_preferences.auto_sync),
        sync_frequency = COALESCE(p_sync_frequency, user_mobile_preferences.sync_frequency),
        data_usage_limit = COALESCE(p_data_usage_limit, user_mobile_preferences.data_usage_limit),
        push_notifications = COALESCE(p_push_notifications, user_mobile_preferences.push_notifications),
        vibration_enabled = COALESCE(p_vibration_enabled, user_mobile_preferences.vibration_enabled),
        haptic_feedback = COALESCE(p_haptic_feedback, user_mobile_preferences.haptic_feedback),
        updated_at = NOW();
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION register_device(
    p_user_id UUID,
    p_device_id VARCHAR(255),
    p_device_name VARCHAR(255),
    p_device_type VARCHAR(50)
)
RETURNS VARCHAR(255) AS $$
DECLARE
    sync_token VARCHAR(255);
BEGIN
    -- Generate sync token
    sync_token := encode(gen_random_bytes(32), 'hex');
    
    -- Insert or update device
    INSERT INTO device_sync (user_id, device_id, device_name, device_type, sync_token)
    VALUES (p_user_id, p_device_id, p_device_name, p_device_type, sync_token)
    ON CONFLICT (user_id, device_id) DO UPDATE SET
        device_name = p_device_name,
        device_type = p_device_type,
        last_sync = NOW(),
        sync_token = sync_token,
        is_active = TRUE,
        updated_at = NOW();
    
    RETURN sync_token;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION log_accessibility_action(
    p_user_id UUID,
    p_action_type VARCHAR(50),
    p_action_data JSONB DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    INSERT INTO accessibility_audit_log (user_id, action_type, action_data)
    VALUES (p_user_id, p_action_type, p_action_data);
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create triggers for updated_at
CREATE TRIGGER update_user_accessibility_preferences_updated_at 
    BEFORE UPDATE ON user_accessibility_preferences 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_mobile_preferences_updated_at 
    BEFORE UPDATE ON user_mobile_preferences 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_offline_data_updated_at 
    BEFORE UPDATE ON offline_data 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_device_sync_updated_at 
    BEFORE UPDATE ON device_sync 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT EXECUTE ON FUNCTION get_user_accessibility_preferences(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION update_user_accessibility_preferences(UUID, BOOLEAN, BOOLEAN, VARCHAR, BOOLEAN, BOOLEAN, BOOLEAN, BOOLEAN) TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_mobile_preferences(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION update_user_mobile_preferences(UUID, BOOLEAN, BOOLEAN, INTEGER, INTEGER, BOOLEAN, BOOLEAN, BOOLEAN) TO authenticated;
GRANT EXECUTE ON FUNCTION register_device(UUID, VARCHAR, VARCHAR, VARCHAR) TO authenticated;
GRANT EXECUTE ON FUNCTION log_accessibility_action(UUID, VARCHAR, JSONB) TO authenticated;

-- Comments
COMMENT ON TABLE user_accessibility_preferences IS 'User accessibility preferences for screen readers, high contrast, etc.';
COMMENT ON TABLE user_mobile_preferences IS 'User mobile preferences for offline mode, sync settings, etc.';
COMMENT ON TABLE offline_data IS 'Cached data for offline access';
COMMENT ON TABLE device_sync IS 'Cross-device synchronization data';
COMMENT ON TABLE accessibility_audit_log IS 'Audit log for accessibility actions';
