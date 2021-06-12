from ntmcrypt import rabin


def main():
    # A
    p_a, q_a, pub_a = rabin.gen_keys(256)
    print(f"User: A\n"
          f"p = {p_a}\n"
          f"q = {q_a}\n"
          f"Public key = {pub_a}\n")

    # B
    p_b, q_b, pub_b = rabin.gen_keys(512)
    print(f"User: B\n"
          f"p = {p_b}\n"
          f"q = {q_b}\n"
          f"Public key = {pub_b}\n")

    # A -> B
    message = "Hello, world!👨‍💻"
    encrypted_data = rabin.encrypt(message, pub_b)
    print(f"A -> B\n"
          f"User A:\n"
          f"Message = '{message}'\n"
          f"Encrypted data = {encrypted_data}\n")

    # B
    decrypted_message = rabin.decrypt(encrypted_data, p_b, q_b)
    print(f"User B:\n"
          f"Decrypted message = {decrypted_message}\n")

    # B -> A
    message = "Hello, world!👨‍💻"
    encrypted_data = rabin.encrypt(message, pub_a)
    print(f"B -> A\n"
          f"User B:\n"
          f"Message = '{message}'\n"
          f"Encrypted data = {encrypted_data}\n")

    # A
    decrypted_message = rabin.decrypt(encrypted_data, p_a, q_a)
    print(f"User A:\n"
          f"Decrypted message = {decrypted_message}\n")


if __name__ == '__main__':
    main()
