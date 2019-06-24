# -*- coding: utf-8 -*-
# @Time : 2019/06
# @Author : 毛雨晴
# @学号：6020116126
# @班级：信管162
# @File : signature.py


import random
import hashlib


class ECPoint(object):
    """
    椭圆曲线上的点
    包含了椭圆曲线的信息，以及椭圆曲线上的点的运算
    """
    # p 建议取值为2的幂次左右

    def __init__(self, x, y, a=1, b=1, p=23):
        # if (x**3 + self.a*x + self.b) % self.p != (y**2) % self.p:
            # raise TypeError
        self.x = int(x)
        self.y = int(y)
        self.a = a
        self.b = b
        self.p = p

    def _fraction_mod(self, over, bottom, n):
        # 分数模除
        x1 = over % n 
        x2 = ( bottom**(n - 2)) % n
        return (x1 * x2) % n

        # bmodn = bottom % n
        # i = 1
        # while True:
        #     if (i * bmodn) % n == 1:
        #         break
        #     i += 1
        # return ((over % n) * i) % n

    def __add__(self, other):
        l = 0
        if self.x == other.x and self.y == other.y:
            l = self._fraction_mod(3*self.x*self.x + self.a, 2*self.y, self.p)
        else:
            # l = ((other.y - self.y) / (other.x - self.x)) % self.p
            l = self._fraction_mod(other.y - self.y, other.x - self.x, self.p)

        xr = (l**2 - self.x - other.x) % self.p
        yr = (l*(self.x - xr) - self.y) % self.p

        return ECPoint(xr, yr)

    def __mul__(self, times):
        if type(times) != int:
            raise TypeError
        point_to_return = ECPoint(self.x, self.y)
        point_self = ECPoint(self.x, self.y)
        for i in range(times - 1):
            point_to_return += point_self
        return point_to_return

    def __rmul__(self, times):
        return self.__mul__(times)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def get_order(self, G):
        """G should be an instance of this class """
        print("G is ({}, {})".format(G.x, G.y))
        for i in range(2, 15000):
            print("i is {}. i*G is ({},{})".format(i, (i*G).x, (i*G).y))
            if i * G == G:
                return i - 1


class Signature(object):
    """ 
    执行签名和验证程序
    """
    def __init__(self, a, b, G, n, pri_k):
        self.a = a
        self.b = b
        self.G = G
        self.n = n
        self.pri_k = pri_k
        self.pub_k = self.pri_k * G

    def get_public_key(self):
        return self.pub_k

    def _fraction_mod(self, over, bottom, n):
        # 分数模除
        x1 = over % n 
        x2 = ( bottom**(n - 2)) % n
        return (x1 * x2) % n
        
        # bmodn = bottom % n
        # i = 1
        # while True:
        #     if (i * bmodn) % n == 1:
        #         break
        #     i += 1
        # return ((over % n) * i) % n

    def sign(self, M):
        """Signature for Message"""
        e = int(hashlib.md5(M.encode("utf-8")).hexdigest(), 16)
        k = random.randint(1, self.n - 1)
        point = k * self.G
        r = (e + point.x) % self.n
        if r == 0 or r+k == self.n:
            return self.sign(M)
        s = self._fraction_mod((k - r*self.pri_k), (1 + self.pri_k), self.n)
        if s == 0:
            return self.sign(M)
        return M, r, s
    
    def verif(self, m, r, s, Public_key):
        if r not in range(1, self.n-1) and s not in range(1, self.n-1):
            print("verif faile")
            return False
        e = int(hashlib.md5(m.encode("utf-8")).hexdigest(), 16)
        print("e is {}".format(e))
        t = (r+s) % self.n
        if t == 0:
            return False
        print("s is {} and t is {} and the publickey is {},{}".format(s,t, Public_key.x, Public_key.y))
        point = s * self.G + t * Public_key 
        if (e+point.x) % self.n == r:
            return True
        else:
            return False


if __name__ == "__main__":
    a = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16)
    b = int("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16)
    p = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16)
    
    Gx = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7", 16)
    Gy = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0", 16)
    n = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)

    G = ECPoint(3, 10, a=1, b=1, p=23)

    Alise = Signature(G.a, G.b, G, 28, 2) 
    Bob = Signature(G.a, G.b, G, 28, 3)

    M, r, s = Alise.sign("aloha")
    print(" M is {} \n r is {} \n s is {}".format(M, r, s))

    print(Bob.verif("aloha", r, s, Alise.get_public_key()))



