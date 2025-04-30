from itertools import cycle


def historical_xor(plaintext, key):
    assert len(key) <= 32
    return bytes(a ^ b for a, b in zip(plaintext, cycle(key)))


key = open('key', 'rb').read().strip()
flag = open('flag', 'rb').read().strip()
ciphertext = historical_xor(2 * flag, key)

print(ciphertext.hex())
with open('ciphertext', 'w') as file:
    file.write(ciphertext.hex())
