# Klee-Minty Problem Solver
### Author: Luiz Henrique de Bastos Souza
This program is designed to solve the Klee-Minty problem using three different algorithms: Simplex, Interior Points and Murty Hybrid.

## What is the Klee-Minty Problem?
The Klee-Minty problem is a special case of linear programming problem that was introduced by Victor Klee and George Minty in 1972. It has the following form:

$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a} $$
$$ \text{maximize } \sum_{j=1}^{n} 2^{n-j}x_j $$
subject to:
$$ 2\sum_{j=1}^{i-1} 2^{i-j}x_j + x_i \leq val_b^{i-1}, \quad i=1,2,\ldots,n $$
$$ x_j \geq 0, \quad j=1,2,\ldots,n $$

This problem is interesting because the Simplex algorithm takes an exponential amount of time to solve it in the worst case, while Interior Point algorithms can solve it in polynomial time. The Murty Hybrid algorithm is a combination of both Simplex and Interior Point algorithms that aims to exploit the advantages of both methods.

## How to Use the Program
The program is written in Python and can be run from the command line. To use it, follow these steps:

- Download or clone the repository to your computer.
- Install the required dependencies by running `pip install -r requirements.txt` in your command prompt or terminal.
- Run the program by executing the command `python main.py --dimensions <dimensions> --val_b <value_b> --algorithm <algorithm>` in your command prompt or terminal, where **<dimensions>** is the dimension of the problem, **<value_b>** is the vector b (15<=value_b<=100) and **<algorithm>** is one of the following: simplex, interior, or murty.
- The program will output the solution to the Klee-Minty problem using the specified algorithm.

## Results
The program will output the optimal solution to the Klee-Minty problem using the specified algorithm. The output will include the objective function value, the values of the decision variables, the number of iterations and the time required to obtain the solution.

## Conclusion
The Klee-Minty problem is a challenging linear programming problem that requires specialized algorithms to solve efficiently. This program offers three different algorithms to solve the problem, each with its own advantages and disadvantages. By using this program, you can explore the performance of these algorithms and gain a deeper understanding of linear programming.

## Acknowledgments
Based on the work of Amanda Dusse and Igor Baratta, former students of professor Rodney Rezende Saldanha at UFMG.

## References:
Katta G. Murty. "Linear complementarity, linear and non linear programming", pag 474-477, 1997
Vannelli.(1993). "Teaching Large-Scale Optimization by an Interior Point Approach"; IEEE Trans. on Education. (36)1:204-209
Kartik's MATLAB code for MA/OR/IE 505
