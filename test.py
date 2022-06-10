from sympy import *
from sympy.parsing.sympy_parser import parse_expr, transformations, stringify_expr
from sympy.parsing.latex import parse_latex
from re import *
from sympy.core.sympify import kernS


# str -> sympy 변환
def P(str):
    str = sub('(?<![0-9])([1]\*{1})|(\*{1}[1])(?!=[0-9])','',str) # 1*, *1 삭제
    #return sympify(str,evaluate=False)
    return parse_expr(str,evaluate=False,transformations='all')



# 단순 비교
correct_latex = r'x^{2}+(y+3) x+2 y^{2}-5 y-4'
# correct_sympy = parse_latex(correct_latex)
correct_answer = 'x**2 + x*(y + 2) + 2*y**2 -3*y-2*y- 4'
student_answer = '(x)**(2)+(y+2)*x+2*(y)**(2)-5*y-4'
correct_sympy = P(correct_answer)
student_sympy = P(student_answer)
#print(correct_sympy, student_sympy,sep='\n')
# print(student_sympy.equals(correct_sympy))
def simple_compare(correct_sympy, student_sympy):
    return student_sympy.equals(correct_sympy)
#print(simple_compare(correct_sympy, student_sympy))




# 인수분해/전개
correct_answer = '(x+1)*(x+2)'
student_answer = '(x+2)*(x+0.5+0.5)'
#correct_answer = 'x**2+3*x+2'
#student_answer = '3*x+x**2+1+1'
correct_sympy = P(correct_answer)
student_sympy = P(student_answer)
#print(correct_sympy.args, student_sympy.args,sep='\n')
#print(simple_compare(correct_sympy, student_sympy))
#print(factor(student_sympy), expand(student_sympy),sep='\n')
def factor_expand_compare(correct_sympy, student_sympy, opt):
    if simple_compare(correct_sympy, student_sympy) == 1:
        if len(correct_sympy.args) != len(student_sympy.args): return False
        if opt == 'f':
            for t in student_sympy.args:
                if t not in correct_sympy.args: return False
            return True
        elif opt == 'e' and student_sympy == expand(student_sympy): return True
        else: return False
    else: return False
#print(factor_expand_compare(correct_sympy, student_sympy,'f'))




# 순서 비교 (오름차순, 내림차순)
# x*(y+2), (y+2)*x 둘 다 같다고 인식
correct_answer = 'x**2+(y+3)*x+2*y**2-5*y-4'
student_answer = '(x)**(2)+(y+3)*x+2*(y)**(2)-5*y-4'
#student_answer = '2*(y)**(2)-5*y-4+(x)**(2)+(y+2)*x'
correct_answer = '2*y**2-5*y-4+(y+3)*x+x**2'
student_answer = '-4+2*y**2-5*y+(y+3)*x+x**2'
correct_sympy = P(correct_answer)
student_sympy = P(student_answer)
#print(student_sympy.args,sympify(str(collect(student_sympy,x)),evaluate=False).args,sep='\n')
#print(degree(correct_sympy,x))
def order_compare(correct_sympy,student_sympy,symbol,order):
    if simple_compare(correct_sympy, student_sympy) == 1:
        compare_tuple = sympify(str(collect(student_sympy, symbol)), evaluate=False).args
        n = len(compare_tuple)
        for i in range(len(compare_tuple)):
            if degree(compare_tuple[i],sympify(symbol)) == 0:
                n = i
                break
        if len(compare_tuple) == len(student_sympy.args):
            if order == "asc":
                return all(student_sympy.args[i].equals(compare_tuple[i]) for i in range(n))
            elif order == "desc":
                return all(student_sympy.args[-i-1].equals(compare_tuple[i]) for i in range(n))
    else: return False
#print(order_compare(correct_sympy, student_sympy, 'x', 'desc'))




# 방정식 단순 비교
correct_answer = '2(x+1)*(x+1/2)=0'
student_answer = '(2x+2)*(1/2x+1/4)=0'
correct_answer = 'x**3-3*x**2+4*x+1=(x+1)*(x**2-4*x+8)-7'
student_answer = '(x+1)*(x**2-4*x+8)-7=x**3-3*x**2+4*x+1'
correct_answer = 'x=1'
student_answer = '2x-x=1'
correct_answer = 'x=x**2'
student_answer = '-x=-x**2'
correct_answer = '(x+1)*(x+2)=0'
student_answer = '-(x+1)*(x+2)=0'
#student_answer = '0=(x+1)*(x+2)'
#student_answer = 'x**2=-3*x-2'
c_split_str = correct_answer.split('=')
s_split_str = student_answer.split('=')

c_split_sympy = list(map(lambda str: P(str), c_split_str))
s_split_sympy = list(map(lambda str: P(str), s_split_str))

def equation_simple_compare(c_split_sympy,s_split_sympy,leading_coeff = 'non-fix'):
    c_poly = c_split_sympy[0]-c_split_sympy[1]
    s_poly = s_split_sympy[0]-s_split_sympy[1]
    c_eq = Eq(c_poly,0)
    s_eq = Eq(s_poly,0)
    if leading_coeff == 'non-fix':
        c_poly = factor(c_poly).as_coeff_Mul()[1]
        s_poly = factor(s_poly).as_coeff_Mul()[1]
    elif any(LT(s_split_sympy[i]).equals(LT(s_poly)) == 0 for i in range(2) if s_split_sympy[i].is_number == 0) == 0: return False
    return Or(simple_compare(c_eq, s_eq),simple_compare(c_eq, s_eq.reversedsign))
#print(equation_simple_compare(c_split_sympy,s_split_sympy,leading_coeff = 'fix'))
#print(equation_simple_compare(c_split_sympy,s_split_sympy))

#def equation_simple_compare(c_split_sympy,s_split_sympy,leading_coeff = 'non-fix'): # Eq(l-r,0)
#    c_sympy = c_split_sympy[0] - c_split_sympy[1]
#    s_sympy = s_split_sympy[0] - s_split_sympy[1]
#    print(c_sympy.as_content_primitive(clear=False), s_sympy.as_content_primitive())
#    if leading_coeff == 'fix' and c_sympy.as_content_primitive()[0] != s_sympy.as_content_primitive()[0]: return False
#    if leading_coeff == 'non-fix':
#        c_sympy = c_sympy.as_content_primitive()[1]
#        s_sympy = s_sympy.as_content_primitive()[1]
#    return simple_compare(c_sympy, s_sympy)
#print(equation_simple_compare(c_split_sympy,s_split_sympy,leading_coeff = 'fix'))
#print(equation_simple_compare(c_split_sympy,s_split_sympy))


#def equation_simple_compare(c_split_sympy,s_split_sympy,leading_coeff = 'non-fix'):
#    c_sympy = c_split_sympy[0] - c_split_sympy[1]
#    s_sympy = s_split_sympy[0] - s_split_sympy[1]
#    if leading_coeff == 'fix' and simplify(c_sympy).is_Number == simplify(s_sympy).is_Number == 0:
#        if LC(c_sympy) != LC(s_sympy): return False
#    if leading_coeff == 'non-fix':
#        c_sympy = factor(c_sympy).as_coeff_Mul()[1]
#        s_sympy = factor(s_sympy).as_coeff_Mul()[1]
#    return simple_compare(c_sympy, s_sympy)
#print(equation_simple_compare(c_split_sympy,s_split_sympy,leading_coeff = 'fix'))
#print(equation_simple_compare(c_split_sympy,s_split_sympy))



# 다항식 정확히 비교 (22.05.20~)
# BQ+R 꼴, a(x-p)**2+q 꼴 등

correct_answer = '(x+1)*(x**2-4*x+8)-7'
student_answer = '(x+1)*(x**2+4+4-4*x)-7'
#correct_answer = '2*(x-1)**2+3'
#student_answer = '2*(x**2-2x+1)+3'
#student_answer = '2*(1-x)**2+3'
#correct_answer = '-1+x'
#student_answer = 'x-1/2-1/2'
#correct_answer = '2*(x+1)'
#student_answer = '2*(x+1)'

correct_sympy = P(correct_answer)
student_sympy = P(student_answer)

def poly_form_compare(correct_sympy,student_sympy): # 다항식 A, B 교환 허용X, 동류항 반드시 정리해야 함
    if simple_compare(correct_sympy,student_sympy) == 0: print('0');return False
    c_args = correct_sympy.args
    s_args = student_sympy.args
    if len(c_args) != len(s_args): print('1');return False
    while True:
        print(c_args, s_args)
        c_args_tmp = ()
        s_args_tmp = ()
        if c_args == s_args == (): print('2');return True
        for i in range(len(c_args)):
            if len(c_args[i].args) != len(s_args[i].args): print('3');return False
            if c_args[i].is_number == 0 and len(c_args[i].args) != len(expand(c_args[i]).args):
                print('전개비교',c_args[i], expand(c_args[i]).args)
                if simple_compare(c_args[i],s_args[i]) == 0: print(c_args,s_args);print('4');return False
                c_args_tmp += c_args[i].args
                s_args_tmp += s_args[i].args
            print('통과', c_args[i], c_args[i])
        c_args = c_args_tmp
        s_args = s_args_tmp

print(poly_form_compare(correct_sympy,student_sympy))



# 방정식 양변 정확히 비교
# A=BQ+R 꼴, y=a(x-p)**2+q 꼴 등

correct_answer = 'x**2-2x=0'
student_answer = 'x**2-2x=0'
correct_answer = 'x**3-3*x**2+4*x+1=(x+1)*(x**2-4*x+8)-7'
student_answer = 'x**3-3*x**2+4*x+1=(x+1)*(x**2-4*x+8)-7'
correct_answer = 'y=2*(x-1)**2+3'
student_answer = 'y=2*(x**2-2x+1)+3'
#correct_answer = 'x**3-3*x**2+4*x+1=(x**2-4*x+8)*(x+1)-7'
#student_answer = 'x**3-3*x**2+4*x+1=(x+1)*(x**2-4*x+8)-7'


c_split_str = correct_answer.split('=')
s_split_str = student_answer.split('=')

c_split_sympy = list(map(lambda str: P(str), c_split_str))
s_split_sympy = list(map(lambda str: P(str), s_split_str))
#print(c_split_sympy, s_split_sympy)
#print(c_split_sympy[1].args[0].args, s_split_sympy[1].args[0].args)
#print(c_split_sympy[1].args[0].args,type(c_split_sympy[1].args[0].args[1]))
#print(s_split_sympy[1].args[0].args,type(s_split_sympy[1].args[0].args[1]))
#print(c_split_sympy[1].args,c_split_sympy[1].is_Pow)
def equation_form_compare(c_split_sympy,s_split_sympy,form = 'non'):
    if equation_simple_compare(c_split_sympy,s_split_sympy,leading_coeff = 'fix') == 0: print('1');return False
    if all(simple_compare(c_split_sympy[i],s_split_sympy[i]) for i in range(2)) == 0: print('2');return False
    if all(len(c_split_sympy[i].args) == len(s_split_sympy[i].args) for i in range(2)) == 0: print('3');return False
    #A=BQ+R 꼴 | y=a(x-p)**2+q 꼴
    # BQ가 두 개의 다항식의 곱으로 되어 있는지 확인 | a(x-p)**2 args 비교
    if len(c_split_sympy[1].args[0].args) != len(s_split_sympy[1].args[0].args): print('4');return False
    # B,Q 단순 비교 | a, (x-p)**2 단순 비교
    if all(simple_compare(c_split_sympy[1].args[0].args[i], s_split_sympy[1].args[0].args[i]) for i in range(len(c_split_sympy[1].args[0].args))) == 0: print('5');return False
    # R 단순 비교 | q 단순 비교
    if simple_compare(c_split_sympy[1].args[1], s_split_sympy[1].args[1]) == 0: print('6');return False
    # (x-p)**2 전개된 형태 방지
    if form == '2_std': pass
    return True
#print(equation_form_compare(c_split_sympy,s_split_sympy,form = '2_std'))


# 숫자 값 비교
#분수 > 소수, 소수 > 분수 허용X, 반드시 유리화, 복소수 a+bi 형태만, 덧셈/곱셈 교환 가능
correct_answer = 'sqrt(2)*I'
student_answer = 'I*sqrt(2)'
#correct_answer = '-sqrt(6)*I/3'
#student_answer = 'sqrt(2)/sqrt(3)/I'
#correct_answer = 'I'
#student_answer = '1*I'
#correct_answer = '1/sqrt(2)'
#student_answer = 'sqrt(2)/2'
#correct_answer = '1+sqrt(2)'
#student_answer = 'sqrt(2)+1'
#correct_answer = 'sqrt(2)*I/sqrt(5)'
#student_answer = 'I*sqrt(10)/5'
#correct_answer = '1/3'
#student_answer = '0.[3]'
correct_sympy = P(correct_answer)
student_sympy = P(student_answer)
#a = sorted(list(correct_sympy.args), key=lambda x: x.as_real_imag())
#b = sorted(list(student_sympy.args), key=lambda x: x.as_real_imag())
#print(a,b)
#print(correct_sympy.args, student_sympy.args)
#print(type(student_sympy), type(correct_sympy))
def exact_number_compare(correct_sympy, student_sympy):
    if simple_compare(correct_sympy, student_sympy) == 0:
        print('1')
        return False
    if len(correct_sympy.args) != len(student_sympy.args):
        print('2')
        return False
    a = sorted(list(correct_sympy.args), key=lambda x: x.as_real_imag())
    b = sorted(list(student_sympy.args), key=lambda x: x.as_real_imag())
    if all(a[i].equals(b[i]) for i in range(len(correct_sympy.args))) == 0:
        print('3')
        return False
    return True
#print(exact_number_compare(correct_sympy, student_sympy))


# 숫자 리스트 비교
correct_answer = '5*I, -5*I, 3, sqrt(2)'
student_answer = '5*I, -5*I, 3, sqrt(2)'
correct_sympy = P('[' + correct_answer + ']')
student_sympy = P('[' + student_answer + ']')
def number_list_compare(correct_sympy, student_sympy,opt='simple',order='non-fix'):
    cnt = len(correct_sympy)
    if cnt != len(student_sympy):
        return False
    if order == 'non-fix':
        correct_sympy.sort(key = lambda x: x.as_real_imag())
        student_sympy.sort(key = lambda x: x.as_real_imag())
    if opt == 'simple':
        return all(simple_compare(correct_sympy[i], student_sympy[i]) for i in range(cnt))
    elif opt == 'exact':
        return all(exact_number_compare(correct_sympy[i], student_sympy[i]) for i in range(cnt))
#print(number_list_compare(correct_sympy, student_sympy,opt='exact',order='non-fix'))

# 순서쌍 1개 비교
# simple만 필요할 것이라 가정
correct_answer = '(1,3*I)'
student_answer = '(1,-3/I)'
correct_sympy = P(correct_answer)
student_sympy = P(student_answer)
#print(correct_sympy, student_sympy)
def pair_compare(correct_sympy, student_sympy):
    cnt = len(correct_sympy)
    if cnt != len(student_sympy):
        return False
    return all(simple_compare(correct_sympy[i], student_sympy[i]) for i in range(cnt))
#print(pair_compare(correct_sympy, student_sympy))

# 순서쌍 리스트 비교
# simple만 필요할 것이라 가정
correct_answer = '(1,1,I),(1,-2,1),(1,1,2)'
student_answer = '(1,1,I),(1,-2,1),(1,1,2)'
correct_sympy = P('[' + correct_answer + ']')
student_sympy = P('[' + student_answer + ']')
#print(correct_sympy, student_sympy)
def pair_list_compare(correct_sympy, student_sympy,order='non-fix'):
    cnt = len(correct_sympy)
    if cnt != len(student_sympy):
        return False
    if order == 'non-fix':
        correct_sympy.sort(key = lambda p: tuple(map(lambda t: t.as_real_imag(),p)))
        student_sympy.sort(key = lambda p: tuple(map(lambda t: t.as_real_imag(),p)))
    return all(pair_compare(correct_sympy[i], student_sympy[i]) for i in range(cnt))
#print(pair_list_compare(correct_sympy, student_sympy,order='non-fix'))