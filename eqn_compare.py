from sympy import *
from re import *
from answer_conversion import *
from poly_compare import *

# 방정식 단순 비교
def EqCompare(correct_sympy, student_sympy,leading_coeff = 'non-fix'):
    if all(IsSimilarTerm(p) == 1 for p in student_sympy) == 0: return False
    print(correct_sympy, student_sympy)
    c_poly = correct_sympy[0]-correct_sympy[1]
    s_poly = student_sympy[0]-student_sympy[1]
    if leading_coeff == 'non-fix':
        c_poly = factor(c_poly).as_coeff_Mul()[1]
        s_poly = factor(s_poly).as_coeff_Mul()[1]
    elif any(IsEqual(LT(student_sympy[i]),LT(s_poly)) == 0 for i in range(2) if student_sympy[i].is_number == 0) == 0: return False
    c_eq = Eq(c_poly, 0)
    s_eq = Eq(s_poly, 0)
    return IsEqual(Eq(c_poly, 0), Or(Eq(s_poly, 0),Eq(s_poly, 0)))

if __name__ == "__main__":
    correct_sympy, student_sympy = Ans2Sympy(r'x^2-8x+15=0','x**2-8x+15=0',f='EqCompare')
    print(EqCompare(correct_sympy, student_sympy,leading_coeff = 'fix'))