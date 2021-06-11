from ntmcrypt import elgamal_ec


def main():
    curve = elgamal_ec.get_elliptic_curve(1)
    print(curve)
    print(curve.get_params())

    # A
    pr_a, pub_a, g_a = elgamal_ec.gen_keys(curve)

    # B
    pr_b, pub_b, g_b = elgamal_ec.gen_keys(curve)

    # A -> B
    message = "Hello, world!👨‍💻"
    encrypted_data = elgamal_ec.encrypt(message, curve, pub_b, g_b)

    # B
    decrypted_message = elgamal_ec.decrypt(*encrypted_data, curve, pr_b)
    print(decrypted_message)

    # B -> A
    message = "Hello, world!👨‍💻"
    encrypted_data = elgamal_ec.encrypt(message, curve, pub_a, g_a)

    # A
    decrypted_message = elgamal_ec.decrypt(*encrypted_data, curve, pr_a)
    print(decrypted_message)


if __name__ == '__main__':
    main()
