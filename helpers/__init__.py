import random
import string


def random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))