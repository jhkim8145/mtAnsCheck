from sympy import *
from re import *
from mts.answer_conversion import *

# 집합 1개를 set 형태로 변환
def single_set(c_set, fType = None):
    f = [lambda x: Latex2Sympy(x), lambda x: Parse2Sympy(x)][fType]
    c_set = str(c_set)

    if c_set in [r'\emptyset', r'∅']: return EmptySet
    else:
        set_e = split('\s*,\s*', c_set[1:-1])
        set_e = list(map(lambda x: f(x), set_e))
        # print('집합 원소들', set_e)
        return FiniteSet(*set_e)

# print(r'\emptyset,{a},{b},{a,b}')
# print(r'∅,{a},{b},{a,b}')
# print(single_set(r'{a,b}', 0))
# print(single_set(r'{a,b}', 1))
# print(single_set(r'{1}', 0))
# print(single_set(r'{1}', 1))
# print(single_set(r'\emptyset', 0))
# print(single_set(r'∅', 1))


# 답 비교. (,로 연결된 집합 여러 개도 비교)
def SetCompare(correct_latex, student_str):

    c_split_str = split('(?<=\}|t)(\s*,\s*)(?=\{|\\\e)', correct_latex)
    s_split_str = split('(?<=\}|∅)(\s*,\s*)(?=\{|∅)', student_str)
    c_split_str = list(filter(lambda x: search(r'\}|\{|\\emptyset', x) != None, c_split_str))
    s_split_str = list(filter(lambda x: search(r'\}|\{|∅', x) != None, s_split_str))
    print('정답을 집합의 리스트로 분할', c_split_str)
    print('학생 답을 집합의 리스트로 분할', s_split_str)

    c_split_str = list(set(c_split_str))
    s_split_str = list(set(s_split_str))
    if len(c_split_str) != len(s_split_str): print('두 답의 길이 다름'); return False

    c_set = [] ; s_set = []
    for i in range(len(c_split_str)):
        c_set.append(single_set(c_split_str[i], 0))
        s_set.append(single_set(s_split_str[i], 1))
    print('집합 형태로 변환', c_set, s_set)

    if set(c_set) != set(s_set): print('두 답이 다름'); return False

    return True

# print(SetCompare(r'{1,2,3}', r'{3,1,2}'))
# print(SetCompare(r'{a}', r'{a,a}')) -> 이런 거 정답 처리?
# print(SetCompare(r'\emptyset,{a},{b},{c},{a,b},{b,c},{a,c},{a,b,c}', r'{c},{a},{b},∅,{b,a},{c,b},{a,c},{b,a,c}'))
# print(SetCompare(r'\emptyset,{a},{b},{a,b}', r'∅,{a},{b},{a,b}'))
# print(SetCompare(r'\emptyset,{a},{b},{a,b}', r'{b},{a},{b,a},∅'))
print(SetCompare(r'{1,2},{1,3},{1,4},{2,3},{2,4},{3,4}', r'{1,2},{4,1},{1,3},{3,4},{4,2},{2,3}'))
