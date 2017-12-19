
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#diag1 = [[str(r)+str(10- int(c)) for (r,c) in zip(rows,cols)]]
#diag2 = [[r+c for (r,c) in zip(rows,cols)]]
#unitlist = row_units + column_units + square_units + diag1 + diag2

diagonal_units_1 = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]
diagonal_units_2 = [['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]
unitlist = row_units + column_units + square_units + diagonal_units_1 + diagonal_units_2

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!

    all_digits = '123456789'
    
    for unit in row_units + column_units + square_units:
        d = dict()
        for digit in all_digits:
            # get all boxes in the unit that have the digit
            boxes_with_digit = ''.join([box for box in unit if digit in values[box]])
            # if a digit is only in 2 boxes:
            if len(boxes_with_digit) == 4:
                # Insert the concatenated boxes names as the key in a dictionary with digit as the value 
                if (boxes_with_digit not in d.keys()): 
                    # print('inserting:', digit, ' in ', boxes_with_digit)
                    d[boxes_with_digit] = digit
                # If the concatenated boxes names are already in the dictionary, we have a twin!
                else:
                    digits = d[boxes_with_digit] + digit
                    # print('updating:', digits, ' in ', boxes_with_digit)

                    for box in unit:
                        if (box in boxes_with_digit):
                            # These 2 boxes must have only these 2 values
                            assign_value(values, box, digits) #values[box] = digits
                            
                        else:
                            # The rest of the boxes cannot have these digits
                            assign_value(values, box, values[box].replace(digits[0], ""))
                            assign_value(values, box, values[box].replace(digits[1], ""))
                            # values[box] = values[box].replace(digits[0], "")
                            # values[box] = values[box].replace(digits[1], "")
    return values
    #raise NotImplementedError

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,'')) 
            # values[peer] = values[peer].replace(digit,'')
    return values
    #raise NotImplementedError

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    all_digits = '123456789'

    for unit in unitlist:
        for digit in all_digits:
            # get all boxes in the unit that have the digit
            boxes_with_digit = [box for box in unit if digit in values[box]]
            # if there is only 1 box, update it
            if len(boxes_with_digit) == 1:
                assign_value(values, boxes_with_digit[0], digit) 
                # values[boxes_with_digit[0]] = digit
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the naked twins strategy
        values = naked_twins(values) 
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    # Chose one of the unfilled square s with the fewest possibilities
    unsolved_values = [box for box in values.keys() if len(values[box]) > 1]
    # print(len(unsolved_values))
    if len(unsolved_values) > 0:
        box, vals = sorted(values.items(), key = lambda x: 10 if (len(x[1]) <= 1) else len(x[1]))[0]
        # print(box, vals)
        for v in vals:
            values_try = values.copy()
            assign_value(values_try, box, v) 
            # values_try[box] = v
            solve_try = search(values_try)
            if solve_try:
                return solve_try
    else:
        return values



def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve((diag_sudoku_grid)))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

