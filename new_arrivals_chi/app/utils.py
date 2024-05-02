import re

# Reference: https://docs.kickbox.com/docs/python-validate-an-email-address
def validate_email_syntax(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Reference: ChatGPT supported regex
def validate_password(password):
    # 1+ lower case, 1+ upper case, 1+ number, 1+ special characters
    pattern = r'(?=.*[a-z]+)(?=.*[A-Z]+)(?=.*\d+)(?=.*[\W_]+).+'
    valid_characters =  re.fullmatch(pattern, password) is not None

    no_space = re.search(r'\s', password) is None
    
    return len(password) >= 8 and valid_characters and no_space
