FILENAME = "config_password_file.txt"  # can't use a password from the dictionary
PASSWORD_LEN = 5  # At least 10 characters ?
REQUIREMENTS = [("Upper", True), ("Lower", True), ("Digits", True), ("Special", True)]
HISTORY = 3  # can't use the 3 last passwords
LOGIN_ATTEMPTS = 3
MAIL_DOMAIN = False  # can't use the mail domain in the password
SPECIAL_CHARACTERS = "!@#$%^&*()"
