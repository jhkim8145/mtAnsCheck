from sympy import *
from re import *
from mts.answer_conversion import *

# 순서쌍 1개 비교
# simple만 필요할 것이라 가정
correct_answer = '(1,3*I)'
student_answer = '(1,-3/I)'
# correct_sympy = P(correct_answer)
# student_sympy = P(student_answer)
#print(correct_sympy, student_sympy)
def single_pair(correct_sympy, student_sympy):
    cnt = len(correct_sympy)
    if cnt != len(student_sympy):
        return False
    return all(sympy_equals(correct_sympy[i], student_sympy[i]) for i in range(cnt))
#print(pair_compare(correct_sympy, student_sympy))

# 순서쌍 리스트 비교
# simple만 필요할 것이라 가정
correct_answer = '(1,1,I),(1,-2,1),(1,1,2)'
student_answer = '(1,1,I),(1,-2,1),(1,1,2)'
# correct_sympy = P('[' + correct_answer + ']')
# student_sympy = P('[' + student_answer + ']')
#print(correct_sympy, student_sympy)
def PairCompare(correct_sympy, student_sympy,order=None):
    cnt = len(correct_sympy)
    if cnt != len(student_sympy):
        return False
    if order == None:
        correct_sympy.sort(key = lambda p: tuple(map(lambda t: t.as_real_imag(),p)))
        student_sympy.sort(key = lambda p: tuple(map(lambda t: t.as_real_imag(),p)))
    return all(single_pair(correct_sympy[i], student_sympy[i]) for i in range(cnt))
#print(PairCompare(correct_sympy, student_sympy,order=None))