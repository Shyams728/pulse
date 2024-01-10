import plotly.express as px
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import streamlit_shadcn_ui as ui
import extra_streamlit_components as stx

# Set Streamlit page configuration
st.set_page_config(
    page_title="Top Charts",
    layout="wide",
    page_icon=":graph:",
)

st.markdown('**Top charts**')
#***************************************Data Access*******************************
# Create a function to load data from the SQLite database
def load_data_from_db(query):
    sqlite_file = '/home/user/pulse/test.sqlite'
    engine = create_engine(f'sqlite:///{sqlite_file}')
    df = pd.read_sql(query, engine)
    return df


def select_the_table(selected_tab):
    # Execute different queries based on the chosen tab
    if selected_tab == 'Transaction Data':
        query = 'SELECT * FROM top_transaction_country;'
    elif selected_tab == 'Insurance Data':
        query = 'SELECT * FROM top_insurence_country;'
    elif selected_tab == 'User Data':
        query = 'SELECT * FROM top_user_country;'
    elif selected_tab == 'Statewise Transaction Data':
        query = 'SELECT * FROM top_transaction_state;'
    elif selected_tab == 'Statewise Insurance Data':
        query = 'SELECT * FROM top_insurance_state;'
    elif selected_tab == 'Statewise User Data':
        query = 'SELECT * FROM top_user_state;'
    return query


#***************************************Data Exploration*******************************
# Create tabs
selected_tab = ui.tabs(options=['Transaction Data', 'Insurance Data', 'User Data', 'Statewise Transaction Data', 'Statewise Insurance Data', 'Statewise User Data'], default_value='Statewise Insurance Data', key="kanaries")

choosen_table = select_the_table(selected_tab)


df = load_data_from_db(choosen_table)

filtered_df = None
container = st.container()
filter_data = container.toggle('filter data')
if filter_data:
    # Create columns
    col3, col4,col5,col6 = container.columns(4)

    # Sidebar input widgets
    selected_years = col3.multiselect('Select Year:', sorted(df['year'].unique()),default=2022,help='Select the Year')
    selected_quarters = col4.multiselect('Select Quarter:', sorted(df['quarter'].unique()),default=[1,2,3,4])

    # Check if 'state' is a column in the DataFrame
    if 'state' in df.columns:
        selected_state = col5.multiselect('Select State/UT:', sorted(df['state'].unique()),default = ['karnataka'])
        entity_type = col6.selectbox('Select Entity Type:', sorted(df['entity_type'].unique()))

        # Filter the DataFrame based on user inputs
        filtered_df = df[(df['state'].isin(selected_state)) & (df['year'].isin(selected_years)) & (df['quarter'].isin(selected_quarters)) & (df['entity_type'] == entity_type)]
    else:
        entity_type = col5.selectbox('Select Entity Type:', sorted(df['entity_type'].unique()))

        # Filter the DataFrame based on user inputs
        filtered_df = df[(df['year'].isin(selected_years)) & (df['quarter'].isin(selected_quarters)) & (df['entity_type'] == entity_type)]

    
    # Display the filtered DataFrame
    ui.table(data=filtered_df.head(), maxHeight=500,key="filtered_data_table")
    # Show filtered data using an expander
    with st.expander('Show Filtered Full Data'):
        st.dataframe(filtered_df,use_container_width = True)
else:
    ui.table(data=df.head(), maxHeight=500,key="df_data_table")
    with st.expander('Show Full Data'):
            st.dataframe(df,use_container_width = True)


#****************************************Data Visualisation****************************
# # Plotly bar chart
# fig = px.bar(
#     filtered_df,
#     y='entity_name',
#     x='amount',
#     orientation='h',
#     color="entity_name",
#     labels={'amount': 'Amount', 'count': 'Transactions'},
#     title='Top Transaction States Data Analysis',
# )

# # Show the plot using Plotly chart in Streamlit
# st.plotly_chart(fig, theme="plotly", use_container_width=True)
