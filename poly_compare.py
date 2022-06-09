from sympy import *
from re import *
from answer_conversion import *

# 단순값 비교
def IsEqual(correct_sympy, student_sympy): #정답 order 관계X
    return student_sympy.equals(correct_sympy)

# 동류항 정리 확인
def IsSimilarTerm(student_sympy):
    s_args = tuple([student_sympy])
    while s_args != ():
        s_tmp = ()
        print(s_args)
        for p in s_args:
            print(p.args, simplify(p).args)
            #if str(p) == str(simplify(p)): continue
            #if [p.args, simplify(p).args] in [[(-1, 1 / 2), ()]]: continue
            if type(p) == Pow: s_tmp += p.args; continue
            if len(p.args) != len(simplify(p).args):
                #print('동1',len(p.args),len(simplify(p).args),p.args, simplify(p).args,p,simplify(p),type(p),type(simplify(p)))
                return False
            #if type(p) != Mul and type(p) != type(simplify(p)):
                #print('동2',type(p),type(simplify(p)))
            #    return False
            s_tmp += p.args
        s_args = s_tmp
    return True

print(type(Parse2Sympy('sqrt(i**2)')),Parse2Sympy('sqrt(i**2)').args,simplify(Parse2Sympy('sqrt(i**2)')).args)
print(IsSimilarTerm(Parse2Sympy('sqrt(2)')))

# 다항식 단순 비교(동류항 정리 조건만 만족, 정답과 차수 일치)
def PolyCompare(correct_sympy, student_sympy): #정답 order 관계X
    correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
    if IsEqual(correct_sympy, student_sympy) == 0: print('1');return False
    if IsSimilarTerm(student_sympy) == 0: print('2');return False
    return degree(correct_sympy) == degree(student_sympy)

#correct_sympy, student_sympy = Ans2Sympy('x^2+4x+4','(x+2)(x+2)')
#print(PolyCompare(correct_sympy, student_sympy))

# 인수분해
def PolyFactorCompare(correct_sympy, student_sympy): #정답 order 관계X
    correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
    if type(student_sympy) == Pow: s_args = tuple([student_sympy.args[0]])
    elif type(student_sympy) == Mul: s_args = student_sympy.args
    else: return False
    if IsEqual(correct_sympy, student_sympy) == 0: return False
    if IsSimilarTerm(student_sympy) == 0: return False
    if all(abs(factor_list(p)[0]) == 1 for p in s_args) == 0: return False
    if all(len(factor_list(p)[1]) == 1 or type(p) in [Mul,Pow] for p in s_args) == 0: return False
    return True

# 전개
def PolyExpansionCompare(correct_sympy, student_sympy): #정답 order 관계X
    correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
    if type(student_sympy) != Add: return False
    if IsEqual(correct_sympy, student_sympy) == 0: return False
    if IsSimilarTerm(student_sympy) == 0: return False
    for s_args in student_sympy.args:
        if any(IsEqual(s_args,c_args) for c_args in correct_sympy.args) == 0:
            return False
    return True

# 순서 비교 (오름차순, 내림차순)
# x*(y+2), (y+2)*x 둘 다 같다고 인식
def PolySortCompare(correct_sympy,student_sympy,symbol,order): #정답 order 관계X
    correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
    if type(student_sympy) != Add: return False
    if IsEqual(correct_sympy, student_sympy) == 0: return False
    compare_tuple = sympify(str(collect(student_sympy, symbol)), evaluate=False).args
    n = len(compare_tuple)
    for i in range(len(compare_tuple)):
        if degree(compare_tuple[i],sympify(symbol)) == 0:
            n = i
            break
    if len(compare_tuple) == len(student_sympy.args):
        if order == "asc":
            return all(student_sympy.args[i].equals(compare_tuple[i]) for i in range(n))
        elif order == "desc":
            return all(student_sympy.args[-i-1].equals(compare_tuple[i]) for i in range(n))


# 다항식 정확히 비교
# BQ+R 꼴, a(x-p)**2+q 꼴 등
def PolyFormCompare(correct_sympy,student_sympy): # 다항식 A, B 교환 허용X, 동류항 반드시 정리해야 함
    correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
    if IsEqual(correct_sympy,student_sympy) == 0: print('0');return False
    c_args = correct_sympy.args
    s_args = student_sympy.args
    if len(c_args) != len(s_args): print('1');return False
    while True:
        print(c_args, s_args)
        c_args_tmp = ()
        s_args_tmp = ()
        if c_args == s_args == (): print('2');return True
        for i in range(len(c_args)):
            if len(c_args[i].args) != len(s_args[i].args): print('3');return False
            if c_args[i].is_number == 0 and len(c_args[i].args) != len(expand(c_args[i]).args):
                print('전개비교',c_args[i], expand(c_args[i]).args)
                if IsEqual(c_args[i],s_args[i]) == 0: print(c_args,s_args);print('4');return False
                c_args_tmp += c_args[i].args
                s_args_tmp += s_args[i].args
            print('통과', c_args[i], c_args[i])
        c_args = c_args_tmp
        s_args = s_args_tmp

