def validate_password_entry(website, username, password, category):

    if not website.strip():
        return False, "Website field cannot be empty."

    if not username.strip():
        return False, "Username field cannot be empty."

    if not password.strip():
        return False, "Password field cannot be empty."

    if not category.strip():
        return False, "Category field cannot be empty."

    return True, ""
