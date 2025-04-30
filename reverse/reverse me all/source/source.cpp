#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
unsigned long djb2_hash(const char* str) {
    unsigned long hash = 0xD2e2a2d;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}
//int main()
//{
//    char word[50];
//
//    printf("Input RezTOP Sucret Key: ");
//
//    scanf("%49s", word);
//    if (djb2_hash(word) == 0x150AE8EA) {
//        printf("Valid Key!!!");
//    }
//    else {
//        printf("Invalid Key!!!");
//    }
//
//}
#include <immintrin.h>
#include "oxorany_include.h"

uint32_t avx2_hash(const char* str) {
    size_t len = strlen(str);
    uint32_t hash = 0xD2e2a1d;

    size_t i = 0;
    for (; i + 32 <= len; i += 32) {
        __m256i chunk = _mm256_loadu_si256((__m256i*)(str + i));

        __m256i sum = _mm256_sad_epu8(chunk, _mm256_setzero_si256());
        uint64_t sum_scalar = _mm256_extract_epi64(sum, 0) +
            _mm256_extract_epi64(sum, 1) +
            _mm256_extract_epi64(sum, 2) +
            _mm256_extract_epi64(sum, 3);

        // Добавляем к хешу
        hash = (hash * 33) + (uint32_t)sum_scalar;
    }

    for (; i < len; ++i) {
        hash = (hash * 33) + str[i];
    }

    return hash;
}
#include <stdlib.h>
int main() {
    char word[50];
    printf("Input RezTOP Sucret Key V2: ");

    scanf("%49s", word);
    if (avx2_hash(word) == djb2_hash(oxorany("RezTOP_1s_G00D"))) { //RezTOP_1s_G00D
        printf(oxorany("cuctf{RezTOP_1s_G00D}\n"));
    }
    else {
        printf(oxorany("Invalid Key!!!\n"));
    }
    system("pause");
    return 0;
}