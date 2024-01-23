import random
import string

def get_random_digits_str(n):
    return ''.join(random.choice(string.digits) for _ in range(n))