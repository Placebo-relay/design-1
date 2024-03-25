import streamlit as st
import numpy as np
from sympy import sympify, symbols, pi, exp, integrate, SympifyError, latex, Integral, sin, cos, tan, atan2, cot, acos, asin, atan, I, Pow
from scipy.integrate import simpson
from sympy.printing.preview import preview
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
        visibility: visible;
    }
    footer:after{
        visibility: visible;
        Content:"Demo for design_practice. Copyright @ 2024";
        display: block;
        position: relative;
        padding: 5px;
        top:3px;
        color: tomato;
        text-align: left;
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)
    st.title('Integral Calculator 🧮')
    st.markdown("### > 👈 sidebar: 📄⚙️")

    st.sidebar.title('Integral config.💡Use it:')
    st.sidebar.success('exp(), pi, sin, cos, tan, I, Pow')
    # Input box for the user-defined function
    st.sidebar.write('## 📈Function')
    st.sidebar.info(f'Example fn: exp(3) * (x **6 + x **5)**0.2')
    user_input = st.sidebar.text_input('Enter the function, use x:', 'x**2')
    if st.sidebar.checkbox('Apply Example fn instead'):
        user_input = 'exp(3)*(x**6+x**5)**0.2'

    try:
        user_function = sympify(user_input, locals={"pi": pi, "exp": exp})
        # Solve the indefinite integral
        ind_integral = integrate(function, symbols('x'))
        st.latex(f"The indefinite integral of ${latex(user_function)}$ is ${latex(ind_integral)} + C$")



    except Exception as e:
        st.write("Invalid input in 📈, please 1) use example, 2) try multiply x, x**2+x is better than x*(x+1)", e)

    # Input boxes for lower and upper bounds
    st.sidebar.info(f'Bounds example: exp(3) * 0.5 * pi + 2')
    x = symbols('x')
    pi_symbol = symbols('pi')
    exp_symbol = symbols('exp')

    st.sidebar.write('## ⬇️⬆️Bounds')
    lower_bound_str = st.sidebar.text_input('⬇️Enter the lower bound:', '0')
    upper_bound_str = st.sidebar.text_input('⬆️Enter the upper bound:', '2*pi')

    try:
        lower_bound_text = sympify(lower_bound_str, locals={"pi": pi, "exp": exp})
        upper_bound_text = sympify(upper_bound_str, locals={"pi": pi, "exp": exp})
        integral_latex = latex(Integral(user_function, (x, lower_bound_text, upper_bound_text)))
        st.sidebar.latex(integral_latex)
        #st.sidebar.write("Parsed lower bound:", lower_bound_text)
        #st.sidebar.write("Parsed upper bound:", upper_bound_text)
    except Exception as e:
        st.sidebar.error("Invalid input in ⬇️⬆️. Use any: pi, 3*pi/4, cos(pi/3).")
        st.sidebar.success('Allowed: exp(), pi, sin, cos, tan, I, Pow')

    col1, _ = st.columns(2)
    
    sympy_result = integrate(user_function, (x, (lower_bound_text), (upper_bound_text)))
    #sympy_result_evalf = sympy_result.evalf()
    result_latex = latex(sympy_result)
    result_latex_evalf = latex(sympy_result.evalf())
    st.latex(f"{integral_latex} = {result_latex} = {result_latex_evalf}")

    if not st.sidebar.checkbox('get Complex/symbolic bounds'):
        num_subintervals = st.sidebar.slider('Number of Subintervals', min_value=100, max_value=1000, value=500, step = 100)
        #with col1: st.latex(integral_latex)
        x_values = np.linspace(float(lower_bound_text), float(upper_bound_text), num_subintervals)
        y_values = [user_function.subs('x', val) for val in x_values]
        simpson_result = simpson(y_values, x_values)
        mid_rectangle_result = custom_midpoint_integration(user_function, float(lower_bound_text), float(upper_bound_text), num_subintervals)
        #sympy_result = integrate(user_function, (x, float(lower_bound_text), float(upper_bound_text)))
  
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

    else:
        st.sidebar.info('Type Complex as I or 3*I+9, use symbols like t m or n to solve without numbers')

if __name__ == '__main__':
    main()
