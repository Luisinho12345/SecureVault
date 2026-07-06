from utils.constants import MIN_USERNAME_LENGTH, MIN_MASTER_PASSWORD_LENGTH


def validate_username(username):

    username = username.strip()

    if len(username) < MIN_USERNAME_LENGTH:
        return False, f"Username must be at least {MIN_USERNAME_LENGTH} characters."

    if not username.replace("_", "").isalnum():
        return False, "Username can only contain letters, numbers and underscores."

    return True, ""


def validate_master_password(password):

    if len(password) < MIN_MASTER_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_MASTER_PASSWORD_LENGTH} characters."

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."

    return True, ""
