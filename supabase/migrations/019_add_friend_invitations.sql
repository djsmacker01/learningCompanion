


CREATE TABLE IF NOT EXISTS friend_invitations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    inviter_id TEXT NOT NULL,
    invitee_email VARCHAR(255) NOT NULL,
    invitation_token VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    message TEXT,
    invited_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    accepted_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '30 days'),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_friend_invitations_inviter ON friend_invitations(inviter_id);
CREATE INDEX idx_friend_invitations_email ON friend_invitations(invitee_email);
CREATE INDEX idx_friend_invitations_token ON friend_invitations(invitation_token);
CREATE INDEX idx_friend_invitations_status ON friend_invitations(status);

