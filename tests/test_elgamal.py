import pytest

from ntmcrypt import elgamal


@pytest.mark.parametrize("num_bits_a, num_bits_b, message", [(60, 69, "eee123123  ;))"),
                                                             (76, 121, "Hello, world!👨‍💻"),
                                                             (89, 76, "super hard test"),
                                                             (122, 37, "test test test test ... and ... test"),
                                                             (97, 84, "elgamal | test | || @34"),
                                                             (115, 63, "Эльгамаль | тест | Ёёу,7")])
def test_elgamal(num_bits_a, num_bits_b, message):
    # A
    p_a, g_a, y_a, pr_a = elgamal.gen_keys(num_bits_a)

    # b
    p_b, g_b, y_b, pr_b = elgamal.gen_keys(num_bits_b)

    # A -> B
    s_key_a = elgamal.gen_session_key(p_b)
    encrypted_blocks, a = elgamal.encrypt(message, s_key_a, p_b, g_b, y_b)

    # B
    decrypted_message = elgamal.decrypt(encrypted_blocks, a, p_b, pr_b)

    assert message == decrypted_message

    # B -> A
    s_key_b = elgamal.gen_session_key(p_a)
    encrypted_blocks, a = elgamal.encrypt(message, s_key_b, p_a, g_a, y_a)

    # A
    decrypted_message = elgamal.decrypt(encrypted_blocks, a, p_a, pr_a)

    assert message == decrypted_message
