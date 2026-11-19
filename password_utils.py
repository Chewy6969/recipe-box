from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    return check_password_hash(password_hash, password)


def demo_password_hashing() -> None:
    password = "example-password"
    password_hash = hash_password(password)
    print("Password:", password)
    print("Hash:", password_hash)
    print("Correct password check:", verify_password(password_hash, password))
    print("Wrong password check:", verify_password(password_hash, "wrong-password"))
