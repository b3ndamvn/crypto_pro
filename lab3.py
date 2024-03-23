import random
import sympy


# Функция для вычисления наибольшего общего делителя
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def find_generator(p):
    r = 1
    s = p - 1
    while True:
        if not p - 1 % 2:
            r *= 2
            s //= 2
        else:
            break
    while True:
        g = random.randint(2, p-2)
        if pow(g, r, p) != 1 and pow(g, p - 1 // 2, p) != 1:
            return g


def get_random_from_z_star(p: int):
    while True:
        g = random.randint(1, p + 1)
        if gcd(p, g) == 1:
            return g


# Функция для генерации ключей
def generate_keys(key_length):
    from main import SolovayStrassenTest
    test = SolovayStrassenTest(key_length, 0.05)
    p = int(test.get_prime())  # простое число p
    g = find_generator(p)  # Выбираем случайное число g < p
    e = random.randint(2, p - 2)  # Закрытый ключ e
    d = pow(g, e, int(p))  # Открытый ключ d
    return p, g, d, e


# Функция для подписи сообщения
def sign_message(message, p, g, e):
    k = get_random_from_z_star(p - 1)
    y1 = pow(g, k, p)
    k_inv = sympy.mod_inverse(k, p - 1)  # Находим обратный элемент для k по модулю p - 1
    y2 = (k_inv * (int(hash(message)) - e * y1)) % (p - 1)
    return [y1, y2]


def verify_signature(message, signature, p, g, d):
    r, s = signature
    if not (0 < r < p and 0 < s < p - 1):
        return False
    left_side = pow(d, r, p) * pow(r, s, p) % p
    right_side = pow(g, int(hash(message)), p)
    return left_side == right_side


if __name__ == '__main__':
    p, g, d, e = generate_keys(500)
    message = "ЛАБЫ НЕ СДАЮТСЯ!"
    signature = sign_message(message, p, g, e)
    print("Сообщение:", message)
    print("Подпись (r, s):", signature)

    verification_result = verify_signature(message, signature, p, g, d)
    print("Результат верификации:", verification_result)
