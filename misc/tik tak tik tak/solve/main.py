from pwn import *

r = remote("127.0.0.1", 8080)

print(r.recvuntil(b"continue...\n\n"))
res = ""
while True:
    s_time = time.time()
    r.sendline(b"1\n")
    print(r.recv(2048))
    e_time = time.time()
    dt = e_time - s_time
    # print(dt)
    if dt > 1:
        res += " "
    elif dt > 0.3:
        res +="-"
    else:
        res += "."
    print(res)