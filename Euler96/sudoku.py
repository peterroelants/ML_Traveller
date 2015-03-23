"""
For the project euler problem I picked the Sudoku solver problem (problem 96)[https://projecteuler.net/problem=96].

This problem is rather trivial with a constraint logic programming solver.
I picked the (Numberjack python)[http://numberjack.ucc.ie/] library to code my solution in.
This library lets you code the constraints in python and uses a number of (C++) constraint solvers
in the back to efficiently solve the problem.
"""
import urllib2
import re
import numpy as np
from Numberjack import *


def parse_sudokus():
    """
    Function to read the sudokus from the given url file, and parse them
    so they are represented in an numpy matrix.

    Returns a list of sudoku matrices.
    """
    # Open the url with the sudokus for the challenge
    data = urllib2.urlopen('https://projecteuler.net/project/resources/p096_sudoku.txt')
    sudokus = [] # List to hold all sudokus
    current_sudoku = None # Current sudoku we are building
    current_sudoku_row = 0 # Current line of the current sudoku we are building
    for line in data:
        # Check if the line is the start of a new sudoku
        result = re.match(r'(Grid \d\d)', line.strip())
        if not result is None:
            # New sudoku
            current_sudoku = np.zeros((9,9), dtype=np.int8)
            current_sudoku_row = 0
            # store the new sudoku
            sudokus.append(current_sudoku)
        else:
            # Get the numbers
            result = re.match(r'(\d{9})', line.strip())
            col_string = result.groups()[0]
            # Fill up sudoku
            for col in xrange(0, 9):
                current_sudoku[current_sudoku_row, col] = int(col_string[col])
            current_sudoku_row += 1
    return sudokus


def solve_sudoku(sudoku):
    """
    Function to solve the given sudoku with the help of the solver.

    Return the solution as a matrix in the solver library.
    """
    # Define the solution matrix that represents the sudoku puzzle
    solution = Matrix(9, 9, 1, 9)

    # Set up the model
    model = Model()

    # Set the constraints for the filled in cells
    for i in xrange(0, 9):
        for j in xrange(0, 9):
            if sudoku[i, j] > 0:
                model.add(solution[i, j] == int(sudoku[i, j]))

    # Add the constraint that all rows need to be different
    model.add([AllDiff(x) for x in solution.row])
    # Add the constraint that all columns need to be different
    model.add([AllDiff(y) for y in solution.col])
 
    # Add the constraint that all cells need to be different
    for i in xrange(0, 3):
        for j in xrange(0, 3):
            # Generate the constraint for each cell
            # x goes over the rows in each cell
            # y goes over the columns in each cell
            model.add(AllDiff(
                [solution[x, y] for x in xrange(i*3, (i+1)*3) for y in xrange(j*3, (j+1)*3)]))

    # Load a solver and solve the problem
    solver = model.load('MiniSat')
    solver.solve()
    return solution


def get_first_three(sudoku):
    """
    Function that solves the given sudoku and returns the first 3 digits of the first row.
    """
    solution = solve_sudoku(sudoku)
    return int(''.join([str(solution[0,i]) for i in xrange(0,3)]))


def main():
    # Get al the puzzles from the url
    sudokus = parse_sudokus()
    # Sum the first 3 digits for each solution
    sum_numbers = 0
    for sudoku in sudokus:
        sum_numbers += get_first_three(sudoku)
    print sum_numbers


if __name__ == "__main__":
    main()