from sympy import *
from re import *
from mts.answer_conversion import *
from mts.poly_compare import *

# 방정식 단순 비교
def EqCompare(correct_sympy, student_sympy, form = None, leading_coeff = None):
    if form != None:
        if all(single_poly(correct_sympy[i], student_sympy[i]) for i in range(2)) == 0:
            return False

    if all(IsSimilarTerm(p) == 1 for p in student_sympy) == 0 and all(IsSimilarTerm(p) == 1 for p in correct_sympy) == 1: print(1);return False
    c_poly = correct_sympy[0]-correct_sympy[1]
    s_poly = student_sympy[0]-student_sympy[1]
    # print(correct_sympy, student_sympy, c_poly, s_poly,sep="\n")
    if leading_coeff == None:
        c_poly = factor(nsimplify(c_poly)).as_coeff_Mul()[1]
        s_poly = factor(nsimplify(s_poly)).as_coeff_Mul()[1]
    else:
        crLTSet = set([LT(correct_sympy[i]) for i in range(2) if correct_sympy[i].is_number == 0])
        stLTSet = set([LT(student_sympy[i]) for i in range(2) if student_sympy[i].is_number == 0])
        # print('Fix',crLTSet,stLTSet,crLTSet & stLTSet)
        if len(crLTSet & stLTSet) == 0: return False
    # print(IsEqual(Eq(c_poly, 0), Eq(s_poly,0)), IsEqual(Eq(c_poly, 0), Eq(s_poly,0).reversedsign))
    return Or(IsEqual(Eq(c_poly, 0), Eq(s_poly,0)), IsEqual(Eq(c_poly, 0), Eq(s_poly,0).reversedsign))

if __name__ == "__main__": # fix: 최고차항 계수 조건 있을 때, 그 외
    # correct_sympy, student_sympy = Ans2Sympy(r'y=300x','y=300*x',f='EqCompare')
    # print('결과: ',EqCompare(correct_sympy, student_sympy),True)
    # correct_sympy, student_sympy = Ans2Sympy(r'y=300x', '300*x=y', f='EqCompare')
    # print('결과: ', EqCompare(correct_sympy, student_sympy),True)
    # correct_sympy, student_sympy = Ans2Sympy(r'y=300x', '-y=-300*x', f='EqCompare')
    # print('결과: ', EqCompare(correct_sympy, student_sympy),True)
    # correct_sympy, student_sympy = Ans2Sympy(r'x^2+2x+1=0', 'x**2+2*x+1=0', f='EqCompare')
    # print('결과: ', EqCompare(correct_sympy, student_sympy,leading_coeff="Fix"),True)
    # correct_sympy, student_sympy = Ans2Sympy(r'x^2+2x+1=0', '0=x**2+2*x+1', f='EqCompare')
    # print('결과: ', EqCompare(correct_sympy, student_sympy,leading_coeff="Fix"),True)
    # correct_sympy, student_sympy = Ans2Sympy(r'x^2+2x+1=0', '-2*x-1=x**2', f='EqCompare')
    # print('결과: ', EqCompare(correct_sympy, student_sympy,leading_coeff="Fix"),True)
    # correct_sympy, student_sympy = Ans2Sympy(r'x^2+2x+1=0', '-x**2-2*x-1=0', f='EqCompare')
    # print('결과: ', EqCompare(correct_sympy, student_sympy,leading_coeff="Fix"),False)
    # correct_sympy, student_sympy = Ans2Sympy(r'-2x-7x=-8', '-2*x-7*x=-8', f='EqCompare')
    # print('결과: ', EqCompare(correct_sympy, student_sympy, leading_coeff="Fix"), True)
    # correct_sympy, student_sympy = Ans2Sympy(r'7x=6', '2*x+2=-5*x+8', f='EqCompare')
    # print('결과: ', EqCompare(correct_sympy, student_sympy, leading_coeff="Fix"), False)
    # correct_sympy, student_sympy = Ans2Sympy(r'y=- \frac{x^{2}}{2} + 16 x', 'y=-0.5*(x)**(2)+16*x', f='EqCompare')
    # print('결과: ', EqCompare(correct_sympy, student_sympy), True)
    correct_sympy, student_sympy = Ans2Sympy(r'3x+7y=-5', '3*x+7*y+5=0', f='EqCompare')
    print('결과: ', EqCompare(correct_sympy, student_sympy, form = "Fix"), False)