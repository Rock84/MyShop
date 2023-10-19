from re import compile


PASSWORD_EMAIL = compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}$")
MOBIL_NUMBER = compile(r"^\\+?[1-9][0-9]{7,14}$")

def password_validator(v: str) -> str:
    if PASSWORD_EMAIL.fullmatch(v) is None:
        raise ValueError('Incorrect password')
    return v

def is_alpha(v: str) -> str:
    if not v.isalpha():
        raise ValueError('Not only letters')
    return v

def is_mobile_number(v: str) -> str:
    if MOBIL_NUMBER.fullmatch(v) is None:
        raise ValueError("Incorrect mobile number")
    return v
