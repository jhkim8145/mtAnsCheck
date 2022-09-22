from sympy import *
from re import *
from mts.answer_conversion import *
from mts.poly_compare import *


# 부등식 1개 비교
def single_ineq(correct_sympy,student_sympy):
    # print(correct_sympy,student_sympy)
    if type(correct_sympy) != type(student_sympy):
        print('type 오류',type(correct_sympy),type(student_sympy))
        return False

    if type(correct_sympy) == And: # (k>1) & (k<5)일 때
        if all(single_ineq(correct_sympy.args[i],student_sympy.args[i]) for i in range(2)):
            return True
        else:
            return all(single_ineq(correct_sympy.args[i-1],student_sympy.args[i]) for i in range(2))

    if all(IsSimilarTerm(student_sympy.args[i]) for i in range(2)) == 0:
        print('부등식 양변 동류항 정리X')
        return False

    cr_poly = Add(correct_sympy.lhs,-correct_sympy.rhs,evaluate=False)
    st_poly = Add(student_sympy.lhs,-student_sympy.rhs,evaluate=False)
    print(cr_poly,'/',st_poly,'poly')

    return single_poly(cr_poly,st_poly)

# correct_sympy, student_sympy = Ans2Sympy(r'-\dfrac{1}{3}<x\le\dfrac{4}{3}a','-1/3<x<= 4/3*a',f = 'IneqCompare')
# correct_sympy, student_sympy = correct_sympy[0], student_sympy[0]
# # print(correct_sympy.args[0].args,correct_sympy.args[1].args[1].args,student_sympy.args[0].args,student_sympy.args[1].args[1].args)
# print(single_ineq(correct_sympy, student_sympy))
# print((Latex2Sympy('\dfrac{4}{3}a')*2/2).args,(Latex2Sympy('4*a/3')*2/2).args)

# 부등식 리스트 비교
def IneqCompare(correct_sympy,student_sympy,form = None):
    # print(correct_sympy,student_sympy)
    if len(correct_sympy) != len(student_sympy):
        print('len 오류');return False

    cr_tmp = correct_sympy[:]
    st_tmp = student_sympy[:]

    for ineq in student_sympy:
        if ineq in correct_sympy:
            cr_tmp.remove(ineq)
            st_tmp.remove(ineq)
        elif any(single_ineq(cr,ineq) for cr in cr_tmp) == 1 and form == None:
            st_tmp.remove(ineq)
        else:
            print('정답 오류'); return false
    return True

if __name__ == "__main__":
    # correct_sympy, student_sympy = Ans2Sympy(r'-\dfrac{1}{3}< x\le\dfrac{4}{3}','-1/3<x<= 4/3',f = 'IneqCompare')
    correct_sympy, student_sympy = Ans2Sympy(r'x\ge1','x>=1', f='IneqCompare')
    print(IneqCompare(correct_sympy, student_sympy))
    # print(single_ineq(correct_sympy[0], student_sympy[0]))
    # print(IneqCompare(correct_sympy, student_sympy))



