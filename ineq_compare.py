from sympy import *
from re import *
from answer_conversion import *
from poly_compare import *


# 부등식 1개 비교
def single_ineq(correct_sympy,student_sympy):
    if type(correct_sympy) != type(student_sympy): return False
    if type(correct_sympy) == And:
        return all(single_ineq(correct_sympy.args[i],student_sympy.args[i]) for i in range(2))
    if all(IsSimilarTerm(student_sympy.args[i]) for i in range(2)) == 0: return False
    cr_poly = correct_sympy.lhs - correct_sympy.rhs
    st_poly = student_sympy.lhs - student_sympy.rhs
    return single_poly(cr_poly,st_poly)

# 부등식 리스트 비교
def IneqCompare(correct_sympy,student_sympy):
    if len(correct_sympy) != len(student_sympy): return False
    cr_tmp = correct_sympy[:]
    st_tmp = student_sympy[:]
    for ineq in student_sympy:
        if ineq in correct_sympy:
            cr_tmp.remove(ineq)
            st_tmp.remove(ineq)
        elif any(single_ineq(cr,ineq) for cr in cr_tmp) == 1:
            st_tmp.remove(ineq)
        else: return false
    return True


if __name__ == "__main__":
    correct_sympy, student_sympy = Ans2Sympy(r'-\dfrac{1}{3}<x\le\dfrac{4}{3}','-1/3<x<= 4/3',f = 'IneqCompare')
    # correct_sympy, student_sympy = Ans2Sympy(r'x<-\dfrac{3}{2}', 'x<-3/2', f='IneqCompare')
    print(IneqCompare(correct_sympy, student_sympy))



