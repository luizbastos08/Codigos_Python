import numpy as np
from scipy.linalg import lu_factor, lu_solve
from timer import _timer
from random import random

@_timer
def interior_point(A, b, c, alpha0=0.99, tolerance=1e-9, max_iterations=100000000):
    """
    Author: Luiz Souza
    Date: april-2023

    Define and adjusts the input parameters for the interior point algorithm.
    """
    xmin = np.zeros(len(c))                             # Define the minimum limit of x equal to zero
    m,n = np.shape(A)
    xmax = np.array(b)                                  # Define the maximum limit of x equal to the values of vector b
    # xmax_norma = np.linalg.norm(xmax)
    
    """
    Define a negative reference value to check if the origin point is an interior point using the inequality Ax <= b,
    already done for the case of augmented matrices.
    """
    rel = np.full(len(c)+len(b),-1)

    """
    Define the first interior point near the origin
    """
    Xini = (1e-11 + 1e-8 * random())*(xmax) 
    Xini = np.array(Xini)

    I = -1*np.eye(len(c))
    expanded_A = np.vstack((A, I))                      # Insert the slack variables into matrix A, creating the augmented matrix A
    
    aux = np.zeros(len(c))
    expanded_b = np.hstack((b, aux))                    # Insert the slack variables into vector b, creating the augmented vector b


    """
    Beginning of the interior point algorithm
    """
    valzero = tolerance**3                              # Value considered for zero
    infmax = 1/(tolerance**4)                           # Value considered for infinite 

    
    # Checks if the start point - Xini is an interior point
    if not np.array_equal(np.sign(np.dot(expanded_A, Xini) - expanded_b), rel):
        solution = {'header': f'INTERIOR POINT - Dim: {len(c)} / Alpha0: {alpha0} / Tolerance: {tolerance}', 
                'message': 'Initial X is not an interior point', 
                'status': 0,
                'error': 1, 
                }
            
        return solution

    M,N = np.shape(expanded_A)                          # Define the values of M and N based on the dimensions of the augmented matrix A

    
    """
    Initiation of the auxiliary variables
    """
    x = Xini
    xold = x
    DeltaX = np.zeros(len(c))
    evolx = []
    evolx.append(Xini)

    iter = 1
    flag = 0

    Dk = np.zeros((M,M))

    """
    Calculates the objetive function with the initial X
    """
    Fobj = c @ Xini
    evolFobj = []
    evolFobj.append(Fobj)
    

    """
    Loop function that calculates the interior point algorithm
    """
    while iter <= max_iterations and flag == 0:
        
        """
        Step I
        Calculates how far each point is from the boundary
        """
        Vk = expanded_b.T - expanded_A @ x.T
        Vk = np.maximum(Vk, np.power(np.finfo(float).eps, 4))
                
        Dk = np.diag(1./Vk)                             # Calculates the diagonal matrix
        
        """
        Step II
        Solves the system of linear equations dx = (A'DkDkA)^(-1)*c
        and calculates dv = -A*dx
        """
        LU, piv = lu_factor(np.dot(np.dot(expanded_A.T, Dk), Dk).dot(expanded_A))
        dx = lu_solve((LU, piv), c)

        dv = np.dot(-expanded_A, dx)
        
        """
        Step III
        Calculates the step (alpha) and
        calculates the new x
        """
        Vaux = np.zeros((M,1))
                
        for i in range(M):
            if dv[i] > -valzero:
                Vaux[i] = -infmax
            else:
                Vaux[i] = Vk[i] / dv[i]
        
        Valpha = np.max(Vaux)
        
        x = x - alpha0*Valpha*dx

        """
        Step IV
        Calculates the new objective function and the dual problem solution yk
        as well as the final gap
        """
               
        for j in range(N):
            if x[j] < xmin[j]:
                x[j] = xmin[j]
            if x[j] > xmax[j]:                
                x[j] = xmax[j]

        """
        Calculates DeltaX
        """         
        if iter != 1:
            DeltaX = x - xold
            
            """
            If the solution x is tolerance unchanged from the precedin one,
            then the algorithm has an optimal solution
            """
            if np.max(np.abs(DeltaX)) < tolerance:
                xold = x
                flag = 1
            
            """
            Evaluate objective function
            """
            Fobj = c @ x
            evolFobj.append(Fobj)

            """
            Calculates the candidate primal solution
            """
            yk = -Dk @ Dk @ dv

            gap_final = np.abs(expanded_b @ yk.T - Fobj) / np.max([1, np.abs(Fobj)])
            """
            The algorithm has an optimal solution
            """
            if gap_final < tolerance:
                flag = 1
   
        evolx.append(x)                             # Storage evolx                         
        xold = x                                    # Storage xold as x

        """
        Evaluate the number of iterations
        """
        if iter >= max_iterations:
            flag = 1
        else:
            if flag == 0:
                iter = iter + 1

    """
    Creates the solution dictionary
    """
    solution = {'header': f'INTERIOR POINT - Dim: {len(c)} / Alpha0: {alpha0} / Tolerance: {tolerance}', 
                'message': 'Optimization terminated successfully', 
                'status': 0, 
                'max_value': Fobj, 
                'solution': x,
                'primal_solution': yk,
                'num_iterations': iter,
                'evolution_x': evolx,
                'evolution_Fobj':evolFobj,
                'gap_final': gap_final,
                }            

    return solution