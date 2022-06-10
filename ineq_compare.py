from sympy import *
from re import *
from answer_conversion import *


# 부등식 1개 비교
def single_ineq(correct_sympy,student_sympy):
    if type(correct_sympy) != type(student_sympy): return False
    if type(correct_sympy) == And:
        return all(single_ineq(correct_sympy.args[i],student_sympy.args[i]) for i in range(2))
    cr_poly = correct_sympy.lhs - correct_sympy.rhs
    st_poly = student_sympy.lhs - student_sympy.rhs
    if like_term_TF(cr_poly) != like_term_TF(st_poly): return False
    if like_term_TF(cr_poly) == False:
        return all(correct_sympy.args[i].equals(student_sympy.args[i]) for i in range(2))
    else:
        return sympy_equals(cr_poly,st_poly)

# 부등식 리스트 비교
def ineq_compare(correct_sympy,student_sympy):
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






