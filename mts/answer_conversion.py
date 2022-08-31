from sympy import *
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application, convert_xor,implicit_application,implicit_multiplication,convert_equals_signs,function_exponentiation
from latex2sympy2 import latex2sympy
from re import split,sub,findall,search,finditer

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
    ptn = '(?<![0-9])([1]\*{1})(?!\*)|(?<!\*)([\*\/]{1}[1])(?![0-9])'
    for i in range(len(ret)):
        ret[i] = Parse2Sympy(sub(ptn,'',str(ret[i])))
    return ret

# str -> sympy 변환
def Parse2Sympy(expr):
    try:
        tmp = sub(r'×', '*', expr)
        return parse_expr(tmp, transformations=standard_transformations+(implicit_multiplication_application, convert_xor,implicit_application,implicit_multiplication,convert_equals_signs,function_exponentiation), local_dict=ns, evaluate=False)
    except:
        print('sympy 변환에 실패했습니다.')
# print(Parse2Sympy('0.5'),Parse2Sympy('i-1'),Parse2Sympy('sin x**2'))
# print(Parse2Sympy('-1+x'),DelMulOne([Parse2Sympy('-1+x')]),Parse2Sympy('-1+x').args,DelMulOne([Parse2Sympy('-1+x')])[0].args )

# latex(str) -> sympy 변환
def Latex2Sympy(expr):
    if 'dot' in expr: return sub(r'}', ']', sub(r'\\dot\{', '[', expr))
    tmp = sub(r'\\times', '*', sub('dfrac', 'frac', expr))

    float_list = findall('[0-9]+\.[0-9]+', tmp)
    if len(float_list) != 0:
        # frac_list = list(map(Rational, float_list))

        float_id = []
        for i in finditer('[0-9]+\.[0-9]+', tmp):
            float_id.append(i.span())

        for k in range(len(float_id)):
            i,j = float_id[::-1][k]
            tmp = tmp[:i] +'a_{'+str(k)+'}'+tmp[j:]

    try:
        def ReArrArgs(sympy):
            sgn = {Add: '+', Mul: '*',Pow:'**'}
            args = list(sympy.args)
            for i in range(len(args)):
                if type(args[i]) in [Mul, Add]:
                    args[i] = ReArrArgs(args[i]).replace('+(-','-(')
            if type(sympy) == Pow and 'sqrt' in str(sympy): return 'sqrt('+args[0]+')'
            elif type(sympy) in [Add,Mul,Pow]:
                join_list = list(map(str, DelMulOne(args)))
            else:
                raise
            return sgn[type(sympy)].join(map(lambda x:'(' + x+')',join_list))

        ptn = '(?<![0-9_])([1]\)?\*{1}\(?)(?!\*)|(?<!\*)(\)?[\*\/]{1}\(?[1])(?![0-9])' # 소괄호 포함. DelMulOne과 다름
        re_str = sub(ptn,'',ReArrArgs(latex2sympy(tmp)))

        for i in range(len(float_list)):
            re_str = re_str.replace('a_' + str(i),float_list[::-1][0])

        return Parse2Sympy(re_str)
    except:
        print('latex2sympy 바로 변환',expr)
        re_str = str(latex2sympy(tmp))

        for i in range(len(float_list)):
            re_str = re_str.replace('a_' + str(i),float_list[::-1][0])

        return Parse2Sympy(re_str)
    else:
        return 'latex 변환에 실패했습니다.'

# print(Latex2Sympy(r'\dfrac{1}{2}+0.5x'),sep="\n")
# print(Parse2Sympy(r'a-5xa'),Parse2Sympy(r'a-5xa').args)
# print(Latex2Sympy(r'0.[5]'))
# print(Latex2Sympy(r'-0.\dot{5}'))
# #print(latex2sympy('a<b<c'),findall(r'([<>][=]?)', str('a<=b<c')),latex2sympy('a<1,a>1'),latex2sympy(r'a\ne2'))
# print(Parse2Sympy('0.5'),together(Parse2Sympy('(i-1)/2')),DelMulOne([Latex2Sympy('i-1,1')]))
# print(Latex2Sympy(r'\sqrt{1-5xy}').args[0].args,Parse2Sympy('sqrt(1-5*x*y)').args[0].args,'요호')
# print(Latex2Sympy(r'\sqrt{1-5xy}'),Parse2Sympy('sqrt(1-5*x*y)'))
# print(Latex2Sympy(r'\dfrac{3}{2}').args)
# print(Parse2Sympy(r'3/2').args)
# print(Latex2Sympy(r'x^2-8x+15'))
# print(Parse2Sympy(r'0.4'))


# 부등식 a<b<c, !=(\ne)(str)을 sympy 형태로 변환
def Ineq2Sympy(correct_latex, student_str):
    cr_l = correct_latex.split(',')
    st_l = student_str.split(',')
    for j in range(2):
        f = [lambda x: Latex2Sympy(x),lambda x: Parse2Sympy(x)][j]
        l = [cr_l,st_l][j]
        for i in range(len(l)):
            if len(findall(r'<|>|\\ge|\\le', l[i])) == 2:
                parts = split(r'([<>][=]?|\\ge|\\le)', l[i])
                tmp = [Rel(f(parts[0]),f(parts[2]),parts[1]).canonical, Rel(f(parts[2]),f(parts[4]),parts[3]).canonical]
                l[i] = And(tmp[0], tmp[1])
            elif len(findall(r'!=|\\ne', l[i])) > 0:
                parts = split(r'!=|\\ne', l[i])
                l[i] = Or(Rel(f(parts[0]),f(parts[1]),'<').canonical, Rel(f(parts[0]),f(parts[1]),'>').canonical)
            else: l[i] = f(l[i]).canonical
    return cr_l,st_l
# print(Ineq2Sympy(r'-\dfrac{1}{2}<x<0.5', '-0.5<x<1/2'))


# compare에 따른 correct_sympy, student_sympy 변환
def Ans2Sympy(correct_latex,student_str,f=None):
    print('Ans2Sympy input', correct_latex, student_str)
    repls = {r'\,':'',r'\rm':''}
    for key in repls.keys():
        correct_latex = correct_latex.replace(key, repls[key])

    if correct_latex == student_str: print('input str 같음'); return True

    if f == 'StrCompare' or f == 'SignCompare' or f == 'NoSignCompare':
        correct_sympy = correct_latex
        student_sympy = student_str
    elif f == 'PairCompare':
        c_split_str = split('(?<=\))(\s*,\s*)(?=\()',correct_latex)
        s_split_str = split('(?<=\))(\s*,\s*)(?=\()',student_str)
        c_split_str = list(filter(lambda x: search(r'\)|\(',x) != None, c_split_str))
        s_split_str = list(filter(lambda x: search(r'\)|\(',x) != None, s_split_str))
        correct_sympy = list(map(lambda str: Latex2Sympy(str[1:-1]), c_split_str))
        student_sympy = list(map(lambda str: list(Parse2Sympy(str)), s_split_str))
    elif f == 'IneqCompare':
        correct_sympy, student_sympy = Ineq2Sympy(correct_latex, student_str)
    else:
        ptn = '(?<![0-9])([1]\*{1})(?!\*)|(?<!\*)([\*\/]{1}[1])(?![0-9])'
        if len(findall(ptn, student_str)) != 0: return False #계수 1 생략X
        if search(r',', correct_latex) != None:
            c_split_str = correct_latex.split(',')
            s_split_str = student_str.split(',')
        elif f == 'EqCompare':
            c_split_str = correct_latex.split('=')
            s_split_str = student_str.split('=')
        else:
            c_split_str = [correct_latex]
            s_split_str = [student_str]

        l_c = len(c_split_str)
        l_s = len(c_split_str)
        for i in range(l_c):
            s = c_split_str[::-1][i]
            if '\\pm' in s:
                c_split_str = c_split_str[:l_c-i-1] + [s.replace('\\pm','+'), s.replace('\\pm','-')] + c_split_str[l_c-i:]

        for i in range(l_s):
            s = s_split_str[::-1][i]
            if '±' in s:
                s_split_str = s_split_str[:l_s-i-1] + [s.replace('±','+'), s.replace('±','-')] + s_split_str[l_s-i:]

        correct_sympy = list(map(lambda str: Latex2Sympy(str), c_split_str))
        student_sympy = list(map(lambda str: Parse2Sympy(str), s_split_str))

    print('Ans2Sympy output', correct_sympy, student_sympy)
    return [correct_sympy, student_sympy]
#Ans2Sympy('x^2+4x+4','x**2+4*(x+1)')
# print(Ans2Sympy('x^2,2x,1','x**2,2*x,1',f = 'PolyCompare'))
# print(Ans2Sympy('(1,1)','(1,1)',f = 'PolyFactorCompare'))
# print(Ans2Sympy('xy+3x+5y+15','xy+3x+5y+10+5',f = 'PolyExpansionCompare'))
# print(Ans2Sympy('(1,1)','(1,1)',f = 'PolySortCompare'))
# print(Ans2Sympy('4000-0.5x','4000-1/2*x',f = 'PolyFormCompare'))
# print(Ans2Sympy('(1,1)','(1,1)',f = 'NumPrimeFactorCompare'))
# print(Ans2Sympy('\pm 1,2','2,±1',f = 'NumCompare'))
# print(Ans2Sympy('(1-i,1),(3xy, -5xy)','(i-1-1,1),(3xy, -5xy)',f = 'PairCompare'))
# print(Ans2Sympy(r'x^2-8x+15=0','x**2-8x+15=0',f = 'EqCompare'))
# print(Ans2Sympy('(1,1)','(1,1)',f = 'IneqCompare'))
# print(Ans2Sympy(r'\rm A','A',f = 'StrCompare'))