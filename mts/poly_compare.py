from sympy import *
from re import *
from mts.answer_conversion import *

# 단순값 비교
def IsEqual(correct_sympy, student_sympy): #정답 order 관계X
    return student_sympy.equals(correct_sympy)

# simplify와 args len, equals 비교 (기호 포함하는 순환소수, 절댓값 compare 제외)
def IsArgsEqual(sympy):
    exp_args = sorted(DelMulOne(map(lambda x: x,sympy.args)),key=lambda x: x.sort_key())
    cp_args = sorted(parse_expr(str(sympy),evaluate=True).args,key=lambda x: x.sort_key())
    # print(sympy,parse_expr(str(sympy),evaluate=True),exp_args,cp_args,'여기')
    # print( exp_args, cp_args)
    if len(exp_args) != len(cp_args): print('IsArgsEqual',1);return False
    if all(IsEqual(exp_args[i],cp_args[i]) for i in range(len(exp_args))) == 0:
        print('IsArgsEqual',2);return False
    return True
# print(IsArgsEqual(Parse2Sympy('Abs(+5)')),Parse2Sympy('Abs(+5)').args)
# print(IsArgsEqual(Parse2Sympy('0.[3]')),Parse2Sympy('0.[3]'))

# 동류항 정리 확인(Add일 때)
def IsSimilarTerm(student_sympy):
    s_args = tuple([student_sympy])
    while s_args != ():
        s_tmp = ()
        #print(s_args)
        for p in s_args:
            if type(p) in [Pow,Mul]: s_tmp += p.args; continue
            if IsArgsEqual(p) == 0: print('IsSimilarTerm',1);return False
            s_tmp += p.args
        s_args = s_tmp
    return True
# print(IsSimilarTerm(Parse2Sympy('xy+3x+5y+10+5')))

# 다항식 1개 비교
def single_poly(correct_sympy, student_sympy): #정답 order 관계X
    if IsEqual(correct_sympy, student_sympy) == 0: print('single_poly',1);return False
    if abs(denom(correct_sympy)).equals(abs(denom(student_sympy))) == 0: print('single_poly',2);return False
    if IsSimilarTerm(student_sympy) == 0: print('single_poly',3);return False
    return True
# correct_sympy, student_sympy = Ans2Sympy(r'500-150\times a','500-150 × a')
# correct_sympy, student_sympy = Ans2Sympy(r'\dfrac{1}{2}ah','1/2*a*h')
# print(correct_sympy,student_sympy)
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# print(single_poly(correct_sympy, student_sympy))

# 다항식 단순 비교(동류항 정리 조건만 만족, 정답과 차수 일치)
def PolyCompare(correct_sympy, student_sympy, order=None): #정답 order 관계X
    if order == None:
        correct_sympy = sorted(correct_sympy, key=lambda x: x.sort_key())
        student_sympy = sorted(student_sympy, key=lambda x: x.sort_key())
    if len(correct_sympy) != len(student_sympy): return False
    if all(single_poly(correct_sympy[i], student_sympy[i]) for i in range(len(correct_sympy))) == 0: print('PolyCompare',1);return False
    return True
# correct_sympy, student_sympy = Ans2Sympy('3yz+2xyz','(15xyz+10x**2yz)/(5x)')
# # correct_sympy, student_sympy = Ans2Sympy(r'3xy, -5xy','-5xy,3xy')
# correct_sympy, student_sympy = Ans2Sympy(r'x-4','x-4')
# print(PolyCompare(correct_sympy, student_sympy))

def NoSignCompare(correct_sympy, student_sympy):
    c_sympy, s_sympy = Latex2Sympy(correct_sympy), Parse2Sympy(student_sympy)
    if IsEqual(c_sympy, s_sympy) == 0: print(0,'정답과 값이 다름');return False

    # 곱셈, 나눗셈 기호, 계수 1, 나누기 1 생략 확인
    ptn = ['×|÷','(?<![0-9.])([1][a-zA-Z]{1})|([a-zA-Z\/][1])(?![0-9])']
    for p in ptn:
        if len(findall(p, student_sympy)) > 0: print(1,'기호, 계수 생략X');return False

    # 학생 답안 항으로 쪼개기
    if type(s_sympy) == Add: terms = s_sympy.args
    else: terms = tuple([s_sympy])

    while terms != ():
        print(terms)
        tmp = ()
        for i in range(len(terms)):
            if type(terms[i]) in [Pow]:
                if terms[i].args[0] < 0: print('분모에 - 있는 경우');return False
                tmp += terms[i].args
                continue
            elif type(terms[i]) in [Mul]:
                # 숫자가 문자보다 앞에 있는지 확인
                if denom(terms[i].args[-1]) != 1 and numer(terms[i].args[-1]) == 1:
                    if search(str(terms[i].args[-1])+'$',str(terms[i])) != None: print('2-0','숫자가 문자 뒤에(1/3이 마지막에 곱해짐)');return False
                    tmp += tuple([terms[i].args[-1].args[0]])
                    t_args = terms[i].args[:-1]
                else:
                    tmp += terms[i].args
                    t_args = terms[i].args

                isnumber = [i.is_number for i in t_args]
                try:
                    if isnumber[0] == isnumber[1] == True and denom(t_args[1]) == 1: print('2-1','곱해진 숫자가 2개 이상');return False
                except:
                    pass

                try:  # 문자가 있을 때
                    k = isnumber.index(True)
                    if k != 0 and denom(t_args[k]) == 1: print('2-2', '숫자가 문자 뒤에');return False
                except:
                    pass

                # 마이너스 맨 앞에 있는지 확인
                minussign = [i.could_extract_minus_sign() for i in t_args]
                if any(TF for TF in minussign[1:]) == 1: print(3,'음수 곱셈 부호(-) 계산X');return False

                # 거듭제곱 꼴 확인
                symbollist = list(filter(lambda x: len(x)!=0,[tuple(i.atoms(Symbol)) for i in t_args]))
                if len(symbollist) != len(set(symbollist)): print(4,'거듭제곱 꼴X');return False

                continue

            tmp += terms[i].args
        terms = tuple(filter(lambda x: x.args != (),tmp))
    return True

# correct_sympy, student_sympy = Ans2Sympy(r'10(x+y)', '10*(x+y)',f='NoSignCompare')
# correct_sympy, student_sympy = Ans2Sympy(r'10a-\dfrac{6}{b}', '10*a-6/b',f='NoSignCompare')
# # correct_sympy, student_sympy = Ans2Sympy(r'-10(3*a+3*b)', '-10*(3*a+b*3)',f='NoSignCompare')
# correct_sympy, student_sympy = Ans2Sympy(r'-\dfrac{b}{2}ah', '(-b)/(2)*(a)*h',f='NoSignCompare') # 정답허용?
# correct_sympy, student_sympy = Ans2Sympy(r'0.1a', '0.a',f='NoSignCompare')
# print(NoSignCompare(correct_sympy, student_sympy))


# 인수분해
def PolyFactorCompare(correct_sympy, student_sympy): #정답 order 관계X
    c_sympy, s_sympy = correct_sympy[0], student_sympy[0]
    if IsEqual(c_sympy, s_sympy) == 0: print(1);return False
    if IsSimilarTerm(s_sympy) == 0: print(2);return False
    s_args = tuple([s_sympy])
    while s_args != ():
        s_tmp = ()
        # print(s_args)
        for p in s_args:
            if type(p) in [Mul,Pow]: print(11);s_tmp += p.args
            elif len(factor_list(p)[1]) == 0 or len(factor_list(p)[1]) == abs(factor_list(p)[0]) == factor_list(p)[1][0][1] == 1:
                continue
            else: print(3);return False
        s_args = s_tmp
    return True
# correct_sympy, student_sympy = Ans2Sympy('\dfrac{1}{2}(x-2)^2','1/2*(x-2)**2')
# # correct_sympy, student_sympy = Ans2Sympy('(a+b)(2-x-2y)','2(a+b)-(x+2y)(a+b)')
# print(PolyFactorCompare(correct_sympy, student_sympy))

# 전개, 순서 비교(오름차순/내림차순)
def PolyExpansionCompare(correct_sympy, student_sympy,symbol=None,order=None): #정답 order 관계X
    c_sympy, s_sympy = correct_sympy[0], student_sympy[0]
    # print(correct_sympy.args, student_sympy.args)
    if type(s_sympy) != Add: return False
    if IsEqual(c_sympy, s_sympy) == 0: return False
    if IsSimilarTerm(s_sympy) == 0: return False
    if len(c_sympy.args) != len(s_sympy.args): return False
    if order == None:
        cr_args = sorted(DelMulOne(c_sympy.args), key=lambda x: x.sort_key())
        st_args = sorted(DelMulOne(s_sympy.args), key=lambda x: x.sort_key())
        return all(IsEqual(cr_args[i], st_args[i]) for i in range(len(cr_args)))
    else:
        degreelist = list(map(lambda t: degree(t, gen=Symbol(symbol)), s_sympy.args))
        print(degreelist,symbol)
        if order == 'Acc':
            return all(degreelist[i] <= degreelist[i + 1] for i in range(len(c_sympy.args) - 1))
        else:
            return all(degreelist[i] >= degreelist[i + 1] for i in range(len(c_sympy.args) - 1))
# correct_sympy, student_sympy = Ans2Sympy('3yz+2xyz','2xyz+3yz')
# print(PolyExpansionCompare(correct_sympy, student_sympy,symbol='y',order='Dec'))

# 다항식 정확히 비교
# BQ+R 꼴, a(x-p)**2+q 꼴 등
def PolyFormCompare(correct_sympy,student_sympy): # 다항식 A, B 교환 허용X, 동류항 반드시 정리해야 함
    c_sympy, s_sympy = correct_sympy[0], student_sympy[0]
    # print(c_sympy,s_sympy)
    if single_poly(c_sympy, s_sympy) == 0: print('0');return False
    c_args = sorted(tuple(map(lambda x: x, DelMulOne(tuple([c_sympy]))[0].args)), key=lambda x: x.sort_key())
    s_args = sorted(tuple(map(lambda x: x, DelMulOne(tuple([s_sympy]))[0].args)), key=lambda x: x.sort_key())
    while c_args != ():
        # print(c_args, s_args)
        c_tmp = ()
        s_tmp = ()
        if len(c_args) != len(s_args): print('1'); return False
        for i in range(len(c_args)):
            if type(c_args[i]) in [Mul,Pow]:
                c_tmp += c_args[i].args
                s_tmp += s_args[i].args
            else:
                if single_poly(c_args[i], s_args[i]) == 0:
                    print('2');return False
        c_args = c_tmp
        s_args = s_tmp
    return True

# correct_sympy, student_sympy = Ans2Sympy(r'-\dfrac{1}{2}(x-3)^2','-1/2(x-3)**2')
# print(PolyFormCompare(correct_sympy, student_sympy))

