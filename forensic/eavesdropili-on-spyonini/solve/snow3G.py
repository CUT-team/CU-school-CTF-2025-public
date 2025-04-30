import random

# Rewritten from https://github.com/Burdi14/snow_cipher/

def ROTL32(x, shift):
    return ((x << shift) | (x >> (32 - shift))) & 0xFFFFFFFF

def ROTL8(x, shift):
    return ((x << shift) | (x >> (8 - shift))) & 0xFF

class SNOW:
    def __init__(self, key):
        self.LFSR = [0] * 16
        self.FSM_R1 = key[1]
        self.FSM_R2 = key[2]
        self.keystream = []
        self.SBOX = [0] * 256
        self.initialize_sbox(self.SBOX)

        for i in range(16):
            self.LFSR[i] = key[0] ^ (i * 0x01010101)

    @staticmethod
    def initialize_sbox(sbox):
        p = 1
        q = 1
        while True:
            p ^= (p << 1) ^ (0x1B if (p & 0x80) else 0)
            p &= 0xFF

            q ^= q << 1
            q ^= q << 2
            q ^= q << 4
            q ^= (0x09 if (q & 0x80) else 0)
            q &= 0xFF

            xformed = q ^ ROTL8(q, 1) ^ ROTL8(q, 2) ^ ROTL8(q, 3) ^ ROTL8(q, 4)
            sbox[p] = xformed ^ 0x63

            if p == 1:
                break
        sbox[0] = 0x63

    def mul_alpha(self, x):
        return (((x << 9) ^ (x >> 23)) & 0xFFFFFFFF)

    def S(self, R):
        return ((self.SBOX[(R >> 24) & 0xFF] << 24) |
                (self.SBOX[(R >> 16) & 0xFF] << 16) |
                (self.SBOX[(R >> 8) & 0xFF] << 8) |
                self.SBOX[R & 0xFF])

    def LFSR_Update(self):
        new_value = self.mul_alpha(self.LFSR[0] ^ self.LFSR[2] ^ self.LFSR[11] ^ self.LFSR[15])
        for i in range(15):
            self.LFSR[i] = self.LFSR[i + 1]
        self.LFSR[15] = new_value

    def FSM_Update(self):
        F = ((self.LFSR[15] + self.FSM_R1) & 0xFFFFFFFF) ^ self.FSM_R2
        FSM_R1_prev = self.FSM_R1
        self.FSM_R1 = FSM_R1_prev ^ ROTL32((F + self.FSM_R2) & 0xFFFFFFFF, 7)
        self.FSM_R2 = self.S(FSM_R1_prev)

    def GenerateKeystreamWord(self):
        ks_word = ((self.LFSR[15] + self.FSM_R1) & 0xFFFFFFFF) ^ self.FSM_R2 ^ self.LFSR[0]
        self.FSM_Update()
        self.LFSR_Update()
        return ks_word

    def Encrypt(self, data: bytearray):
        for i in range(len(data)):
            if i % 4 == 0:
                self.keystream.append(self.GenerateKeystreamWord())
            byte = (self.keystream[-1] >> (8 * (i % 4))) & 0xFF
            data[i] ^= byte

def PrintAsHex(data: bytes):
    for c in data:
        print(f'{c:02x}', end='')
    print()

def random_uint32():
    return random.getrandbits(32)

# if __name__ == '__main__':
#     text = bytearray(b'abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcddd')
#     key = [random_uint32(), random_uint32(), random_uint32()]
#     cipher = SNOW(key)
    
    
#     print(text.hex())
#     cipher.Encrypt(text)
#     PrintAsHex(text)
