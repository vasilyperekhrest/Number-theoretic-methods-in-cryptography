import pytest

from ntmcrypt import elgamal_ec


@pytest.mark.parametrize("message", ["qwerty123",
                                     "🎶🤪👾✊🏿🧵💫",
                                     "2319686834234234",
                                     "Привет, мир!",
                                     "!№%:,.;()_+-='",
                                     "Hello (привет), world (мир)"])
def test_elgamal_ec(message):
    curve = elgamal_ec.get_elliptic_curve(1)

    # A
    pr_a, pub_a, g_a = elgamal_ec.gen_keys(curve)

    # B
    pr_b, pub_b, g_b = elgamal_ec.gen_keys(curve)

    # A -> B
    encrypted_data = elgamal_ec.encrypt(message, curve, pub_b, g_b)

    # B
    decrypted_message = elgamal_ec.decrypt(*encrypted_data, curve=curve, private_key=pr_b)
    assert message == decrypted_message

    # B -> A
    encrypted_data = elgamal_ec.encrypt(message, curve, pub_a, g_a)

    # A
    decrypted_message = elgamal_ec.decrypt(*encrypted_data, curve=curve, private_key=pr_a)
    assert message == decrypted_message
