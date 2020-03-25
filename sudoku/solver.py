from sudoku import rules

class Puzzle(object):

    def __init__(self):
        #self.puzzle_map.clear()
        self.puzzle_map = []
        for i in range(9):
            self.puzzle_map.append([]) #add a empty line
            for j in range(9):
                self.puzzle_map[i].append([])
                #for k in range(9):
                self.puzzle_map[i][j].append(rules.Cell())

    def puzzle_copyto(self, dest):
        '''get a copy of puzzle map for working purpose'''
        for i in range(9):
            for j in range(9):
                dest.puzzle_map[i][j].clear()
                for k in range(len(self.puzzle_map[i][j])):
                    dest.puzzle_map[i][j].append(self.puzzle_map[i][j][k].copy_cell())

    def convert_board(self):
        tmpboard = rules.Board()
        for i in range(9):
            for j in range(9):
                tmpboard.Cells[i][j] = self.puzzle_map[i][j][0].copy_cell()
        return tmpboard


    def puzzle_trim(self):
        '''after puzzle change, trim out all invalid chioces
        return = 1, still work to do, 0:solved already; -1: current puzzle is dead'''
        tmpboard = rules.Board()
        for i in range(9):
            for j in range(9):
                if self.puzzle_map[i][j][0].Status == rules.STATUS_INIT or self.puzzle_map[i][j][0].Status == rules.STATUS_CONFIRMED:
                    tmpboard.Cells[i][j] = self.puzzle_map[i][j][0].copy_cell()

        #first of all, check whehter the board is overall valid
        #tmpboard.print_layout()
        if tmpboard.validate() != 0:
            #print("dead board, no carry on")
            return -1 #if the current board is invalid, dead try

        for i in range(9):
            for j in range(9):
                if tmpboard.Cells[i][j].Status != rules.STATUS_INIT and tmpboard.Cells[i][j].Status != rules.STATUS_CONFIRMED:
                    self.puzzle_map[i][j].clear()
                    for k in range(1,10):
                        tmpcell = rules.Cell()
                        tmpcell.set(k, (i+1,j+1), rules.STATUS_TEST)
                        if tmpboard.validate(tmpcell)==0:
                            self.puzzle_map[i][j].append(tmpcell)
                    if len(self.puzzle_map[i][j]) == 1:
                        self.puzzle_map[i][j][0].Status = rules.STATUS_CONFIRMED

        #self.print_puzzle()
        issolved = True
        ilen =0
        for i in range(9):
            for j in range(9):
                ilen = len(self.puzzle_map[i][j])
                if ilen == 0:
                    #has slots without any possilble answers , dead
                    #print(f"slot(ilen) has 0 choices")
                    return -1
                elif ilen > 1:
                    #some slots still have multiple choices
                    issolved = False
                else:
                    continue
        if issolved: return 0
        return 1

    def puzzle_confirm(self, acell):
        self.puzzle_map[acell.Position[0]-1][acell.Position[1]-1].clear()
        self.puzzle_map[acell.Position[0]-1][acell.Position[1]-1].append(acell)
        self.puzzle_map[acell.Position[0]-1][acell.Position[1]-1][0].Status = rules.STATUS_CONFIRMED

    def puzzle_setup(self, aboard):
        for i in range(9):
            for j in range(9):
                self.puzzle_map[i][j].clear()
                if aboard.Cells[i][j].Status == rules.STATUS_INIT or aboard.Cells[i][j].Status == rules.STATUS_CONFIRMED:
                    tmpcell = aboard.Cells[i][j].copy_cell()
                    self.puzzle_map[i][j].append(tmpcell)
                else:
                    for k in range(1,10):
                        tmpcell = rules.Cell()
                        tmpcell.set(k, (i+1,j+1), rules.STATUS_TEST)
                        if aboard.validate(tmpcell)==0:
                            self.puzzle_map[i][j].append(tmpcell)
                    if len(self.puzzle_map[i][j]) == 1:
                        self.puzzle_map[i][j][0].Status = rules.STATUS_CONFIRMED


    def puzzle_next_start(self):
        canlist = []
        ir = 0
        jr = 0
        shortlen = 1
        lenr = 10
        for i in range(9):
            for j in range(9):
                shortlen = len(self.puzzle_map[i][j])
                #print(f"pos({i+1},{j+1}) has {shortlen} choices")
                if shortlen > 1:
                    if shortlen < lenr:
                        lenr = shortlen
                        ir = i
                        jr = j
                elif shortlen == 1:
                    continue
                else:
                    return None
        if lenr == 10: return None
        for k in range(lenr):
            canlist.append(self.puzzle_map[ir][jr][k].copy_cell())
        return canlist

    def print_puzzle(self):
        len1 = 0
        for i in range(9):
            for j in range(9):
                len1 = len(self.puzzle_map[i][j])
                str1 = f"SLOT[{i+1},{j+1}]-"
                if len1 == 0:
                    str1 = str1 + "EMPTY"
                else:
                    if self.puzzle_map[i][j][0].Status == rules.STATUS_INIT:
                        str1 = str1 + "INITL: " +str(self.puzzle_map[i][j][0].Value)
                    elif self.puzzle_map[i][j][0].Status == rules.STATUS_CONFIRMED:
                        str1 = str1 + "CNFRM: "+str(self.puzzle_map[i][j][0].Value)
                    else:
                        str1 = str1 + "CHICE: "
                        for k in range(len1):
                            str1 = str1 + f"{str(self.puzzle_map[i][j][k].Value)} "
                print(str1)

class Solver(object):
    #puzzle_solver = Puzzle()
    #solution_list = []

    def __init__(self):
        '''init the solution list'''
        '''init the puzzle map which is a 3d list to contain Cell choices'''
        self.puzzle_solver = Puzzle()
        self.solution_list = []
        self.sudoku_game = rules.Board()

    def setup(self):
        self.puzzle_solver.puzzle_setup(self.sudoku_game)

    def add_solution(self, puzzle):
        '''a board list, to keep the solution'''
        self.solution_list.append(puzzle.convert_board())



    def check_answer(self, puzzle):
        '''
        solve the sudoku
        1. look for all the possible answers for every empty slot
        2. if there is a slot with only one possible answer, it is.
        3. if there is any slot without any possible answers, dead. withdrawn
        4. start from the slot with the least possible answers, try one
        5. goto step 1
        '''
        solvable = False
        candidates = puzzle.puzzle_next_start()
        if candidates is None: return False
        working_puzzle = Puzzle()
        for i in range(len(candidates)):
            #print(f"------Try cell: {candidates[i].cell_string()}--------")
            puzzle.puzzle_copyto(working_puzzle)#make a memory, for next soulton, restore it
            working_puzzle.puzzle_confirm(candidates[i])
            re = working_puzzle.puzzle_trim()
            if re == 1:
                #not dead, not finished yet
                #print(f"valid trim, goto next")
                if self.check_answer(working_puzzle):
                    #this candidate works, recursively checked
                    #record this candidate as successful solution
                    #continue to try other possibilities
                    solvable = True
                    continue
            elif re == 0:#already finsihed
                #print(f"solved")
                self.add_solution(working_puzzle)
                solvable = True
                continue
            else:
                #this candidate is either trim wrong or a dead answer, discard this candidate
                #print("trim fail, goto next candidates")
                continue
        return solvable

    def print_solution(self, allanswer=False):
        j = len(self.solution_list)
        if j == 0 : print("NO Answer!")
        if allanswer:
            for i in range(j):
                print(f"ANSWER #{i+1}")
                self.solution_list[i].print_layout()
        else:
            print(f"ANSWER ")
            self.solution_list[0].print_layout()

    def start_solve(self):
        self.setup()
        apuzzle = Puzzle()

        self.puzzle_solver.puzzle_copyto(apuzzle)
        self.solution_list.clear()
        #apuzzle.print_puzzle()
        if self.check_answer(apuzzle):
            return True
        else:
            return False

    def load_game(self, nos):
        return self.sudoku_game.setup_random(nos)

    def display(self):
        print("")
        self.sudoku_game.print_layout()
        print("")

    def restart_game(self):
        self.sudoku_game.restart_board()

    def erase(self, rowpos, colpos):
        self.sudoku_game.update_cell_by_value(0, rowpos, colpos, False)

    def input(self, value, rowpos, colpos):
        self.sudoku_game.update_cell_by_value(value, rowpos, colpos)

    def complete_cmd(self):
        return self.solution_list[0].get_complete_cmd()

    def is_fill_all(self):
        return self.sudoku_game.is_full()

    def submit_game(self):
        return self.sudoku_game.is_full() and (self.sudoku_game.validate()==0)
