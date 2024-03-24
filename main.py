import streamlit as st
import numpy as np
from sympy import sympify, symbols, pi, exp, integrate, SympifyError
from scipy.integrate import simps

def main():
    st.title('Integral Calculator')

    # Input box for the user-defined function
    user_input = st.text_input('Enter the function (use x, exp and pi):', 'x**2')

    try:
        user_function = sympify(user_input, locals={"pi": pi, "exp": exp})
        st.write("Parsed function:", user_function)
    except Exception as e:
        st.write("Invalid input:", e)

    # Input boxes for lower and upper bounds
    x = symbols('x')
    pi_symbol = symbols('pi')
    exp_symbol = symbols('exp')
    
    lower_bound_str = st.text_input('Enter the lower bound:', '0')
    upper_bound_str = st.text_input('Enter the upper bound:', '2*pi')

    try:
        lower_bound_text = sympify(lower_bound_str, locals={"pi": pi, "exp": exp})
        upper_bound_text = sympify(upper_bound_str, locals={"pi": pi, "exp": exp})
        col1, col2 = st.columns(2)
        with col1: st.write("Parsed lower bound:", lower_bound_text)
        with col2: st.write("Parsed upper bound:", upper_bound_text)
    except Exception as e:
        st.write("Invalid input in bound section:", e)

    x_values = np.linspace(float(lower_bound_text), float(upper_bound_text), 1000)
    y_values = [user_function.subs('x', val) for val in x_values]
    result = simps(y_values, x_values)

    st.write("Result of integration using Simpson's method:", result)

if __name__ == '__main__':
    main()
