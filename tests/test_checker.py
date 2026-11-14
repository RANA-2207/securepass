from checker import check_password, entropy_bits, generate_password


def test_common_password_is_weak():
    assert check_password("password")["level"] == "Weak"


def test_short_password_is_weak():
    assert check_password("aB1!")["level"] == "Weak"


def test_strong_password():
    assert check_password("T7#kLp9!vQ2zRm4$")["level"] == "Strong"


def test_sequence_is_flagged():
    result = check_password("Abcd1234!xyz")
    assert any("sequences" in i for i in result["issues"])


def test_repeated_characters_flagged():
    result = check_password("aaaa")
    assert any("repeating" in i for i in result["issues"])


def test_entropy_grows_with_length():
    assert entropy_bits("Abcdef1!Abcdef1!") > entropy_bits("Abcdef1!")


def test_generated_password_is_strong():
    pw = generate_password()
    assert len(pw) == 16
    assert check_password(pw)["level"] == "Strong"
