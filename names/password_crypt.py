#!/usr/bin/python
#_*_ coding:utf-8 _*_

from cryptography.fernet import Fernet

##  key = base64.urlsafe_b64encode(os.urandom(32))  生成key


## 如果修改了 下面的密钥key，请同步修改一下  webssh/main.py 中的，不然无法解密。

def  encrypt_p(password):## 加密
        f = Fernet('Ow2Qd11KeZS_ahNOMicpWUr3nu3RjOUYa0_GEuMDlOc=')
        p1 = password.encode()
        token = f.encrypt(p1)
        p2 = token.decode()
        return   p2

def  decrypt_p(password):  ## 解密
        f = Fernet('Ow2Qd11KeZS_ahNOMicpWUr3nu3RjOUYa0_GEuMDlOc=')
        p1 = password.encode()
        token = f.decrypt(p1)
        p2 = token.decode()
        return p2


def pyecharts_add(echa):
        """
         echarts 添加 自适应 宽度
        :param echa:
        :return:
        """
        a = echa.split('</div>')
        a1 = a[0].split('"')
        b = a1[3].split(';')
        a1[3] = b[1]
        div = '"'.join(a1)

        onresize = "    myChart_%s.resize(); " % (a1[1])
        ret = div + "</div>" + a[1]
        return ret,onresize





if  __name__=='__main__':
        a = encrypt_p('123')
        print(a)
        b = decrypt_p('gAAAAABaR3yZXkUbkFOJDa2h0EFprRoc5EsMjFLcKicUWAdQOTfX-cmbXXAv_d1S216QcHuT4zrV6zk4NO-tYBXlSyjl-1OaRw==')
        print(b)