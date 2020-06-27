from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

#Password encryption 
def encrypt_password(password):
    return pwd_context.encrypt(password)

#Verification of original password matches with encrypted password which returns boolean value
def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)

