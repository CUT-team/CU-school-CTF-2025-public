

def encode_flag(flag):
    transformed = []
    for i, char in enumerate(flag):
        val = (ord(char) + i + 42) % 256
        transformed.append(val)

    key = [0x37, 0x15, 0x93, 0x42, 0x66, 0x28, 0x51, 0x19]
    xored = []
    for i, val in enumerate(transformed):
        xored.append(val ^ key[i % len(key)])

    salt = [0x8A, 0x45, 0xC2, 0x7D]
    interleaved = []
    for i, val in enumerate(xored):
        interleaved.append(val)
        interleaved.append(salt[i % len(salt)])
    
    hex_values = [f"0x{val:02X}" for val in interleaved]

    return hex_values

if __name__ == "__main__":
    flag = input("Enter your CTF flag: ")
    encoded = encode_flag(flag)

    print("\nEncoded flag array (for C++):")
    print("unsigned char encoded_flag[] = {" + ", ".join(encoded) + "};")
    print(f"\nArray length: {len(encoded)}")
