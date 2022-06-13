from sympy import *
from sympy.parsing.sympy_parser import parse_expr,T
from latex2sympy2 import latex2sympy
from re import split,sub,findall,search

ns={'Symbol':Symbol,'Integer':Integer,'Float':Float,'Rational':Rational,'Eq':Eq,'I':I,
    'i':I,'E':E,'e':E,'pi':pi,'exp':exp,'log':log,'ln':ln,'logten':lambda x:log(x,10),
    'sqrt':sqrt,'factorial':factorial,'fact':factorial,'sin':sin,'cos':cos,'tan':tan,
    'sec':sec,'csc':csc,'cot':cot,'asin':asin,'arcsin':asin,'acos':acos,'arccos':acos,
    'atan':atan,'arctan':atan,'acsc':acsc,'arccsc':acsc,'asec':asec,'arcsec':asec,
    'acot':acot,'arccot':acot,'sinh':sinh,'cosh':cosh,'tanh':tanh,
    'coth':coth,'asinh':asinh,'arsinh':asinh,'arcsinh':asinh,'acosh':acosh,
    'arcosh':acosh,'arccosh':acosh,'atanh':atanh,'artanh':atanh,'arctanh':atanh,
    'acoth':acoth,'arcoth':acoth,'arccoth':acoth}


# -1*1 -> -1로 변환
def DelMulOne(sympy_tuple):
    ret = list(sympy_tuple)
    ptn = '(?<![0-9])([1]\*{1})|(\*{1}[1])(?![0-9])'
    for i in range(len(ret)):
        ret[i] = Parse2Sympy(sub(ptn,'',str(ret[i])))
    return ret

# str -> sympy 변환
def Parse2Sympy(expr):
    #print(expr, parse_expr(expr, transformations='all', local_dict=ns, evaluate=False))
    return parse_expr(expr, transformations=T[:11], local_dict=ns, evaluate=False)
# print(Parse2Sympy('0.5'),Parse2Sympy('i-1'),Parse2Sympy('sin x**2'))
# print(Parse2Sympy('-1+x'),DelMulOne([Parse2Sympy('-1+x')]),Parse2Sympy('-1+x').args,DelMulOne([Parse2Sympy('-1+x')])[0].args )

# latex(str) -> sympy 변환
def Latex2Sympy(expr):
    try: # ****순환소수는 sympy 형태로 답안 적기****
        return Parse2Sympy(expr)
    except:
        tmp = sub('dfrac','frac',expr)
        return Parse2Sympy(str(latex2sympy(tmp)))
# # print(Latex2Sympy(r'-5xy'))
# print(Latex2Sympy(r'-0.[5]'))
# print(latex2sympy(r'-0.\dot{5}'))
# #print(latex2sympy('a<b<c'),findall(r'([<>][=]?)', str('a<=b<c')),latex2sympy('a<1,a>1'),latex2sympy(r'a\ne2'))
# print(Parse2Sympy('0.5'),together(Parse2Sympy('(i-1)/2')),DelMulOne([Latex2Sympy('i-1,1')]))

# 부등식 a<b<c, !=(\ne)(str)을 sympy 형태로 변환
def Ineq2Sympy(ineq):
    l = ineq.split(',')
    for i in range(len(l)):
        if len(findall(r'<|>|\\ge|\\le', l[i])) == 2:
            parts = split(r'([<>][=]?|\\ge|\\le)', l[i])
            try:
                tmp = [Parse2Sympy(''.join(parts[:3])).canonical, Parse2Sympy(''.join(parts[-3:])).canonical]
            except:
                tmp = [Latex2Sympy(''.join(parts[:3])).canonical, Latex2Sympy(''.join(parts[-3:])).canonical]
            l[i] = And(tmp[0], tmp[1])
        elif len(findall(r'!=|\\ne', l[i])) > 0:
            parts = split(r'!=|\\ne', l[i])
            l[i] = Or((Parse2Sympy(parts[0]+'<'+parts[1])).canonical, (Parse2Sympy(parts[0]+'>'+parts[1])).canonical)
        else: l[i] = Parse2Sympy(l[i]).canonical
    return l
#print(Ineq2Sympy(r'x!= 1,x>1,a\ge b\ge c'))


# compare에 따른 correct_sympy, student_sympy 변환
def Ans2Sympy(correct_latex,student_str,f=None):
    if f == 'PairCompare':
        c_split_str = split('(?<=\))(\s*,\s*)(?=\()',correct_latex)
        s_split_str = split('(?<=\))(\s*,\s*)(?=\()',student_str)
        c_split_str = list(filter(lambda x: search(r'\)|\(',x) != None, c_split_str))
        s_split_str = list(filter(lambda x: search(r'\)|\(',x) != None, s_split_str))
        correct_sympy = list(map(lambda str: Latex2Sympy(str[1:-1]), c_split_str))
        student_sympy = list(map(lambda str: list(Parse2Sympy(str)), s_split_str))
    elif f == 'IneqCompare':
        correct_sympy = Ineq2Sympy(c_split_str)
        student_sympy = Ineq2Sympy(s_split_str)
    else:
        if search(r',', correct_latex) != None:
            c_split_str = correct_latex.split(',')
            s_split_str = student_str.split(',')
        elif f == 'EqCompare':
            c_split_str = correct_latex.split('=')
            s_split_str = student_str.split('=')
        else:
            c_split_str = [correct_latex]
            s_split_str = [student_str]
        correct_sympy = list(map(lambda str: Latex2Sympy(str), c_split_str))
        student_sympy = list(map(lambda str: Parse2Sympy(str), s_split_str))
    return correct_sympy, student_sympy
#Ans2Sympy('x^2+4x+4','x**2+4*(x+1)')
# print(Ans2Sympy('x^2+2x+1+1','x**2+2*x+1',f = 'PolyCompare'))
# print(Ans2Sympy('(1,1)','(1,1)',f = 'PolyFactorCompare'))
# print(Ans2Sympy('xy+3x+5y+15','xy+3x+5y+10+5',f = 'PolyExpansionCompare'))
# print(Ans2Sympy('(1,1)','(1,1)',f = 'PolySortCompare'))
# print(Ans2Sympy('(1,1)','(1,1)',f = 'PolyFormCompare'))
# print(Ans2Sympy('(1,1)','(1,1)',f = 'NumPrimeFactorCompare'))
# print(Ans2Sympy('(1-i,1),(3xy, -5xy)','(i-1-1,1),(3xy, -5xy)',f = 'PairCompare'))
# print(Ans2Sympy(r'x^2-8x+15=0','x**2-8x+15=0',f = 'EqCompare'))
# print(Ans2Sympy('(1,1)','(1,1)',f = 'IneqCompare'))