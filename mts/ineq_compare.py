from sympy import *
from re import *
from mts.answer_conversion import *
from mts.poly_compare import *

# 부등식 a<b<c, !=(\ne)(str)을 sympy 형태로 변환
def Ineq2Sympy(correct_latex, student_str, poly=None):

    _poly = poly

    cr_l = correct_latex.split(',')
    st_l = student_str.split(',')
    poly_test = [True, True]
    # print(cr_l,st_l,'여기')
    for j in range(2):
        f = [lambda x: Latex2Sympy(x),lambda x: Parse2Sympy(x)][j]
        l = [cr_l,st_l][j]

        for i in range(len(l)):
            ptn = [r'[<>][=]?|\\[gl][et]',r'!=|\\ne'] # 부등식 관련 명령어 추출 정규식
            rel = list(map(lambda x: x.replace("\\",""), findall('|'.join(ptn), l[i])))
            parts = split('|'.join(ptn), l[i])
            print(rel, parts)

            if len(findall(ptn[0], l[i])) == 2: # a <(=) x <(=) b 변환
                ineq = [Rel(f(parts[0]),f(parts[1]),rel[0]),Rel(f(parts[1]),f(parts[2]),rel[1])]
                l[i] = And(ineq[0].canonical, ineq[1].canonical)
            elif len(findall(ptn[1], l[i])) > 0: # x != a 변환
                ineq = [Rel(f(parts[0]), f(parts[1]), '<'), Rel(f(parts[0]), f(parts[1]), '>')]
                l[i] = Or(ineq[0].canonical, ineq[1].canonical)
            elif "=" in l[i] and len(findall('[<|>]', l[i])) == 0: # x = a 변환
                parts = split('=', l[i])
                ineq = [Rel(f(parts[0]), f(parts[1]), '==')]
                l[i] = ineq[0].canonical
            else:
                ineq = [Rel(f(parts[0]), f(parts[1]), rel[0])]
                l[i] = ineq[0].canonical

            if poly != None: # x로만 써야 하는 경우 -x는 false 나오게
                before_poly = list(map(f, parts))

                if type(l[i]) in [And, Or]:
                    after_poly = [l[i].args[0].args[0]] * len(before_poly)
                else:
                    after_poly = [l[i].args[0]] * len(before_poly)

                if any(single_poly(b,a) for b,a in zip(before_poly,after_poly)) == 0:
                    poly_test[j] = False

    print('부등식 변환 성공', cr_l, st_l)

    if len(set(poly_test)) == 2:
        print('poly:Fix 좌변 다항식 비교 실패')
        return False

    return cr_l,st_l
# print(Ineq2Sympy(r'2<2x','2<2*x', poly="Fix"))

# 부등식 1개 비교
def single_ineq(c_sympy,s_sympy,form = None,poly=None):

    _form = form
    _poly = poly

    print('-----',c_sympy,s_sympy)
    if type(c_sympy) != type(s_sympy):
        print('부등호 방향(type) 오류',type(c_sympy),type(s_sympy))
        return False

    if type(c_sympy) == And or type(c_sympy) == Or: # (k>1) & (k<5)일 때
        if all(single_ineq(c_sympy.args[i],s_sympy.args[i]) for i in range(2)) == 0:
            print('AndOr 정답X')
            return False

        if poly != None:  # x로만 써야 하는 경우 2*x는 false 나오게
            if single_poly(c_sympy.args[0].lhs, s_sympy.args[0].lhs) == 0:
                print('poly:Fix 좌변 다항식 불일치')
                return False

    else:
        if (all(IsSimilarTerm(c_sympy.args[i]) for i in range(2)) == 1
                and all(IsSimilarTerm(s_sympy.args[i]) for i in range(2)) == 0):
            print('부등식 양변 동류항 정리X')
            return False

        cr_poly = simplify(c_sympy.lhs-c_sympy.rhs)
        st_poly = simplify(s_sympy.lhs-s_sympy.rhs)
        if simplify(cr_poly/st_poly).is_number == 0:
            print('좌변-우변 비교 실패')
            return False

        if poly != None:  # x로만 써야 하는 경우 2*x는 false 나오게
            if single_poly(c_sympy.lhs, s_sympy.lhs) == 0:
                print('poly:Fix 좌변 다항식 불일치')
                return False

    return True



# correct_sympy, student_sympy = Ans2Sympy(r'-\dfrac{1}{3}<x\le\dfrac{4}{3}a','-1/3<x<= 4/3*a',f = 'IneqCompare')
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# # print(correct_sympy.args[0].args,correct_sympy.args[1].args[1].args,student_sympy.args[0].args,student_sympy.args[1].args[1].args)
# print(single_ineq(correct_sympy, student_sympy))
# print((Latex2Sympy('\dfrac{4}{3}a')*2/2).args,(Latex2Sympy('4*a/3')*2/2).args)

# 부등식 리스트 비교
def IneqCompare(correct_latex, student_str,form = None, poly=None):

    _poly = poly

    if Ineq2Sympy(correct_latex, student_str,_poly) == False: # poly:Fix 좌변 다항식 비교 실패
        return False
    else:
        correct_sympy, student_sympy = Ineq2Sympy(correct_latex, student_str,_poly)

    _form = form

    # print(correct_sympy,student_sympy)
    if len(correct_sympy) != len(student_sympy):
        print('len 오류');return False

    cr_tmp = correct_sympy[:]
    st_tmp = student_sympy[:]

    for ineq in student_sympy:
        if ineq in correct_sympy:
            cr_tmp.remove(ineq)
            st_tmp.remove(ineq)
        elif any(single_ineq(cr,ineq,_form,_poly) for cr in cr_tmp) == 1 and _form == None:
            st_tmp.remove(ineq)
        else:
            print('정답과 일치하는 부등식 없음'); return false
    return True

if __name__ == "__main__":
    # correct_sympy, student_sympy = Ans2Sympy(r'-\dfrac{1}{3}< x\le\dfrac{4}{3}','-1/3<x<= 4/3',f = 'IneqCompare')
    # correct_sympy, student_sympy = Ans2Sympy(r'x\ge 8,x!=7,x=2','8<=x,x=2,x!=7', f='IneqCompare')
    # correct_sympy, student_sympy = Ans2Sympy(r'1<x<3','-1>-x>-3', f='IneqCompare')
    # print(IneqCompare(correct_sympy, student_sympy,poly="Fix"),False)
    # correct_sympy, student_sympy = Ans2Sympy(r'1<x<3', '3>x>1', f='IneqCompare')
    # print(IneqCompare(correct_sympy, student_sympy, poly="Fix"),True)
    # correct_sympy, student_sympy = Ans2Sympy(r'1<x<3', '6>2*x>2', f='IneqCompare')
    # print(IneqCompare(correct_sympy, student_sympy, poly="Fix"), False)
    correct_sympy, student_sympy = Ans2Sympy(r'-5<5x<5', '-1<x <1', f='IneqCompare')
    print(IneqCompare(correct_sympy, student_sympy, poly="Fix"), False)



