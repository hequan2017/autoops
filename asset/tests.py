import base64
from Crypto.Cipher import AES
from Crypto import Random



BS = 16
key = "1234567890123456"
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.urlsafe_b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.urlsafe_b64decode(enc.encode('utf-8'))
        iv = enc[:BS]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[BS:]))

a = AESCipher(key=key)
b = a.encrypt(raw='123456')
b1 = b.decode()
print(b1,type(b),type(b1))

c = a.decrypt(enc='N4wGyzPTnggQtUr_gyGcsxMzU136thzPIc8y3mJ2uxg=')
print(c)