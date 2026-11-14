import math
import re
import secrets
import string
from pathlib import Path

COMMON = set(
    Path(__file__).with_name("common_passwords.txt").read_text().split()
)
SEQUENCES = ("0123", "1234", "2345", "3456", "4567", "5678", "6789",
             "abcd", "bcde", "cdef", "qwer", "wert", "asdf", "zxcv")
LEVELS = ["Weak", "Medium", "Strong"]


def entropy_bits(password: str) -> float:
    """Rough strength estimate: length x log2(size of character pool)."""
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[^A-Za-z0-9]", password):
        pool += 32
    if pool == 0:
        return 0.0
    return round(len(password) * math.log2(pool), 1)


def generate_password(length: int = 16) -> str:
    """Make a random strong password using the secure 'secrets' module."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_"
    while True:
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        if (re.search(r"[a-z]", pw) and re.search(r"[A-Z]", pw)
                and re.search(r"\d", pw) and re.search(r"[^A-Za-z0-9]", pw)):
            return pw


def check_password(password: str) -> dict:
    """Return the level, entropy, a list of issues and a suggestion."""
    issues = []
    if len(password) < 8:
        issues.append("Use at least 8 characters (12 or more is better).")
    if not re.search(r"[a-z]", password):
        issues.append("Add lowercase letters.")
    if not re.search(r"[A-Z]", password):
        issues.append("Add uppercase letters.")
    if not re.search(r"\d", password):
        issues.append("Add numbers.")
    if not re.search(r"[^A-Za-z0-9]", password):
        issues.append("Add special characters like ! @ # $.")

    is_common = password.lower() in COMMON
    if is_common:
        issues.append("This is a very common password that attackers try first.")

    has_repeat = bool(re.search(r"(.)\1{2,}", password))
    if has_repeat:
        issues.append("Avoid repeating the same character 3 or more times.")

    has_sequence = any(s in password.lower() for s in SEQUENCES)
    if has_sequence:
        issues.append("Avoid easy sequences like 1234 or qwer.")

    bits = entropy_bits(password)
    if bits < 40:
        level = 0
    elif bits < 60:
        level = 1
    else:
        level = 2
    if has_repeat or has_sequence:
        level = max(level - 1, 0)
    if is_common or not password:
        level = 0

    result = {
        "level": LEVELS[level],
        "entropy": bits,
        "issues": issues,
        "suggestion": None,
    }
    if level < 2:
        result["suggestion"] = generate_password()
    return result
