from sage.geometry.hyperbolic_space.hyperbolic_isometry import moebius_transform
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import pad


output = ""

PrecisionComplex = ComplexField(1000)
matrix_M = random_matrix(PrecisionComplex, 2, 2)

for _ in range(3):
    point = PrecisionComplex.random_element()
    image = moebius_transform(matrix_M, point)
    output += f"{point}, {image}\n"

key_point = PrecisionComplex.random_element()

output += f"{key_point}\n"
mapped_point = moebius_transform(matrix_M, key_point)

key_int = int((mapped_point.real() * modulus).round()) % (2**128)
iv_int = int((mapped_point.imag() * modulus).round()) % (2**128)

cipher_instance = AES.new(long_to_bytes(key_int), AES.MODE_CBC, iv=long_to_bytes(iv_int))

flag = b"cuctf{[REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED]}"

encrypted_flag = cipher_instance.encrypt(pad(flag, AES.block_size))
output += f"{encrypted_flag.hex()}"

with open("output.txt", 'w') as out:
    out.write(output)
