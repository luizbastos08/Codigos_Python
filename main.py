from KleeMinty_Solver.klee_minty import *
from KleeMinty_Solver.hibrydAlgorithm import *
from results_generator import *
import json
import numpy as np
from KleeMinty_Solver.murtyAlgorithm import murty
from KleeMinty_Solver.revised_simplex import revised_simplex, simplex
from KleeMinty_Solver.interior_points import interior_point
import argparse

"""
    Author: Luiz Henrique de Bastos Souza
    Date: april-2023
"""

"""
dimensions = [2, 4, 6, 10, 14, 18, 20, 22, 24, 26]
val_b = 100
alpha0 = [0.01, 0.05, 0.10, 0.30, 0.50, 0.70]
tolerance = [1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10]

# Abrindo o arquivo JSON e lendo seu conteúdo
with open('dados.json', 'r') as f:
    dados = json.load(f)


for i in range(len(dimensions)):

    #Calcula o tempo médio de execução para o algoritmo de pontos interiores
    aux = []
    for j in range(10):
        A, b, c = klee_minty(dimensions=dimensions[i], val_b=val_b)
        sol_ip = interior_point(A, b, c, alpha0=alpha0[4], tolerance=tolerance[1])
        aux.append(sol_ip['elapsed_time'])
    mean = np.mean(aux)
    # Adicionando valores para a chave "Simplex\nExecution Time"
    dados['dataframe1']['Interior Points\nExecution Time'][i] = round(mean,4)

    #Calcula o número de iterações para o algoritmo de pontos interiores
    A, b, c = klee_minty(dimensions=dimensions[i], val_b=val_b)
    sol_ip = interior_point(A, b, c, alpha0=alpha0[4], tolerance=tolerance[1])
    print(solution_to_str(sol_ip))
    # Adicionando valores para a chave "Simplex\nExecution Time"
    dados['dataframe2']['Interior Points\nIterations'][i] = sol_ip['num_iterations']

# Salva o dicionário atualizado de volta ao arquivo JSON
with open('dados.json', 'w') as f:
    json.dump(dados, f)

f.close()
"""

def Solve_Klee_Minty(dimensions, val_b, algorithm, tolerance=1e-9, alpha0=0.99):
    # Define the Klee-Minty problem
    A, b, c = klee_minty(dimensions=dimensions, val_b=val_b)

    # Select the algorithm to use and solve
    if algorithm == "simplex":
        solution = simplex(A, b, c)
    elif algorithm == "interior":
        solution = interior_point(A, b, c, alpha0=alpha0, tolerance=tolerance)
    elif algorithm == "murty":
        solution = hybrid(A, b, c, alpha0=alpha0, tolerance=tolerance)
    else:
        raise ValueError("Invalid algorithm: {}".format(algorithm))

    # Return the solution
    return solution


def print_solution_summary(solution_dict):
    #Print the solution in a cleaner form
    print("{}:".format(solution_dict["header"]))
    print("Max Value: {}".format(solution_dict["max_value"]))
    print("Number of Iterations: {}".format(solution_dict["num_iterations"]))
    print("Elapsed Time: {:.4f} seconds".format(solution_dict["elapsed_time"]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dimensions', type=int, default=3, help='dimension of Klee-Minty problem')
    parser.add_argument('-b', '--val_b', type=float, default=100, help='vector b in Klee-Minty problem')
    parser.add_argument('-a', '--algorithm', choices=['simplex', 'interior', 'murty'], default='murty', help='algorithm to solve Klee-Minty problem')
    parser.add_argument('-t', '--tolerance', type=float, default=1e-9, help='tolerance for the solver')
    parser.add_argument('-alpha', '--alpha0', type=float, default=0.99, help='initial barrier parameter')
    args = parser.parse_args()
    
    solution = Solve_Klee_Minty(args.dimensions, args.val_b, args.algorithm, args.tolerance, args.alpha0)
    print_solution_summary(solution)