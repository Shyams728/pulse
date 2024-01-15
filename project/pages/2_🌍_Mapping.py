import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
import streamlit_shadcn_ui as ui
import extra_streamlit_components as stx
# Set Streamlit page configuration
st.set_page_config(
    layout="wide",
    initial_sidebar_state='collapsed',
    page_icon = ":globe:",
)

#***************************************Data Access*******************************
# Create a function to load data from the SQLite database
def load_data_from_db(query):
    sqlite_file = 'project/test.sqlite'
    engine = create_engine(f'sqlite:///{sqlite_file}')
    df = pd.read_sql(query, engine)
    return df


def select_the_table(selected_tab):
    # Execute different queries based on the chosen tab
    if selected_tab == 'Transaction Country Data':
        query = 'SELECT * FROM map_transaction_hover_counry;'
    elif selected_tab == 'Transaction State Data':
        query = 'SELECT * FROM map_transaction_hover_state;'
    elif selected_tab == 'Insurance Country Data':
        query = 'SELECT * FROM map_insurence_hover_counry;'
    elif selected_tab == 'Insurance State Data':
        query = 'SELECT * FROM map_insurence_hover_state;'
    elif selected_tab == 'User Country Data':
        query = 'SELECT * FROM map_user_hover_contry;'
    elif selected_tab == 'User State Data':
        query = 'SELECT * FROM map_user_hover_state;'
    return query


def plot_map_chart(data):
    fig= px.choropleth(
    data,
    geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
    featureidkey='properties.ST_NM',
    locations='state',
    hover_name="state",
    hover_data=["state",
            'total_transactions_amount',
            'total_transactions_count',
            'year',
            'quarter'],
    color='state',
    color_continuous_scale='orRd'
    )
    fig.update_geos(fitbounds="locations") # To show-up the Indian boundaries
    st.plotly_chart(fig)


#***************************************Data Exploration*******************************
first_box = st.container(border=True)
col1, col2 = first_box.columns([7,1])

with col1:
    # Create tabs
    selected_tab = ui.tabs(options=['Transaction Country Data', 'Transaction State Data', 'Insurance Country Data', 'Insurance State Data', 'User Country Data', 'User State Data'], default_value= 'User State Data', key="two_birds")
with col2:
    filter_data = st.toggle('filter data')

choosen_table = select_the_table(selected_tab)
df = load_data_from_db(choosen_table)
filtered_df = None

container = st.container(border=True)

if filter_data:
    # Create columns
    col3, col4,col5,col6 = container.columns(4)

    # Sidebar input widgets
    selected_years = col3.multiselect('Select Year:', sorted(df['year'].unique()),default=2022,help='Select the Year')
    selected_quarters = col4.multiselect('Select Quarter:', sorted(df['quarter'].unique()),default=[1,2,3,4])
    selected_state = col5.multiselect('Select State/UT:', sorted(df['state'].unique()),default = ['karnataka'])
    # entity_type = col6.selectbox('Select Entity Type:', sorted(df['entity_type'].unique()))

    # Filter the DataFrame based on user inputs
    filtered_df = df[(df['state'].isin(selected_state)) & (df['year'].isin(selected_years)) & (df['quarter'].isin(selected_quarters))]
else:
    # If 'filter data' is not selected
    filtered_df = df

# Create main container
main_box = st.container(border=True)

# Create columns
col2, col3 = main_box.columns([3, 2])


# Access data from container1 in col2
with col2:
    # Display the filtered DataFrame
    st.write(f"Displaying Chart for {selected_tab} table:")
    

    # Display the filtered DataFrame
    # st.dataframe(df, height=480, use_container_width=True)
    plot_map_chart(filtered_df)



with col3:

    st.write(f"Displaying data from {selected_tab} table:")
    ui.table(data=filtered_df.head(), maxHeight=500,key="filtered_data_table")
    # Display the filtered DataFrame




# ----------------------------------Geo map visualization---------------------------------------------------------------




































# # Get the list of table names
# table_names = [
#     'aggregated_user_counry',
#     'map_transaction_hover_state',
#     'top_transaction_country',
#     'top_insurence_state',
#     'aggregated_transaction_state',
#     'map_user_hover_contry',
#     'map_insurence_hover_counry',
#     'aggregated_user_state',
#     'map_user_hover_state',
#     'map_transaction_hover_counry',
#     'top_insurence_country',
#     'aggregated_insurence_state',
#     'aggregated_transaction_country',
#     'top_user_country',
#     'top_user_state',
#     'map_insurence_hover_state',
#     'aggregated_insurence_country',
#     'top_transaction_state'
# ]

# # Function to fetch data from a selected table
# def fetch_data(selected_table):
#     query = f'SELECT * FROM {selected_table};'
#     df = pd.read_sql(query, engine)
#     return df

# # Streamlit app
# st.title("SQL Table Visualization")


# st.header("Plotly Charts")

# # Create dropdown for selecting a table
# selected_table = st.selectbox("Select a table:", table_names)

# # Fetch data based on the selected table
# selected_data = fetch_data(selected_table)

# # Display the selected data
# st.write(f"Displaying data from {selected_table} table:")
# ui.table(data=selected_data.head(), maxHeight=300)
# # st.dataframe(selected_data)

# # Manipulate data based on columns
# if not selected_data.empty:
#     st.header("Data Manipulation")
    
#     # Show columns
#     st.write("Columns:", selected_data.columns.tolist())

#     # Filter data based on a column
#     selected_column = st.selectbox("Select a column to filter:", selected_data.columns)
#     filter_value = st.text_input(f"Enter value to filter in {selected_column} column:")
#     filtered_data = selected_data[selected_data[selected_column] == filter_value]
#     st.write(f"Filtered Data based on {selected_column} column:")
#     st.dataframe(filtered_data)

#     # Sort data based on a column
#     sort_column = st.selectbox("Select a column to sort:", selected_data.columns)
#     ascending_order = st.checkbox("Sort in ascending order")
#     sorted_data = selected_data.sort_values(by=sort_column, ascending=ascending_order)
#     st.write(f"Sorted Data based on {sort_column} column:")
#     st.dataframe(sorted_data)

#     # Line chart
#     x_line = st.selectbox("Select X-axis for Line Chart:", selected_data.columns)
#     y_line = st.selectbox("Select Y-axis for Line Chart:", selected_data.columns)
#     line_chart = px.line(selected_data, x=x_line, y=y_line)
#     st.plotly_chart(line_chart)

#     # Bar chart
#     x_bar = st.selectbox("Select X-axis for Bar Chart:", selected_data.columns)
#     y_bar = st.selectbox("Select Y-axis for Bar Chart:", selected_data.columns)
#     bar_chart = px.bar(selected_data, x=x_bar, y=y_bar)
#     st.plotly_chart(bar_chart)

#     # Scatter plot
#     x_scatter = st.selectbox("Select X-axis for Scatter Plot:", selected_data.columns)
#     y_scatter = st.selectbox("Select Y-axis for Scatter Plot:", selected_data.columns)
#     scatter_plot = px.scatter(selected_data, x=x_scatter, y=y_scatter)
#     st.plotly_chart(scatter_plot)


#     st.header("Table View")
#     # Add your table-related code here
#     st.selectbox("Select", [1, 2, 3])
#     st.text('Sample metric data')
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Temperature", "70 °F", "1.2 °F")
#     col2.metric("Wind", "9 mph", "-8%")
#     col3.metric("Humidity", "86%", "4%")

#     options = st.multiselect(
#         'What are your favorite colors',
#         ['Green', 'Yellow', 'Red', 'Blue'],
#         ['Yellow', 'Red']
#     )
#     st.write('You selected:', options)

#     st.subheader('Expander')
#     st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})
#     expander = st.expander("See explanation")
#     expander.write('''
#         The chart above shows some numbers I picked for you.
#         I rolled actual dice for these, so they're *guaranteed* to
#         be random.
#     ''')
#     expander.image("https://static.streamlit.io/examples/dice.jpg")

#     st.subheader("Container")
#     container = st.container(border=True)
#     container.write("This is inside the container")
#     container.header('Container check')
#     container.write('Container check')
#     st.write("This is outside the container")
#     container.write("This is inside too")

#     st.subheader("Metric Card")
#     cols = st.columns(3)
#     with cols[0]:
#         ui.metric_card(title="Total Revenue", content="$45,231.89", description="+20.1% from last month", key="card1")
#     with cols[1]:
#         ui.metric_card(title="Total Revenue", content="$45,231.89", description="+20.1% from last month", key="card2")
#     with cols[2]:
#         ui.metric_card(title="Total Revenue", content="$45,231.89", description="+20.1% from last month", key="card3")

#     st.subheader("Tab Bar")
#     chosen_id = stx.tab_bar(data=[
#         stx.TabBarItemData(id=1, title="ToDo", description="Tasks to take care of"),
#         stx.TabBarItemData(id=2, title="Done", description="Tasks taken care of"),
#         stx.TabBarItemData(id=3, title="Overdue", description="Tasks missed out"),
#     ], default=1)
#     st.info(f"{chosen_id=}")
#     if chosen_id == 1:
#         st.write("Tasks to take care of")
#     if chosen_id == 2:
#         st
        

#     st.subheader("Chart Container")
#     chart_container = st.container()
#     # Add your chart-related code here
#     chart_container.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

# st.subheader("Dashboard Footer")
# # Add any additional components or information at the end of the dashboard
