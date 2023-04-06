import numpy as np

def murty(A, c, x):
    """
    Author: Luiz Souza
    Date: april-2023
    """
    I = 1*np.eye(len(c))
    A = np.hstack((A, I))                      # Insert the slack variables into matrix A, creating the augmented matrix A

    m,n = np.shape(A)
    # Starting tableau
    B = np.where(x > 0)[0]                      # index set of basic variables
    # R, jb = row_echelon(A[:, B])     # reduced row echelon form
    R = np.abs(np.linalg.qr(A[:, B], mode='r'))
    jb = np.where(np.abs(R) > 1e-10)[1]
    while len(B) > np.linalg.matrix_rank(A[:, B]):
        # Calculate search direction
        d = np.zeros(n)
        a = np.arange(R.shape[1])
        a[jb] = []  # columns that are not part of eye matrix
        d[B[jb]] = -R[:, a[0]]
        d[B[a[0]]] = 1

        # calculate step
        z = sum(c * d)
        rate = x[B] / d[B]
        if z <= 0:
            f = np.where((d[B] < 0) & (rate <= 0))[0]
            lambda_ = -np.min(rate[f])
        else:
            f = np.where((d[B] > 0) & (rate >= 0))[0]
            lambda_ = -np.max(rate[f])
        i = f[np.argmin(-rate[f])]

        if not i:
            break # optimal solution

        # step towards search direction (d = tetha)
        x = x + lambda_*d
        
        # update
        if np.all(jb != i):
            R = np.delete(R, i, axis=1)
        else:
            # pivotal operation
            ib = np.nonzero(R[:, i])[0]
            in_idx = np.argmax(np.abs(R[ib, a]), axis=1)
            in_idx = a[in_idx][0]
            R[ib, :] = R[ib, :] / R[ib, in_idx]
            inp = np.nonzero(np.arange(m) != ib)[0]
            R[inp, :] = R[inp, :] - R[inp, in_idx][:, None] * R[ib, :]
            R = np.delete(R, i, axis=1)  # remove column
            jb[jb == i] = in_idx  # update index of eye matrix
        jb[jb > i] = jb[jb > i] - 1

    
    return x, B




    
    
def row_echelon(A):
    m,n = np.shape(A)
    p = []
    for i in range(m):
        if A[i][i] == 0:
            print('Divido por zero!!! Parar')
        for j in range(i+1,m):
            ratio = -A[j][i]/A[i][i]
            A = RowAdd(A, i, j, ratio)
        A = RowScale(A, i, 1/A[i][i])
        if A[i][i] == 1:
            p.append(i)
    p = np.array(p)
    return A, p

def RowScale(A,k,scale):
# =============================================================================
#     A is a NumPy array.  RowScale will return duplicate array with the
#     entries of row k multiplied by scale.
# =============================================================================
    m = A.shape[0]  # m is number of rows in A
    n = A.shape[1]  # n is number of columns in A
    
    B = np.copy(A).astype('float64')

    for j in range(n):
        B[k][j] *= scale
        
    return B

def RowAdd(A,k,l,scale):
# =============================================================================
#     A is a numpy array.  RowAdd will return duplicate array with row
#     l modifed.  The new values will be the old values of row l added to 
#     the values of row k, multiplied by scale.
# =============================================================================
    m = A.shape[0]  # m is number of rows in A
    n = A.shape[1]  # n is number of columns in A
    
    B = np.copy(A).astype('float64')
        
    for j in range(n):
        B[l][j] += B[k][j]*scale
        
    return B
            
