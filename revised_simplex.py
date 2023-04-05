import numpy as np
from scipy.linalg import lu_factor, lu_solve
from timer import _timer


@_timer
def simplex(A,b,c):
    Xini = np.array(np.zeros(len(b)))
    B, = np.where(Xini != 0.0)
    aux, = np.where(Xini == 0.0)
    aux = aux + len(b)
    B = np.concatenate((B, aux), axis=0)

    solution = revised_simplex(A,b,c, B)

    return solution


def revised_simplex(A, b, c, B, tolerance=1e-9, max_iterations=100000000):
        
    I = 1*np.eye(len(c))
    A = np.hstack((A, I))                      # Insert the slack variables into matrix A, creating the augmented matrix A
    
    aux = np.zeros(len(c))
    c = np.hstack((c, aux))                    # Insert the slack variables into vector b, creating the augmented vector b
    
    m,n = np.shape(A)
    
    # Step 1:- We are given an initial basis B
    N = np.setdiff1d(np.arange(0, n), B)

    LU, piv = lu_factor(A[:,B])
    xB = lu_solve((LU, piv), b)

    #xB = np.linalg.solve(A[:,B], b)
    xb1 = xB
    iter = 0
    evolx =[]
    evolobj = []

    while True:
        iter += 1

        # Step 2: Solve A_B^Ty = c_B and compute s_N = c_N - A_N^Ty
        # Declare optimality if s_N <= 0
        # Else find the entering non-basic variable x_{N(k)}
        #y = np.linalg.solve(A[:, B].T, c[B])
        LU, piv = lu_factor(A[:, B].T)
        y = lu_solve((LU, piv), c[B])
        sN = c[N] - A[:, N].T @ y
        k = np.argmax(sN)
        sNmax = sN[k]

        if sNmax <= tolerance:
            x = np.zeros(n)
            x[B] = xB
            obj = c @ x
            evolx.append(x)
            evolobj.append(evolobj)

            solution = {'header': f'SIMPLEX - Dim: {len(c)/2} / Tolerance: {tolerance}', 
                'message': 'Optimization terminated successfully', 
                'status': 0, 
                'max_value': obj, 
                'solution': x,
                'primal_solution': y,
                'num_iterations': iter,
                'evolution_x': evolx,
                'evolution_Fobj':evolobj,
                'gap_final': sNmax,
                }

            return solution

        # Step 3: Solve A_Bd = a_{N(k)}
        # Find theta = Min_{i=1,...,m|d_i > 0} xB(i)/d(i)
        # Let theta = xB(l)/d(l)
        # x_{B(l)} is the leaving basic variable
        # Also check for unboundedness if d <= 0
        d = np.linalg.solve(A[:, B], A[:, N[k]])
        zz = np.where(d > tolerance)[0]

        if zz.size == 0:
            raise Exception('System is unbounded')
        ii = np.argmin(xB[zz] / d[zz])
        theta = np.min(xB[zz] / d[zz])
        l = zz[ii]

        # Step 4: Update B and N
        # Also x(B(i)) = x(B(i)) - theta*d(i), i=1,...,m and i not equal to l
        temp = B[l]
        B[l] = N[k]
        N[k] = temp
        xB -= theta * d
        xB[l] = theta