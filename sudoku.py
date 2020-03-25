from sudoku import solver
import sys
import os

inputvalue = 0
inputrowpos = 0
inputcolpos = 0

def action(words, paralist):
    s = words.upper().strip()
    l = s.split()
    if len(l) == 0: return -1
    paralist.clear()
    if l[0] == "COMPLETE": return 7
    if l[0] == "QUIT" or l[0]== "Q": return 0
    if l[0] == "HELP": return 1
    if l[0] == "SUBMIT": return 2
    if l[0] == "RESTART": return 3
    if l[0] == "CHANGE": return 6

    if l[0] == "KILL":
        l.pop(0)
        if len(l)<1: return -1
        for i in range(len(l)):
            if (len(l[i]) ==2 and
                l[i][:1] in "ABCDEFGHI" and
                l[i][1:].isdigit()):
                paralist.append(int(l[i][1:]))
                paralist.append(ord(l[i][:1])-ord("A")+1)
            else: return -1
        return 4


    for i in range(len(l)):
        if (len(l[i]) ==4 and
            l[i][:1] in "ABCDEFGHI" and
            l[i][1:2].isdigit() and
            l[i][2:3] == "=" and
            l[i][3:].isdigit()):
            paralist.append(int(l[i][3:]))
            paralist.append(int(l[i][1:2]))
            paralist.append(ord(l[i][:1])-ord("A")+1)
        else:
            return -1

    return 5

def start():

    print("\t***********************")
    print("\t****  S U D O K U  ****")
    print("\t***********************")
    alist = []
    while True:
        answer = input("Occupied Slots# >>")
        ians = int(answer)
        if ians < 20 or ians > 60:
            print("Error: input an invalid number!")
        else:
            break
    asolver = solver.Solver()

    if not asolver.load_game(ians):
        print("Error: loading game error!")
        exit(0)

    if not asolver.start_solve():
        print("Error: loading engine error!")
        exit(0)

    act = 0
    while True:
        if act !=7:
            asolver.display()
            words = input(">>> >> > ")
        act = action(words, alist)

        if act == -1:
            print("Error: Invalid input!")
            continue
        elif act == 0:
            #i = os.system("cls")
            break
        elif act == 1:
            i = os.system("cls")
            asolver.print_solution()
            continue
        elif act == 2:
            if not asolver.is_fill_all():
                print("Error: not finished, cannot sumbit!")
                continue

            if asolver.submit_game():
                print("\t***********************")
                print("\t****   YOU WON !   ****")
                print("\t***********************")
            else:
                print("\t***********************")
                print("\t****     LOSER     ****")
                print("\t***********************")
            if input("continue? >").lower() == "yes":
                #i = os.system("cls")
                start()
            else:
                #i = os.system("cls")
                break
        elif act == 3:
            asolver.restart_game()
            #i = os.system("cls")
            continue
        elif act == 4:
            for i in range(int(len(alist)/2)):
                asolver.erase(alist[i*2], alist[i*2+1])
            continue
        elif act == 5:
            for i in range(int(len(alist)/3)):
                asolver.input(alist[i*3], alist[i*3+1], alist[i*3+2])
            continue
        elif act == 6:
            asolver.load_game(ians)
            asolver.start_solve()
            continue
        elif act == 7:
            words = asolver.complete_cmd()
            print(words)
            continue


start()
