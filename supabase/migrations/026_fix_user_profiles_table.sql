




ALTER TABLE user_profiles 
ADD COLUMN IF NOT EXISTS first_name VARCHAR(100),
ADD COLUMN IF NOT EXISTS last_name VARCHAR(100),
ADD COLUMN IF NOT EXISTS avatar_url TEXT,
ADD COLUMN IF NOT EXISTS bio TEXT,
ADD COLUMN IF NOT EXISTS timezone VARCHAR(50) DEFAULT 'UTC',
ADD COLUMN IF NOT EXISTS language VARCHAR(10) DEFAULT 'en',
ADD COLUMN IF NOT EXISTS email_notifications BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS sms_notifications BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS study_reminders BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS privacy_level VARCHAR(20) DEFAULT 'private';


UPDATE user_profiles 
SET 
    first_name = 'User',
    last_name = 'Name',
    timezone = 'UTC',
    language = 'en',
    email_notifications = true,
    sms_notifications = false,
    study_reminders = true,
    privacy_level = 'private'
WHERE first_name IS NULL;


COMMENT ON COLUMN user_profiles.first_name IS 'User first name';
COMMENT ON COLUMN user_profiles.last_name IS 'User last name';
COMMENT ON COLUMN user_profiles.avatar_url IS 'URL to user avatar image';
COMMENT ON COLUMN user_profiles.bio IS 'User biography/description';
COMMENT ON COLUMN user_profiles.timezone IS 'User timezone for scheduling';
COMMENT ON COLUMN user_profiles.language IS 'User preferred language';
COMMENT ON COLUMN user_profiles.email_notifications IS 'Enable email notifications';
COMMENT ON COLUMN user_profiles.sms_notifications IS 'Enable SMS notifications';
COMMENT ON COLUMN user_profiles.study_reminders IS 'Enable study reminders';
COMMENT ON COLUMN user_profiles.privacy_level IS 'Privacy level: private, friends, public';


CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_privacy_level ON user_profiles(privacy_level);
CREATE INDEX IF NOT EXISTS idx_user_profiles_timezone ON user_profiles(timezone);
CREATE INDEX IF NOT EXISTS idx_user_profiles_language ON user_profiles(language);














