from ntmcrypt import diffie_hellman


def main():
    p, g = diffie_hellman.gen_public_shared_keys(120)
    print(f"Public shared keys:\n"
          f"p = {p}\n"
          f"g = {g}\n")

    # A
    pub_a, pr_a = diffie_hellman.gen_keys(p, g)
    print(f"User: A\n"
          f"Public key = {pub_a}\n"
          f"Private key = {pr_a}\n")

    # B
    pub_b, pr_b = diffie_hellman.gen_keys(p, g)
    print(f"User: B\n"
          f"Public key = {pub_b}\n"
          f"Private key = {pr_b}\n")

    # A -> B
    shared_key_a = diffie_hellman.create_private_shared_key(pub_b, pr_a, p)
    print(f"A -> B\n"
          f"User A:\n"
          f"Private shared key = {shared_key_a}\n")

    # B -> A
    shared_key_b = diffie_hellman.create_private_shared_key(pub_a, pr_b, p)
    print(f"B -> A\n"
          f"User B:\n"
          f"Private shared key = {shared_key_b}\n")


if __name__ == '__main__':
    main()
