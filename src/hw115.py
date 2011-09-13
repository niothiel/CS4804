from heapq import heappush, heappop
from math import sqrt
import random

class EasyQueue:
    def __init__(self):
        self.h = []
    
    def queue(self, priority, value):
        heappush(self.h, (priority, value))
    
    def dequeue(self):
        return heappop(self.h)[1]
    
    def peek(self):
        return self.h[0]
    
    def contains(self, obj):
        for priority, value in self.h:
            if value == obj:
                return True
        return False
    
    def __len__(self):
        return len(self.h)

class State:
    def __init__(self, board):
        self.board = board
    
    def _get_swapped(self, idx1, idx2):
        new_board = self.board[:]
        temp = new_board[idx1]
        new_board[idx1] = new_board[idx2]
        new_board[idx2] = temp
        return State(new_board)
        
    def get_permutations(self):
        permutations = []
        board = self.board
        idx = board.index(-1)
        
        side_len = sqrt( len(board) )
        side_len = int(side_len)
        
        if idx > (side_len - 1):
            swap = idx - side_len
            up = self._get_swapped(idx, swap)
            permutations.append(up)
        
        if idx < (side_len * side_len - side_len):
            swap = idx + side_len
            down = self._get_swapped(idx, swap)
            permutations.append(down)
        
        if (idx % side_len) > 0:
            swap = idx - 1
            left = self._get_swapped(idx, swap)
            permutations.append(left)
        
        if (idx % side_len) < (side_len - 1):
            swap = idx + 1
            right = self._get_swapped(idx, swap)
            permutations.append(right)
        
        return permutations
        
    def __str__(self):
        return 'State: ' + str( self.board )
    
    def __eq__(self, other):
        if type(self) == type(other):
            return self.board == other.board
        else:
            return False
        
    def __hash__(self):
        return hash( str(self.board) )

def get_depth(x, came_from):
    if x not in came_from.keys():
        return 0
    return 1 + get_depth(came_from[x], came_from)

def solve(start, end, h_func):
    closedset = []
    openset = EasyQueue()
    came_from = {}
    
    g_scores = {}
    h_scores = {}
    f_scores = {}
    
    g_scores[start] = 0
    h_scores[start] = h_func(start, end)
    f_scores[start] = g_scores[start] + h_scores[start]
    
    openset.queue(f_scores[start], start)
    num_expansions = 0
    while len(openset) > 0:
        x = openset.dequeue()
        num_expansions += 1
        if x.board == end.board:
            print "Yay, we win!"
            depth = get_depth(x, came_from)
            return (num_expansions)
        
        closedset.append(x)
        
        for perm in x.get_permutations():
            if perm in closedset:
                continue
            
            temp_g = g_scores[x] + 1
            temp_g_is_better = False
            
            if not openset.contains(perm):
                openset.queue(temp_g, perm)
                temp_g_is_better = True
            elif temp_g < g_scores[perm]:
                temp_g_is_better = True
            else:
                temp_g_is_better = False
            
            if temp_g_is_better:
                came_from[perm] = x
                g_scores[perm] = temp_g
                h_scores[perm] = h_func(perm, end)
                f_scores[perm] = g_scores[perm] + h_scores[perm]

def h1(state, goal):
    h = 0
    for n in range( len(state.board) ):
        if state.board[n] != goal.board[n]:
            h += 1
    return h

def h2(state, goal):
    return 0

def h3(state, goal):
    return 0

def h4(state, goal):
    return 0

def bfs(state, goal):
    return 0

def generate8(N=1000):
    init_board = [1, 2, 3, 4, -1, 6, 7, 8, 9]
    return _generate(init_board, N)

def generate15(N=1000):
    init_board = [1, 2, 3, 4, 5, 6, 7, -1, 9, 10, 11, 12, 13, 14, 15, 16]
    return _generate(init_board, N)

def _generate(board, N):
    #random.seed(1)
    start = State(board)
    end = State(board)
    
    for n in range(N):
        end = random.choice( end.get_permutations() )
        
    return (start, end)

def do_heuristic_test():
    start, end = generate8()
    print start, end
    print solve(start, end, bfs)
    pass

def main():
    start = State([-1, 1, 2, 4, 6, 3, 7, 5, 8])
    #start = State([1, 2, 3, 4, 5, 6, 7, -1, 8])
    end = State([1, 2, 3, 4, 5, 6, 7, 8, -1])
    
    print 'H1:', solve(start, end, h1)
    print 'BFS:', solve(start, end, bfs)
    
    for n in range(100):
        print generate8()[1]

if __name__ == "__main__":
    #main()
    do_heuristic_test()