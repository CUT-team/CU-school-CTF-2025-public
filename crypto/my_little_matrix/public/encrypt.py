import numpy as np


flag = b"cuctf{[HEHE_READCTED_HEHE]}"
key = np.matrix("[some_big_int_sq_mat]")


plaintext = np.array(list(flag))
eye = np.identity(len(key[0]), dtype=int)

key += eye * (np.square(plaintext) - np.diag(key))
key += key.T

combined = np.tril(key) @ np.triu(key)

combined.tofile("flag.npy")
