import secrets
import string

def merchantRefNum():
    alphabet = string.ascii_letters + string.digits
    ref = ''.join(secrets.choice(alphabet) for i in range(50))
    return ref
