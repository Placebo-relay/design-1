import streamlit as st
import numpy as np
import sympy as sp

def main():
    st.title('Integral Calculator')

    # Input box for the user-defined function
    function_str = st.text_input('Enter the function (use x as the variable):', 'x**2')

    # Input boxes for lower and upper bounds
    lower_bound_str = st.text_input('Enter the lower bound:', '0')
    upper_bound_str = st.text_input('Enter the upper bound:', '1')

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
    x = np.linspace(a, b, n+1)
    y = [f.subs('x', xi) for xi in x]
    h = (b - a) / n
    result = (h / 3) * (y[0] + 4 * sum(y[i] for i in range(1, n, 2)) + 2 * sum(y[i] for i in range(2, n-1, 2)) + y[n])
    return result
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
        x = sp.symbols('x')
        function = sp.sympify(function_str)

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

    except (sp.SympifyError, ValueError) as e:
        st.write('Error: Invalid input. Please enter a valid function and bounds.')

def simpsons_method(f, a, b, n=100):
    try:
        x = np.linspace(a, b, n+1)
        y = f.subs('x', x)
        h = (b - a) / n
        result = (h / 3) * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
        return result
    except (sp.SympifyError, ValueError) as e:
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
  
