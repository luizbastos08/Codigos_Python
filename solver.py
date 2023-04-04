from time import time
from functools import wraps
from murty import point_to_vertex
from scipy.optimize import linprog
from random import random
import numpy as np
from scipy.linalg import solve
from scipy.linalg import lu_factor, lu_solve

# See documentation for the SciPy functions at:
# https://docs.scipy.org/doc/scipy/reference/optimize.linprog-revised_simplex.html


def _timer(func):
    """
    Decorator that times each solution
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        solution = func(*args, **kwargs)
        end = time()
        solution['elapsed_time'] = end - start
        return solution

    return wrapper

@_timer
def simplex(A, b, c, x0=None, max_iterations=100000000):
    """
    Uses revised SIMPLEX algorithm to solves LP problem of the form:
    maximize c*x with: A*x <= b and x >= 0
    :param x0: Initial vertex (Default is origin)
    :param max_iterations: Maximum number of iterations to be run
    :return: Dictionary with solution info
    """
    header = f'SIMPLEX - Dim: {len(c)}'
    try:
        scipy_solution = linprog(c=-c, A_ub=A, b_ub=b, method='revised simplex', x0=x0,
                                 options= {'maxiter': max_iterations})
    except Exception as error:
        return {'header': header, 'error': error}
    solution = {'header': header, 'message': scipy_solution.message, 'status': scipy_solution.status,
                'max_value': -scipy_solution.fun, 'solution': scipy_solution.x, 'num_iterations': scipy_solution.nit, }
    # return _generic_solver('revised simplex', A, b, c, x0, {'maxiter': max_iterations})
    return solution

@_timer
def hybrid(A, b, c, alpha0=0.99995, tolerance=1e-8, max_iterations=100000000):
    solution_ip = interior_point(A, b, c, alpha0, tolerance, max_iterations)
    if 'error' in solution_ip:
        x0_simplex = None
    else:
        x0_simplex = point_to_vertex(solution_ip['solution'], A, b)
    # x0_simplex = None if 'error' in solution_ip else point_to_vertex(solution_ip['solution'], A, b)
    solution_simplex = simplex(A, b, c, x0_simplex, max_iterations)
    return _merge_solutions(solution_ip, solution_simplex)


def _merge_solutions(solution_int_point, solution_simplex):
    """
    Merges solutions into a single solution for the hybrid algorithm
    """
    solution = {'header': solution_int_point['header'].replace('INTERIOR POINT', 'HYBRID')}
    for key, value in solution_int_point.items():
        if key == 'header':
            continue
        solution[key] = {'interior_point': value}
    for key, value in solution_simplex.items():
        if key == 'header':
            continue
        if key in solution:
            solution[key]['simplex'] = value
            if key == 'num_iterations' or key == 'elapsed_time':
                solution[key]['total'] = solution[key]['interior_point'] + solution[key]['simplex']
    return solution


def solution_to_str(solution, level=1, hide=('message', 'status', 'solution')):
    """
    Useful script to have solution as a more user-friendly text
    """
    ans = ''
    for key, value in solution.items():
        if hide and key in hide:
            continue
        if key == 'header':
            ans += f'{value}\n'
            continue
        ans += '\t' * level + key + ': '
        if isinstance(value, dict):
            ans += '\n' + solution_to_str(value, level=level + 1)
        else:
            ans += f'{value}\n'
    return ans

@_timer
def interior_point(A, b, c, alpha0=0.99995, tolerance=1e-9, max_iterations=100000000):
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
                 
        if iter != 1:
            DeltaX = x - xold
            
            if np.max(np.abs(DeltaX)) < tolerance:
                xold = x
                flag = 1
            
            Fobj = c @ x
            
            evolFobj.append(Fobj)

            yk = -Dk @ Dk @ dv

            gap_final = np.abs(expanded_b @ yk.T - Fobj) / np.max([1, np.abs(Fobj)])
            if gap_final < tolerance:
                flag = 1

        Fobj = c @ x
        evolFobj.append(Fobj)
        
        evolx.append(x)
        xold = x

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
                'num_iterations': iter,
                }            

    return solution