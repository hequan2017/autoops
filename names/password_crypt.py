#!/usr/bin/python
#_*_ coding:utf-8 _*_

from cryptography.fernet import Fernet

##  key = base64.urlsafe_b64encode(os.urandom(32))  生成key


def  encrypt_p(password):
        f = Fernet('Ow2Qd11KeZS_ahNOMicpWUr3nu3RjOUYa0_GEuMDlOc=')
        p1 = password.encode()
        token = f.encrypt(p1)
        p2 = token.decode()
        return   p2

def  decrypt_p(password):
        f = Fernet('Ow2Qd11KeZS_ahNOMicpWUr3nu3RjOUYa0_GEuMDlOc=')
        p1 = password.encode()
        token = f.decrypt(p1)
        p2 = token.decode()
        return p2


