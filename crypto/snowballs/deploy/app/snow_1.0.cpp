#include <iostream>
#include <cstdint>
#include <vector>
#include <random>

#define ROTL16(x, shift) ((x << shift) | (x >> (16 - shift)))
#define ROTL8(x, shift) ((x << shift) | (x >> (8 - shift)))

class SNOW {
private:
    uint16_t LFSR[16];
    uint16_t FSM_R1, FSM_R2;
    std::vector <uint16_t> keystream;
    uint8_t SBOX[256];

    void static initialize_sbox(uint8_t sbox[256]) {
        uint8_t p = 1, q = 1;

        do {
            p = p ^ (p << 1) ^ (p & 0x80 ? 0x1B : 0);

            q ^= q << 1;
            q ^= q << 2;
            q ^= q << 4;
            q ^= q & 0x80 ? 0x09 : 0;

            uint8_t xformed = q ^ ROTL8(q, 1) ^ ROTL8(q, 2) ^ ROTL8(q, 3) ^ ROTL8(q, 4);

            sbox[p] = xformed ^ 0x63;
        } while (p != 1);

        sbox[0] = 0x63;
    }

    uint16_t S(uint16_t R){
        return ((SBOX[(0xFF00 & R) >> 8] << 8) + SBOX[0x00FF & R]);
    }

    void LFSR_Update() {
        uint16_t new_value = (LFSR[0] ^ LFSR[3] ^ LFSR[9]);
        for (int i = 0; i < 15; i++) {
            LFSR[i] = LFSR[i + 1];
        }
        LFSR[15] = new_value;
    }

    void FSM_Update() {
        uint16_t F = ((LFSR[15] + FSM_R1) & 0xFFFF) ^ FSM_R2;
        uint16_t FSM_R1_prev = FSM_R1;

        FSM_R1 = FSM_R1_prev ^ ROTL16((F + FSM_R2), 7);
        FSM_R2 = S(FSM_R1_prev & 0xFFFF);
    }

public:
    void Encrypt(std::string &text) {
        for (size_t i = 0; i < text.size(); i++) {
            if (i % 2 == 0){
                keystream.push_back(GenerateKeystreamWord());
            }
            text[i] ^= i % 2 == 0 ? (keystream.back() & 0xFF00) >> 8 : keystream.back() & 0xFF;
        }
    }

    explicit SNOW(std::vector<uint16_t> key) {
        initialize_sbox(SBOX);
        LFSR[0] = key[0];
        for (int i = 0; i < 15; ++i){
            LFSR[i + 1] = (LFSR[i] >> (1)) + ((((LFSR[i] >> 15)) ^ (LFSR[i] & 0x1)) << 16);
        }
        FSM_R1 = 0xFFFF - LFSR[15];
        FSM_R2 = key[1];
    }

    uint16_t GenerateKeystreamWord() {
        uint16_t keystream = ((LFSR[15] + FSM_R1) & 0xFFFF) ^ FSM_R2 ^ LFSR[0];
        FSM_Update();
        LFSR_Update();
        return keystream;
    }
};

void PrintAsHex(const std::string &data) {
    for (unsigned char c : data) {
        if ((int)c < 16)
        std::cout << std::hex << '0' << (int)c ;
        else
            std::cout << std::hex << (int)c ;
    }
    std::cout << std::endl;
}

uint16_t random_uint16() {
    static std::random_device rd;

    static std::mt19937 mt(rd());

    std::uniform_int_distribution<uint16_t> dist(0, 0xFFFF);

    return dist(mt);
    }

int main() {
    const char* tmp_flag = getenv("FLAG");
    if (tmp_flag == nullptr) {
        std::cerr << "Error: FLAG environment variable is not set." << std::endl;
        return 1;
    }
    std::string flag = tmp_flag;

    std::vector<uint16_t> key = {random_uint16(), random_uint16()};
    SNOW cipher(key);

    cipher.Encrypt(flag);
    PrintAsHex(flag);
    return 0;
}
