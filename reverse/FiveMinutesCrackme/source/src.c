#include <windows.h>
#include <string.h>
#include "oxorany.h"
#include "lazy_importer.hpp"
#include "intrin.h"
int main() {
    HANDLE hStdIn = LI_FN(GetStdHandle)((DWORD)oxorany(STD_INPUT_HANDLE));
    HANDLE hStdOut = LI_FN(GetStdHandle)((DWORD)oxorany(STD_OUTPUT_HANDLE));

    const char* prompt = oxorany("Enter password: ");
    const char* correct = oxorany("Correct! Flag: cuctf{1_L0vE_R5v5Rse}\n");
    const char* incorrect = oxorany("Incorrect password!\n");
    const char* password = oxorany("cuctf{1_L0vE_R5v5Rse}");

    char buffer[128] = { oxorany(0) };
    DWORD bytesRead = oxorany(0);
    LI_FN(WriteConsoleA)((HANDLE)hStdOut, prompt, (DWORD)LI_FN(strlen)(prompt), (LPDWORD)NULL, (LPVOID)NULL);
    LI_FN(ReadConsoleA)((HANDLE)hStdIn, buffer, sizeof(buffer) - oxorany(2), &bytesRead, (PCONSOLE_READCONSOLE_CONTROL)NULL);
    if (bytesRead >= oxorany(2) && buffer[bytesRead - oxorany(2)] == oxorany('\r')) {
        buffer[bytesRead - oxorany(2)] = oxorany('\0');
    }
    if (LI_FN(strcmp)(buffer, password) == oxorany(0) ) {
        LI_FN(WriteConsoleA)((HANDLE)hStdOut, (CONST VOID*)correct, (DWORD)LI_FN(strlen)(correct), (LPDWORD)oxorany(NULL), (LPVOID)oxorany(NULL));
    }
    else {
        LI_FN(WriteConsoleA)((HANDLE)hStdOut, (CONST VOID*)incorrect, (DWORD)LI_FN(strlen)(incorrect), (LPDWORD)oxorany(NULL), (LPVOID)oxorany(NULL));
    }
    LI_FN(ReadConsoleA)((HANDLE)hStdIn, buffer, sizeof(buffer) - oxorany(2), &bytesRead, (PCONSOLE_READCONSOLE_CONTROL)NULL);
    return oxorany(0);
}