import numpy as np


def swap_rows(M, row_index_1, row_index_2):
    """
    Swap rows in the given matrix.

    Parameters:
    - matrix (numpy.array): The input matrix to perform row swaps on.
    - row_index_1 (int): Index of the first row to be swapped.
    - row_index_2 (int): Index of the second row to be swapped.
    """

    M = M.copy()
    M[[row_index_1, row_index_2]] = M[[row_index_2, row_index_1]]
    return M


# M = np.array([[1, 3, 6], [0, -5, 2], [-4, 5, 8]])
# print(M)


def get_index_first_non_zero_value_from_column(M, column, starting_row):
    """
    Retrieve the index of the first non-zero value in a specified column of the given matrix.

    Parameters:
    - matrix (numpy.array): The input matrix to search for non-zero values.
    - column (int): The index of the column to search.
    - starting_row (int): The starting row index for the search.

    Returns:
    int: The index of the first non-zero value in the specified column, starting from the given row.
                Returns -1 if no non-zero value is found.
    """
    column_array = M[starting_row:, column]
    for i, val in enumerate(column_array):
        if not np.isclose(val, 0, atol=1e-5):
            index = i + starting_row
            return index

    return -1


def augmented_matrix(A, B):
    """
    Create an augmented matrix by horizontally stacking two matrices A and B.

    Parameters:
    - A (numpy.array): First matrix.
    - B (numpy.array): Second matrix.

    Returns:
    - numpy.array: Augmented matrix obtained by horizontally stacking A and B.
    """
    augmented_M = np.hstack((A, B))
    return augmented_M


def row_echelon_form(A, B):
    """
    Utilizes elementary row operations to transform a given set of matrices,
    which represent the coefficients and constant terms of a linear system, into row echelon form.

    Parameters:
    - A (numpy.array): The input square matrix of coefficients.
    - B (numpy.array): The input column matrix of constant terms.

    Returns:
    numpy.array: A new augmented matrix in row echelon form with pivots as 1.
    """

    det_A = np.linalg.det(A)
    if np.isclose(det_A, 0) == True:
        return "Singular system"

    A = A.copy()
    B = B.copy()

    A = A.astype("float64")
    B = B.astype("float64")

    num_rows = len(A)
    M = augmented_matrix(A, B)

    for row in range(num_rows):
        pivot_candidate = M[row, row]

        if np.isclose(pivot_candidate, 0) == True:
            first_non_zero_pivot_candidate = get_index_first_non_zero_value_from_column(
                M, row, row
            )
            M = swap_rows(M, row, first_non_zero_pivot_candidate)
            pivot = M[row, row]

        else:
            pivot = pivot_candidate

        M[row] = (1 / pivot) * M[row]

        for j in range(row + 1, num_rows):
            value_below_pivot = M[j, row]
            M[j] = M[j] - value_below_pivot * M[row]

    return M


def back_substitution(M):
    """
    Perform back substitution on an augmented matrix (with unique solution) in reduced row echelon form to find the solution to the linear system.

    Parameters:
    - M (numpy.array): The augmented matrix in row echelon form with unitary pivots (n * n+1).

    Returns:
    numpy.array:
    The solution vector of the linear system.
    """

    M = M.copy()
    num_rows = M.shape[0]

    for row in reversed(range(num_rows)):
        substitution_row = M[row]

        for j in range(row):
            row_to_reduce = M[j]
            value = row_to_reduce[row]
            row_to_reduce = row_to_reduce - value * substitution_row
            M[j, :] = row_to_reduce

    solution = M[:, -1]
    return solution


def gaussian_elimination(A, B):
    """
    Solve a linear system represented by an augmented matrix using the Gaussian elimination method.

    Parameters:
    - A (numpy.array): Square matrix of size n x n representing the coefficients of the linear system
    - B (numpy.array): Column matrix of size 1 x n representing the constant terms.

    Returns:
    numpy.array: The solution vector.
    """

    row_echelon_M = row_echelon_form(A, B)

    solution = back_substitution(row_echelon_M)

    return solution


from utils import string_to_augmented_matrix

equations = """
3*x + 6*y + 6*w +8*z = 1
5*x + 3*y + 6*w = -10
4*y - 5*w + 8*z = 8
4*w + 8*z = 9
"""

variables, A, B = string_to_augmented_matrix(equations)

sols = gaussian_elimination(A, B)

if not isinstance(sols, str):
    for variable, solution in zip(variables.split(" "), sols):
        print(f"{variable} = {solution:.4f}")

else:
    print(sols)
