import pytest

from ntmcrypt import williams


@pytest.mark.parametrize("message, num_bits_a, num_bits_b",
                         [("qwerty123", 45, 78),
                          ("🎶🤪👾✊🏿🧵💫", 467, 235),
                          ("2319686834234234", 563, 234),
                          ("Привет, мир!", 222, 768),
                          ("!№%:,.;()_+-='", 354, 233),
                          ("Hello (привет), world (мир)", 22, 346)])
def test_williams(message, num_bits_a, num_bits_b):
    # A
    pr_a, pub_a = williams.gen_keys(num_bits_a)

    # B
    pr_b, pub_b = williams.gen_keys(num_bits_b)

    # A -> B
    encrypted_data = williams.encrypt(message, pub_b)

    # B
    decrypted_message = williams.decrypt(encrypted_data, pr_b, pub_b)
    assert message == decrypted_message

    # B -> A
    encrypted_data = williams.encrypt(message, pub_a)

    # A
    decrypted_message = williams.decrypt(encrypted_data, pr_a, pub_a)
    assert message == decrypted_message
