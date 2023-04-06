from KleeMinty_Solver.murtyAlgorithm import murty
from KleeMinty_Solver.revised_simplex import revised_simplex
from KleeMinty_Solver.interior_points import interior_point
from KleeMinty_Solver.timer import _timer


@_timer
def hybrid(A, b, c, alpha0=0.99, tolerance=1e-9, max_iterations=100000000):
    solution_ip = interior_point(A, b, c, alpha0, tolerance, max_iterations)
    if 'error' in solution_ip:
        x0_simplex = None
    else:
        x, B = murty(A,-c, solution_ip['primal_solution'])
    # x0_simplex = None if 'error' in solution_ip else point_to_vertex(solution_ip['solution'], A, b)
    solution_simplex = revised_simplex(A,b,c, B)
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