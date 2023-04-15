import os

current_path = os.getcwd()

with open(os.path.join(current_path, "shutter_api", "Keys", "SQL.key"), "r") as f:
    SQL_KEY = f.read()

with open(os.path.join(current_path, "shutter_api", "Keys", "jwt.key"), "r") as f:
    JWT_KEY = f.read()

with open(os.path.join(current_path, "shutter_api", "Keys", "Encryption.key"), "r") as f:
    ENCRYPTION_KEY = f.read().encode("utf-8")

with open(os.path.join(current_path, "shutter_api", "Keys", "SQL_encryption.key"), "r") as f:
    SQL_ENCRYPTION_KEY = f.read().encode("utf-8")
