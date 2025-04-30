import numpy as np


M = np.fromfile("flag.npy", int)
C = matrix(np.reshape(M, (sqrt(len(M)), sqrt(len(M)))))

flag = ''.join(chr(sqrt(i // 2)) for i in C.cholesky().diagonal())

print(flag)
