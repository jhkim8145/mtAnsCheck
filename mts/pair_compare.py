from sympy import *
from re import *
from mts.answer_conversion import *
from mts.poly_compare import *

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
    return all(IsEqual(correct_sympy[i], student_sympy[i]) for i in range(cnt))
#print(pair_compare(correct_sympy, student_sympy))

# 순서쌍 리스트 비교
# simple만 필요할 것이라 가정
# correct_answer = '(1,1,I),(1,-2,1),(1,1,2)'
# student_answer = '(1,1,I),(1,-2,1),(1,1,2)'
# correct_sympy = P('[' + correct_answer + ']')
# student_sympy = P('[' + student_answer + ']')
# print(correct_sympy, student_sympy)
def PairCompare(correct_sympy, student_sympy,order=None):
    cnt = len(correct_sympy)
    if student_sympy == False: return False
    if cnt != len(student_sympy):
        return False
    if order == None:
        correct_sympy.sort(key = lambda p: tuple(map(lambda t: t.as_real_imag(),p)))
        student_sympy.sort(key = lambda p: tuple(map(lambda t: t.as_real_imag(),p)))
    return all(single_pair(correct_sympy[i], student_sympy[i]) for i in range(cnt))
# correct_sympy, student_sympy = Ans2Sympy(r'(1,2),(1,3)','(1,3),(1,2)',f='PairCompare')
correct_sympy, student_sympy = Ans2Sympy(r'(3,1)','(3,1)',f='PairCompare')
# correct_sympy, student_sympy = Ans2Sympy(r'\left(\dfrac{a+7}{2},\,\dfrac{9+b}{2}\right)','((a-7)/(2),(9+b)/(2))',f='PairCompare')
# correct_sympy, student_sympy = Ans2Sympy(r'\left(\dfrac{-4+a}{2},\,\dfrac{1+b}{2}\right)','((a-4)/(2),(1+b)/(2))',f='PairCompare')
# print('ㄱㄱ', correct_sympy, student_sympy)
print(PairCompare(correct_sympy, student_sympy,order=None))