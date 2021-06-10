from ntmcrypt import williams


def main():
    # A
    pr_a, pub_a = williams.gen_keys(256)

    # B
    pr_b, pub_b = williams.gen_keys(512)

    # A -> B
    message = "Hello, world!👨‍💻"
    encrypted_data = williams.encrypt(message, pub_b)

    # B
    decrypted_message = williams.decrypt(encrypted_data, pr_b, pub_b)
    print(decrypted_message)

    # B -> A
    message = "Hello, world!👨‍💻"
    encrypted_data = williams.encrypt(message, pub_a)

    # A
    decrypted_message = williams.decrypt(encrypted_data, pr_a, pub_a)
    print(decrypted_message)


if __name__ == '__main__':
    main()
