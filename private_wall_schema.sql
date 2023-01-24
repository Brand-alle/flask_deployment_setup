-- SELECT messages.*, first_name, last_name, email, senders.created_at as sender_created_at, senders.updated_at as sender_updated_at FROM messages JOIN users as senders on messages.sender_id = senders.id
-- DELETE from messages WHERE messages.id = 7; 
-- INSERT INTO messages (content, created_at ,sender_id, recipient_id, user_id) VALUES ( "FSDDFS" ,now() , "1", "3" ,"1" );
-- SELECT messages.*, first_name, last_name, email, senders.created_at as sender_created_at, senders.updated_at as sender_updated_at FROM messages JOIN users as senders on messages.sender_id = senders.id
SELECT * FROM messages WHERE sender_id = 2