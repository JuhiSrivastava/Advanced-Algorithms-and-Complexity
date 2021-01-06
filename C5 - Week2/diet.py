# python3
from sys import stdin
from itertools import combinations 
import numpy as np
import copy

EPS = 1e-6
PRECISION = 20
BigNum = 1e9

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

def ReadEquation(A,B,i):
    equi = [A[x] for x in i]
    val = [B[x] for x in i]
    return Equation(equi, val)

def SelectPivotElement(a, used_rows, used_columns):
    pivot_element = Position(0, 0)
    while used_rows[pivot_element.row]:
        pivot_element.row += 1
    while used_columns[pivot_element.column]:
        pivot_element.column += 1
    if a[pivot_element.row][pivot_element.column] == 0:
        for i in range(pivot_element.column+1,len(a[pivot_element.row])):
            if a[pivot_element.row][i] !=0:
                pivot_element.column = i
                break
    return pivot_element

def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column;

def ProcessPivotElement(a, b, pivot_element):
    element = a[pivot_element.row][pivot_element.column]
    if element != 1 and element != 0:
        for i in range(len(a[pivot_element.row])):
            a[pivot_element.row][i] /= element
        b[pivot_element.row] /= element
    for i in range(len(a)):
        if i!=pivot_element.row:
            element = a[i][pivot_element.column]
            if element != 0:
                for j in range(len(a[i])):
                    a[i][j] = a[i][j] - (a[pivot_element.row][j] * element)
                b[i] = b[i] - (b[pivot_element.row]*element)
    
def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True

def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)
    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = SelectPivotElement(a, used_rows, used_columns)
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)

    return b

def addEquations( n, m, A, B):
    for i in range(m):
        d = [0.0] * m
        d[i] = -1.0
        A.append(d)
        B.append(0.0)
    A.append([1.0] * m)
    B.append(BigNum)

def solve_diet_problem(n, m, A, B, c):
    addEquations(n, m, A, B)
    #print(A,B)
    n = n + m + 1
    comb = combinations([_ for _ in range(n)],m)
    answer  = -1
    currentScore = -float('inf')
    finalsoln = []
    for x in list(comb):
        sendA = copy.deepcopy(A)
        sendB = copy.deepcopy(B)
        equation = ReadEquation(sendA,sendB,x)
        solution = SolveEquation(equation)
        if len(solution) == 0:
            continue
        flag = False
        for j in range(len(c)):
            if solution[j] < -0.0001:
                flag = True
                break
        if flag:
            continue
        for i in range(n):
            result = 0
            for j in range(m):
                result += A[i][j]*solution[j]
            if result > B[i] + 1e-3:
                flag = True
                break
        if flag:
            continue
        else:
            temp = 0
            for j in range(len(c)):
                temp += c[j]*solution[j]
            if temp <= currentScore:
                continue
            else:
                currentScore = temp
                finalsoln = solution
                if x[-1] == n-1:
                    answer  = 1
                else:
                    answer = 0

    return [answer, finalsoln]

n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
  A += [list(map(int, stdin.readline().split()))]
B = list(map(int, stdin.readline().split()))
c = list(map(int, stdin.readline().split()))

anst, ansx = solve_diet_problem(n, m, A, B, c)

if anst == -1:
  print("No solution")
if anst == 0:  
  print("Bounded solution")
  print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
if anst == 1:
  print("Infinity")