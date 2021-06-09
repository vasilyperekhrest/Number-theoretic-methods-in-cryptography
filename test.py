from ntmcrypt import diemitko


def main():
    p = diemitko.prime_gen(80, False)
    print(p)


if __name__ == '__main__':
    main()
