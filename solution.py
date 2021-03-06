
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
    # we first find all possible naked twins values on the board
    all_possible_naked_twins_values = [values[box] for box in values.keys()
                                       if len(values[box]) == 2]

    # then we use those values and isolate only the ones that appears more than once on the board: our candidates
    #candidate_naked_twins_values = [candidate for candidate in all_possible_naked_twins_values
    #                                if all_possible_naked_twins_values.count(candidate)>1]

    naked_twins = [[box1,box2] for box1 in potential_twins \
                    for box2 in peers[box1] \
                    if set(values[box1])==set(values[box2]) ]

    # with our candidates, we iterate through our unitlist and find units that have square with the candidate values
    units_with_candidates = [u for u in unitlist for candidate in candidate_naked_twins_values for s in u
                             if values[s]==candidate]

    # once we isolated the possible units with our candidate values, we get a list of all values for that unit
    units_with_candidates_values_list = dict(("+".join(u), [values[s] for s in u]) for u in units_with_candidates)

    # with the unit value list, we confirm our naked-twins by verifying that they occur more than once in a unit
    #    and add them to our list.
    naked_twin_list = [twins for twins in candidate_naked_twins_values for u in units_with_candidates
                       if units_with_candidates_values_list["+".join(u)].count(twins)>1] 

    # with the confirmed set of naked-twins, we search the units that have them and add them to a dictionary
    units_with_naked_twins = dict(("+".join(u),naked) for u in units_with_candidates for naked in naked_twin_list
                                   if units_with_candidates_values_list["+".join(u)].count(naked)>1)
    
    # Eliminate the naked twins as possibilities for their peers
    # we already have the list of units and the naked-twins associated with them in our dictionary
    for naked_unit in units_with_naked_twins.keys():
        naked = units_with_naked_twins[naked_unit]

        # we just need to iterate through them and for squares that are not the ones with the naked-twins values,
        for box in naked_unit.split('+'):

            # if the boxes are not part of the naked-twins.
            if values[box] != naked:
                for digit in naked:
                    # remove the digits from boxes that are not part of the naked-twins.  DONE!
                    values = assign_value(values, box, values[box].replace(digit,''))
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

