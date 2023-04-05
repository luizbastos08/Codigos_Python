from klee_minty import *
from hibrydAlgorithm import *
from results_generator import *
import json
import numpy as np
from murtyAlgorithm import murty
from revised_simplex import revised_simplex, simplex
from interior_points import interior_point


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

A, b, c = klee_minty(dimensions=3, val_b=100)

sol_simplex = simplex(A, b, c)
sol_ip = interior_point(A, b, c, alpha0=0.99, tolerance=1e-9)
sol_hybrid = hybrid(A, b, c, alpha0=0.99, tolerance=1e-9)


print(sol_simplex)
print('\n')
print(sol_ip)
print('\n')
print(sol_hybrid)
