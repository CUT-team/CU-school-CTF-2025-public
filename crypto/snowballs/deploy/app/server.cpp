#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <cstring>
#include <netinet/in.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define PORT 7007

const std::string HOST = "0.0.0.0";

const std::string EXE_PATH = "./snow_1.0";

std::string run_exe(const std::string& exe_path) {
    std::string output;
    char buffer[128];
    FILE* pipe = popen(exe_path.c_str(), "r");
    if (!pipe) return "Error executing file";
    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        output += buffer;
    }
    pclose(pipe);
    return output;
}

void start_server(const std::string& host = HOST, int port = PORT, const std::string& exe_path = EXE_PATH) {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        std::cerr << "Error creating socket" << std::endl;
        return;
    }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("0.0.0.0");
    server_addr.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        std::cerr << "Bind failed" << std::endl;
        close(server_fd);
        return;
    }

    if (listen(server_fd, 5) == -1) {
        std::cerr << "Listen failed" << std::endl;
        close(server_fd);
        return;
    }

    std::cout << "Server listening on " << host << ":" << port << std::endl;

    while (true) {
        client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);
        if (client_fd == -1) {
            std::cerr << "Accept failed" << std::endl;
            continue;
        }

        std::cout << "Connection established" << std::endl;
        std::string output = run_exe(exe_path);
        std::cout << "Sending output to client: "  <<  output << std::endl;
        send(client_fd, output.c_str(), output.size(), 0);
        close(client_fd);
    }

    close(server_fd);
}

int main() {
    start_server();
    return 0;
}
