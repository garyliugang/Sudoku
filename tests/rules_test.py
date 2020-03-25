import pytest
from sudoku import rules
from sudoku import solver



def test_setup_manual():
    #test manual setup()
    game = rules.Board()
    manualsetup = "xx4xx3x8x6xxxxxxxx37xx5xx127239xx85x5xx26x9xxx6973xxx1xx53x726xx9xxxxx4xxxx1xxx7x"
    assert game.setup_manual(manualsetup)

    st = game.value_string()
    assert st == manualsetup

    #test pos()
    st = ""
    for i in range(1,10):
        for j in range(1, 10):
            if game.pos(i, j).Value == 0:
                st = "x"
            else:
                st = str(game.pos(i, j).Value)
            assert manualsetup[((i-1)*9+j-1):((i-1)*9+j)] == st

    #test_house():
    for i in range(1,10):
        spr = int((i-1)/3) * 3
        spc = (i%3-1) *3
        if spc < 0: spc += 9
        sp = spr * 9 + spc
        st = ""
        st = "".join([manualsetup[sp: sp+3], manualsetup[sp+9:sp+12], manualsetup[sp+18:sp+21]])
        assert game.house(i).value_string() == st

    # test_col():
    for i in range(1, 10):
        st = ""
        for j in range(1, 10):
            st = "".join([st,manualsetup[(j-1)*9+i-1:(j-1)*9+i]])
        assert game.col(i).value_string() ==st

    #test_row():
    st = ""
    for i in range(1, 10):
        st = "".join(manualsetup[(i-1)*9:(i-1)*9+9])
        assert game.row(i).value_string() == st

    #Section.value_string() & Board.value_string() has also been tested.

    #test section.validate
    for i in range(1, 10):
        assert game.row(i).validate()
        assert game.col(i).validate()
        assert game.house(i).validate()


    game.print_layout()
    asolver = solver.Solver()
    assert asolver.start_solve(game)
    asolver.print_solution()


def test_setup_auto():


    asolver = solver.Solver()
    #for i in range(150):
    #game.setup_manual("xx4xx3x8x6xxxxxxxx37xx5xx127239xx85x5xx26x9xxx6973xxx1xx53x726xx9xxxxx4xxxx1xxx7x")
    assert asolver.load_game(35)
    assert asolver.start_solve()
    asolver.display()
    assert 1==2

def tmpf(cells):
    '''cell.Position = (9,9)
    cell.Value = 9
    cell.Status = 9
    '''
    acell = rules.Cell()
    acell.Value = 9
    '''b = []
    b.append(acell)
    cells = b'''
    cells[0] = acell

def tmpff(cell = None):

    print(cell)
    if not cell: return 1
    return 0

def test_misc():
    a = "good morning"
    l = list(a)
    b = "".join(l)
    assert a == b

    b = ""
    #b = b.join(a[0:2]).join(a[5:2])
    b = "".join([a[0:4], a[5:9]])#"morning"])
    assert b == "goodmorn"
    x=[]
    for i in range(9): x.append(rules.Cell())
    y = 0
    tmpf(x)
    assert x[0].Value == 9
    assert y ==0

    x = None
    '''if not x: print("not None is True")
    if x: print("None is true")
    assert tmpff() == 0
    assert tmpff(x) == 1

    x = [[1,2,3,4,5],['a','b','c','d','e'],['A','B','C','D','E'],['h','i','j','k','l'],['H','I','J','K','L']]
    assert x[3,3] == x[3][3]
'''
def test_validate():
    pass
