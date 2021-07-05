import pytest

from ntmcrypt import utils
from ntmcrypt import shamir


@pytest.mark.parametrize("message, num_bits",
                         [("qwerty123", 45),
                          ("🎶🤪👾✊🏿🧵💫", 467),
                          ("2319686834234234", 563),
                          ("Привет, мир!", 222),
                          ("!№%:,.;()_+-='", 354),
                          ("Hello (привет), world (мир)", 22)])
def test_shamir(message, num_bits):
    p = utils.prime_gen(num_bits)
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
    # A
    encrypted_data = shamir.encrypt(message, pub_a, p)

    # B
    encrypted_data = shamir.encrypt(encrypted_data, pub_b, p)

    # A
    encrypted_data = shamir.encrypt(encrypted_data, pr_a, p)

    # B
    decrypted_message = shamir.decrypt(encrypted_data, pr_b, p)
    assert message == decrypted_message

    # B -> A
    # B
    encrypted_data = shamir.encrypt(message, pub_b, p)

    # A
    encrypted_data = shamir.encrypt(encrypted_data, pub_a, p)

    # B
    encrypted_data = shamir.encrypt(encrypted_data, pr_b, p)

    # A
    decrypted_message = shamir.decrypt(encrypted_data, pr_a, p)
    assert message == decrypted_message
