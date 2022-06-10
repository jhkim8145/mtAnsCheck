from ineq_compare import *
from poly_compare import *
from answer_conversion import *

correct_latex = input(r'문제 정답(latex, $ 가능): ')
#correct_str = input('문제 정답(str): ')
student_str = input('학생 답안(str): ')

'''
poly_simple_compare: 0
factor_compare: 1
expand_compare: 2
order_compare: 3
poly_form_compare: 4
number_compare: 5
primefactor_compare: 6
pair_compare: 7
equation_simple_compare: 8
ineq_compare: 9
'''
compare_number = input('compare_number: ')
compare_dict = {'0': 'PolyCompare', '1': 'PolyFactorCompare', '2': 'PolyExpansionCompare', '3': 'PolySortCompare', '4': 'PolyFormCompare',
                '5':'NumCompare', '6':'NumPrimeFactorCompare', '7':'PairCompare', '8':'EqCompare', '9':'IneqCompare'}
correct_sympy, student_sympy = Ans2Sympy(correct_latex,student_str,f=compare_dict[compare_number])

print(compare_dict[compare_number] + ' 실행합니다.')
if compare_number == '3':
    symbol = input('symbol: ')
    order = input('내림차순: desc, 오름차순: asc 입력: ')
    print(PolySortCompare(correct_sympy, student_sympy, symbol, order))
elif compare_number == '5':
    type = input('type: ')
    order = input('order: ')
    print(NumCompare(correct_sympy, student_sympy, type, order))
elif compare_number == '7':
    order = input('order: ')
    print(PairCompare(correct_sympy, student_sympy, order))
elif compare_number == '8':
    leading_coeff = input('leading_coeff: ')
    print(EqCompare(correct_sympy, student_sympy, leading_coeff))
elif compare_number == '0':
    print(PolyCompare(correct_sympy, student_sympy))
elif compare_number == '1':
    print(PolyFactorCompare(correct_sympy, student_sympy))
elif compare_number == '2':
    print(PolyExpansionCompare(correct_sympy, student_sympy))
elif compare_number == '4':
    print(PolyFormCompare(correct_sympy, student_sympy))
elif compare_number == '6':
    print(NumPrimeFactorCompare(correct_sympy, student_sympy))



# if compare_number == '3':
#     symbol = input('symbol: ')
#     order = input('내림차순: desc, 오름차순: asc 입력: ')
#     print(exec(compare_dict[compare_number] + '(correct_sympy, student_sympy, symbol, order)'))
# elif compare_number == '5':
#     type = input('type: ')
#     order = input('order: ')
#     print(exec(compare_dict[compare_number] + '(correct_sympy, student_sympy, type, order)'))
# elif compare_number == '7':
#     order = input('order: ')
#     print(exec(compare_dict[compare_number] + '(correct_sympy, student_sympy, order)'))
# elif compare_number == '8':
#     leading_coeff = input('leading_coeff: ')
#     print(exec(compare_dict[compare_number] + '(correct_sympy, student_sympy, leading_coeff)'))
# else:
#     print(compare_dict[compare_number] + ' 실행합니다.')
#     print(PolyCompare(correct_sympy, student_sympy))
#     print(exec(compare_dict[compare_number] + '(correct_sympy, student_sympy)'))