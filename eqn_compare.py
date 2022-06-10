# 방정식 단순 비교
def equation_simple_compare(c_split_sympy,s_split_sympy,leading_coeff = 'non-fix'):
    c_poly = c_split_sympy[0]-c_split_sympy[1]
    s_poly = s_split_sympy[0]-s_split_sympy[1]
    c_eq = Eq(c_poly,0)
    s_eq = Eq(s_poly,0)
    if leading_coeff == 'non-fix':
        c_poly = factor(c_poly).as_coeff_Mul()[1]
        s_poly = factor(s_poly).as_coeff_Mul()[1]
    elif any(LT(s_split_sympy[i]).equals(LT(s_poly)) == 0 for i in range(2) if s_split_sympy[i].is_number == 0) == 0: return False
    return Or(sympy_equals(c_eq, s_eq),sympy_compare(c_eq, s_eq.reversedsign))