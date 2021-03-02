# import credentials
from dotenv import load_dotenv
import os
load_dotenv()

username = os.getenv("iliad-username")
password = os.getenv("iliad-password")

import iliad

user = iliad.User(username,password)
print(user.data)