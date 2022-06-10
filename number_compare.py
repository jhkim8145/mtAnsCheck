from sympy import *
from re import *
from answer_conversion import *


# 숫자 값 비교
#분수 > 소수, 소수 > 분수 허용X, 반드시 유리화, 복소수 a+bi 형태만, 덧셈/곱셈 교환 가능
def single_number(correct_sympy, student_sympy):
    if IsEqual(correct_sympy, student_sympy) == 0: return False
    c_args = tuple([correct_sympy])
    s_args = tuple([student_sympy])
    while c_args != () and s_args != ():
        c_tmp = ()
        s_tmp = ()
        for i in range(len(c_args)):
            #print(type(c_args[i]),type(s_args[i]))
            if type(c_args[i]) != type(s_args[i]): return False
            c_tmp += c_args[i].args
            s_tmp += s_args[i].args
        c_args = c_tmp
        s_args = s_tmp
    return True

# 숫자 리스트 비교
# 덧셈식, 곱셈식은 따로 만들어야 할듯
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

correct_sympy = P('[' + correct_answer + ']')
student_sympy = P('[' + student_answer + ']')
#print('요',correct_sympy,student_sympy)
def NumCompare(correct_sympy, student_sympy,type='all',order='non-fix'):
    # 리스트 비교(항목 개수, 동류항 정리, 정렬)
    cnt = len(correct_sympy)
    if cnt != len(student_sympy): print('1');return False
    if all(IsSimilarTerm(student_sympy[i]) for i in range(cnt)) == 0: print('2');return False
    if order == 'non-fix':
        correct_sympy.sort(key = lambda x: x.as_real_imag())
        student_sympy.sort(key = lambda x: x.as_real_imag())
    # 개별 항목 값 비교
    if type == 'all':
        return all(IsEqual(correct_sympy[i], student_sympy[i]) for i in range(cnt))
    elif type == 'fix':
        return all(single_number(correct_sympy[i], student_sympy[i]) for i in range(cnt))
#print('여기',number_list_compare(correct_sympy, student_sympy,type='fix',order='non-fix'))


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