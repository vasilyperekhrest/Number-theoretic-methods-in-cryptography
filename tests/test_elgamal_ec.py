import gmpy2

from ntmcrypt import elgamal_ec


def main():
    curve = elgamal_ec.get_elliptic_curve(1)
    print(f"Elliptic curve:\n"
          f"{curve}\n")
    print(curve.get_params())

    # A
    pr_a, pub_a, g_a = elgamal_ec.gen_keys(curve)
    print(f"User: A\n"
          f"Private key = {pr_a}\n"
          f"Public key = {pub_a}\n"
          f"g = {g_a}\n")

    # B
    pr_b, pub_b, g_b = elgamal_ec.gen_keys(curve)
    print(f"User: B\n"
          f"Private key = {pr_b}\n"
          f"Public key = {pub_b}\n"
          f"g = {g_b}\n")

    # A -> B
    message = "Hello, world!👨‍💻"
    encrypted_data = elgamal_ec.encrypt(message, curve, pub_b, g_b)
    print(f"A -> B\n"
          f"User A:\n"
          f"Message = '{message}'\n"
          f"Encrypted data = {encrypted_data[0]}, {encrypted_data[1]}\n")

    # B
    decrypted_message = elgamal_ec.decrypt(*encrypted_data, curve=curve, private_key=pr_b)
    print(f"User B:\n"
          f"Decrypted message = {decrypted_message}\n")

    # B -> A
    message = "Hello, world!👨‍💻"
    encrypted_data = elgamal_ec.encrypt(message, curve, pub_a, g_a)
    print(f"B -> A\n"
          f"User B:\n"
          f"Message = '{message}'\n"
          f"Encrypted data = {encrypted_data[0]}, {encrypted_data[1]}\n")

    # A
    decrypted_message = elgamal_ec.decrypt(*encrypted_data, curve=curve, private_key=pr_a)
    print(f"User A:\n"
          f"Decrypted message = {decrypted_message}\n")


if __name__ == '__main__':
    main()
