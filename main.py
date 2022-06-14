from ineq_compare import *
from poly_compare import *
from answer_conversion import *

while True:
    correct_latex = input(r'문제 정답(latex, $ 가능): ')
    #correct_str = input('문제 정답(str): ')
    student_str = input('학생 답안(str): ')

    '''
    StrCompare: 0
    PolyCompare: 1
    PolyFactorCompare: 2
    PolyExpansionCompare: 3
    PolyFormCompare: 4
    NumCompare: 5
    primefactor_compare: 6
    PairCompare: 7
    EqCompare: 8
    IneqCompare: 9
    '''
    compare_number = input('compare_number: ')
    compare_dict = {'0': 'StrCompare','1': 'PolyCompare', '2': 'PolyFactorCompare', '3': 'PolyExpansionCompare', '4': 'PolyFormCompare',
                    '5':'NumCompare', '6':'NumPrimeFactorCompare', '7':'PairCompare', '8':'EqCompare', '9':'IneqCompare'}
    correct_sympy, student_sympy = Ans2Sympy(correct_latex,student_str,f=compare_dict[compare_number])

    print(compare_dict[compare_number] + ' 실행합니다.')

    if compare_number == '3':
        symbol = input('symbol: ')
        order = input('내림차순: Dec, 오름차순: Acc 입력: ')
        print(globals()[compare_dict[compare_number]](correct_sympy, student_sympy, symbol, order))
    elif compare_number == '5':
        type = input('type: ')
        order = input('order: ')
        print(globals()[compare_dict[compare_number]](correct_sympy, student_sympy, type, order))
    elif compare_number == '7':
        order = input('order: ')
        print(globals()[compare_dict[compare_number]](correct_sympy, student_sympy, order))
    elif compare_number == '8':
        leading_coeff = input('leading_coeff: ')
        print(globals()[compare_dict[compare_number]](correct_sympy, student_sympy, leading_coeff))
    else:
        print(globals()[compare_dict[compare_number]](correct_sympy, student_sympy))