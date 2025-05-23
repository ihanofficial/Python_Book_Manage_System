import os
salt = os.urandom(16).hex()  # 生成随机盐
print(salt)
print(type(salt))