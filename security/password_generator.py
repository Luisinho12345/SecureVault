import random
import string


def generate_password(
    length=16,
    use_uppercase=True,
    use_lowercase=True,
    use_numbers=True,
    use_symbols=True
):

    pools = []

    if use_lowercase:
        pools.append(string.ascii_lowercase)

    if use_uppercase:
        pools.append(string.ascii_uppercase)

    if use_numbers:
        pools.append(string.digits)

    if use_symbols:
        pools.append("!@#$%^&*()-_=+[]{}")

    if not pools:
        return ""

    all_chars = "".join(pools)

    password_chars = [random.choice(pool) for pool in pools]

    remaining = length - len(password_chars)

    if remaining > 0:
        password_chars += [random.choice(all_chars) for _ in range(remaining)]

    random.shuffle(password_chars)

    return "".join(password_chars[:length])


def check_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_=+[]{}" for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"
