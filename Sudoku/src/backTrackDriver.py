from Sudoku import Sudoku

FileName='repubblica.txt'
with open(FileName) as myfile:
    for line in myfile:
        problem=Sudoku(line,True)
        if problem.BackTrack():
            print("Solution computed")
            print(problem)
            print("Number of calls to isAdmissible: "+str(problem.count)+"\n")
        else:
            print(problem.istance)
            print("No solution")
