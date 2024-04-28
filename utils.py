import re
from config import ENABLE_REMOTE_CODE_MITIGATION

def validate_username(username):
    if not ENABLE_REMOTE_CODE_MITIGATION:
        return username
    # Check if the username contains only alphanumeric characters
    if re.match(r"^[a-zA-Z0-9]+$", username):
        return username
    else:
        raise ValueError("Username should only contain [a-zA-Z0-9]")

def validate_password(password):
    if not ENABLE_REMOTE_CODE_MITIGATION:
        return password 
    if len(password) < 8 or len(password) > 40:
        raise ValueError("Password should be within 8 to 40 characters")
    # Check for no whitespace or punctuation
    if re.search(r'\s|[^a-zA-Z0-9@_]', password):
        raise ValueError("Password should only contain [a-zA-Z0-9@_]")
    # Add more conditions as needed (e.g., special characters)
    return password 

def validate_input(user_input):
    if not ENABLE_REMOTE_CODE_MITIGATION:
        return user_input
    if len(user_input) > 100:
        return ValueError("Too long input, maximum length 100 characters") 
    # Check if the input contains only alphanumeric characters, underscores, and at symbols
    if re.match(r"^[a-zA-Z0-9_@]+$", user_input):
        return user_input
    else:
        return ValueError("Too long input, maximum length 100 characters") 
