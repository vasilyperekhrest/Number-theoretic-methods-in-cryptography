from ntmcrypt import utils
from ntmcrypt import shamir


def main():
    p = utils.prime_gen(256)
    print(f"p = {p}\n")

    # A
    pub_a, pr_a = shamir.gen_keys(p)
    print(f"User: A\n"
          f"Public key = {pub_a}\n"
          f"Private key = {pr_a}\n")

    # B
    pub_b, pr_b = shamir.gen_keys(p)
    print(f"User: B\n"
          f"Public key = {pub_b}\n"
          f"Private key = {pr_b}\n")

    # A -> B
    message = "Hello, world!👨‍💻"

    # A
    encrypted_data = shamir.encrypt(message, pub_a, p)
    print(f"A -> B\n"
          f"User A:\n"
          f"Message = '{message}'\n"
          f"Encrypted data = {encrypted_data}\n")

    # B
    encrypted_data = shamir.encrypt(encrypted_data, pub_b, p)
    print(f"User B:\n"
          f"Encrypted data = {encrypted_data}\n")

    # A
    encrypted_data = shamir.encrypt(encrypted_data, pr_a, p)
    print(f"User A:\n"
          f"Encrypted data = {encrypted_data}\n")

    # B
    decrypted_message = shamir.decrypt(encrypted_data, pr_b, p)
    print(f"User B:\n"
          f"Decrypted message = {decrypted_message}\n")

    # B -> A
    message = "Hello, world!👨‍💻"

    # B
    encrypted_data = shamir.encrypt(message, pub_b, p)
    print(f"B -> A\n"
          f"User B:\n"
          f"Message = '{message}'\n"
          f"Encrypted data = {encrypted_data}\n")

    # A
    encrypted_data = shamir.encrypt(encrypted_data, pub_a, p)
    print(f"User A:\n"
          f"Encrypted data = {encrypted_data}\n")

    # B
    encrypted_data = shamir.encrypt(encrypted_data, pr_b, p)
    print(f"User B:\n"
          f"Encrypted data = {encrypted_data}\n")

    # A
    decrypted_message = shamir.decrypt(encrypted_data, pr_a, p)
    print(f"User A:\n"
          f"Decrypted message = {decrypted_message}\n")


if __name__ == '__main__':
    main()
