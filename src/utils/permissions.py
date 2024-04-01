
admins = []

def is_admin(user_id):
	if user_id in admins:
		return True
	return False