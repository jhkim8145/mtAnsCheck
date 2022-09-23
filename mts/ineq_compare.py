from sympy import *
from re import *
from mts.answer_conversion import *
from mts.poly_compare import *


# 부등식 1개 비교
def single_ineq(c_sympy,s_sympy,form = None, poly=None):
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

        if poly != None:
            if IsEqual(c_sympy.lhs,s_sympy.lhs) == 0:
                print('poly:Fix 좌변 다항식 비교 실패')
                return False

    return True



# correct_sympy, student_sympy = Ans2Sympy(r'-\dfrac{1}{3}<x\le\dfrac{4}{3}a','-1/3<x<= 4/3*a',f = 'IneqCompare')
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# # print(correct_sympy.args[0].args,correct_sympy.args[1].args[1].args,student_sympy.args[0].args,student_sympy.args[1].args[1].args)
# print(single_ineq(correct_sympy, student_sympy))
# print((Latex2Sympy('\dfrac{4}{3}a')*2/2).args,(Latex2Sympy('4*a/3')*2/2).args)

# 부등식 리스트 비교
def IneqCompare(correct_sympy,student_sympy,form = None, poly=None):

    _form = form
    _poly = poly

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
            print('정답 오류'); return false
    return True

if __name__ == "__main__":
    # correct_sympy, student_sympy = Ans2Sympy(r'-\dfrac{1}{3}< x\le\dfrac{4}{3}','-1/3<x<= 4/3',f = 'IneqCompare')
    correct_sympy, student_sympy = Ans2Sympy(r'-3<-x+2<-1','x+3>6', f='IneqCompare')
    # correct_sympy, student_sympy = Ans2Sympy(r'x\ge 8,x!=7,x=2','8<=x,x=2,x!=7', f='IneqCompare')
    print(IneqCompare(correct_sympy, student_sympy,poly="Fix"))
    # print(single_ineq(correct_sympy[0], student_sympy[0],form = "Fix", poly= "Fix"))
    # print(IneqCompare(correct_sympy, student_sympy))



