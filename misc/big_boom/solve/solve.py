import string


def reverse_djbx33a(target_hash: int, length: int, alphabet: str):
    MASK = 0xFFFFFFFFFFFFFFFF
    results = []
    cur_hash = (target_hash ^ length) & MASK

    def dfs(pos: int, h: int, s: str):
        if pos == 0:
            if h == 5381:
                results.append(s)
            return
        for c in alphabet:
            ordc = ord(c)
            if ((h - ordc) % 33) == 0:
                prev_hash = ((h - ordc) // 33) & MASK
                dfs(pos - 1, prev_hash, c + s)

    dfs(length, cur_hash, "")
    return results

alphabet = string.printable
max_len = 7

target_hashes = [6385415121, 193433130, 210654488433, 6953250040028, 6383401807, 210722229252]

for target_hash in target_hashes:
    print(f"{target_hash=}:")
    found = False
    for length in range(1, max_len + 1):
        words = reverse_djbx33a(target_hash, length, alphabet)
        if words:
            print(words)
            found = True
    if not found:
        print("404. ¯\_(ツ)_/¯")