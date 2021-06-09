from ntmcrypt import diemitko
from ntmcrypt import shamir


def main():
    p = diemitko.prime_gen(256)

    # A
    pub_a, pr_a = shamir.gen_keys(p)

    # B
    pub_b, pr_b = shamir.gen_keys(p)

    # A -> B
    message = "Hello, world!👨‍💻"

    # A
    encrypted_data = shamir.encrypt(message, pub_a, p)

    # B
    encrypted_data = shamir.encrypt(encrypted_data, pub_b, p)

    # A
    encrypted_data = shamir.encrypt(encrypted_data, pr_a, p)

    # B
    decrypted_message = shamir.decrypt(encrypted_data, pr_b, p)
    print(decrypted_message)


if __name__ == '__main__':
    main()
