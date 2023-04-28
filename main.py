from KleeMinty_Solver.klee_minty import *
from KleeMinty_Solver.hybridAlgorithm import *
from KleeMinty_Solver.results_generator import *
import json
import numpy as np
from KleeMinty_Solver.murtyAlgorithm import murty
from KleeMinty_Solver.revised_simplex import revised_simplex, simplex
from KleeMinty_Solver.interior_points import interior_point
import argparse

"""
    Author: Luiz Henrique de Bastos Souza
    Date: april-2023
    Based on the work of Amanda Dusse and Igor Baratta, former students of professor Rodney Rezende Saldanha at UFMG.
"""

def solution_project_I_UFMG():
    """
    A function that calculates the solution for the Klee-Minty problem
    using the simplex algorithm, interior point algorithm and murty-hybrid algorithm
    and generate the results in a word file.
    This function aims to answer all the questions given in the first project
    of the optimization course given by Prof. Rodney Saldanha at UFMG
    """
    dimensions = [2, 4, 6, 10, 14, 18, 20, 22, 24, 26]
    dimensions_aux = [2, 6, 10, 14, 18, 22, 26]
    val_b = 100
    alpha0 = [0.01, 0.05, 0.10, 0.30, 0.50, 0.70, 0.8, 0.9, 0.95, 0.99]
    tolerance = [1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10]

    # Opening the JSON file and reading its contents
    with open('dados.json', 'r') as f:
        dados = json.load(f)

    
    for i in range(len(dimensions)):

        #Set the Klee-Minty Problem
        A, b, c = klee_minty(dimensions=dimensions[i], val_b=val_b)
        
        #Calculates the average running time for the interior points algorithm
        aux = []
        aux_hybrid = []
        for j in range(10):
            sol_ip = interior_point(A, b, c, alpha0=alpha0[8], tolerance=1e-3)
            sol_hybrid = hybrid(A, b, c, alpha0=alpha0[8], tolerance=1e-3)
            aux.append(sol_ip['elapsed_time'])
            aux_hybrid.append(sol_hybrid['elapsed_time'])
        mean = np.mean(aux)
        mean_hybrid = np.mean(aux_hybrid)
        # Adding values for the "Simplex\Execution Time" key
        dados['dataframe1']['Interior Points\nExecution Time'][i] = round(mean,4)
        dados['dataframe1']['Hybrid\nExecution Time'][i] = round(mean_hybrid,4)

        #Calculates the error of the solution for the interior points algorithm
        x_solution = sol_ip['solution'][dimensions[i]-1]
        correct_x_solution = val_b**(dimensions[i]-1)
        error_x_solution = 100 * abs(correct_x_solution - x_solution) / correct_x_solution

        x_solution_hybrid = sol_hybrid['solution']['simplex'][dimensions[i]-1]
        error_x_solution_hybrid = 100 * abs(correct_x_solution - x_solution_hybrid) / correct_x_solution
        #Calculates the error of the objetive function for the interior points algorithm
        Fobj_solution = sol_ip['max_value']
        correct_Fobj_solution = val_b**(dimensions[i]-1)
        error_Fobj_solution = 100 * abs(correct_Fobj_solution - Fobj_solution) / correct_Fobj_solution

        Fobj_solution_hybrid = sol_hybrid['max_value']['simplex']
        error_Fobj_solution_hybrid = 100 * abs(correct_Fobj_solution - Fobj_solution_hybrid) / correct_Fobj_solution
        # Adding values for the "Simplex\Execution Time" key
        dados['dataframe2']['Interior Points\nIterations'][i] = sol_ip['num_iterations']
        dados['dataframe3']['Interior Points\nObjective Funcion Error (%)'][i] = round(error_Fobj_solution,9)
        dados['dataframe4']['Interior Points\nSolution Error (%)'][i] = round(error_x_solution,9)

        dados['dataframe2']['Hybrid\nIterations'][i] = sol_hybrid['num_iterations']['total']
        dados['dataframe3']['Hybrid\nObjective Funcion Error (%)'][i] = error_Fobj_solution_hybrid
        dados['dataframe4']['Hybrid\nSolution Error (%)'][i] = error_x_solution_hybrid
    """
    for i in range(len(dimensions_aux)):
        #Set the Klee-Minty Problem
        A, b, c = klee_minty(dimensions=dimensions_aux[i], val_b=val_b)

        
        for j in range(len(alpha0)):
            aux_interior_point = []
            aux_hybrid = []
            for z in range(10):
                sol_ip = interior_point(A, b, c, alpha0=alpha0[j], tolerance=tolerance[5])
                sol_hybrid = hybrid(A, b, c, alpha0=alpha0[j], tolerance=tolerance[5])
                aux_interior_point.append(sol_ip['elapsed_time'])
                aux_hybrid.append(sol_hybrid['elapsed_time'])
            mean_interior_point = np.mean(aux_interior_point)
            mean_hybrid = np.mean(aux_hybrid)
            #Calculates the error of the solution for the interior points algorithm
            x_solution = sol_ip['solution'][dimensions_aux[i]-1]
            correct_x_solution = val_b**(dimensions_aux[i]-1)
            error_x_solution = 100 * abs(correct_x_solution - x_solution) / correct_x_solution
            #Calculates the error of the objetive function for the interior points algorithm
            Fobj_solution = sol_ip['max_value']
            correct_Fobj_solution = val_b**(dimensions_aux[i]-1)
            error_Fobj_solution = 100 * abs(correct_Fobj_solution - Fobj_solution) / correct_Fobj_solution
            # Adding values for the "Simplex\Execution Time" key
            if dimensions_aux[i] == 2:
                dados['dataframe5']['Exec Time\nn=2'][j] = round(mean_interior_point,4)
                dados['dataframe6']['Iterations\nn=2'][j] = sol_ip['num_iterations']
                dados['dataframe7']['Objective Function Error (%)\nn=2'][j] = round(error_Fobj_solution,9)
                dados['dataframe8']['Solution Error (%)\nn=2'][j] = round(error_x_solution,9)
                dados['dataframe9']['Exec Time\nn=2'][j] = round(mean_hybrid,4)
                dados['dataframe10']['Iterations\nn=2'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 6:
                dados['dataframe5']['Exec Time\nn=6'][j] = round(mean_interior_point,4)
                dados['dataframe6']['Iterations\nn=6'][j] = sol_ip['num_iterations']
                dados['dataframe7']['Objective Function Error (%)\nn=6'][j] = round(error_Fobj_solution,9)
                dados['dataframe8']['Solution Error (%)\nn=6'][j] = round(error_x_solution,9)
                dados['dataframe9']['Exec Time\nn=6'][j] = round(mean_hybrid,4)
                dados['dataframe10']['Iterations\nn=6'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 10:
                dados['dataframe5']['Exec Time\nn=10'][j] = round(mean_interior_point,4)
                dados['dataframe6']['Iterations\nn=10'][j] = sol_ip['num_iterations']
                dados['dataframe7']['Objective Function Error (%)\nn=10'][j] = round(error_Fobj_solution,9)
                dados['dataframe8']['Solution Error (%)\nn=10'][j] = round(error_x_solution,9)
                dados['dataframe9']['Exec Time\nn=10'][j] = round(mean_hybrid,4)
                dados['dataframe10']['Iterations\nn=10'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 14:
                dados['dataframe5']['Exec Time\nn=14'][j] = round(mean_interior_point,4)
                dados['dataframe6']['Iterations\nn=14'][j] = sol_ip['num_iterations']
                dados['dataframe7']['Objective Function Error (%)\nn=14'][j] = round(error_Fobj_solution,9)
                dados['dataframe8']['Solution Error (%)\nn=14'][j] = round(error_x_solution,9)
                dados['dataframe9']['Exec Time\nn=14'][j] = round(mean_hybrid,4)
                dados['dataframe10']['Iterations\nn=14'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 18:
                dados['dataframe5']['Exec Time\nn=18'][j] = round(mean_interior_point,4)
                dados['dataframe6']['Iterations\nn=18'][j] = sol_ip['num_iterations']
                dados['dataframe7']['Objective Function Error (%)\nn=18'][j] = round(error_Fobj_solution,9)
                dados['dataframe8']['Solution Error (%)\nn=18'][j] = round(error_x_solution,9)
                dados['dataframe9']['Exec Time\nn=18'][j] = round(mean_hybrid,4)
                dados['dataframe10']['Iterations\nn=18'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 22:
                dados['dataframe5']['Exec Time\nn=22'][j] = round(mean_interior_point,4)
                dados['dataframe6']['Iterations\nn=22'][j] = sol_ip['num_iterations']
                dados['dataframe7']['Objective Function Error (%)\nn=22'][j] = round(error_Fobj_solution,9)
                dados['dataframe8']['Solution Error (%)\nn=22'][j] = round(error_x_solution,9)
                dados['dataframe9']['Exec Time\nn=22'][j] = round(mean_hybrid,4)
                dados['dataframe10']['Iterations\nn=22'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 26:
                dados['dataframe5']['Exec Time\nn=26'][j] = round(mean_interior_point,4)
                dados['dataframe6']['Iterations\nn=26'][j] = sol_ip['num_iterations']
                dados['dataframe7']['Objective Function Error (%)\nn=26'][j] = round(error_Fobj_solution,9)
                dados['dataframe8']['Solution Error (%)\nn=26'][j] = round(error_x_solution,9)
                dados['dataframe9']['Exec Time\nn=26'][j] = round(mean_hybrid,4)
                dados['dataframe10']['Iterations\nn=26'][j] = sol_hybrid['num_iterations']['total']
        
        for j in range(len(tolerance)):
            aux_interior_point = []
            aux_hybrid = []
            for z in range(10):
                sol_ip = interior_point(A, b, c, alpha0=alpha0[4], tolerance=tolerance[j])
                sol_hybrid = hybrid(A, b, c, alpha0=alpha0[4], tolerance=tolerance[j])
                aux_interior_point.append(sol_ip['elapsed_time'])
                aux_hybrid.append(sol_hybrid['elapsed_time'])
            mean_interior_point = np.mean(aux_interior_point)
            mean_hybrid = np.mean(aux_hybrid)
            #Calculates the error of the solution for the interior points algorithm
            x_solution = sol_ip['solution'][dimensions_aux[i]-1]
            correct_x_solution = val_b**(dimensions_aux[i]-1)
            error_x_solution = 100 * abs(correct_x_solution - x_solution) / correct_x_solution
            #Calculates the error of the objetive function for the interior points algorithm
            Fobj_solution = sol_ip['max_value']
            correct_Fobj_solution = val_b**(dimensions_aux[i]-1)
            error_Fobj_solution = 100 * abs(correct_Fobj_solution - Fobj_solution) / correct_Fobj_solution
            # Adding values for the "Simplex\Execution Time" key
            if dimensions_aux[i] == 2:
                dados['dataframe11']['Exec Time\nn=2'][j] = round(mean_interior_point,4)
                dados['dataframe12']['Iterations\nn=2'][j] = sol_ip['num_iterations']
                dados['dataframe13']['Objective Function Error (%)\nn=2'][j] = round(error_Fobj_solution,7)
                dados['dataframe14']['Solution Error (%)\nn=2'][j] = round(error_x_solution,7)
                dados['dataframe15']['Exec Time\nn=2'][j] = round(mean_hybrid,4)
                dados['dataframe16']['Iterations\nn=2'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 6:
                dados['dataframe11']['Exec Time\nn=6'][j] = round(mean_interior_point,4)
                dados['dataframe12']['Iterations\nn=6'][j] = sol_ip['num_iterations']
                dados['dataframe13']['Objective Function Error (%)\nn=6'][j] = round(error_Fobj_solution,7)
                dados['dataframe14']['Solution Error (%)\nn=6'][j] = round(error_x_solution,7)
                dados['dataframe15']['Exec Time\nn=6'][j] = round(mean_hybrid,4)
                dados['dataframe16']['Iterations\nn=6'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 10:
                dados['dataframe11']['Exec Time\nn=10'][j] = round(mean_interior_point,4)
                dados['dataframe12']['Iterations\nn=10'][j] = sol_ip['num_iterations']
                dados['dataframe13']['Objective Function Error (%)\nn=10'][j] = round(error_Fobj_solution,7)
                dados['dataframe14']['Solution Error (%)\nn=10'][j] = round(error_x_solution,7)
                dados['dataframe15']['Exec Time\nn=10'][j] = round(mean_hybrid,4)
                dados['dataframe16']['Iterations\nn=10'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 14:
                dados['dataframe11']['Exec Time\nn=14'][j] = round(mean_interior_point,4)
                dados['dataframe12']['Iterations\nn=14'][j] = sol_ip['num_iterations']
                dados['dataframe13']['Objective Function Error (%)\nn=14'][j] = round(error_Fobj_solution,7)
                dados['dataframe14']['Solution Error (%)\nn=14'][j] = round(error_x_solution,7)
                dados['dataframe15']['Exec Time\nn=14'][j] = round(mean_hybrid,4)
                dados['dataframe16']['Iterations\nn=14'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 18:
                dados['dataframe11']['Exec Time\nn=18'][j] = round(mean_interior_point,4)
                dados['dataframe12']['Iterations\nn=18'][j] = sol_ip['num_iterations']
                dados['dataframe13']['Objective Function Error (%)\nn=18'][j] = round(error_Fobj_solution,7)
                dados['dataframe14']['Solution Error (%)\nn=18'][j] = round(error_x_solution,7)
                dados['dataframe15']['Exec Time\nn=18'][j] = round(mean_hybrid,4)
                dados['dataframe16']['Iterations\nn=18'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 22:
                dados['dataframe11']['Exec Time\nn=22'][j] = round(mean_interior_point,4)
                dados['dataframe12']['Iterations\nn=22'][j] = sol_ip['num_iterations']
                dados['dataframe13']['Objective Function Error (%)\nn=22'][j] = round(error_Fobj_solution,7)
                dados['dataframe14']['Solution Error (%)\nn=22'][j] = round(error_x_solution,7)
                dados['dataframe15']['Exec Time\nn=22'][j] = round(mean_hybrid,4)
                dados['dataframe16']['Iterations\nn=22'][j] = sol_hybrid['num_iterations']['total']
            elif dimensions_aux[i] == 26:
                dados['dataframe11']['Exec Time\nn=26'][j] = round(mean_interior_point,4)
                dados['dataframe12']['Iterations\nn=26'][j] = sol_ip['num_iterations']
                dados['dataframe13']['Objective Function Error (%)\nn=26'][j] = round(error_Fobj_solution,7)
                dados['dataframe14']['Solution Error (%)\nn=26'][j] = round(error_x_solution,7)
                dados['dataframe15']['Exec Time\nn=26'][j] = round(mean_hybrid,4)
                dados['dataframe16']['Iterations\nn=26'][j] = sol_hybrid['num_iterations']['total']
        """

    # Saves updated dictionary back to JSON file
    with open('dados.json', 'w') as f:
        json.dump(dados, f)

    f.close()

    gen_results()

    return


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
    #print("Solution: {}".format(solution_dict["solution"]['simplex'][2]))
    print("Number of Iterations: {}".format(solution_dict["num_iterations"]))
    print("Elapsed Time: {:.4f} seconds".format(solution_dict["elapsed_time"]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dimensions', type=int, default=3, help='dimension of Klee-Minty problem')
    parser.add_argument('-b', '--val_b', type=float, default=100, help='vector b in Klee-Minty problem')
    parser.add_argument('-a', '--algorithm', choices=['simplex', 'interior', 'murty'], default='murty', help='algorithm to solve Klee-Minty problem')
    parser.add_argument('-t', '--tolerance', type=float, default=1e-9, help='tolerance for the solver')
    parser.add_argument('-alpha', '--alpha0', type=float, default=0.99, help='initial barrier parameter')
    parser.add_argument('-r', '--results', choices=['cmd', 'word'], default='cmd', help='set the results format')
    args = parser.parse_args()
    
    solution = Solve_Klee_Minty(args.dimensions, args.val_b, args.algorithm, args.tolerance, args.alpha0)
    
    if args.results == 'word':
        solution_project_I_UFMG()
    else:
        print_solution_summary(solution)
    
    