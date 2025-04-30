#include <iostream>
#include <cstdint>
#include <vector>
#include <tuple>


#define ROTL16(x, shift) ((x << shift) | (x >> (16 - shift)))
#define ROTL8(x, shift) ((x << shift) | (x >> (8 - shift)))


class SNOW_from_1_cycle {
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
    explicit SNOW_from_1_cycle(uint16_t fsm_r1, uint16_t fsm_r2, std::vector<uint16_t>& lfsr)
            : FSM_R1(fsm_r1), FSM_R2(fsm_r2) {
        initialize_sbox(SBOX);
        std::copy(lfsr.begin(), lfsr.end(), LFSR);
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
        std::cout << std::hex << (int)c;
    }
    std::cout << std::endl;
}

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


std::vector<std::tuple<uint16_t, uint16_t, std::vector<uint16_t>>> find_fsm_lfsr(uint16_t keystream_1_check) {
    std::vector<std::tuple<uint16_t, uint16_t, std::vector<uint16_t>>> result;
    uint8_t SBOX[256];
    initialize_sbox(SBOX);
    uint16_t key_0_init = 0x0000;

    while (key_0_init != 0xFFFF) {
        std::vector<uint16_t> LFSR(16);
        LFSR[0] = key_0_init;
        for (int i = 0; i < 15; ++i){
            LFSR[i + 1] = (LFSR[i] >> (1)) + ((((LFSR[i] >> 15)) ^ (LFSR[i] & 0x1)) << 16);
        }

        uint16_t FSM_R1_0 = 0xFFFF - LFSR[15];
        uint16_t FSM_R1_1 = LFSR[15];
        uint16_t FSM_R2_1 = (SBOX[(0xFF00 & FSM_R1_0) >> 8] << 8) + SBOX[0x00FF & FSM_R1_0];

        uint16_t new_value = (LFSR[0] ^ LFSR[3] ^ LFSR[9]);
        for (int i = 0; i < 15; i++) {
            LFSR[i] = LFSR[i + 1];
        }
        LFSR[15] = new_value;

        uint16_t keystream_1 = ((LFSR[15] + FSM_R1_1) & 0xFFFF) ^ FSM_R2_1 ^ LFSR[0];

        if (keystream_1 == keystream_1_check) {
            result.emplace_back(FSM_R1_1, FSM_R2_1, LFSR);
        }

        ++key_0_init;
    }
    return result;
}

int main(){
    std::string encrypted = "7f6931f0fc11af0e10f3aeba58254eb20f9d6098daf7ed72de39edc140e746cd98";
    std::string key_1_chunk = encrypted.substr(4, 4);

    // cu ct = 0x6375 0x6374

    std::vector<std::tuple<uint16_t, uint16_t, std::vector<uint16_t>>> potential_values = find_fsm_lfsr(0x6374 ^ stoul(key_1_chunk, nullptr,16));
    for (auto it: potential_values) {
        auto [FSM_R1_1, FSM_R2_1, LFSR] = it;
        std::cout << "Decrypting...\n\n\n" ;

        SNOW_from_1_cycle cipher(FSM_R1_1, FSM_R2_1, LFSR);
        std::vector<uint16_t> keystream;
        for (auto i = 1; i < encrypted.size() / 4; ++i) {
            uint16_t chunk_encrypted =  stoul(encrypted.substr(i*4, 4), nullptr, 16);
             uint16_t chunk_decrypted = cipher.GenerateKeystreamWord() ^ chunk_encrypted;
            std::cout << std::hex << char(chunk_decrypted >> 8) << char(chunk_decrypted & 0xFF);

        }

        std::cout << "\n";
    }
    return 0;
}

