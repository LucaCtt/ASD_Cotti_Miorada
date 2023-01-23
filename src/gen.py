from datetime import datetime
import numpy as np


class Inst:
    def __init__(self, A, P, gen_at):
        self.A = A
        self.M = A.shape[1]
        self.N = A.shape[0]
        self.P = P
        self.gen_at = gen_at


def gen_inst(M, N, P):
    A = np.empty((N, M), dtype=int)

    for i in range(0, N):
        row = np.zeros(M, dtype=int)
        unique = False

        # Genera una riga casuale finchè non è sia non vuota
        # (almeno un elemento diverso da zero)
        # sia unica rispetto alle righe già generate
        while not row.any() or not unique:
            row = np.random.binomial(1, P, M)

            unique = True  
            # Itera solo sulle righe già generate
            for element in A[0:i]:
                if (row == element).all():
                    unique = False

        A[i] = row

    return Inst(A, P, datetime.today())


def write_inst(output_file, inst):
    with open(output_file, 'w') as file:
        file.write(f';;; Generated at: {inst.gen_at}\n')
        file.write(f';;; M: {str(inst.M)}\n')
        file.write(f';;; N: {str(inst.N)}\n')
        file.write(f';;; P: {str(inst.P)}')

        for row in inst.A:
            file.write(f'\n{np.array2string(row)[1:-1]} -')
