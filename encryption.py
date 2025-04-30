from cryptography.fernet import Fernet


with open("secret.key", "r+") as f:
    # if f.read() == "":
    #     key = Fernet.generate_key()
    #     f.write(key.decode())
    # else:
    f.seek(0)
    key = f.read().encode()


cipher = Fernet(key)


def decrypt(text: bytes):
    return cipher.decrypt(text.encode()).decode()


def encrypt(text: bytes):
    return cipher.encrypt(text.encode()).decode()

message = "Hello, world!"
encrypted = encrypt(message)
print("Encrypted:", encrypted)

decrypted = decrypt(encrypted)
print("Decrypted:", decrypted)






def test_encryption_and_decryption_functions(text: str):
    assert text == decrypt(encrypt(text))





test_encryption_and_decryption_functions("hello world")
test_encryption_and_decryption_functions("secret message")
test_encryption_and_decryption_functions("1234567890")