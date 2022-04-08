import bcrypt


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password


email = "test@gmail.com"
password = "badPassword"

hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

newUser = User(email, hashed)

print(password)
print(newUser.password)

print(bcrypt.checkpw("test".encode("utf-8"), newUser.password))
