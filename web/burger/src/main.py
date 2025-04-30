mapping = {
    0: "patty",
    1: "tomato",
    2: "lettuce",
}

flag = "cuctf{r3333333ally777_l0ng_bug36_br0}"

def to_ternary(c):
    res = ""
    while c:
        res += str(c % 3)
        c //= 3
    return res[::-1].rjust(5, "0")
result = []
delay = 0
for letter in flag:
    for code in to_ternary(ord(letter)):
        result.append(
            f"<div class='ingredient {mapping[int(code)]}' style='animation-delay: {delay}ms'></div>"
        )
        delay += 100
    result.append(
        f"<div class='ingredient middle-bun' style='animation-delay: {delay}ms'></div>"
    )
    delay += 100

print("".join(result))