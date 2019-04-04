# -*- coding:utf-8 -*- 


class ECPoint(object):
    """椭圆曲线上的点

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
        bmodn = bottom % n
        i = 1
        while True:
            if (i * bmodn) % n == 1:
                break
            i += 1
        return ((over % n) * i) % n

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
    
    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def get_order(self, G):
        """G should be an instance of this class """
        print("G is ({}, {})".format(G.x, G.y))
        for i in range(2, 15000):
            print("i is {}. i*G is ({},{})".format(i,(i*G).x, (i*G).y))
            if i * G == G:
                return i - 1
            
    
if __name__ == "__main__":
    a = ECPoint(3, 10)
    b = ECPoint(9, 7)
    c = ECPoint(17, 3)
    # print(22*a, " and ", 12*c)
    for i in range(30):
        print("{}c is({},{})".format(i, (i*c).x, (i*c).y))