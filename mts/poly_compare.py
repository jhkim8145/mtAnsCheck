from sympy import *
from re import *
from mts.answer_conversion import *

# 단순값 비교
def IsEqual(sympy1, sympy2): #정답 order 관계X
    return sympy1.equals(sympy2)

# simplify와 args len, equals 비교 (기호 포함하는 순환소수, 절댓값 compare 제외)
def IsArgsEqual(sympy):
    exp_args = DelMulOne(map(lambda x: x,sympy.args))
    cp_args = parse_expr(str(sympy),evaluate=True).args
    # print(sympy,parse_expr(str(sympy),evaluate=True),exp_args,cp_args,'여기')
    # print(exp_args, cp_args)
    if len(exp_args) != len(cp_args): print('IsArgsEqual',1);return False
    tmp = list(exp_args[:])
    for args1 in exp_args:
        if any(IsEqual(args1,args2) for args2 in cp_args) == 0: print('IsArgsEqual',2);return False
        tmp.remove(args1)
    return len(tmp) == 0
# print(IsArgsEqual(Parse2Sympy('Abs(+5)')),Parse2Sympy('Abs(+5)').args)
# print(IsArgsEqual(Parse2Sympy('0.[3]')),Parse2Sympy('0.[3]'))
# print(IsArgsELse2Sympy('x-4*a/3')))

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

# 분모, 분자 차수 비교
def IsDegreeEqual(cr_sp, st_sp):
    def Degree(a):
        try: n = degree(a)
        except: n = 0
        return n
    if Degree(cr_sp) != Degree(st_sp): return False
    if type(cr_sp) == Add:
        tmp_args = cr_sp.args
    else:
        tmp_args = tuple([cr_sp])

    n = 0
    for i in tmp_args:
        if Degree(denom(i)) != n: n = Degree(denom(i))

    if type(st_sp) == Add:
        tmp_args = st_sp.args
    else:
        tmp_args = tuple([st_sp])

    m = 0
    for i in tmp_args:
        if Degree(denom(i)) != m: m = Degree(denom(i))

    if n != m: return False
    else: return True


# 다항식 1개 비교
def single_poly(cr_sp, st_sp, form=None): #정답 order 관계X

    if IsEqual(cr_sp, st_sp) == 0:
        print(1, '단순비교 false',cr_sp,st_sp); return False

    # 다항식 분자, 분모 차수 확인(x**2/x 방지)
    if IsDegreeEqual(cr_sp, st_sp) == 0:
        print(2, '차수비교 false', cr_sp, st_sp); return False

    if IsSimilarTerm(cr_sp) == 1 and IsSimilarTerm(st_sp) == 0:
        print(3, '동류항 정리X'); return False

    if form != None:
        sblist = list(cr_sp.atoms(Symbol))
        for i in range(len(sblist)):
            cr_tmp = DelMulOne(cr_sp.subs(sblist[i],UnevaluatedExpr(1),order='none').args)
            st_tmp = DelMulOne(st_sp.subs(sblist[i], UnevaluatedExpr(1), order='none').args)
        for i in cr_tmp:
            if i not in st_tmp: print(4, 'form:fix X');return False

    return True
# correct_sympy, student_sympy = Ans2Sympy(r'500-150\times a','500-150 × a')
# correct_sympy, student_sympy = Ans2Sympy(r'\dfrac{1}{2}-0.5x','1/2-0.5x')
# print(correct_sympy,student_sympy)
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# print(single_poly(correct_sympy, student_sympy,form="Fix"))

# 다항식 단순 비교(동류항 정리 조건만 만족, 정답과 차수 일치)
def PolyCompare(correct_sympy, student_sympy, form=None, order=None): #정답 order 관계X
    if order == None:
        correct_sympy = sorted(correct_sympy, key=lambda x: x.sort_key())
        student_sympy = sorted(student_sympy, key=lambda x: x.sort_key())
    if len(correct_sympy) != len(student_sympy): return False
    if all(single_poly(correct_sympy[i], student_sympy[i], form) for i in range(len(correct_sympy))) == 0: print('PolyCompare',1);return False
    return True
# correct_sympy, student_sympy = Ans2Sympy('3yz+2xyz','(15xyz+10x**2yz)/(5x)')
# # correct_sympy, student_sympy = Ans2Sympy(r'3xy, -5xy','-5xy,3xy')
# correct_sympy, student_sympy = Ans2Sympy(r'4000-0.5x','4000-1/2*x')
# print(PolyCompare(correct_sympy, student_sympy,form="Fix"))

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
        # print(terms)
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
        print(s_args)
        for p in s_args:
            if type(p) in [Mul,Pow]: print(11);s_tmp += p.args
            elif (len(factor_list(p)[1]) == 0
                  or (len(factor_list(p)[1]) == 1
                    and abs(factor_list(p)[0]) <= 1
                    and factor_list(p)[1][0][1] == 1)
                    ):
                continue
            else: print(3);return False
        s_args = s_tmp
    return True
# correct_sympy, student_sympy = Ans2Sympy('\dfrac{1}{2}(x-2)^2','1/2*(x-2)**2')
# correct_sympy, student_sympy = Ans2Sympy('(4a+\dfrac{b}{2})^2','(4*a+b/2)**2')
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
        if order == 'Acc':
            return all(degreelist[i] <= degreelist[i + 1] for i in range(len(c_sympy.args) - 1))
        else:
            return all(degreelist[i] >= degreelist[i + 1] for i in range(len(c_sympy.args) - 1))
# correct_sympy, student_sympy = Ans2Sympy('3yz+2xyz','2xyz+3yz')
# correct_sympy, student_sympy = Ans2Sympy('x^2+x','x**2+x')
# print(PolyExpansionCompare(correct_sympy, student_sympy,symbol='x',order='Dec'))

# 다항식 정확히 비교
# BQ+R 꼴, a(x-p)**2+q 꼴 등
def PolyFormCompare(correct_sympy,student_sympy): # 다항식 A, B 교환 허용X, correct_sympy에 따라 동류항 정리 여부 결정
    c_sympy, s_sympy = correct_sympy[0], student_sympy[0]
    if single_poly(c_sympy, s_sympy) == 0: print('0');return False

    c_args = sorted(tuple(map(lambda x: x, DelMulOne(tuple([c_sympy]))[0].args)), key=lambda x: x.sort_key())
    s_args = sorted(tuple(map(lambda x: x, DelMulOne(tuple([s_sympy]))[0].args)), key=lambda x: x.sort_key())
    while c_args != ():
        print(c_args, s_args)
        c_tmp = ()
        s_tmp = ()
        if len(c_args) != len(s_args): print('1'); return False
        for i in range(len(c_args)):
            if str(c_args[i]) == str(s_args[i]): continue
            if type(c_args[i]) in [Mul,Pow]:
                c_tmp += c_args[i].args
                s_tmp += s_args[i].args
            else:
                if single_poly(c_args[i], s_args[i]) == 0:
                    print('2');return False
        c_args = c_tmp
        s_args = s_tmp
    return True

# correct_sympy, student_sympy = Ans2Sympy(r'3a-5','a*3-10/2')
# print(PolyFormCompare(correct_sympy, student_sympy))