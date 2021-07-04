import pytest

from ntmcrypt import diffie_hellman


@pytest.mark.parametrize("num_bits", [50,
                                      60,
                                      70,
                                      80,
                                      90,
                                      100])
def test_diffie_hellman(num_bits):
    p, g = diffie_hellman.gen_public_shared_keys(num_bits)

    # A
    pub_a, pr_a = diffie_hellman.gen_keys(p, g)

    # B
    pub_b, pr_b = diffie_hellman.gen_keys(p, g)

    # A -> B
    shared_key_a = diffie_hellman.create_private_shared_key(pub_b, pr_a, p)

    # B -> A
    shared_key_b = diffie_hellman.create_private_shared_key(pub_a, pr_b, p)

    assert shared_key_a == shared_key_b
