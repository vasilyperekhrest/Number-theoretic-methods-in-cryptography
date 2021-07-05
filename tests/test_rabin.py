import pytest

from ntmcrypt import rabin


@pytest.mark.parametrize("message, num_bits_a, num_bits_b",
                         [("qwerty123", 67, 78),
                          ("🎶🤪👾✊🏿🧵💫", 467, 235),
                          ("2319686834234234", 563, 234),
                          ("Привет, мир!", 222, 768),
                          ("!№%:,.;()_+-='", 354, 233),
                          ("Hello (привет), world (мир)", 80, 346)])
def test_rabin(message, num_bits_a, num_bits_b):
    # A
    p_a, q_a, pub_a = rabin.gen_keys(num_bits_a)

    # B
    p_b, q_b, pub_b = rabin.gen_keys(num_bits_b)

    # A -> B
    encrypted_data = rabin.encrypt(message, pub_b)

    # B
    decrypted_message = rabin.decrypt(encrypted_data, p_b, q_b)
    assert message == decrypted_message

    # B -> A
    encrypted_data = rabin.encrypt(message, pub_a)

    # A
    decrypted_message = rabin.decrypt(encrypted_data, p_a, q_a)
    assert message == decrypted_message
