import time

def cross(A, B):
    return [a + b for a in A for b in B]

def display(values):
    width = 1+max(len(values[s]) for s in squares)

    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols)
        if r in 'CF':
            print line

def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits:
            values[s] = d
    return values

def grid_values(grid):
    chars = [c for c in grid if c in digits or c in '0.']
    return dict(zip(squares, chars))

def solve(grid, place):
    search(parse_grid(grid), place)

def is_solved(values):
    for s in squares:
        if len(values[s]) > 1:
            return False

        peer_list = peers[s]
        vals = [values[x] for x in peer_list]
        value = values[s]
        if value in vals:
            return False

    return True

def place_a(values, square, value):
    values[square] = value
    return values

def place_b(values, square, value):
    values[square] = value

    peer_list = peers[square]
    for p in peer_list:
        values[p] = values[p].replace(value, '')
        if len(values[p]) == 0:
            return False

    return values

def place_c(values, square, value):
    explored = []
    return place_c_helper(values, square, value, explored)

def place_c_helper(values, square, value, explored):
    values[square] = value
    explored.append(square)

    peer_list = peers[square]
    for p in peer_list:
        values[p] = values[p].replace(value, '')
        if len(values[p]) == 0:
            return False
        if len(values[p]) == 1 and p not in explored:
            place_c_helper(values, p, values[p], explored)

    return values

def place_d(values, square, value):
    values[square] = value

    peer_list = peers[square]
    vals = [values[x] for x in peer_list]
    if value in vals:
        return False
    else:
        return values

def search(values, place):
    if values == False:
        return

    if is_solved(values):
        #display(values)
        return
    
    cell = None
    options = None
    
    for s in squares:
        if len(values[s]) > 1:
            cell = s
            options = values[s]
            break

    if cell is None:
        return
    
    for o in options:
        newValues = values.copy()
        newValues = place(newValues, cell, o)
        search(newValues, place)

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

easy1 = '483921657967345820251876493548132976720504138136790245372680514814253769695017382'
easy2 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
med1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
med2  = '.237....68...6.59.9.....7......4.97.3.7.96..2.........5..47.........2....8.......'
hard1 = '7.....4...2..7..8...3..8.799..5..3...6..2..9...1.97..6...3..9...3..4..6...9..1.35'
hard2 = '....7..2.8.......6.1.2.5...9.54....8.........3....85.1...3.2.8.4.......9.7..6....'

funcs = [place_a, place_b, place_c, place_d]
puzzles = [easy1, easy2, med1, med2, hard1, hard2]

for f in funcs:
    for p in puzzles:
        t = time.clock()
        solve(p, f)
        elapsed = time.clock() - t
        print elapsed