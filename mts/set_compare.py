from sympy import *
from re import *
from mts.answer_conversion import *

# 집합 스트링을 list(원소)로 변경.
def split_set(string):

    str_list = []

    while string != '':
        try:
            lgalho_cnt = 0
            rgalho_cnt = 0
            for i in range(100):
                if string[i] == '{': lgalho_cnt += 1
                if string[i] == '}': rgalho_cnt += 1
                if lgalho_cnt == rgalho_cnt:
                    if string[i] == ',':
                        str_list.append(string[:i])
                        string = string[i + 1:]
                        break
                    if i == len(string)-1:
                        str_list.append(string)
                        string = ''
                        break
        except IndexError:
            print('괄호에 문제 있음'); return False
    return str_list

# print(split_set(r'1,2,3'))
# print(split_set(r'\varnothing,{a},{b},{a,b}'))
# print(split_set(r'1,{2,3},{{3},4,{5}}'))
# print(split_set(r'1,{2,3},{{3},4,{5}}'))
# print(split_set(r'{{2,{3}}'))

# 집합 1개를 set 형태로 변환
def single_set(c_set, fType = None):
    f = [lambda x: Latex2Sympy(x), lambda x: Parse2Sympy(x)][fType]
    c_set = str(c_set)

    if c_set in [r'\varnothing', r'∅']: return EmptySet
    elif search('\s*\}|\{\s*', c_set) == None:
        return c_set
    else:
        set1 = split_set(c_set[1:-1])
        if set1 == False: return False
        print('집합 원소 구분', set1)
        Set_e = []
        for i in range(len(set1)):
            Set_e.append(single_set(set1[i], fType))
        return FiniteSet(*Set_e)

# print(r'\varnothing,{a},{b},{a,b}')
# print(r'∅,{a},{b},{a,b}')
# print(single_set(r'{a,b}', 0))
# print(single_set(r'{a,b}', 1))
# print(single_set(r'{1}', 0))
# print(single_set(r'{1}', 1))
# print(single_set(r'\varnothing', 0))
# print(single_set(r'∅', 1))
# print(single_set(r'{1,2,3}', 0))
# print(single_set(r'{1,{2,3}}', 0))
# print(single_set(r'{{1},2,{1,2}}', 0))
# print(single_set(r'{{1},2,{1,2}}', 1))
# print(single_set(r'{{2,{3}}', 1))

# 답 비교. (,로 연결된 집합 여러 개도 비교)
def SetCompare(correct_latex, student_str):

    c_split_str = split_set(correct_latex)
    s_split_str = split_set(student_str)
    if s_split_str == False: return False
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
# print(SetCompare(r'{1,2,3}', r'1,2,3'))
# print(SetCompare(r'\varnothing,{a},{b},{c},{a,b},{b,c},{a,c},{a,b,c}', r'{c},{a},{b},∅,{b,a},{c,b},{a,c},{b,a,c}'))
# print(SetCompare(r'\varnothing,{a},{b},{a,b}', r'∅,{a},{b},{a,b}'))
# print(SetCompare(r'\varnothing,{a},{b},{a,b}', r'{b},{a},{b,a},∅'))
# print(SetCompare(r'{1,2},{1,3},{1,4},{2,3},{2,4},{3,4}', r'{1,2},{4,1},{1,3},{3,4},{4,2},{2,3}'))
# print(SetCompare(r'\varnothing,{1},{{2,3}},{1,{2,3}}', r'∅,{1},{{3,2},1},{{3,2}}'))
print(SetCompare(r'\varnothing,{1,{2,3}}', r'∅,{1},{{2,3}}'))
# print(SetCompare(r'\varnothing,{1,{2,3}}', r'∅,{{2,3},1}'))
# print(SetCompare(r'\varnothing,{2},{4},{2,4}', r'∅,{4,2},{4},{2}'))
# print(SetCompare(r'{{2,{3}}}', r'{{2,{3}}')) # 괄호 누락된 문항
# print(SetCompare(r'{1}', r'1'))
