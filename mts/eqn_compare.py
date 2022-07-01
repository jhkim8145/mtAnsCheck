from sympy import *
from re import *
from mts.answer_conversion import *
from mts.poly_compare import *

# 방정식 단순 비교
def EqCompare(correct_sympy, student_sympy,leading_coeff = None):
    if all(IsSimilarTerm(p) == 1 for p in student_sympy) == 0: print(1);return False
    print(correct_sympy, student_sympy)
    c_poly = correct_sympy[0]-correct_sympy[1]
    s_poly = student_sympy[0]-student_sympy[1]
    print(c_poly,s_poly)
    if leading_coeff == None:
        c_poly = factor(c_poly).as_coeff_Mul()[1]
        s_poly = factor(s_poly).as_coeff_Mul()[1]
    # elif IsEqual(abs(LT(s_poly)),abs(LT(c_poly))) == 0:
    #     print(2);return False
    else:
        crLTSet = set([LT(student_sympy[i]) for i in range(2) if student_sympy[i].is_number == 0])
        stLTSet = set([LT(correct_sympy[i]) for i in range(2) if student_sympy[i].is_number == 0])
        print(crLTSet,stLTSet)
        if len(crLTSet-stLTSet) == len(stLTSet-crLTSet) != 0: return False
    # print(set([LT(student_sympy[i]) for i in range(2) if student_sympy[i].is_number == 0])==set([LT(correct_sympy[i]) for i in range(2) if student_sympy[i].is_number == 0]))
    # elif any(IsEqual(LT(student_sympy[i]),LT(Or(s_poly,-s_poly))) for i in range(2) if student_sympy[i].is_number == 0) == 0:
    #     print(2, [IsEqual(LT(student_sympy[i]),LT(s_poly)) for i in range(2) if student_sympy[i].is_number == 0],[[LT(student_sympy[i]),LT(s_poly) ]for i in range(2) if student_sympy[i].is_number == 0]);return False
    print(Eq(c_poly, 0), Eq(s_poly, 0),Eq(s_poly,0).reversedsign,IsEqual(Eq(c_poly, 0), Eq(s_poly,0)))
    return Or(IsEqual(Eq(c_poly, 0), Eq(s_poly,0)), IsEqual(Eq(c_poly, 0), Eq(s_poly,0).reversedsign))

if __name__ == "__main__":
    correct_sympy, student_sympy = Ans2Sympy(r'y=300*x','-300*x=-y',f='EqCompare')
    print(EqCompare(correct_sympy, student_sympy,leading_coeff = 'Fix'))