import pytest

from ntmcrypt import rsa


@pytest.mark.parametrize("message, num_bits_a, num_bits_b",
                         [("qwerty123", 45, 78),
                          ("🎶🤪👾✊🏿🧵💫", 467, 235),
                          ("2319686834234234", 563, 234),
                          ("Привет, мир!", 222, 768),
                          ("!№%:,.;()_+-='", 354, 233),
                          ("Hello (привет), world (мир)", 22, 346)])
def test_rsa(message, num_bits_a, num_bits_b):
    # A
    n_a, pub_a, pr_a = rsa.gen_keys(num_bits_a)

    # B
    n_b, pub_b, pr_b = rsa.gen_keys(num_bits_b)

    # A -> B
    encrypted_data = rsa.encrypt(message, pub_b, n_b)

    # B
    decrypted_message = rsa.decrypt(encrypted_data, pr_b, n_b)
    assert message == decrypted_message

    # B -> A
    encrypted_data = rsa.encrypt(message, pub_a, n_a)

    # A
    decrypted_message = rsa.decrypt(encrypted_data, pr_a, n_a)
    assert message == decrypted_message
