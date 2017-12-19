
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
unitlist_orginal = row_units + column_units + square_units
box_allvalues = '123456789'

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
# First select boxes with 2 entries
    #all_possible_naked_twins_values = [values[box] for box in values.keys() if len(values[box]) == 2]

    # then we use those values and isolate only the ones that appears more than once on the board: our candidates
    for unit in unitlist_orginal:
        d = dict()
        for digit in box_allvalues:
            # get all boxes in the unit that have the values
            potential_twin = [box for box in unit if digit in values[box]]
            
            boxes_with_digit = ''.join(potential_twin)
            print(boxes_with_digit)
            # if a digit is only in 2 boxes:
            if len(boxes_with_digit) == 4:
                # Insert the concatenated boxes names as the key in a dictionary with digit as the value 
                if (boxes_with_digit not in d.keys()): 
                    print('inserting:', digit, ' in ', boxes_with_digit)
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
    return values
    #raise NotImplementedError

def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function

    #all_digits = '123456789'

    for unit in unitlist:
        for digit in cols:
            Box_OneValue = [box for box in unit if digit in values[box]]
            if len(Box_OneValue) == 1:
                assign_value(values, Box_OneValue[0], digit) 
    return values
    #raise NotImplementedError

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function

    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    #raise NotImplementedError

def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function

    values = reduce_puzzle(values)
    if values is False:
        return False
    # Chose one of the unfilled square s with the fewest possibilities
    not_solved = [box for box in values.keys() if len(values[box]) > 1]
    if len(not_solved) > 0:
        box, vals = sorted(values.items(), key = lambda x: 10 if (len(x[1]) <= 1) else len(x[1]))[0]
        for v in vals:
            attempted_values = values.copy()
            attempted_values[box] = v
            attempted_sol = search(attempted_values)
            if attempted_sol:
                return attempted_sol
    else:
        return values

    #raise NotImplementedError


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

if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

