import random
import string


def generate_short_key(length: int = 6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))
