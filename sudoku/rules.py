import random

STATUS_CONFIRMED = 1
STATUS_INIT = 0
STATUS_TEST = 2
STATUS_UNDEFINE = -1

SUDOKU_HINT = [
    "[HINT]:",
    "  1. 'b2=1': fill slot B2 with '1'",
    "  2. 'submit': submit the answer",
    "  3. 'kill b2': erase slot B2",
    "  4. 'restart': restart same game",
    "  5. 'change': load different map",
    "  6. 'help': show answers",
    "  7. 'quit': quit"
]


class Cell(object):
    ''' a class to define one cell,  which includes:
    Position, Value and Status parameters.'''
    def __init__(self):
        self.Value = 0
        self.Position = (0,0)
        self.Status = STATUS_UNDEFINE

    def set(self, value, pos, status):
        self.Value = value
        self.Position = pos
        self.Status = status

    def copy_cell(self):
        acopy = Cell()
        acopy.Value = self.Value
        acopy.Status = self.Status
        acopy.Position = self.Position
        return acopy

    def cell_string(self):
        if self.Status == STATUS_INIT: s = "I"
        elif self.Status == STATUS_CONFIRMED: s = "C"
        elif self.Status == STATUS_TEST: s = "T"
        else: s = "U"
        str1 = f"[{self.Value}@({self.Position[0]},{self.Position[1]}){s}]"
        return str1

    def draw(self):
        pass


class Section(object):
    '''9 cells collection, could be rows, columns or houses'''

    def __init__(self, givencells):
        self.Cells = []
        for i in range(9):
            self.Cells.append(givencells[i])

    def length(self):
        return len(self.Cells)

    def find_empties(self, value):
        '''from section, search all empty cells with the value'''
        res = []
        for i in range(self.length()):
            if self.Cells[i].Value == value: return None
            if self.Cells[i].Status == STATUS_UNDEFINE:
                acell = Cell()
                acell.set(value, (self.Cells[i].Position), STATUS_CONFIRMED)
                res.append(acell)
        return res

    def find_position(self, value):
        for i in range(9):
            if self.Cells[i].Value == value:
                return self.Cells(i).Position
        return None

    def find_occurs(self, value):
        exists = 0
        for i in range(9):
            #print(f"cells[{i}].Value={self.Cells[i].Value} <> {value}")
            if self.Cells[i].Value == value:
                exists += 1
        #print(f"Found {exists}times of Value{value}")
        return exists

    def addr_mapping(self, setiontype, sectionindex, cell):
        '''given a cell from board, convert to a cell in section'''
        pass

    def validate(self, acell = None):
        '''Check whether there is no duplication'''
        if acell is None:
            for i in range(9):
                if self.find_occurs(i+1) > 1:
                    #no duplication, but no exisit is acceptable
                    return False
        else:
            if self.find_occurs(acell.Value) > 0:
                return False
        return True

    def value_string(self):
        '''convert the list of cells into a string with all values'''
        st = ""

        for i in range(len(self.Cells)):
            if self.Cells[i].Value > 0:
                st = "".join([st, str(self.Cells[i].Value)])
            else:
                st = "".join([st, "x"])
        return st

    def print_layout(self):
        '''print a section contents layout in console'''
        st = f"{self.Cells[0].Position[0]} |"
        for i in range(len(self.Cells)):
            if self.Cells[i].Value > 0:
                if self.Cells[i].Status == STATUS_INIT:
                    st = "".join([st, "[", str(self.Cells[i].Value), "]|"])
                else:
                    st = "".join([st, " ", str(self.Cells[i].Value), " |"])
            else:
                st = "".join([st, " ", "  |"])

        print(st)

    def draw(self):
        for i in range(0,9):
            self.Cells(i).draw()

class Board(object):
    '''Full 9x9 Soduku board'''

    def __init__(self):
        self.Cells = []
        self.init_cells()

    def init_cells(self, initpos=True):
        self.Cells.clear()
        acell = Cell()
        for i in range(0,9):
            self.Cells.append([]) #add a empty line
            for j in range(0,9):
                acell = Cell()
                if not initpos: acell.Position = (i+1,j+1)
                self.Cells[i].append(acell) #add a empty cell

    def update_cell(self, cell):
        acell = cell.copy_cell()
        cell.Value = self.Cells[cell.Position[0]-1][cell.Position[1]-1].Value
        cell.Status = self.Cells[cell.Position[0]-1][cell.Position[1]-1].Status
        cell.Position = self.Cells[cell.Position[0]-1][cell.Position[1]-1].Position
        self.Cells[cell.Position[0]-1][cell.Position[1]-1].Value = acell.Value
        self.Cells[cell.Position[0]-1][cell.Position[1]-1].Status = acell.Status
        self.Cells[cell.Position[0]-1][cell.Position[1]-1].Position = acell.Position

    def update_cell_by_value(self, value, rowpos, colpos, isInput=True):
        if self.Cells[rowpos-1][colpos-1].Status == STATUS_INIT: return
        self.Cells[rowpos-1][colpos-1].Value = value
        self.Cells[rowpos-1][colpos-1].Position = (rowpos, colpos)
        if isInput:
            self.Cells[rowpos-1][colpos-1].Status = STATUS_CONFIRMED
        else:
            self.Cells[rowpos-1][colpos-1].Status = STATUS_UNDEFINE


    def col(self, index):
        '''return a column section based on the index. pytest..passed'''
        return Section([row[index-1] for row in self.Cells])

    def row(self, index):
        '''return a row section based on the index. pytest..passed'''
        return Section(self.Cells[index-1])

    def pos(self, indexrow, indexcol):
        '''return a cell based on the given address. pytest..passed'''
        return self.Cells[indexrow -1][indexcol-1]

    def house(self, index):
        '''return a house section based on given index
        pytest pass'''
        res =[]
        r = int((index-1)/3) * 3
        c = ((index)%3-1) * 3
        if c < 0: c += 9
        for rr in range(r, r+3):
            for cc in range(c, c+3):
                res.append(self.Cells[rr][cc])
        return Section(res)

    def find_house_availables(self, value, houseindex):
        availist = self.house(houseindex).find_empties(value)
        if availist is None: return None
        ilen = len(availist)
        i = 0
        pos = 0
        for i in range(ilen):
            if self.validate(availist[pos]) != 0:
                availist.pop(pos)
            else:
                pos += 1
        str = f"Value{value} in House{houseindex} Availables: > "
        for i in range(len(availist)):
            str = str + availist[i].cell_string()
        #print(str)
        return availist

    def random_choose(self, choices):
        '''from a cell list, randomly choose one cell and pop it from the choice'''
        i = random.randint(1, len(choices))
        return choices.pop(i-1)

    def value_string(self):
        st = ""
        for i in range(1, 10):
            st = "".join([st, self.row(i).value_string()])
        return st

    def is_full(self):
        st = self.value_string()
        if (st.find("x") > 0 or st.find("X") > 0):
            return False
        else:
            return True

    def print_layout(self):
        print("    A   B   C   D   E   F   G   H   I")
        print("  +---+---+---+---+---+---+---+---+---+")
        for i in range(1, 10):
            self.row(i).print_layout()
            if i != 9:
                print(f"  +---+---+---+---+---+---+---+---+---+\t{SUDOKU_HINT[i-1]}")

        print("  +---+---+---+---+---+---+---+---+---+")


    def house_index(self, cell):
        a = int(cell.Position[0]/3)
        if cell.Position[0]%3 == 0: a -= 1
        b = int(cell.Position[1]/3)
        if cell.Position[1]%3 == 0: b -= 1
        houseno = a*3 + b + 1
        #print(f"Pos({cell.Position[0]},{cell.Position[1]})=>Hse(a:{a},b:{b}={houseno})")
        return houseno

    def validate(self, cell=None):

        if cell is not None: #cell.Value in range(1, 10):
            a = self.row(cell.Position[0]).validate(cell)
            #print(f"Cell{cell.cell_string()} validate check {a} in rowindex{cell.Position[0]}")
            if not a: return 1
            a = self.col(cell.Position[1]).validate(cell)
            if not a: return 2
            i = self.house_index(cell)
            a = self.house(i).validate(cell)
            if not a: return 3
            #print(f"Hse #{i} check ... passed")
        else:
            for i in range(1, 10):
                if not self.row(i).validate():
                    return 1
                #print(f"*Row #{i} check ... passed")
                if not self.col(i).validate():
                    return 2
                #print(f"*Col #{i} check ... passed")
                if not self.house(i).validate():
                    return 3
                #print(f"*Hse #{i} check ... passed")
        return 0

    def setup_manual(self, arrangement):
        '''give a board map, and init setup, arrangement is str, which use x as empty slot'''

        l = list(arrangement[:81])
        self.init_cells()

        r = -1
        c = -1
        ti = 0
        for i in range(81):
            if l[i].isdigit():
                ti = int(l[i])
                if ti in range(1,10):
                    r = int(i/9)
                    c = (i+1)%9 -1
                    if c<0: c += 9
                    self.Cells[r][c].set(ti, (r,c), STATUS_INIT)
            elif l[i] == 'x' or l[i] == 'X':
                continue
            else:
                self.init_cells()
                return False
        return True



    def set_number(self, nos, hseindex):
        availableinhse = [] #cell list to store the avaiable locatation for different number

        if hseindex > 9:
            #print(f"Value{nos} Passed, goto value{nos+1}")
            hseindex = 1
            nos += 1
            if nos == 10:
                #print(f"Fill in Complete!")
                return True
        availableinhse = self.find_house_availables(nos, hseindex)
        if availableinhse is None:
            #print(f"House{hseindex} Failed - None choices")
            return False
        availablenos = len(availableinhse)
        if availablenos == 0: #no available in this house, previous assumption is wrong
            #print(f"House{hseindex} Failed - No availables")
            return False

        while len(availableinhse) > 0:
            acell = self.random_choose(availableinhse)
            #print(f"Try cell: {acell.cell_string()}")
            self.update_cell(acell)
            if self.set_number(nos, hseindex+1):
                return True
            else:
                self.update_cell(acell)
                continue

        return False

    def get_solved_board(self):
        self.init_cells(False)
        #for i in range(1,10):
        return self.set_number(1, 1)

    def restart_board(self):
        for i in range(9):
            for j in range(9):
                if self.Cells[i][j].Status != STATUS_INIT:
                    acell = Cell()
                    acell.Position = (i + 1, j + 1)
                    self.update_cell(acell)

    def align_solved_board(self, occupiednos):
        #cut off 81-occupiednos slots randomly
        count = 0
        emptynos = 81 - occupiednos
        while count < emptynos:
            offset = random.randint(1, 81 - count)
            for x in range(9):
                for y in range(9):
                    if self.Cells[x][y].Status == STATUS_INIT or self.Cells[x][y].Status == STATUS_CONFIRMED:
                        offset -= 1
                    if offset == 0:
                        acell = Cell()
                        acell.Position = (x+1, y+1)
                        self.update_cell(acell)
                        count += 1
                        break
                if offset == 0: break
        for x in range(9):
            for y in range(9):
                if self.Cells[x][y].Status != STATUS_UNDEFINE:
                    self.Cells[x][y].Status = STATUS_INIT

    def get_complete_cmd(self):
        words = ""
        for i in range(9):
            for j in range(9):
                words = words + chr(self.Cells[i][j].Position[1]+ord("A")-1)+str(self.Cells[i][j].Position[0])+"="+str(self.Cells[i][j].Value) +" "
        return words

    def setup_random(self, occupiednos):
        if not self.get_solved_board(): return False

        #print(st)
        self.align_solved_board(occupiednos)
        return True
