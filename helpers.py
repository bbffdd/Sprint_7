import random
import string


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_courier_credentials():
    return (
        generate_random_string(),
        generate_random_string(),
        generate_random_string(),
    )
