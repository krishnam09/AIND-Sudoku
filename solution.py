assignments = []

def assign_value(values, box, value):
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    for unit in column_units+row_units:
        unit_values = [values[b] for b in unit]
        pairs = [b for n,b in enumerate(unit) if (len(values[b]) == 2) and (values[b] in unit_values[:n]+unit_values[n+1:])]
        for nt in pairs:
            for peer in unit:
                for d in values[nt]:
                    if (len(values[peer]) >2):
                        values = assign_value(values, peer, values[peer].replace(d,''))

    return values

def cross(A, B):
    return [s + t for s in A for t in B]

def grid_values(grid):
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    result = dict(zip(boxes, grid))
    for a in result.keys():
        if result[a] == '.':
            result[a] = '123456789'
    return result

def display(values):
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

    return

def eliminate(values):
    data = [x for x in values.keys() if len(values[x]) == 1]
    for x in data:
        string = values[x]
        for peer in peers[x]:
            values = assign_value(values, peer, values[peer].replace(string, ''))
    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled, count = False, 0

    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    values = grid_values(grid)
    values=reduce_puzzle(values)
    return values

### Parameters to be used globally
rows = 'ABCDEFGHI'
cols = '123456789'
Range='0123456789'
boxes = cross(rows, cols)
row_units = [cross(s, cols) for s in rows]
column_units = [cross(rows, t) for t in cols]

square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[r+c for (r,c) in zip(rows,cols)], [r+c for (r,c) in zip(rows,cols[::-1])]]
unitlist = row_units + column_units + square_units  + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

if __name__ == '__main__':
    #diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'  # Easy Grid#
    diag_sudoku_grid='2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
