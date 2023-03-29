from BifidCipher import BifidCipher


def main():
    cipher = BifidCipher('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    a = cipher.encrypt_message('hello, how are you')
    print(a)
    print(cipher.decrypt_message(a))


if __name__ == '__main__':
    main()
