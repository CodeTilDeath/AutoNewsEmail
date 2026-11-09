import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
assert SECRET_KEY
FERNET = Fernet(SECRET_KEY)

sendEmail = ""
sendPassword = ""
receiveEmail = ""

encryptedEmail = FERNET.encrypt(sendEmail.encode()).decode()
encryptedPassword = FERNET.encrypt(sendPassword.encode()).decode()
encryptedREmail = FERNET.encrypt(receiveEmail.encode()).decode()

with open("Credentials.txt","a") as f:
    f.write(encryptedEmail + "\n") 
    f.write(encryptedPassword+ "\n")
    f.write(encryptedREmail+ "\n")