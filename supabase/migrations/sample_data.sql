
INSERT INTO users (id, email, username, password_hash, first_name, last_name, created_at, is_active) VALUES
    ('550e8400-e29b-41d4-a716-446655440001', 'john.doe@example.com', 'johndoe', '$2a$10$example_hash_1', 'John', 'Doe', NOW() - INTERVAL '30 days', TRUE),
    ('550e8400-e29b-41d4-a716-446655440002', 'jane.smith@example.com', 'janesmith', '$2a$10$example_hash_2', 'Jane', 'Smith', NOW() - INTERVAL '15 days', TRUE),
    ('550e8400-e29b-41d4-a716-446655440003', 'mike.wilson@example.com', 'mikewilson', '$2a$10$example_hash_3', 'Mike', 'Wilson', NOW() - INTERVAL '7 days', TRUE);


INSERT INTO topics (id, user_id, title, description, difficulty_level, target_sessions_per_week, created_at, is_active, color_tag) VALUES
  
    ('660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', 'Python Programming', 'Learning Python fundamentals and advanced concepts', 3, 4, NOW() - INTERVAL '25 days', TRUE, '#3B82F6'),
    ('660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440001', 'Machine Learning', 'Understanding ML algorithms and implementations', 4, 3, NOW() - INTERVAL '20 days', TRUE, '#10B981'),
    ('660e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440001', 'Web Development', 'Full-stack web development with React and Node.js', 2, 5, NOW() - INTERVAL '15 days', TRUE, '#F59E0B'),
    
    
    ('660e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440002', 'Data Science', 'Statistics, data analysis, and visualization', 3, 3, NOW() - INTERVAL '12 days', TRUE, '#8B5CF6'),
    ('660e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440002', 'SQL Database', 'Database design and query optimization', 2, 4, NOW() - INTERVAL '10 days', TRUE, '#EF4444'),
    
  
    ('660e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440003', 'JavaScript Fundamentals', 'Learning JavaScript from basics to advanced', 1, 5, NOW() - INTERVAL '5 days', TRUE, '#F97316');


INSERT INTO study_sessions (id, topic_id, user_id, session_date, duration_minutes, confidence_before, confidence_after, notes, session_type, completed, created_at) VALUES
    
    ('770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', CURRENT_DATE - INTERVAL '1 day', 45, 6, 8, 'Learned about list comprehensions and lambda functions', 'study', TRUE, NOW() - INTERVAL '1 day'),
    ('770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', CURRENT_DATE - INTERVAL '3 days', 60, 5, 7, 'Practiced object-oriented programming concepts', 'practice', TRUE, NOW() - INTERVAL '3 days'),
    ('770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', CURRENT_DATE - INTERVAL '5 days', 30, 4, 6, 'Reviewed basic syntax and data types', 'review', TRUE, NOW() - INTERVAL '5 days'),
    
   
    ('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440001', CURRENT_DATE - INTERVAL '2 days', 90, 3, 5, 'Studied linear regression and gradient descent', 'study', TRUE, NOW() - INTERVAL '2 days'),
    ('770e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440001', CURRENT_DATE - INTERVAL '6 days', 75, 2, 4, 'Introduction to supervised learning', 'study', TRUE, NOW() - INTERVAL '6 days'),
    
    ('770e8400-e29b-41d4-a716-446655440006', '660e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440002', CURRENT_DATE - INTERVAL '1 day', 50, 5, 7, 'Analyzed dataset with pandas and created visualizations', 'practice', TRUE, NOW() - INTERVAL '1 day'),
    ('770e8400-e29b-41d4-a716-446655440007', '660e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440002', CURRENT_DATE - INTERVAL '4 days', 40, 4, 6, 'Learned about statistical distributions', 'study', TRUE, NOW() - INTERVAL '4 days'),
    
  
    ('770e8400-e29b-41d4-a716-446655440008', '660e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440002', CURRENT_DATE - INTERVAL '2 days', 35, 6, 8, 'Practiced complex JOIN queries', 'practice', TRUE, NOW() - INTERVAL '2 days'),
    
    
    ('770e8400-e29b-41d4-a716-446655440009', '660e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440003', CURRENT_DATE - INTERVAL '1 day', 25, 3, 5, 'Learned about variables and data types', 'study', TRUE, NOW() - INTERVAL '1 day'),
    ('770e8400-e29b-41d4-a716-446655440010', '660e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440003', CURRENT_DATE - INTERVAL '3 days', 20, 2, 4, 'Introduction to JavaScript basics', 'study', TRUE, NOW() - INTERVAL '3 days');


INSERT INTO user_analytics (id, user_id, topic_id, total_study_time, total_sessions, current_streak, longest_streak, average_confidence_gain, last_session_date, next_recommended_date, mastery_level, updated_at) VALUES
    
    ('880e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', 135, 3, 1, 2, 2.33, CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE + INTERVAL '1 day', 2, NOW()),
    ('880e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440002', 165, 2, 1, 1, 2.00, CURRENT_DATE - INTERVAL '2 days', CURRENT_DATE + INTERVAL '1 day', 1, NOW()),
    ('880e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440003', 0, 0, 0, 0, 0.00, NULL, CURRENT_DATE + INTERVAL '1 day', 1, NOW()),
    
  
    ('880e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440004', 90, 2, 1, 1, 2.00, CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE + INTERVAL '1 day', 1, NOW()),
    ('880e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440005', 35, 1, 1, 1, 2.00, CURRENT_DATE - INTERVAL '2 days', CURRENT_DATE + INTERVAL '1 day', 1, NOW()),
    
   
    ('880e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440006', 45, 2, 1, 1, 2.00, CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE + INTERVAL '1 day', 1, NOW());


UPDATE users SET last_login = NOW() - INTERVAL '1 hour' WHERE id = '550e8400-e29b-41d4-a716-446655440001';
UPDATE users SET last_login = NOW() - INTERVAL '2 hours' WHERE id = '550e8400-e29b-41d4-a716-446655440002';
UPDATE users SET last_login = NOW() - INTERVAL '30 minutes' WHERE id = '550e8400-e29b-41d4-a716-446655440003';
