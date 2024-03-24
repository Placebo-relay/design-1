import streamlit as st
import numpy as np
import pandas as pd
from sympy import sympify, symbols, pi, exp, integrate, SympifyError

def midpoint_rectangle_integration(f, a, b, n):
    # Calculate the width of each subinterval
    dx = (b - a) / n
    # Calculate the midpoint of each subinterval
    x_midpoints = np.linspace(a + 0.5*dx, b - 0.5*dx, n)
    # Evaluate the function at the midpoints and sum the areas of the rectangles
    return dx * np.sum(f(x_midpoints))

def simpsons_rule_integration(f, a, b, n):
    # Calculate the width of each subinterval
    dx = (b - a) / n
    # Generate the x values at the endpoints and midpoints of the subintervals
    x = np.linspace(a, b, n+1)
    # Calculate the weights for the Simpson's rule
    w = np.full(n+1, 1)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    w *= dx / 3
    # Evaluate the function at the x values and calculate the integral using Simpson's rule
    return np.sum(w * f(x))

def main():
    st.title('Integral Calculator')

    # Input box for the user-defined function
    user_input = st.text_input('Enter the function (use x, exp and pi):', 'x**2')

    try:
        user_function = sympify(user_input, locals={"pi": pi, "exp": exp})
        st.write("Parsed function:", user_function)
    except SympifyError as e:
        st.write("Invalid input for function:", e)
        return  # Exit the function if there's an error

    # Input boxes for lower and upper bounds
    x = symbols('x')
    pi_symbol = symbols('pi')
    exp_symbol = symbols('exp')
    
    lower_bound_str = st.text_input('Enter the lower bound:', '0')
    upper_bound_str = st.text_input('Enter the upper bound:', '2*pi')

    try:
        lower_bound_text = sympify(lower_bound_str, locals={"pi": pi, "exp": exp})
        upper_bound_text = sympify(upper_bound_str, locals={"pi": pi, "exp": exp})
        st.write("Parsed lower bound:", lower_bound_text)
        st.write("Parsed upper bound:", upper_bound_text)
    except SympifyError as e:
        st.write("Invalid input in bound section:", e)
        return  # Exit the function if there's an error

    # Calculate the integral using different methods
    n = 100  # Number of subintervals for midpoint rectangle and Simpson's rule

    # Perform definite integration
    definite_result = integrate(user_function, (x, lower_bound_text, upper_bound_text))

    # Perform midpoint rectangle method integration
    if user_function == x:
        midpoint_result = 0.5 * (upper_bound_text**2 - lower_bound_text**2)  # Area under y=x is (1/2)*(b^2 - a^2)
    else:
        midpoint_result = midpoint_rectangle_integration(lambda x: user_function, float(lower_bound_text), float(upper_bound_text), n)

    # Perform Simpson's rule integration
    simpson_result = simpsons_rule_integration(lambda x: user_function, float(lower_bound_text), float(upper_bound_text), n)

    # Display the results in a dataframe
    results_df = pd.DataFrame({
        'Method': ['Definite', 'Midpoint Rectangle', 'Simpson\'s Rule'],
        'Result': [definite_result, midpoint_result, simpson_result]
    })
    st.write(results_df)

if __name__ == '__main__':
    main()
