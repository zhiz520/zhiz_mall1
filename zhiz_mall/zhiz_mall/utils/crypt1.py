from cryptography.fernet import Fernet


# 生成一个新的密钥
key = b'FwCKX-hn_zCoF6-zHdZpq2MOwqSl27FEULswle8osD8='

# 加密
def generate_encrypt(openid, key=key):
    # 实例化Fernet
    pher_suite = Fernet(key)
    # 加密
    encrypt_openid = pher_suite.encrypt(openid.encode())
    return encrypt_openid.decode()


# 解密
def generate_decrypt(token, key=key):
    # 实例化Fernet
    pher_suite = Fernet(key)
    # 解密
    try:
        openid = pher_suite.decrypt(token).decode()
        return openid
    except Exception:
        return None

if __name__ == '__main__':
    a = generate_encrypt('nagnaongagni')
    print(type(a))
    b = generate_decrypt(a)
    print(type(b), b)