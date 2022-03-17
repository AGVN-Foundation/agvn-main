import bcrypt

'''
  Last Updated: 18/06/2021 by Aaron

  Desc: Use bcrypt to hash the password, return the hashed password
'''

def hash_password(password):
  hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  print("DEBUG: generated password")
  return hashed


'''
  Last Updated: 18/06/2021 by Aaron
  
  Desc: check if the password matches with the hashed_pwd, return true or false.
'''
def check_password(password, hashed_pwd):
  return bcrypt.checkpw(password.encode('utf-8'), hashed_pwd)