from sympy import *
from re import *
from mts.answer_conversion import *
from mts.poly_compare import *

"""
sympy 인식 못 하는 답: 대분수, +(양수부호) 포함여부, ×/÷ 기호
latex 인식 못 하는 답: 순환소수

-> str으로 비교 or 함수 따로 제작

모든 분수는 기약 + 가분수만 받음
중등 - 숫자끼리, 같은 문자끼리 반드시 거듭제곱
"""


# expr = '2**2'
# p = Parse2Sympy(expr)
# print(p,simplify(p),expand(p))

# 숫자 값 비교
#분수 > 소수, 소수 > 분수 허용X, 반드시 유리화, 복소수 a+bi 형태만, 덧셈/곱셈 교환 가능, 정답,학생답 form 같음
def single_num(correct_sympy, student_sympy,form = None,de = None,rt = None):
    if IsEqual(correct_sympy, student_sympy) == 0: print('single_num',1);return False
    if IsSimilarTerm(student_sympy) == 0: print('single_num',2);return False
    pow = symbols('POW')
    if pow in tuple(count_ops(correct_sympy, visual = True).atoms(Symbol)):
        if pow not in tuple(count_ops(student_sympy, visual = True).atoms(Symbol)): # sqrt 포함된 답일 때 계산한 소수값을 적을 경우 오답 처리.
            print('single_num', '루트에 계산기 사용.'); return False
    if rt == 'Fix':
        if len(findall('sqrt', str(correct_sympy))) != len(findall('sqrt', str(student_sympy))):
            print('single_num', '루트 개수 다름.'); return False
    if form == 'Fix': # 소수 != 분수, 약분 전!=후, 거듭제곱 전!=후, 통분 전!= 후, i != sqrt(-1), 덧셈곱셈 교환 가능
        c_sympy = DelMulOne([correct_sympy])[0] # split 1 때문에 추가, 예) -\dfrac{10}{2}, -10/2
        s_sympy = DelMulOne([student_sympy])[0]
        if type(c_sympy) != type(s_sympy): print('single_num', 3);return False
        if abs(denom(c_sympy)).equals(abs(denom(s_sympy))) == 0: print('single_num', 4);return False
        if len(c_sympy.args) != len(s_sympy.args): print('single_num', 5,correct_sympy.args,student_sympy.args);return False
        c_args = sorted(c_sympy.args, key=lambda x: x.sort_key())
        s_args = sorted(s_sympy.args, key=lambda x: x.sort_key())
        if all(IsEqual(c_args[i],s_args[i]) for i in range(len(c_args))) == 0: print('single_num', 6);return False
    if de == "Rtn": # 유리화 전!=후
        if student_sympy.as_numer_denom()[1].is_Rational == 0: return False
    return True
# correct_sympy, student_sympy = Ans2Sympy(r'\dfrac{3}{4}+\dfrac{i}{4}','3/4+i/4')
# correct_sympy, student_sympy = Ans2Sympy(r'(\dfrac{1}{7})^4\pi','(((1)/(7)))**(4)*pi')
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# print(correct_sympy, student_sympy)
# print(correct_sympy.args, student_sympy.args)
# print(single_num(correct_sympy, student_sympy,form='Fix'))
# correct_sympy, student_sympy = Ans2Sympy(r'2','2*1')
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# print(correct_sympy, student_sympy)
# print(correct_sympy.args, student_sympy.args)
# print(single_num(correct_sympy, student_sympy,form='Fix'))
# print(single_num(latex2sympy('\\infty'),P('oo'))) # 무한대 테스트

# 정답에 루트 포함 & 학생이 루트 계산값 입력 시 오답 처리 확인용.
# correct_sympy, student_sympy = Ans2Sympy(r'30\sqrt{0.02}','30*sqrt(0.02)')
# correct_sympy, student_sympy = Ans2Sympy(r'30\sqrt{0.02}','3*sqrt(2)') # evalf()로 해도 두 값이 달라서 IsEqual에서 오답처리.
# correct_sympy, student_sympy = Ans2Sympy(r'7\sqrt{0.3}','0.7*sqrt(30)')
# correct_sympy, student_sympy = Ans2Sympy(r'\sqrt{94}','sqrt(94)')
# correct_sympy, student_sympy = Ans2Sympy(r'2\sqrt{30}','sqrt(120)')
# correct_sympy, student_sympy = Ans2Sympy(r'45\sqrt{\frac{11}{2}}','45*sqrt((11)/(2))')
# correct_sympy, student_sympy = Ans2Sympy(r'45\sqrt{\frac{11}{2}}','45*sqrt(5.5)')
# correct_sympy, student_sympy = Ans2Sympy(r'20\sqrt{0.07}','2*sqrt(7)')
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# print(correct_sympy, student_sympy)
# # print(NumCompare(correct_sympy, student_sympy, rt = 'Fix'))
# print(str(correct_sympy.evalf(16))[:-1], str(student_sympy.evalf(16))[:-1])
# print(single_num(correct_sympy, student_sympy))
# print(single_num(correct_sympy, student_sympy.evalf()))

# 문제를 그대로 썼을 때 오답 처리 어떻게?
# correct_sympy, student_sympy = Ans2Sympy(r'\sqrt{10}','sqrt(2)*sqrt(5)')
# correct_sympy, student_sympy = Ans2Sympy(r'6\sqrt{0.02}','2*sqrt(0.1)*3*sqrt(0.2)') # IsEqual에서 오답 처리됨.
# correct_sympy, student_sympy = Ans2Sympy(r'\sqrt{3}','(sqrt(6))/(sqrt(2))')
# correct_sympy, student_sympy = Ans2Sympy(r'2\sqrt{3}','2*(sqrt(21))/(sqrt(7))')
# correct_sympy, student_sympy = Ans2Sympy(r'\sqrt{15}','((sqrt(9))/(sqrt(2)))/((sqrt(3))/(sqrt(10)))')
# correct_sympy, student_sympy = Ans2Sympy(r'2 \sqrt{42}','(1)/(2)*sqrt(28)*sqrt(24)')
# correct_sympy, student_sympy = Ans2Sympy(r'24 \sqrt{30}','2*sqrt(3)*3*sqrt(5)*4*sqrt(2)')
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# print(correct_sympy, student_sympy)
# print(correct_sympy.evalf(), student_sympy.evalf())
# print(single_num(correct_sympy, student_sympy))
# print(count_ops(sqrt(2)*sqrt(5), visual = True))

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


def NumCompare(correct_sympy, student_sympy,form=None,order=None,de=None,rt=None):

    _form = form
    _de = de
    _rt = rt

    # print(sign(correct_sympy[0]), student_sympy)
    # 리스트 비교(항목 개수, 동류항 정리, 정렬)
    cnt = len(correct_sympy)
    if cnt != len(student_sympy): print('1','진짜?');return False
    if order == None:
        correct_sympy = sorted(correct_sympy,key = lambda x: x.as_real_imag())
        student_sympy = sorted(student_sympy,key = lambda x: x.as_real_imag())
    # 개별 항목 값 비교
    return all(single_num(correct_sympy[i], student_sympy[i],form=_form, de=_de, rt=_rt) for i in range(cnt))

# if __name__ == "__main__":
#     # correct_sympy, student_sympy = Ans2Sympy(r'\frac{\sqrt{6}+\sqrt{3}}{3}','sqrt(6)/3+sqrt(3)/3',f='NumCompare')
#     # print('결과: ',NumCompare(correct_sympy, student_sympy, de = "Rtn"),True)
#     # correct_sympy, student_sympy = Ans2Sympy(r'\frac{\sqrt{6}+\sqrt{3}}{3}', '(sqrt(2)+1)/sqrt(3)', f='NumCompare')
#     # print('결과: ', NumCompare(correct_sympy, student_sympy, de="Rtn"), False)
#     # correct_sympy, student_sympy = Ans2Sympy(r'\frac{\sqrt{6}+\sqrt{3}}{3}', 'sqrt(2)/sqrt(3)+1/sqrt(3)', f='NumCompare')
#     # print('결과: ', NumCompare(correct_sympy, student_sympy, de="Rtn"), False)
#     # correct_sympy, student_sympy = Ans2Sympy(r'\pm \sqrt{17} i', 'sqrt(17)*I,-sqrt(17)*I', f='NumCompare')
#     # correct_sympy, student_sympy = Ans2Sympy(r'63\sqrt{0.06}', '6.3*sqrt(6)', f='NumCompare')
#     print('결과: ', NumCompare(correct_sympy, student_sympy), True)
# print(NumCompare(correct_sympy, student_sympy, rt = 'Fix'))
# correct_sympy, student_sympy = Ans2Sympy(r'6','2*3')
# # print(correct_sympy,student_sympy,correct_sympy[0].args,student_sympy[0].args)
# print('순서X',NumCompare(correct_sympy, student_sympy,Type='all'))
# # print('순서O',NumCompare(correct_sympy, student_sympy,Type='all',order='Fix'))
# print('↓ 정답과 type 일치')
# print('순서X',NumCompare(correct_sympy, student_sympy,Type='Fix'))
# # print('순서O',NumCompare(correct_sympy, student_sympy,Type='Fix',order='Fix'))



# str 비교, ** 순환소수 ** 이걸로!!
def StrCompare(correct_sympy, student_sympy):
    c_str = sub(r'[\s]+','', correct_sympy)
    s_str = sub(r'[\s]+', '', student_sympy)
    return c_str == s_str

def SignCompare(correct_sympy, student_sympy, order=None):  # form = 'Fix'만 가능. 양수, 음수, 절댓값
    c_str = correct_sympy.split(',')
    s_str = student_sympy.split(',')
    if len(c_str) != len(s_str): return False

    sign_num = [c_str[:], s_str[:]]
    for i in range(2):
        for j in range(len(c_str)):
            print(1)
            f = [lambda x: Latex2Sympy(x),lambda x: Parse2Sympy(x)][i]
            # ↓ 절댓값 있는 경우 evaluate가 되어버려 IsArgsEqual = False가 되어 추가
            if type(f(sign_num[i][j])) == Abs: tmp = f(sign_num[i][j]).args[0]
            else: tmp = f(sign_num[i][j])
            sgn = ''.join(findall(r'[+\-]',sign_num[i][j]))
            sign_num[i][j] = [sgn,DelMulOne([tmp])[0],type(f(sign_num[i][j])) == Abs]
    if order == None:
        sign_num[0] = sorted(sign_num[0], key=lambda x: x[1].sort_key())
        sign_num[1] = sorted(sign_num[1], key=lambda x: x[1].sort_key())
    print(sign_num)
    return all(And(StrCompare(sign_num[0][i][0],sign_num[1][i][0]),
                   single_num(sign_num[0][i][1],sign_num[1][i][1],form='Fix')
                   ,sign_num[0][i][2] == sign_num[1][i][2]) for i in range(len(c_str)))

# correct_sympy, student_sympy = Ans2Sympy(r'|-\dfrac{4}{7}|, \dfrac{4}{7}','Abs(-4/7), 4/7',f = 'SignCompare')
# correct_sympy, student_sympy = Ans2Sympy(r'|+2.5|, 2.5','Abs(2.5), 2.5',f = 'SignCompare')
# print(SignCompare(correct_sympy, student_sympy))
# print(Parse2Sympy('Abs(+5)').args,Latex2Sympy('|+5|').args)
# correct_sympy, student_sympy = Ans2Sympy(r'500\times a+200\times b','500×a+200×b',f = 'SignCompare')
# print(SignCompare(correct_sympy, student_sympy,Mul='True'))


# 소인수분해 1개
def NumPrimeFactorCompare(correct_sympy, student_sympy): #정답 order 관계X
    c_sympy, s_sympy = correct_sympy[0], student_sympy[0]
    if IsEqual(c_sympy, s_sympy) == 0: return False
    s_args = s_sympy.args
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
# correct_sympy, student_sympy = Ans2Sympy(r'2^2\times3\times5','2**2×3×5',f = 'NumPrimeFactorCompare')
# print(NumPrimeFactorCompare(correct_sympy, student_sympy))
