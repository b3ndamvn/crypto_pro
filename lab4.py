"""
Подбрасывание монеты на основании проблемы дискретного логарифмирования с безусловной связанностью (вар. 1)
"""

import random

from main import SolovayStrassenTest
from lab3 import find_generator


def generate_protocol_parameters(key_length):
    s_s_test = SolovayStrassenTest(key_length, 0.05)
    p = s_s_test.get_prime()
    g = find_generator(p)
    return p, g


def binding_stage(p, g):
    bit = random.randint(0, 1)
    x = random.randint(0, p)
    if bit == 0:
        if x % 2:
            x //= 2
    else:
        if not x % 2:
            x += 1

    r = pow(g, x, p)
    return x, r


if __name__ == '__main__':
    p, g = generate_protocol_parameters(15)
    x, r = binding_stage(p, g)
    print(r)
    print(r == pow(g, x, p))
