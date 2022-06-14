from sympy import *
from re import *
from answer_conversion import *
from poly_compare import *
from sympy.parsing.sympy_parser import parse_expr,T
from sympy.core.sympify import kernS

"""
sympy 인식 못 하는 답: 대분수, + 부호
latex 인식 못 하는 답: 순환소수

-> str으로 비교 or 함수 따로 제작

모든 분수는 가분수로 받음
"""

# 숫자 값 비교
#분수 > 소수, 소수 > 분수 허용X, 반드시 유리화, 복소수 a+bi 형태만, 덧셈/곱셈 교환 가능, 정답,학생답 type 같음
def single_number(correct_sympy, student_sympy,Type = 'all'):
    if IsEqual(correct_sympy, student_sympy) == 0: print('single_num',1);return False
    if IsSimilarTerm(student_sympy) == 0: print('single_num',2);return False
    if Type == 'fix': # 소수 != 분수, 약분 전!=후, 유리화 전!=후, 거듭제곱 전!=후, 통분 전!= 후, i != sqrt(-1), 덧셈곱셈 교환 가능
        if type(correct_sympy) != type(student_sympy): print('single_num', 3);return False
        if abs(denom(correct_sympy)).equals(abs(denom(student_sympy))) == 0: print('single_num', 4);return False
        if len(correct_sympy.args) != len(student_sympy.args): print('single_num', 5);return False
        c_args = sorted(correct_sympy.args, key=lambda x: x.sort_key())
        s_args = sorted(student_sympy.args, key=lambda x: x.sort_key())
        if all(IsEqual(c_args[i],s_args[i]) for i in range(len(c_args))) == 0: print('single_num', 6);return False
    return True
# correct_sympy, student_sympy = Ans2Sympy(r'\dfrac{3}{4}+\dfrac{i}{4}','3/4+i/4')
# correct_sympy, student_sympy = Ans2Sympy(r'(\dfrac{1}{7})^4','(((1)/(7)))**(4)')
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# print(correct_sympy, student_sympy)
# print(correct_sympy.args, student_sympy.args)
# print(single_number(correct_sympy, student_sympy,Type='fix'))

# correct_sympy, student_sympy = Ans2Sympy(r'3^2*7^4','7**4*3**2')
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# print(correct_sympy, student_sympy)
# print(correct_sympy.args, student_sympy.args)
# print(single_number(correct_sympy, student_sympy,Type='fix'))


# 숫자 리스트 비교
# 동류항 정리 안 하는 덧셈식, 곱셈식은 따로 만들어야 할듯
correct_answer = '5*I, -5+I, 3.0, sqrt(2)'
student_answer = '5*I, I-5, 3, sqrt(2)'
correct_answer = '3/4+I/4'
student_answer = '(3+sqrt(-1))/4'
correct_answer = '500'
student_answer = '1000/2'
correct_answer = '1/sqrt(2)'
student_answer = 'sqrt(2)/2'
correct_answer = '-1'
student_answer = '1/I**(10)'
#correct_answer = '900'
#student_answer = '30**2'
#student_answer = '21**2+2*21*9+9**2'
correct_answer = '1/2**3'
student_answer = '2**(-3)'

#correct_answer = '2**3'
#student_answer = '2*2**2'


def NumCompare(correct_sympy, student_sympy,Type='all',order=None):
    # print(sign(correct_sympy[0]), student_sympy)
    # 리스트 비교(항목 개수, 동류항 정리, 정렬)
    cnt = len(correct_sympy)
    if cnt != len(student_sympy): print('1');return False
    if order == None:
        correct_sympy = sorted(correct_sympy,key = lambda x: x.as_real_imag())
        student_sympy = sorted(student_sympy,key = lambda x: x.as_real_imag())
    # 개별 항목 값 비교
    return all(single_number(correct_sympy[i], student_sympy[i],Type = Type) for i in range(cnt))

# correct_sympy, student_sympy = Ans2Sympy(r'+5','+5')
# print(sign(correct_sympy[0]),sign(student_sympy[0]))
# print('순서X',NumCompare(correct_sympy, student_sympy,Type='all'))
# print('순서O',NumCompare(correct_sympy, student_sympy,Type='all',order='fix'))
# print('↓ 정답과 type 일치')
# print('순서X',NumCompare(correct_sympy, student_sympy,Type='fix'))
# print('순서O',NumCompare(correct_sympy, student_sympy,Type='fix',order='fix'))

# str 비교, ** 순환소수 ** 이걸로!!
def StrCompare(correct_sympy, student_sympy):
    correct_sympy = sub(r'[\s]+','', correct_sympy)
    student_sympy = sub(r'[\s]+', '', student_sympy)
    return correct_sympy == student_sympy

def SignCompare(correct_sympy, student_sympy,order=None):
    c_str = correct_sympy.split(',')
    s_str = student_sympy.split(',')
    if len(c_str) != len(s_str): return False
    c_sign_num = []
    s_sign_num = []
    for str in c_str:
        if '+' in str: c_sign_num.append(['+',Latex2Sympy(str)])
        elif '-' in str: c_sign_num.append(['-',Latex2Sympy(str)])
        else: c_sign_num.append(['',Latex2Sympy(str)])
    print(correct_sympy,student_sympy)
    print(correct_sympy, student_sympy)

# correct_sympy, student_sympy = Ans2Sympy(r'+1','-1',f = 'SignCompare')
# print(SignCompare(correct_sympy, student_sympy))

# 소인수분해
def NumPrimeFactorCompare(correct_sympy, student_sympy): #정답 order 관계X
    if IsEqual(correct_sympy, student_sympy) == 0: return False
    s_args = student_sympy.args
    while s_args != ():
        s_tmp = ()
        for args in s_args:
            if type(args) == Pow:
                s_tmp += tuple([args.args[0]])
            elif type(args) == Mul:
                s_tmp += args.args
            elif type(args) == Integer:
                if isprime(args) == 0: return False
            else: return False
        s_args = s_tmp
    return True