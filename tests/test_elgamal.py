from ntmcrypt import elgamal


def main():
    # A
    p_a, g_a, y_a, pr_a = elgamal.gen_keys(150)
    print(f"User: A\n"
          f"p = {p_a}\n"
          f"g = {g_a}\n"
          f"y = {y_a}\n"
          f"Private key = {pr_a}\n")

    # b
    p_b, g_b, y_b, pr_b = elgamal.gen_keys(120)
    print(f"User: A\n"
          f"p = {p_b}\n"
          f"g = {g_b}\n"
          f"y = {y_b}\n"
          f"Private key = {pr_b}\n")

    # A -> B
    s_key_a = elgamal.gen_session_key(p_b)
    message = "Hello, world!👨‍💻"
    encrypted_blocks, a = elgamal.encrypt(message, s_key_a, p_b, g_b, y_b)
    print(f"A -> B\n"
          f"User A:\n"
          f"Message = '{message}'\n"
          f"Session key = {s_key_a}\n"
          f"Encrypted data = {encrypted_blocks}\n"
          f"a = {a}\n")

    # B
    decrypted_message = elgamal.decrypt(encrypted_blocks, a, p_b, pr_b)
    print(f"User B:\n"
          f"Decrypted message = {decrypted_message}\n")

    # B -> A
    s_key_b = elgamal.gen_session_key(p_a)
    message = "Hello, world!👨‍💻"
    encrypted_blocks, a = elgamal.encrypt(message, s_key_b, p_a, g_a, y_a)
    print(f"B -> A\n"
          f"User B:\n"
          f"Message = '{message}'\n"
          f"Session key = {s_key_b}\n"
          f"Encrypted data = {encrypted_blocks}\n"
          f"a = {a}\n")

    # A
    decrypted_message = elgamal.decrypt(encrypted_blocks, a, p_a, pr_a)
    print(f"User A:\n"
          f"Decrypted message = {decrypted_message}\n")


if __name__ == '__main__':
    main()
