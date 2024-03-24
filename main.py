import streamlit as st
import numpy as np
from sympy import sympify, symbols, pi, exp, SympifyError

def main():
    st.title('Integral Calculator')

    # Input box for the user-defined function
    user_input = st.text_input('Enter the function (use x as the variable):', 'x**2')

    try:
        function_str = sympify(user_input, locals={"pi": pi, "exp": exp})
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
        lower_bound = sympify(lower_bound_str, locals={"pi": pi, "exp": exp})
        upper_bound = sympify(upper_bound_str, locals={"pi": pi, "exp": exp})
        st.write("Parsed lower bound:", lower_bound)
        st.write("Parsed upper bound:", upper_bound)
    except Exception as e:
        st.write("Invalid input:", e)

    # Method selection
    method = st.selectbox('Select the method for integral calculation:', ['Simpson\'s Method', 'Mid-Rectangle Method'])

    if st.button('Calculate Integral'):
        # Call the function to calculate the integral
        calculate_integral(function_str, lower_bound_str, upper_bound_str, method)
                # Showcase the code snippets for the selected method
        if method == 'Simpson\'s Method':
            st.subheader('Code Snippet for Simpson\'s Method')
            st.code("""
def simpsons_method(f, a, b, n=100):
    try:
        x = np.linspace(a, b, n+1)
        y = [f.subs('x', xi) for xi in x]  # Evaluate the function at each x value
        h = (b - a) / n
        result = (h / 3) * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
        return result
    except (SympifyError, ValueError) as e:
        st.write(f'Error: Invalid input. Please enter a valid function and bounds. Details: {e}')
            """)

        elif method == 'Mid-Rectangle Method':
            st.subheader('Code Snippet for Mid-Rectangle Method')
            st.code("""
def mid_rectangle_method(f, a, b, n=100):
    h = (b - a) / n
    result = sum(f.subs('x', a + (i + 0.5) * h) for i in range(n)) * h
    return result
            """)


def calculate_integral(function_str, lower_bound_str, upper_bound_str, method):
    try:
        # Parse the user-defined function using SymPy
        x = symbols('x')
        function = sympify(function_str)

        # Convert the bounds to numerical values
        lower_bound = float(lower_bound_str)
        upper_bound = float(upper_bound_str)

        # Perform integral calculation based on the selected method
        if method == 'Simpson\'s Method':
            result = simpsons_method(function, lower_bound, upper_bound)
        elif method == 'Mid-Rectangle Method':
            result = mid_rectangle_method(function, lower_bound, upper_bound)

        # Display the result to the user
        st.write(f'The result of the integral using {method} is: {result}')

    except (SympifyError, ValueError) as e:
        st.write('Error: Invalid input. Please enter a valid function and bounds.')

def simpsons_method(f, a, b, n=100):
    try:
        x = np.linspace(a, b, n+1)
        y = [f.subs('x', xi) for xi in x]  # Evaluate the function at each x value
        h = (b - a) / n
        result = (h / 3) * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
        return result
    except (SympifyError, ValueError) as e:
        st.write(f'Error: Invalid input. Please enter a valid function and bounds. Details: {e}')

def mid_rectangle_method(f, a, b, n=100):
    h = (b - a) / n
    result = 0
    for i in range(n):
        result += f.subs('x', a + (i + 0.5) * h)
    result *= h
    return result

if __name__ == '__main__':
    main()
  
