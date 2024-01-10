import streamlit as st
main_box = st.container(border=True)


# Create columns
col1, col2 = main_box.columns(2)

# Create containers within each column
with col1:
    container1 = st.container(border=True)
    with container1:
        data_col1 = "Data in Column 1"

# Access data from container1 in col2
with col2:
    container2 = st.container(border=True)
    with container2:
        st.write("Data from Column 1:", data_col1)
