from sympy import *
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application, convert_xor,implicit_application,implicit_multiplication,convert_equals_signs,function_exponentiation
from latex2sympy2 import latex2sympy
from re import split,sub,findall,search,finditer
from mts.set_compare import *

ns={'Symbol':Symbol,'Integer':Integer,'Float':Float,'Rational':Rational,'Eq':Eq,'I':I,
    'i':I,'E':E,'e':E,'pi':pi,'exp':exp,'log':log,'ln':ln,'logten':lambda x:log(x,10),
    'sqrt':sqrt,'factorial':factorial,'fact':factorial,'sin':sin,'cos':cos,'tan':tan,
    'sec':sec,'csc':csc,'cot':cot,'asin':asin,'arcsin':asin,'acos':acos,'arccos':acos,
    'atan':atan,'arctan':atan,'acsc':acsc,'arccsc':acsc,'asec':asec,'arcsec':asec,
    'acot':acot,'arccot':acot,'sinh':sinh,'cosh':cosh,'tanh':tanh,
    'coth':coth,'asinh':asinh,'arsinh':asinh,'arcsinh':asinh,'acosh':acosh,
    'arcosh':acosh,'arccosh':acosh,'atanh':atanh,'artanh':atanh,'arctanh':atanh,
    'acoth':acoth,'arcoth':acoth,'arccoth':acoth}

def P(string):
    return parse_expr(string, transformations=standard_transformations+(implicit_multiplication_application, convert_xor,implicit_application,implicit_multiplication,convert_equals_signs,function_exponentiation), local_dict=ns, evaluate=False)
# print(simplify(P('x-1-2')),P('1-a'),P('x-10'),P('x-y'))

# -1*1 -> -1로 변환
def DelMulOne(sympy_tuple):
    ret = list(sympy_tuple)
    ptn = '(?<![0-9])([1]\*{1})(?!\*)|(?<!\*)([\*\/]{1}[1])(?![0-9])'
    for i in range(len(ret)):
        ret[i] = P(sub(ptn,'',str(ret[i])))
    return ret

# sympy(str) -> sympy 변환
def Parse2Sympy(expr):
    try:
        tmp = sub(r'×', '*', expr)
        if type(P(tmp)) == Mul and expr[:2] == '-(':
            tmp = '(-1)*' + expr[1:]
        return P(tmp)
    except:
        print('sympy 변환에 실패했습니다.')
# print(Parse2Sympy('0.5'),Parse2Sympy('i-1'),Parse2Sympy('sin x**2'))
# print(type(P('2*i')))
# print(Parse2Sympy('-1+x'),DelMulOne([Parse2Sympy('-1+x')]),Parse2Sympy('-1+x').args,DelMulOne([Parse2Sympy('-1+x')])[0].args )
# print(Parse2Sympy('-2(a - 2*b)*(x - y)'))


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
            # print(sympy)
            sgn = {Add: '+', Mul: '*',Pow:'**'}
            Args = list(sympy.args)
            for i in range(len(Args)):
                if type(Args[i]) in [Mul, Add]:
                    Args[i] = ReArrArgs(Args[i])
            if type(sympy) == Pow and 'sqrt' in str(sympy): return 'sqrt('+Args[0]+')' # 수정필요
            elif type(sympy) in [Add,Mul,Pow]:
                join_list = list(map(str, Args))
                if type(sympy) == Mul and join_list[0] == '-1':
                    pass
                    # join_list.insert(0,f'({join_list[0]}*{join_list[1]})')
                    # del join_list[1],join_list[2]
            else:
                raise
            ret = sgn[type(sympy)].join(map(lambda x:'(' + x+')',join_list))
            # print(ret,'ret')
            return ret

        ptn = {'(?<![0-9_\-])([1]\)?\*{1}\(?)(?!\*)|(?<!\*)(\)?[\*\/]{1}\(?[1])(?![0-9])':'', # 소괄호 포함. DelMulOne과 다름
               '(?<![0-9])([1]\*{1})(?!\*)|(?<!\*)([\*\/]{1}[1])(?![0-9])':'',
               '\(\-1\)\*':'-','\(1\)\*':''}
        re_str = ReArrArgs(latex2sympy(tmp))

        for key in ptn.keys():
            re_str = sub(key, ptn[key], re_str)

        for i in range(len(float_list)):
            re_str = re_str.replace('a_' + str(i), float_list[::-1][0])

        if Parse2Sympy(re_str).equals(latex2sympy(expr)):
            print("ReArrArgs 성공")
            return Parse2Sympy(re_str)
        else:
            print("ReArrArgs 실패", re_str)
            raise

    except:
        print('latex2sympy 바로 변환', expr)
        re_str = str(latex2sympy(tmp))

        for i in range(len(float_list)):
            re_str = re_str.replace('a_' + str(i),float_list[::-1][0])

        return Parse2Sympy(re_str)
    else:
        return 'latex 변환에 실패했습니다.'

# print(latex2sympy('\sqrt{2}').args, latex2sympy('2^{\\frac{1}{2}}').args)
# print(Latex2Sympy('20\sqrt{0.07}').args, Parse2Sympy('2*sqrt(7)').args)
# print(Latex2Sympy('x-1'),Parse2Sympy('x-1'))
# print(Latex2Sympy(r'\dfrac{1}{2}+0.5x'),sep="\n")
# print(Parse2Sympy(r'a-5xa'),Parse2Sympy(r'a-5xa').args)
# print(Latex2Sympy(r'0.[5]'))
# print(Latex2Sympy(r'-0.\dot{5}'))
# print(latex2sympy('a<b<c'),findall(r'([<>][=]?)', str('a<=b<c')),latex2sympy('a<1,a>1'),latex2sympy(r'a\ne2'))
# print(Parse2Sympy('0.5'),together(Parse2Sympy('(i-1)/2')),DelMulOne([Latex2Sympy('i-1,1')]))
# print(Latex2Sympy(r'\sqrt{1-5xy}').args[0].args,Parse2Sympy('sqrt(1-5*x*y)').args[0].args,'요호')
# print(Latex2Sympy(r'\sqrt{1-5xy}'),Parse2Sympy('sqrt(1-5*x*y)'))
# print(Latex2Sympy(r'\dfrac{3}{2}').args)
# print(Parse2Sympy(r'3/2').args)
# print(Latex2Sympy(r'x^2-8x+15'))
# print(Parse2Sympy(r'0.4'))
# print(Latex2Sympy('-(a-2b)(x-y)') ,'|', Parse2Sympy('-(a-2b)(x-y)'))
# print('-----------')
# print(Latex2Sympy('-(a-2b)-(x-y)').args,'|',latex2sympy('-(a-2b)-(x-y)').args,'|', Parse2Sympy('-(a-2b)-(x-y)').args)
# print('-----------')
# print(Latex2Sympy('-(a-2b)(x-y)-(a-2b)(x-y)'),'|',latex2sympy('-(a-2b)(x-y)-(a-2b)(x-y)'),'|', Parse2Sympy('-(a-2*b)*(x-y)-(a-2*b)*(x-y)'))
# print('-----------')
# print(Latex2Sympy('\\frac{1}{2}'))#,latex2sympy('\\frac{1}{2}'),Parse2Sympy('1/2'))
# print('-----------')
# print(Latex2Sympy('4 x^{2}-20 x y+8 x z+ 25 y^{2} - 20 y z + 4 z^{2}'))
# print(Latex2Sympy('-5xy'),Parse2Sympy('-5*x*y'))
# print(Latex2Sympy(r'0.5'),Parse2Sympy('1/2'))
# print('-----------')
# print(latex2sympy(r'A\cap B'))
# print(latex(Interval.Ropen(P('0'),P('1'))))



# compare에 따른 correct_sympy, student_sympy 변환
def Ans2Sympy(correct_latex,student_str,f = None):

    print('Ans2Sympy input', correct_latex, student_str)
    repls = {r'\,': '', r'\rm': '', r'\left': '', r'\right': '', r'\\hbox{\s*또는\s*}': ','}
    for key in repls.keys():
        correct_latex = correct_latex.replace(key, repls[key])

    if correct_latex.replace(" ","") == student_str.replace(" ",""): print('input str 같음'); return True

    if f in ['StrCompare', 'SignCompare', 'NoSignCompare', 'IneqCompare', 'IntvCompare', 'SetCompare']:
        correct_sympy = correct_latex
        student_sympy = student_str
    elif f == 'PairCompare':
        # if any([search(r'^\(', student_str) == None, search(r'\)$', student_str) == None]): return False
        # else: student_str = student_str[1:-1]
        # c_split_str = split('(?<=\))(\s*,\s*)(?=\()',correct_latex)
        # s_split_str = split('(?<=\))(\s*,\s*)(?=\()',student_str)
        c_split_str = split_set(correct_latex, 0)
        s_split_str = split_set(student_str, 0)
        print(c_split_str,s_split_str)
        # c_split_str = list(filter(lambda x: search(r'\)|\(',x) != None, c_split_str))
        # s_split_str = list(filter(lambda x: search(r'\)|\(',x) != None, s_split_str))
        # print(c_split_str, s_split_str)
        # correct_sympy = list(map(lambda str: Latex2Sympy(str[1:-1]), c_split_str))
        # student_sympy = list(map(lambda str: list(Parse2Sympy(str)), s_split_str))
        correct_sympy = list(map(lambda str: list(map(lambda x: Latex2Sympy(x), split('\s*,\s*', str[1:-1]))), c_split_str))
        if s_split_str != False:
            student_sympy = list(map(lambda str: list(map(lambda x: Parse2Sympy(x), split('\s*,\s*', str[1:-1]))), s_split_str))
        else: student_sympy = False
    else:
        ptn = '(?<![0-9])([1]\*{1})(?!\*)|(?<!\*)([\*\/]{1}[1])(?![0-9])'
        if len(findall(ptn, student_str)) != 0: return False #계수 1 생략X
        if search(r',', correct_latex) != None or search(r',', student_str) != None:
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

        correct_sympy = list(map(lambda Str: Latex2Sympy(Str), c_split_str))
        student_sympy = list(map(lambda Str: Parse2Sympy(Str), s_split_str))

    print('Ans2Sympy output', correct_sympy, student_sympy)
    return [correct_sympy, student_sympy]
# Ans2Sympy('x^2+4x+4','x**2+4*(x+1)')
# Ans2Sympy('x-1,x+1','x+1,x-1',f = 'PolyCompare')
# Ans2Sympy('-(a-2b)(x-y)','-(a-2*b)*(x-y)',f = 'PolyFactorCompare')
# Ans2Sympy('xy+3x+5y+15','xy+3x+5y+10+5',f = 'PolyExpansionCompare')
# Ans2Sympy('4000-0.5x','4000-1/2*x',f = 'PolyFormCompare')
# Ans2Sympy('\pm 1,2','2,±1',f = 'NumCompare')
# Ans2Sympy('(1-i,1),(3xy, -5xy)','(i-1-1,1),(3xy, -5xy)',f = 'PairCompare')
# Ans2Sympy('(1-i,1)','(i-1-1,1)',f = 'PairCompare')
# Ans2Sympy(r'x^2-8x+15=0','x**2-8x+15=0',f = 'EqCompare')
# Ans2Sympy(r'\rm A','A',f = 'StrCompare')
# Ans2Sympy(r'\pm \sqrt{17} i', 'sqrt(17)*I,-sqrt(17)*I', f='NumCompare')
# Ans2Sympy(r'-5\le 3x-2 < 7','-5 <= 3x-2 < 7',f = 'IneqCompare')
# if __name__ == "__main__":
#     # Ans2Sympy(r'x\ge 8,x!=7,x=2','8<=x,x!=7,x=2',f = 'IneqCompare')
#     Ans2Sympy(r'\left(1,\dfrac{1}{2}\right)', '(1,1/2)', f='PairCompare')