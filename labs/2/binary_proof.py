import numpy as np
def binary_list(n):
    return [[int(j) for j in '{:0{}b}'.format(i, n)] for i in range(n*n-1)]

all_ = binary_list(7)
all_sum = np.array([sum(x) for x in all_])
idxs = np.where(all_sum <= 4)
lesst4 = np.array(all_)[idxs].tolist()
lesst4 = [int(''.join([str(y) for y in x]),2) for x in lesst4]
print(lesst4)

result1 = [0 + x % (100+1 - 0) for x in lesst4]
print(result1)