import csv
import sys


# rule checks return True if it breaks the rule
def rowrule(index, puzzle):  # puzzle is the "solution" array
    for e in range(index - (index % 9), index - (index % 9) + 9):
        if puzzle[index] == puzzle[e] and index != e:
            return True
    return False


def colrule(index, puzzle):
    column = index % 9
    for e in range(9):
        if puzzle[index] == puzzle[e * 9 + column] and index != e * 9 + column:
            return True
    return False


def blockrule(index, puzzle):
    blockrowindex = index // 27
    blockcolindex = (index % 9) // 3
    for e in range(3):
        for f in range(3):
            if puzzle[index] == puzzle[((blockrowindex * 3 + e) * 9) + (blockcolindex * 3 + f)] and index != ((blockrowindex * 3 + e) * 9) + (blockcolindex * 3 + f):
                return True
    return False


def backtrack(index, givenvalues):  # givenvalues is the givens array
    index -= 1
    while givenvalues[index]:
        index -= 1
        if index < 0:
            sys.exit("puzzle impossible")
    return index


# Initialize relevant lists
sudoku = [0] * 81
givens = [False] * 81

# Read Sudoku puzzle into "sudoku"
with open('sudoku.csv', "rb") as fin:
    reader = csv.reader(fin)
    sudokuraw = list(reader)
for r in range(9):
    for c in range(9):
        sudoku[r * 9 + c] = int(sudokuraw[r][c])
        if sudoku[r * 9 + c] != 0:
            givens[r * 9 + c] = True

# The solve loop
ind = 0
while ind < 81:
    if not givens[ind]:  # if that square wasn't part of the given puzzle
        sudoku[ind] += 1

        if sudoku[ind] >= 10:  # if it cannot be increased
            sudoku[ind] = 0
            ind = backtrack(ind, givens)

        elif not (rowrule(ind, sudoku) or colrule(ind, sudoku) or blockrule(ind, sudoku)):  # if it doesn't violate any rules
            ind += 1  # move on to the next square

        else:  # if it breaks a rule but isn't at 9 yet
            pass  # do nothing (number increments on next loop)

    else:  # otherwise that square was part of the given puzzle
        ind += 1  # move on to the next square

# Output solved puzzle
solved = [[0, 0, 0, 0, 0, 0, 0, 0, 0]] * 9
fout = open('sudoku_solved.csv', "wb")
writer = csv.writer(fout)
for r in range(9):
    for c in range(9):
        solved[r][c] = sudoku[r * 9 + c]
    print(solved[r])  # show solution to screen
    # writer.writerow(solved[r]) # save solution to file

fin.close()
fout.close()
