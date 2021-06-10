from ntmcrypt import rabin


def main():
    # A
    p_a, q_a, pub_a = rabin.gen_keys(256)

    # B
    p_b, q_b, pub_b = rabin.gen_keys(512)

    # A -> B
    message = "Hello, world!👨‍💻"
    encrypted_message = rabin.encrypt(message, pub_b)

    # B
    decrypted_message = rabin.decrypt(encrypted_message, p_b, q_b)
    print(decrypted_message)


if __name__ == '__main__':
    main()
