import random
import math
import sympy


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
        n = self.__calculate_n()
        if not n % 2:
            n += 1
        t = self.__calculate_t()
        for i in range(t):
            a = self.__get_random_a(n)
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


class CryptoHelper:
    @staticmethod
    def __get_number(number_length: int) -> int:
        min_val = 2 ** (number_length - 1)
        max_val = 2 ** number_length - 1
        return random.randint(min_val, max_val)

    @staticmethod
    def get_random_number_from_set_pseudo_squares(p, q):
        z = 2
        while True:
            z_p = sympy.jacobi_symbol(z, p)
            z_q = sympy.jacobi_symbol(z, q)
            if z_p == -1 and z_q == -1:
                return z
            z += 1


class GoldwasserMicali:
    def __init__(self, x: list, number_length: int):
        self.x = x
        self.number_length = number_length
        self.solovay_strassen = SolovayStrassenTest(number_length, 0.05)
        self.blum_integer, self.p_and_q = self.__get_blum_integer()
        self.z = CryptoHelper.get_random_number_from_set_pseudo_squares(self.p_and_q[0], self.p_and_q[1])

    def __get_blum_integer(self):
        p = self.solovay_strassen.get_prime()
        q = self.solovay_strassen.get_prime()
        while True:
            if p % 4 != 3:
                p = self.solovay_strassen.get_prime()
            if q % 4 != 3:
                q = self.solovay_strassen.get_prime()
            if p % 4 == 3 and q % 4 == 3:
                return p * q, [p, q]

    def encrypt(self):
        result = []
        for num in self.x:
            y = (pow(self.z, num) * pow(random.randrange(self.blum_integer), 2)) % self.blum_integer
            result.append(y)
        return result

    def decrypt(self, encrypted_x: list, p: int):
        result = []
        for num in encrypted_x:
            if sympy.jacobi_symbol(num, p) == -1:
                result.append(1)
            elif sympy.jacobi_symbol(num, p) == 1:
                result.append(0)
        return result


if __name__ == '__main__':
    gold_micali = GoldwasserMicali([1, 0, 1, 1, 0, 0], 16)
    a = gold_micali.encrypt()
    print(a)
    print(gold_micali.decrypt(a, gold_micali.p_and_q[0]))
