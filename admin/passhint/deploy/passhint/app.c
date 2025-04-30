#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <stdint.h>
#include <errno.h>
#include <time.h>
#include <poll.h>

#define REQUIRED_FD_COUNT 1800
#define FLAG_MAX_LENGTH 256
#define PATH_MAX_LENGTH 256

unsigned char encoded_flag[] = {0xBA, 0x8A, 0xB5, 0x45, 0x1C, 0xC2, 0xE3, 0x7D, 0xF2, 0x8A, 0x82, 0x45, 0xC0, 0xC2, 0x64, 0x7D, 0x9E, 0x8A, 0x72, 0x45, 0x3E, 0xC2, 0xEA, 0x7D, 0xF3, 0x8A, 0x8A, 0x45, 0xF7, 0xC2, 0x70, 0x7D, 0xA6, 0x8A, 0x8F, 0x45, 0x06, 0xC2, 0x2F, 0x7D, 0xF5, 0x8A, 0xB9, 0x45, 0xCE, 0xC2, 0x94, 0x7D, 0x44, 0x8A, 0x85, 0x45, 0xE6, 0xC2, 0x3E, 0x7D, 0x1E, 0x8A, 0xEC, 0x45};

void decode_flag(const unsigned char* encoded, size_t encoded_size, char* output) {
    unsigned char deinterleaved[FLAG_MAX_LENGTH];
    size_t deinterleaved_size = 0;

    for (size_t i = 0; i < encoded_size; i += 2) {
        deinterleaved[deinterleaved_size++] = encoded[i];
    }

    unsigned char key[] = {0x37, 0x15, 0x93, 0x42, 0x66, 0x28, 0x51, 0x19};
    size_t key_size = sizeof(key);
    unsigned char dexored[FLAG_MAX_LENGTH];

    for (size_t i = 0; i < deinterleaved_size; i++) {
        dexored[i] = deinterleaved[i] ^ key[i % key_size];
    }

    for (size_t i = 0; i < deinterleaved_size; i++) {
        unsigned char val = (dexored[i] - i - 42) % 256;
        if (dexored[i] < (i + 42)) val += 256;
        output[i] = (char)val;
    }

    output[deinterleaved_size] = '\0';
}


int check_fd_limit() {
    struct rlimit rlim;
    if (getrlimit(RLIMIT_NOFILE, &rlim) == 0) {
        if (rlim.rlim_cur < REQUIRED_FD_COUNT) {
            return 0; 
        }
    }
    return 1; 
}


int custom_open_file(const char* path, int* descriptors, int index) {
    



    
    if (index % 4 == 0) {
        int sock_fd = socket(AF_UNIX, SOCK_STREAM, 0);
        if (sock_fd >= 0) {
            descriptors[index] = sock_fd;
            return 1;
        }
        return 0;
    }

    
    int flags = O_CREAT | O_WRONLY;
    if (index % 3 == 0) flags |= O_APPEND;

    
    if (index % 5 == 0) {
        access(path, F_OK);
    }

    
    if (index % 100 == 99) {
        struct pollfd pfd = { .fd = 0, .events = POLLIN };
        poll(&pfd, 1, 0);
    }

    
    if (index > 1020) {
        
        int test_fd = dup(0); 
        if (test_fd < 0) {
            
            return 0;
        }
        close(test_fd);
    }

    
    descriptors[index] = open(path, flags, 0600);

    return (descriptors[index] >= 0) ? 1 : 0;
}

int main() {
    char work_dir[PATH_MAX_LENGTH] = "/tmp/hints/";

    
    struct stat st;
    if (stat(work_dir, &st) != 0) {
        fprintf(stderr, "Ошибка: невозможно получить доступ к подсказке.\n");
        exit(1);
    }

    int *file_descriptors = (int*)malloc(sizeof(int) * REQUIRED_FD_COUNT);
    if (!file_descriptors) {
        fprintf(stderr, "Ошибка.\n");
        exit(2);
    }

    
    for (int i = 0; i < REQUIRED_FD_COUNT; i++) {
        file_descriptors[i] = -1;
    }

    printf("Начинаю процесс получения подсказки...\n");



    
    char file_path[PATH_MAX_LENGTH];
    int success_count = 0;
    int batch_size = 100;
    int result = 1;

    
    for (int batch = 0; batch < REQUIRED_FD_COUNT/batch_size && result; batch++) {
        int start_idx = batch * batch_size;
        int end_idx = (batch + 1) * batch_size;
        if (end_idx > REQUIRED_FD_COUNT) end_idx = REQUIRED_FD_COUNT;

        for (int i = start_idx; i < end_idx; i++) {
            snprintf(file_path, sizeof(file_path), "%sfile_%d.tmp", work_dir, i);

            if (!custom_open_file(file_path, file_descriptors, i)) {
                result = 0;
                break;
            }

            success_count++;
        }
    }

    
    if (success_count < REQUIRED_FD_COUNT) {
        fprintf(stderr, "Ошибка: проверка целостности данных не удалась.\n");
        
        for (int i = 0; i < REQUIRED_FD_COUNT; i++) {
            if (file_descriptors[i] >= 0) {
                close(file_descriptors[i]);

                
                if (i % 4 != 0) {
                    snprintf(file_path, sizeof(file_path), "%sfile_%d.tmp", work_dir, i);
                    unlink(file_path);
                }
            }
        }

        free(file_descriptors);
        exit(4);
    }

    printf("Подсказка успешно получена!\n");

    
    for (int i = 0; i < REQUIRED_FD_COUNT; i++) {
        if (file_descriptors[i] >= 0) {
            close(file_descriptors[i]);

            if (i % 4 != 0) {
                snprintf(file_path, sizeof(file_path), "%sfile_%d.tmp", work_dir, i);
                unlink(file_path);
            }
        }
    }
    
    char original_flag[FLAG_MAX_LENGTH];
    decode_flag(encoded_flag, sizeof(encoded_flag), original_flag);

    printf("Елена, вот ваша подсказка для пароля от 1C: %s\n", original_flag);
    printf("Пожалуйста, больше не забывайте его!\n");

    free(file_descriptors);
    return 0;
}