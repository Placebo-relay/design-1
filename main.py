import streamlit as st
import numpy as np
from sympy import sympify, symbols, pi, exp, integrate, SympifyError
from scipy.integrate import simpson
import pandas as pd

def custom_midpoint_integration(func, a, b, n):
    """
    Custom midpoint integration function to approximate the definite integral of a function.

    Parameters:
    func (function): The function to be integrated.
    a (float): The lower bound of the interval.
    b (float): The upper bound of the interval.
    n (int): The number of subintervals.

    Returns:
    float: The approximate value of the definite integral.
    """
    h = (b - a) / n  # Width of each subinterval
    result = 0
    x = symbols('x')  # Define the symbol for the variable
    for i in range(n):
        midpoint = a + (i + 0.5) * h  # Midpoint of the subinterval
        result += func.subs(x, midpoint)  # Evaluate the function at the midpoint using sympy
    result *= h  # Multiply by the width of the subintervals
    return result

def main():
    hide_menu = """
    <style>
    header {
        visibility: hidden;
    }
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    footer:after{
        visibility: visible;
        Content:"Demo for ikt_PRO. Copyright @ 2023";
        display: block;
        position: relative;
        padding: 5px;
        top:3px;
        color: tomato;
        text-align: left;
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)
    st.title('Integral Calculator')

    # Input box for the user-defined function
    st.sidebar.write('Use exp() and pi in Function and Bounds')
    st.sidebar.info('Example: exp(3)*(x**6+x**5)**0.2')
    user_input = st.sidebar.text_input('Enter the function (use x, exp and pi):', 'x**2')
    if st.sidebar.checkbox('Apply Example function'):
        user_input = 'exp(3)*(x**6+x**5)**0.2'

    try:
        user_function = sympify(user_input, locals={"pi": pi, "exp": exp})
        col01, col02 = st.columns(2)
        with col01: st.write("Parsed function:", user_function)
    except Exception as e:
        st.write("Invalid input:", e)

    # Input boxes for lower and upper bounds
    st.sidebar.info(f'Bounds example: exp(3) * 0.5 * pi + 2')
    x = symbols('x')
    pi_symbol = symbols('pi')
    exp_symbol = symbols('exp')
    
    lower_bound_str = st.sidebar.text_input('Enter the lower bound:', '0')
    upper_bound_str = st.sidebar.text_input('Enter the upper bound:', '2*pi')

    try:
        lower_bound_text = sympify(lower_bound_str, locals={"pi": pi, "exp": exp})
        upper_bound_text = sympify(upper_bound_str, locals={"pi": pi, "exp": exp})
        col1, col2 = st.columns(2)
        with col1: st.write("Parsed lower bound:", lower_bound_text)
        with col2: st.write("Parsed upper bound:", upper_bound_text)
    except Exception as e:
        st.write("Invalid input in bound section:", e)

    num_subintervals = st.sidebar.slider('Number of Subintervals', min_value=100, max_value=1000, value=500, step = 100)
    x_values = np.linspace(float(lower_bound_text), float(upper_bound_text), num_subintervals)
    y_values = [user_function.subs('x', val) for val in x_values]
    
    simpson_result = simpson(y_values, x_values)
    mid_rectangle_result = custom_midpoint_integration(user_function, float(lower_bound_text), float(upper_bound_text), num_subintervals)
    sympy_result = integrate(user_function, (x, float(lower_bound_text), float(upper_bound_text))).evalf()
    
    data = {
        'Method': ['Sympy', 'Simpson', 'Mid-Rectangle'],
        'Result': [sympy_result.evalf(), simpson_result.evalf(), mid_rectangle_result.evalf()]
    }
    df = pd.DataFrame(data)
    df['% Difference'] = 100 * abs(df['Result'] - sympy_result.evalf()) / sympy_result.evalf()
    #df['% Difference'] = df['% Difference']
    #df['Result'] = df['Result'].apply(lambda x: format(x, '.15f'))
    #df['% Difference'] = df['% Difference'].apply(lambda x: format(x, '.15f')) 
    st.write("Integration Results:")
    st.dataframe(df, hide_index=True)

if __name__ == '__main__':
    main()
