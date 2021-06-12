from ntmcrypt import rsa


def main():
    # A
    n_a, pub_a, pr_a = rsa.gen_keys(256)
    print(f"User: A\n"
          f"N = {n_a}\n"
          f"Public key = {pub_a}\n"
          f"Private key = {pr_a}\n")

    # B
    n_b, pub_b, pr_b = rsa.gen_keys(512)
    print(f"User: B\n"
          f"N = {n_b}\n"
          f"Public key = {pub_b}\n"
          f"Private key = {pr_b}\n")

    # A -> B
    message = "Hello, world!👨‍💻"
    encrypted_data = rsa.encrypt(message, pub_b, n_b)
    print(f"A -> B\n"
          f"User A:\n"
          f"Message = '{message}'\n"
          f"Encrypted data = {encrypted_data}\n")

    # B
    decrypted_message = rsa.decrypt(encrypted_data, pr_b, n_b)
    print(f"User B:\n"
          f"Decrypted message = {decrypted_message}\n")

    # B -> A
    message = "Hello, world!👨‍💻"
    encrypted_data = rsa.encrypt(message, pub_a, n_a)
    print(f"B -> A\n"
          f"User B:\n"
          f"Message = '{message}'\n"
          f"Encrypted data = {encrypted_data}\n")

    # A
    decrypted_message = rsa.decrypt(encrypted_data, pr_a, n_a)
    print(f"User A:\n"
          f"Decrypted message = {decrypted_message}\n")


if __name__ == '__main__':
    main()
