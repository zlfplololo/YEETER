import bcrypt
hashe = bcrypt.gensalt()
print(hashe)
psw = bcrypt.hashpw(b"pass", hashe)
print(psw)
