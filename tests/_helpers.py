import secrets
import string


def generate_random_pagerduty_id() -> str:
    alphabet = string.ascii_letters + string.digits

    return "".join(secrets.choice(alphabet) for i in range(7))
