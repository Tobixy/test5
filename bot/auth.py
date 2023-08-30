def is_authorized(user_id):
    authorized_ids = [123456789, 987654321]  # Replace with actual authorized user IDs
    return user_id in authorized_ids

def is_developer(user_id):
    developer_ids = [987654321]  # Replace with actual developer user IDs
    return user_id in developer_ids
