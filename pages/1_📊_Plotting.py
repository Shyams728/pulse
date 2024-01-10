import extra_streamlit_components as stx
import streamlit as st
import streamlit_shadcn_ui as ui
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📈 Tables")

# Define the SQLite database file path
sqlite_file = 'test.sqlite'

# Create a SQLAlchemy engine and connect to the SQLite database
engine = create_engine(f'sqlite:///{sqlite_file}')

# Get the list of table names
table_names = [
    'aggregated_user_counry',
    'map_transaction_hover_state',
    'top_transaction_country',
    'top_insurence_state',
    'aggregated_transaction_state',
    'map_user_hover_contry',
    'map_insurence_hover_counry',
    'aggregated_user_state',
    'map_user_hover_state',
    'map_transaction_hover_counry',
    'top_insurence_country',
    'aggregated_insurence_state',
    'aggregated_transaction_country',
    'top_user_country',
    'top_user_state',
    'map_insurence_hover_state',
    'aggregated_insurence_country',
    'top_transaction_state'
]

# Function to fetch data from a selected table
def fetch_data(selected_table):
    query = f'SELECT * FROM {selected_table};'
    df = pd.read_sql(query, engine)
    return df

# Streamlit app
st.title("SQL Table Visualization")

# Create tabs
selected_tab = ui.tabs(options=['sql', 'Visualisation', 'DataFrame', 'Live'], default_value='Visualisation', key="kanaries")

# Check the selected tab and perform actions
if selected_tab == 'sql':
    st.text('Hi SQL')
elif selected_tab == 'Visualisation':
    st.text('Hi Visualisation')
    
# Create dropdown for selecting a table
selected_table = st.selectbox("Select a table:", table_names)

# Fetch data based on the selected table
selected_data = fetch_data(selected_table)

# Display the selected data
st.write(f"Displaying data from {selected_table} table:")
st.dataframe(selected_data)


# Manipulate data based on columns
if not selected_data.empty:
    st.header("Data Manipulation")
    
    # Show columns
    st.write("Columns:", selected_data.columns.tolist())

    # Filter data based on a column
    selected_column = st.selectbox("Select a column to filter:", selected_data.columns)
    filter_value = st.text_input(f"Enter value to filter in {selected_column} column:")
    filtered_data = selected_data[selected_data[selected_column] == filter_value]
    st.write(f"Filtered Data based on {selected_column} column:")
    st.dataframe(filtered_data)

    # Sort data based on a column
    sort_column = st.selectbox("Select a column to sort:", selected_data.columns)
    ascending_order = st.checkbox("Sort in ascending order")
    sorted_data = selected_data.sort_values(by=sort_column, ascending=ascending_order)
    st.write(f"Sorted Data based on {sort_column} column:")
    st.dataframe(sorted_data)




# Create Plotly charts
st.header("Plotly Charts")

# Additional visualization (you can customize this based on your needs)
st.write(f"Visualization for {selected_table}:")

# Line chart
x_line = st.selectbox("Select X-axis for Line Chart:", selected_data.columns)
y_line = st.selectbox("Select Y-axis for Line Chart:", selected_data.columns)
line_chart = px.line(selected_data, x=x_line, y=y_line)
st.plotly_chart(line_chart)

# Bar chart
x_bar = st.selectbox("Select X-axis for Bar Chart:", selected_data.columns)
y_bar = st.selectbox("Select Y-axis for Bar Chart:", selected_data.columns)
bar_chart = px.bar(selected_data, x=x_bar, y=y_bar)
st.plotly_chart(bar_chart)

# Scatter plot
x_scatter = st.selectbox("Select X-axis for Scatter Plot:", selected_data.columns)
y_scatter = st.selectbox("Select Y-axis for Scatter Plot:", selected_data.columns)
scatter_plot = px.scatter(selected_data, x=x_scatter, y=y_scatter)
st.plotly_chart(scatter_plot)
# Add your visualization code here based on the selected_data DataFrame

# Save the streamlit app as a .py file and run it using: streamlit run your_app.py



a,b = st.tabs( ["Chart", "Table"])
with a:
    st.subheader("Chart")
with b:
    st.subheader("Table")
    st.selectbox("Select", [1, 2, 3])

    if 1:
        st.text('sample metric data')
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", "70 °F", "1.2 °F")
        col2.metric("Wind", "9 mph", "-8%")
        col3.metric("Humidity", "86%", "4%")
    if 2:
        options = st.multiselect(
            'What are your favorite colors',
            ['Green', 'Yellow', 'Red', 'Blue'],
            ['Yellow', 'Red'])

        st.write('You selected:', options)


st.subheader('expander')

st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

expander = st.expander("See explanation")
expander.write('''
    The chart above shows some numbers I picked for you.
    I rolled actual dice for these, so they're *guaranteed* to
    be random.
''')
expander.image("https://static.streamlit.io/examples/dice.jpg")


st.subheader("Container")

container = st.container(border=True)
container.write("This is inside the container")
container.header('container check')
container.write('container check')
st.write("This is outside the container")

# Now insert some more in the container
container.write("This is inside too")


st.subheader("Metric Card")

cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="Total Revenue", content="$45,231.89", description="+20.1% from last month", key="card1")
with cols[1]:
    ui.metric_card(title="Total Revenue", content="$45,231.89", description="+20.1% from last month", key="card2")
with cols[2]:
    ui.metric_card(title="Total Revenue", content="$45,231.89", description="+20.1% from last month", key="card3")

st.subheader("Tab Bar")

chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="ToDo", description="Tasks to take care of"),
    stx.TabBarItemData(id=2, title="Done", description="Tasks taken care of"),
    stx.TabBarItemData(id=3, title="Overdue", description="Tasks missed out"),
], default=1)
st.info(f"{chosen_id=}")


