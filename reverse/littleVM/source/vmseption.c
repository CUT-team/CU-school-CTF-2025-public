#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define MEM_SIZE 1024
#define NUM_REGS 8

uint8_t mem[MEM_SIZE];
uint8_t regs[NUM_REGS];
uint16_t pc = 0;

void load_program(const char *filename) {
    FILE *f = fopen(filename, "rb");
    if (!f) {
        perror("fopen");
        exit(1);
    }
    fread(mem, 1, MEM_SIZE, f);
    fclose(f);
}

void run_vm() {
    while (1) {
        uint8_t opcode = mem[pc++];
        switch (opcode) {
            case 0x01: {
                uint8_t reg = mem[pc++];
                uint8_t imm = mem[pc++];
                if (reg == 1 && imm == 0x00) {
                    regs[reg] = getchar();
                } else {
                    regs[reg] = imm;
                }
                break;
            }
            case 0x02: { // ADD
                uint8_t r1 = mem[pc++];
                uint8_t r2 = mem[pc++];
                regs[r1] += regs[r2];
                break;
            }
            case 0x03: { // XOR
                uint8_t r1 = mem[pc++];
                uint8_t r2 = mem[pc++];
                regs[r1] ^= regs[r2];
                break;
            }
            case 0x04: { // CMP
                uint8_t r1 = mem[pc++];
                uint8_t r2 = mem[pc++];
                regs[7] = (regs[r1] == regs[r2]) ? 1 : 0;
                break;
            }
            case 0x05: { // JNE
                uint16_t addr = mem[pc++];
                if (regs[7] == 0)
                    pc = addr;
                break;
            }
            case 0x06: { // OUT
                uint8_t reg = mem[pc++];
                putchar(regs[reg]);
                break;
            }
            case 0xFF: // HALT
                return;
            default:
                return;
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <program.vmcode>\n", argv[0]);
        return 1;
    }
    load_program(argv[1]);
    run_vm();
    return 0;
}
