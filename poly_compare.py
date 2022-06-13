from sympy import *
from re import *
from answer_conversion import *

# 단순값 비교
def IsEqual(correct_sympy, student_sympy): #정답 order 관계X
    return student_sympy.equals(correct_sympy)

# simplify와 args len, equals 비교
def IsArgsEqual(sympy):
    exp_args = sorted(tuple(map(lambda x: x*2/2,sympy.args)),key=lambda x: x.sort_key())
    cp_args = sorted(parse_expr(str(sympy),evaluate=True).args,key=lambda x: x.sort_key())
    #print(exp_args,cp_args,'여기')
    if len(exp_args) != len(cp_args): print('IsArgsEqual',1);return False
    if all(IsEqual(exp_args[i],cp_args[i]) for i in range(len(exp_args))) == 0:
        print('IsArgsEqual',2);return False
    return True
# print(IsArgsEqual(Parse2Sympy('ab**2-2a**2b-ab-ab')))

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
# print(PolyCompare(correct_sympy, student_sympy))

# 인수분해
def PolyFactorCompare(correct_sympy, student_sympy): #정답 order 관계X
    correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
    if IsEqual(correct_sympy, student_sympy) == 0: print(1);return False
    if IsSimilarTerm(student_sympy) == 0: print(2);return False
    s_args = tuple([student_sympy])
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
def PolyExpansionCompare(correct_sympy, student_sympy,order=None,symbol=None): #정답 order 관계X
    correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
    print(correct_sympy.args, student_sympy.args)
    if type(student_sympy) != Add: return False
    if IsEqual(correct_sympy, student_sympy) == 0: return False
    if IsSimilarTerm(student_sympy) == 0: return False
    if len(correct_sympy.args) != len(student_sympy.args): return False
    if order == None:
        cr_args = sorted(tuple(map(lambda x: x*2/2,correct_sympy.args)), key=lambda x: x.sort_key())
        st_args = sorted(tuple(map(lambda x: x*2/2,student_sympy.args)), key=lambda x: x.sort_key())
        return all(IsEqual(cr_args[i], st_args[i]) for i in range(len(cr_args)))
    else:
        degree_list = list(map(lambda t: degree(t, gen=Symbol(symbol)), student_sympy.args))
        if order == 'Acc':
            return all(degree_list[i] <= degree_list[i + 1] for i in range(len(correct_sympy.args) - 1))
        else:
            return all(degree_list[i] >= degree_list[i + 1] for i in range(len(correct_sympy.args) - 1))
# correct_sympy, student_sympy = Ans2Sympy('3yz+2xyz','2xyz+3yz')
# print(PolyExpansionCompare(correct_sympy, student_sympy))

# 다항식 정확히 비교
# BQ+R 꼴, a(x-p)**2+q 꼴 등
def PolyFormCompare(correct_sympy,student_sympy): # 다항식 A, B 교환 허용X, 동류항 반드시 정리해야 함
    correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
    print(correct_sympy,student_sympy)
    if single_poly(correct_sympy, student_sympy) == 0: print('0');return False
    c_args = sorted(tuple(map(lambda x: x*2/2,(correct_sympy*2/2).args)),key=lambda x: x.sort_key())
    s_args = sorted(tuple(map(lambda x: x*2/2,(student_sympy*2/2).args)),key=lambda x: x.sort_key())
    while c_args != ():
        print(c_args, s_args)
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

