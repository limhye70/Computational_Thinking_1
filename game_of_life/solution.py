"""
How Acorn will appear at generation=1000
"""
import numpy as np
from collections import defaultdict
from itertools import product
import time
import matplotlib.pyplot as plt


def expand_matrix(a,m):
    """ Zero-pad matrix 'a'.
    1. surround 'a' with two zero rows/colums.
    2. Add a zero row and column until (rows-2) and (cols-2) are both multiplied by m
    3. used in function `comepute_n`
    Args:
        a (array): Input matrix
        m (int): unit shape
    Returns:
        matrix(array): zero-padded 'a'
    """

    # wrap the original matrxi with zeros first
    for x in range(2):
        a = np.vstack([np.array([0]*a.shape[1]), a, np.array([0]*a.shape[1])])
        a = np.hstack([np.array([0]*a.shape[0]).reshape(a.shape[0],1), a, np.array([0]*a.shape[0]).reshape(a.shape[0],1)])

    # how many zero_row does it need? it's not multitple of (m+2), km+2
    a_1 = a.copy()
    i = 1
    while (a_1.shape[0]-2) % m != 0:
        a_1 = np.vstack([a_1, np.array([0]*a_1.shape[1])])
        i+=1

    j = 1
    while (a_1.shape[1]-2) % m != 0:
        a_1 = np.hstack([a_1, np.array([0]*a_1.shape[0]).reshape(a_1.shape[0],1)])
        j+=1

    return a_1


def compute_n(a,m):
    """count living neighbours of target cells.
    This is used to create a (m+2)-by-(m+2) hashtable.
    Args:
        a (list) : An m-by-m matrix flattend row-by-row e.g., [[0000],[1111],[0011],[1100]] is saved as [0,0,0,0,1,1,1,1,0,0,1,1,1,1,0,0]
    Returns:
        dictionary: 
            - key(list): target cells' indexes
            - value(int): number of living nerigbours. e.g., {(0,3):4}: (0,3)-entry has 4 living neighbours.
    """

    # Identify target positions (mxm)
    k = m+3 # first target position
    target_positions = [i for i in range(k,k+m)] # first target row (1-by-m)
    for i in range(m-1): # move down until mth target row
        target_positions+=[r+(m+2) for r in target_positions[-m:]]
    
    # Identify neighbour positions for each target position
    n_position_collection=defaultdict(list)
    for k in target_positions:
        n_positions = [k-1,k,k+1] # neibour' positions beside the target cell (middle row)
        n_positions = [i-(m+2) for i in n_positions] + n_positions+[i+(m+2) for i in n_positions] # add neighbour positions' above and beneath target cell
        n_position_collection[k] = [i for i in n_positions if i!=k] # exclude target cell's position (k)

    # count living neighbours
    living_neighbours = defaultdict()
    for k,v in n_position_collection.items():
        n_values = [a[i] for i in v]  # get neighbour cell values using indexes
        living_neighbours[k] = sum(n_values) # sum living neighbours
    return living_neighbours

def life_or_death (cell, n):
    """ Determine the next status of the target cell
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

def clean_matrix(a):
    """Removes empthy edge rows and columns
    Args:
        a(array): a matrix to be cleaned
    Returns:
        array: a trimmed array
    """
    # cleaning result by removing surrounding empty rows and columns
    while a[:,0].sum() == 0: # columns
        a = a[:,1:]
    while a[:,-1].sum() == 0:
        a = a[:,:-1]

    while a[0,:].sum() == 0: # rows
        a = a[1:,:]
    while a[-1,:].sum() == 0:
        a = a[:-1,:]

    return a

def next_generation(a,m,hashmap):
    """Predict next generation using a hashmap
    1. prediction proceeds for m-by-m from left to right and top to bottom at a time
    2. Each (m+2)-by-(m+2) matrix is looked up iin `hashmap` to get the next generation of it's central m-by-m part.
    2. zero edges will be trimmed after the operation is done.

    Args:
        a (array): matrix to be predicted
        m (int): target matrix size
        hashmap (dict): 
            - key (list): a flattened (m+2)-by-(m+2) matrix block
            - value (list): a flattened m-by-m target matrix, the next generation of key 
    Returns:
        array: next generation of `a`

    """

    a = expand_matrix(a,m)

    # move the box by row from right to left
    i = 0
    j = 0
    partition_output=defaultdict()
    while i+m+2 <= a.shape[0]:
        j = 0
        while j+m+2 <= a.shape[1]:
            a_partition = a[i:i+m+2,j:j+m+2]
            j+=m
            lookup_value = tuple(a_partition.flatten())
            partition_output[(i,j)]=np.array(hashmap[lookup_value]).reshape([m,m])
        i+=m # move toe the next row

    # assembe output into a matrix form
    row_assemble=defaultdict()
    for k,v in partition_output.items():
        if k[0] not in row_assemble.keys():
            row_assemble[k[0]]=v
        else:
            row_assemble[k[0]]=np.hstack([row_assemble[k[0]],v])

    x=0        
    for v in row_assemble.values():
        if x == 0:
            col_assemble = v
            x += 1
            
        else:
            col_assemble = np.vstack([col_assemble,v])
               
    return col_assemble



def main(a,m,n):
    """ Play Game of Life
    Args:
        a (array): Input matrix
        m (int): unit matrix length
        n (int): Number of generation to simulate
    Return:
        array: the matrix representing the state after 'n' generation
    """

    #create hashmap for target matrix mxm
    print(f'creating a hashmap m={m}')
    hashmap = defaultdict(list)
    for z in product([0,1], repeat=2**(m+2)):
        hashmap[z]= [life_or_death(z[k],v) for k,v in compute_n(z,m).items()]
    # print('done')
    for i in range(n):
        if i == 0:
            b = clean_matrix(next_generation(a,m,hashmap))
        else:
            b = clean_matrix(next_generation(b,m,hashmap))
    return b
    

if __name__ == "__main__":
    # # Input
    acorn = np.array([[0,1,0,0,0,0,0],[0,0,0,1,0,0,0],[1,1,0,0,1,1,1]])
    m=2
    n = 1000

    # Run
    start_time = time.time()
    solution = main(acorn, m,n)
    end_time = time.time()

    # visualise
    plt.axis('off')
    plt.imshow(solution, cmap='Blues', interpolation='none')
    plt.savefig('solution_week2.png')

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
    
    with open("solution_summary_week2.txt", "w", encoding="utf-8") as file:
        file.write(summary)

    # np.savetxt("solution.txt", solution, delimiter=" ", fmt="%d")


