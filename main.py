import random
import math
import sympy
from sympy import Integer


class SolovayStrassenTest:
    def __init__(self, bit_length, reliability_parameter):
        self.bit_length = bit_length
        self.reliability_parameter = reliability_parameter

    def __calculate_n(self):
        min_val = 2 ** (self.bit_length - 1)
        max_val = 2 ** self.bit_length - 1
        return random.randint(min_val, max_val)

    def __calculate_t(self):
        t = 1
        while self.reliability_parameter <= 1/2 ** t:
            t += 1
        return t

    def __get_random_a(self, n):
        return random.randrange(2, n-1)
    
    def __pow(self, x, y, n):
        res = x
        for i in range(y):
            res = res * x % n
        return res

    def start(self):
        n = Integer(self.__calculate_n())
        if not n % 2:
            n += 1
        t = self.__calculate_t()
        for i in range(t):
            a = Integer(self.__get_random_a(n))
            if math.gcd(a, n) > 1:
                return n, f'{n} - составное'
            r = sympy.jacobi_symbol(a, n)
            if r < 0:
                r = r + n
            s = pow(a, (n-1)//2, n)
            if r != s:
                return n, f'{n} - составное'
        return n, f'{n} - простое с вероятностью {1 - 0.5 ** t}'

    def get_prime(self):
        while True:
            n, a = self.start()
            if sympy.isprime(n):
                return n
