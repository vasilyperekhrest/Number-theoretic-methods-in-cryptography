from ntmcrypt import elgamal


def main():
    # A
    p_a, g_a, y_a, pr_a = elgamal.gen_keys(150)

    # b
    p_b, g_b, y_b, pr_b = elgamal.gen_keys(120)

    # A -> B
    s_key_a = elgamal.gen_session_key(p_b)
    message = "Hello, world!👨‍💻"
    encrypted_blocks, a = elgamal.encrypt(message, s_key_a, p_b, g_b, y_b)

    # B
    decrypted_message = elgamal.decrypt(encrypted_blocks, a, p_b, pr_b)
    print(decrypted_message)


if __name__ == '__main__':
    main()
