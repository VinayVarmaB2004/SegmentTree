import streamlit as st
import pandas as pd

# Streamlit Page Configuration
st.set_page_config(page_title="Segment Tree", layout="centered")

# Initialize session state for array
if "array" not in st.session_state:
    st.session_state.array = []
    st.session_state.updated_array = []
if "update_checked" not in st.session_state:
    st.session_state.update_checked = False  # Ensure it exists

st.title("Range Queries Computator")

# Input for array size
array_size = st.number_input("Enter the size of the array:", min_value=1, step=1, key="array_size")

# Input for array elements
array_input = st.text_area("Enter initial elements of the array (comma-separated):", placeholder="e.g., 1,2,3,4,5")

# Parse input array
if st.button("Submit Array"):
    elements = array_input.split(',')
    if len(elements) == array_size:
        st.session_state.array = [int(x.strip()) for x in elements]
        st.session_state.updated_array = st.session_state.array.copy()
        st.rerun()  # Refresh UI after array is set
    else:
        st.error(f"Please enter exactly {array_size} values.")

# Ensure operations and updates only show after array is initialized
if st.session_state.updated_array:
    # Display operations section
    st.subheader("Operations")
    operation = st.selectbox("Select operation:", ["Min", "Max", "Sum", "Product"])

    # Range Query Input (only if array is initialized)
    L = st.number_input("Enter Left Index (L):", min_value=0, max_value=len(st.session_state.updated_array)-1, step=1, key="L")
    R = st.number_input("Enter Right Index (R):", min_value=L, max_value=len(st.session_state.updated_array)-1, step=1, key="R")

    if st.button("Perform Operation"):
        sub_array = st.session_state.updated_array[L:R+1]
        result = 0
        if operation == "Min":
            result = min(sub_array)
        elif operation == "Max":
            result = max(sub_array)
        elif operation == "Sum":
            result = sum(sub_array)
        elif operation == "Product":
            result = 1
            for num in sub_array:
                result *= num
        
        st.success(f"{operation} in range [{L}, {R}] is: {result}")

    # Update section
    st.subheader("Update Array Values")
    update_checked = st.checkbox("Want to update an element?", key="update_checked")

    if update_checked:
        update_index = st.number_input("Enter index to update:", min_value=0, max_value=len(st.session_state.updated_array)-1, step=1)
        new_value = st.number_input("Enter new value:", step=1)

        if st.button("Update Value"):
            st.session_state.updated_array[update_index] = new_value
            st.rerun()  # Refresh UI after update

    # Display array in table format (with yellow background)
    data = {"Index": list(range(len(st.session_state.updated_array))), "Value": st.session_state.updated_array}
    df = pd.DataFrame(data)

    # Apply styling for yellow background
    def highlight_cells(val):
        return "background-color: #FFFACD; border: 2px solid black; text-align: center"

    styled_df = df.style.applymap(highlight_cells)

    st.dataframe(styled_df)  # Now updates instantly!
