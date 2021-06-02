import gmpy2


def str_to_blocks(string: str, p: gmpy2.mpz) -> list[gmpy2.mpz]:
    blocks = []

    string_buffer = ""

    for byte in bytes(string, "utf-8"):
        string_buffer += str(byte).zfill(3)
        if len(string_buffer) + 3 >= p.num_digits():
            blocks.append(gmpy2.mpz(string_buffer))
            string_buffer = ""

    if string_buffer != "":
        blocks.append(gmpy2.mpz(string_buffer))

    return blocks


def blocks_to_str(blocks: list[gmpy2.mpz]):
    string_bytes = bytearray()
    buffer_bytes = bytearray()

    for block in blocks:
        block = str(block)[::-1]
        for pos in range(0, len(block), 3):
            buffer_bytes.append(gmpy2.mpz(block[pos:pos + 3][::-1]))

        string_bytes += buffer_bytes[::-1]
        buffer_bytes.clear()

    return string_bytes.decode("utf-8")
