from sympy import *
from re import *
from mts.answer_conversion import *

# 구간을 sympy 형태로 변환
def Intv2Sympy(correct_latex, student_str):
    # student_str 형태 : (1,2) [1,2] [1,2) (1,2]
    # correct_latex 형태 : (\left)[\(\[]수,수(\right)[\)\]]

    repls = {r'\,': '', r'\rm': '', r'\left': '', r'\right': ''}
    for key in repls.keys():
        correct_latex = correct_latex.replace(key, repls[key])

    c_split_str = split('(?<=[\)\]])(\s*,\s*)(?=[\(\[])', correct_latex)
    s_split_str = split('(?<=[\)\]])(\s*,\s*)(?=[\(\[])', student_str)
    # print(c_split_str, s_split_str, 'Ans2Sympy에 넣을 거')
    c_split_str = list(filter(lambda x: search(r'[\)\]]|[\(\[]', x) != None, c_split_str))
    s_split_str = list(filter(lambda x: search(r'[\)\]]|[\(\[]', x) != None, s_split_str))
    print(c_split_str, s_split_str, 'Ans2Sympy에 넣을 거에서 , 제거')
    correct_galho = list(map(lambda str: [str[0], str[-1]], c_split_str))
    correct_sympy = list(map(lambda str: list(map(lambda x: Latex2Sympy(x), split('\s*,\s*', str[1:-1]))), c_split_str))
    student_galho = list(map(lambda str: [str[0], str[-1]], s_split_str))
    student_sympy = list(map(lambda str: list(map(lambda x: Parse2Sympy(x), split('\s*,\s*', str[1:-1]))), s_split_str))
    print('correct sympy', correct_sympy)
    print('student sympy', student_sympy)
    print('correct 괄호들', correct_galho)
    print('student 괄호들', student_galho)

    Intv_dict = {'(' : {')': lambda x,y: Interval.open(x,y), ']': lambda x,y: Interval.Lopen(x,y)},
                '[' : {')': lambda x,y: Interval.Ropen(x,y), ']': lambda x,y: Interval(x,y)}}
    correct_Intv = [(Intv_dict[w[0]][w[1]])(v[0], v[1]) for v,w in zip(correct_sympy, correct_galho)]
    student_Intv = [(Intv_dict[w[0]][w[1]])(v[0], v[1]) for v,w in zip(student_sympy, student_galho)]
    return correct_Intv, student_Intv

# print(Intv2Sympy(r'\left[0,1\right],\left[2,\infty\right)', r'(0,1),[2,3)'))
# print(Intv2Sympy(r'\left[-\infty,\infty\right)', r'(-oo,oo)'))
# print(Intv2Sympy(r'\left(-\infty,1\right],\left(1,\infty\right)', r'(-oo,1),(1,oo)'))
# print(Intv2Sympy(r'\left(-\infty,2\right]', r'(-oo,2]'))
# print(Intv2Sympy(r'\left(-\infty,-1\right],\left[3,\infty\right)', r'(-oo,-1],[3,oo)'))
# print(Intv2Sympy(r'\left[3,6\right]', r'[3,6]')) # 폐구간
# print(Intv2Sympy(r'\left[-1,0\right)', r'[-1,0)')) # 반개구간 (오른쪽 오픈)
# print(Intv2Sympy(r'\left(10,11\right)', r'(10,11)')) # 개구간
# print(Intv2Sympy(r'\left(-5,-2\right]', r'(-5,-2]')) # 반개구간 (왼쪽 오픈)
# print(Intv2Sympy(r'\left(5,-2\right]', r'(5,-2]')) # 잘못 표기된 구간 (공집합)
# print(Intv2Sympy(r'\left(-5,3\right]', r'(-5,2]')[0][0].as_relational(symbols('x'))) # interval -> 부등식 형태로 바꿈
print(Intv2Sympy(r'\left(-\infty,3\right]', r'(-oo,2+1]'))
# print(Intv2Sympy(r'\left[-\infty,3\right]', r'(-5,2]')[0][0].as_relational(symbols('x')))

# 무한대가 포함되면 무한대 쪽 괄호는 open 여부 판별할 때 무시됨. 아래 비교할 때 참고해야 함.

# 구간 1개 비교
def single_intv(c_intv, s_intv):

    if c_intv.is_left_unbounded != s_intv.is_left_unbounded: return False
    if c_intv.is_right_unbounded != s_intv.is_right_unbounded: return False
    if c_intv.left_open != s_intv.left_open: return False
    if c_intv.right_open != s_intv.right_open: return False

    return True