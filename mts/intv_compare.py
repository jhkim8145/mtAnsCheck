from sympy import *
from re import *
from mts.answer_conversion import *
from mts.poly_compare import *


# 구간 1개를 interval 형태로 변환 (합집합, 교집합 포함)
def single_intv(c_intv, fType = None):
    try:
        f = [lambda x: Latex2Sympy(x), lambda x: Parse2Sympy(x)][fType]
        c_intv = str(c_intv)
        Intv_dict = {'(': {')': lambda x, y: Interval.open(x, y), ']': lambda x, y: Interval.Lopen(x, y)},
                        '[' : {')': lambda x,y: Interval.Ropen(x,y), ']': lambda x,y: Interval(x,y)}}

        if r'\cup' in c_intv or r'∪' in c_intv:
            c_split_str = split(r'\s*(\\cup|∪)\s*', c_intv)
            c_split_str = list(filter(lambda x: search(r'[\)\]]|[\(\[]', x) != None, c_split_str))
            # print('합집합 분리', c_split_str)
            result = EmptySet
            for i in range(len(c_split_str)):
                result = Union(result, single_intv(c_split_str[i], fType))
        elif r'\cap' in c_intv or r'∩' in c_intv:
            c_split_str = split(r'\s*(\\cap|∩)\s*', c_intv)
            c_split_str = list(filter(lambda x: search(r'[\)\]]|[\(\[]', x) != None, c_split_str))
            # print('교집합 분리', c_split_str)
            result = UniversalSet
            for i in range(len(c_split_str)):
                result = Intersection(result, single_intv(c_split_str[i], fType))
        else:
            # print('집합 기호 없음', c_intv)
            # if any([search(r'\s*(\[|\()\s*', c_intv[0]) == None, search(r'\s*(\]|\))\s*', c_intv[-1]) == None]):
            #     print('괄호 누락'); return False
            correct_sympy = list(map(lambda x: f(x), split('\s*,\s*', c_intv[1:-1])))
            l_galho = c_intv[0] ; r_galho = c_intv[-1]
            if [l_galho, correct_sympy[0]] == ['[', -oo] or [r_galho, correct_sympy[1]] == [']', oo]:
                # '[-oo' 또는 'oo]'는 잘못 표기한 것이므로 공집합 처리.
                result = EmptySet
            else:
                result = Intv_dict[l_galho][r_galho](simplify(correct_sympy[0]), simplify(correct_sympy[1]))
        return result
    except:
        print('변환 못 해요')
        return False

# print(single_intv(r'(-\infty, -1) \cup [-1, \infty)', 0))
# print(single_intv(r'(-oo, -1) ∪ [-1, oo)', 1))
# print(single_intv(r'(-\infty, -1) \cap [-1, \infty)', 0))
# print(single_intv(r'(-oo, -1) ∩ [-1, oo)', 1))
# print(single_intv(r'[0,1]', 0))
# print(single_intv(r'0,1]', 1))

# 두 구간이 일치한지 비교
def IntvCompare(correct_latex, student_str):
#     # student_str 형태 : (1,2) [1,2] [1,2) (1,2]
#     # correct_latex 형태 : (\left)?[\(\[]수,수(\right)?[\)\]]
#
    # try:
    c_split_str = split('(?<=[\)\]])(\s*,\s*)(?=[\(\[])', correct_latex)
    s_split_str = split('(?<=[\)\]])(\s*,\s*)(?=[\(\[])', student_str)
    c_split_str = list(filter(lambda x: search(r'[\)\]]|[\(\[]', x) != None, c_split_str))
    s_split_str = list(filter(lambda x: search(r'[\)\]]|[\(\[]', x) != None, s_split_str))
    print(c_split_str, s_split_str, 'single_intv에 넣을 거')

    correct_intv = EmptySet
    student_intv = EmptySet
    for i in range(len(c_split_str)):
        correct_intv = Union(correct_intv, single_intv(c_split_str[i], 0))
    for i in range(len(s_split_str)):
        s_intv = single_intv(s_split_str[i], 1)
        if s_intv == False: print('구간 입력 잘못됨'); return False
        student_intv = Union(student_intv, s_intv)
    print('변형된 interval', correct_intv, student_intv)
    if correct_intv != student_intv: print('두 구간이 다름'); return False
    return True

# print(IntvCompare(r'[3,6]', r'[3,6]')) # 폐구간
# print(IntvCompare(r'[-1,0)', r'[-1,0)')) # 반개구간 (오른쪽 오픈)
# print(IntvCompare(r'(10,11)', r'(10,11)')) # 개구간
# print(IntvCompare(r'(-5,-2]', r'(-5,-2]')) # 반개구간 (왼쪽 오픈)
# print(IntvCompare(r'(-\infty,\infty)', r'(-oo,oo)'))
# print(IntvCompare(r'(-\infty,\infty)', r'(-oo,0),(0,oo)')) # 0이 빠져서 오답.
# print(IntvCompare(r'(-\infty,1),(1,\infty)', r'(1,oo),(-oo,1)')) # ,로 연결된 것은 pair 순서 무관.
# print(IntvCompare(r'(-\infty,2]', r'(-oo,2]'))
# print(IntvCompare(r'(-\infty,2]', r'[2,-oo)')) # 잘못 표기한 구간 (공집합)
# print(IntvCompare(r'(-\infty,-1],[3,\infty)', r'(-oo,-1],[3,oo)'))
# print(IntvCompare(r'(-\infty,3]', r'(-oo,2+1]'))
# print(IntvCompare(r'(-\infty, -1] \cup [3, \infty)', r'(-oo, -1] ∪ [3, oo)'))
# print(IntvCompare(r'[1,4]', r'{1,4},[2,3]'))


# print(IntvCompare(r'(-5,3]', r'(-5,2]')[0][0].as_relational(symbols('x'))) # interval -> 부등식 형태로 바꿈