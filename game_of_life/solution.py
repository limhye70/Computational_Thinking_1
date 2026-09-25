"""
How Acorn will appear at generation=1000
"""
import numpy as np
from collections import defaultdict
import time
import matplotlib.pyplot as plt

def get_indexes(a):
    """Extract all (row, column) index pairs from a matrix
    Args:
        a (array): Input matrix
    Returns:
        list: A list of (i,j) tuples
    """
    indexes=[]
    for x in range(a.shape[0]):
        for y in range(a.shape[1]):
            indexes.append((x,y))
    return (indexes)

def expand_matrix(a):
    """ Expands the matrix by adding zeros around it
    Args:
        a (array): Input matrix (mxn)
    Returns:
        array: An (m+2)x(n+2) matrix
    """
    # expand a by 1 row from all sides
    zero_row = np.array([0]*a.shape[1])
    a_1 = np.vstack([zero_row,a,zero_row])
    zero_col = np.array([0]*a_1.shape[0]).reshape(a_1.shape[0],1)
    a_2 = np.hstack([zero_col,a_1,zero_col])
    return a_2

def compute_n (a):
    """ Computes the number of living neigher cells for each cell in the matrix
    Args:
        a (array): Input matrix of 0s and 1s
                    - 1: living cell
                    - 0: dead cell
    Returns:
        array: A matrix of same shape as 'a', where each entry is the count of living neighers for the corresponding cell.
    """
    neighbours = defaultdict(list)  
    for x,y in get_indexes (a):
        n_indexes = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x+1,y-1),(x+1,y),(x,y+1),(x+1,y+1)] # neighbour indexes
        mask = [(x in range(a.shape[0])) & (y in range(a.shape[1])) for x,y in n_indexes]
        neighbours[(x,y)] = [a for a,b in zip(n_indexes, mask) if b]

    b = np.zeros(a.shape) # array with the same shape as a to save the number of living neighbours
    for k, v in neighbours.items():
        life=[]
        for x in v:
            life.append(a[x])
        n=sum(life)
        b[k]=n

    return(b)

def life_or_death (cell, n):
    """ Determine the next status of the input cell
    Args:
        cell (int): Current status of the cell (0 or 1)
        n (int): Number of living neighbours of the corresponding cell. 
    
    Returns:
        int: 0 or 1, the status of the cell after one generation
    """
    if cell == 1:
        if n in (2,3):
            return 1
        else:
            return 0

    if cell == 0:
        if n == 3:
            return 1
        else:
            return 0

def next_generation (a):
    """ Compute the next generation of the matrix
    Args:
        a (array): Input matrix
    Retruns:
        array: the matrix after one generation
    """
    a_2 = expand_matrix(a)
    b = compute_n(a_2)

    # compute life or death
    result = np.zeros(a_2.shape)
    for i in get_indexes(a_2):
        result[i] = life_or_death(a_2[i],b[i])

    # cleaning result by removing surrounding empty rows and columns
    while result[:,0].sum() == 0: # columns
        result = result[:,1:]
    while result[:,-1].sum() == 0:
        result = result[:,:-1]

    while result[0,:].sum() == 0: # rows
        result = result[1:,:]
    while result[-1,:].sum() == 0:
        result = result[:-1,:]

    return result


def main (a, n):
    """ Play Game of Life
    Args:
        a (array): Input matrix
        n (int): Number of generation to simulate
    Return:
        array: the matrix representing the state after 'n' generation
    """
    for i in range(n):
        if i == 0:
            b = next_generation(a)
        else:
            b = next_generation(b)
    return b


if __name__ == "__main__":
    # Input
    acorn = np.array([[0,1,0,0,0,0,0],[0,0,0,1,0,0,0],[1,1,0,0,1,1,1]])
    n = 1000

    # Run
    start_time = time.time()
    solution = main(acorn, n)
    end_time = time.time()

    # visualise
    plt.axis('off')
    plt.imshow(solution, cmap='Blues', interpolation='none')
    plt.savefig('solution.png')

    # Save the result
    summary = f"""
            # Generation: {n}
            # Total Living Cells: {solution.sum()}
            # Shape of the output matrix: {solution.shape}
            # Living Cells by Columns:
                {solution.sum(0)}
            # Living Cells by Rows:
                {solution.sum(1)}
    
            Running Time: {end_time - start_time} secs
            """
    
    with open("solution_summary.txt", "w", encoding="utf-8") as file:
        file.write(summary)

    np.savetxt("solution.txt", solution, delimiter=" ", fmt="%d")



