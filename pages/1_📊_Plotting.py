import extra_streamlit_components as stx
import streamlit as st
import streamlit_shadcn_ui as ui
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    initial_sidebar_state='collapsed',
    page_title="📈 Tables",
    page_icon= ':chart:'  
)

st.title("📈 Tables")

# ***************************************Data Access*******************************

# Create a function to load data from the SQLite database
def load_data_from_db(query):
    sqlite_file = 'test.sqlite'
    # Use a context manager to ensure proper resource management
    with create_engine(f'sqlite:///{sqlite_file}').connect() as engine:
        df = pd.read_sql(query, engine)
    return df

def select_the_table(selected_tab):
    # Execute different queries based on the chosen tab
    tables = {
        'Transaction Data': 'agregated_transaction_country',
        'Transaction State Data': 'aggregated_transaction_state',
        'Insurance Data': 'aggregated_insurence_country',
        'Insurance State Data': 'aggregated_insurence_state',
        'User Country Data': 'aggregated_user_counry',
        'User State Data': 'agregated_user_state'
    }
    return tables.get(selected_tab, None)

# ***************************************Data Exploration*******************************

first_box = st.container(border=True)
col1, col2 = first_box.columns([7, 1])

with col1:
    # Create tabs
    selected_tab = ui.tabs(
        options=['Transaction Data', 'Transaction State Data', 'Insurance Data', 'Insurance State Data',
                 'User Country Data', 'User State Data'], default_value='User State Data', key="two_birds")
with col2:
    filter_data = st.toggle('Filter Data')

chosen_table = select_the_table(selected_tab)
if chosen_table is None:
    st.warning("Please select a valid table.")
else:
    df = load_data_from_db(f'SELECT * FROM {chosen_table}')
    
    filtered_df = None

    filter_box = st.container(border=True)

if filter_data:
    # Create columns
    col3, col4, col5, col6 = filter_box.columns(4)

    # Sidebar input widgets
    selected_years = col3.multiselect('Select Year:', sorted(df['year'].unique()), default=[2022],
                                      help='Select the Year')
    selected_quarters = col4.multiselect('Select Quarter:', sorted(df['quarter'].unique()), default=[1, 2, 3, 4])

    # Check if 'state' is a column in the DataFrame
    if 'state' in df.columns:
        selected_state = col5.multiselect('Select State/UT:', sorted(df['state'].unique()), default= ['karnataka'])
        
        if 'type_of_transaction' in df.columns:
            entity_type = col6.multiselect('Select Transaction Type:', sorted(df['type_of_transaction'].unique()))
            # Filter the DataFrame based on user inputs
            filtered_df = df[(df['state'].isin(selected_state)) & (df['year'].isin(selected_years)) & (
                        df['quarter'].isin(selected_quarters)) & (df['type_of_transaction'].isin(entity_type))]
        else:
            entity_type = col6.multiselect('Select Phone Brand:', sorted(df['phone_brand'].unique()))
            # Filter the DataFrame based on user inputs
            filtered_df = df[(df['state'].isin(selected_state)) & (df['year'].isin(selected_years)) & (
                        df['quarter'].isin(selected_quarters)) & (df['phone_brand'].isin(entity_type))]
    else:
        if 'type_of_transaction' in df.columns:
            entity_type = col5.multiselect('Select Transaction Type:', sorted(df['type_of_transaction'].unique()))
            # Filter the DataFrame based on user inputs
            filtered_df = df[(df['year'].isin(selected_years)) & (df['quarter'].isin(selected_quarters)) & (
                        df['type_of_transaction'].isin(entity_type))]
        else:
            entity_type = col5.multiselect('Select Phone Brand:', sorted(df['phone_brand'].unique()))
            # Filter the DataFrame based on user inputs
            filtered_df = df[(df['year'].isin(selected_years)) & (df['quarter'].isin(selected_quarters)) & (
                        df['phone_brand'].isin(entity_type))]
   
    # Show filtered data using an expander
    with st.expander('Show Filtered Full Data'):
        st.dataframe(filtered_df, use_container_width=True)

else:
    filtered_df = df
    with st.expander('Show Full Data'):
        st.dataframe(df, use_container_width=True)
    
ui.table(data=filtered_df.head(), maxHeight=500, key="filtered_data_table")



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
    stx.TabBarItemData(id='smile', title="ToDo", description="Tasks to take care of"),
    stx.TabBarItemData(id=2, title="Done", description="Tasks taken care of"),
    stx.TabBarItemData(id=3, title="Overdue", description="Tasks missed out"),
], default=1)
st.info(f"{chosen_id=}")

if chosen_id == 'smile':
    st.write("ToDo")
if chosen_id == '2':
    st.write("Done")
if chosen_id == '3':
    st.write("Overdue")


val = stx.stepper_bar(steps=["Ready", "Get Set", "Go"])
st.info(f"Phase #{val}")
stx.TabBar(data = ['total revenue','state revenue'], default=None, return_type=str, key=None)