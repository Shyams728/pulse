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
    initial_sidebar_state = "collapsed", 
    page_icon=":graph:",
)

st.markdown('**Top charts**')
#***************************************Data Access*******************************
# Create a function to load data from the SQLite database
def load_data_from_db(query):
    sqlite_file = 'project/test.sqlite'
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



def plot_barchart_top(df, x, y, title):
    # Plotly bar chart
    fig = px.bar(
        df,
        y=x,
        x=y,
        orientation='h',
        color="entity_name",
        labels={'amount': 'Amount', 'count': 'Transactions'},
        title=title,
    )
    # Show the plot using Plotly chart in Streamlit
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


#***************************************Data Exploration*******************************
first_box = st.container(border=True)
col1, col2 = first_box.columns([6,1])

with col1:
    # Create tabs
    selected_tab = ui.tabs(options=['Transaction Data', 'Insurance Data', 'User Data', 'Statewise Transaction Data', 'Statewise Insurance Data', 'Statewise User Data'], default_value='Statewise Insurance Data', key="kanaries")
with col2:
    filter_data = st.toggle('filter data')

choosen_table = select_the_table(selected_tab)
df = load_data_from_db(choosen_table)

filtered_df = None



filter_box = st.container(border=True)
if filter_data:
    # Create columns
    col3, col4,col5,col6 = filter_box.columns(4)

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

    
    # Show filtered data using an expander
    with st.expander('Show Filtered Full Data'):
        st.dataframe(filtered_df,use_container_width = True)

else:
    
    with st.expander('Show Full Data'):
            st.dataframe(df,use_container_width = True)



display_box_df_charts = st.container(border=True)
df_col, charts_col = display_box_df_charts.columns([1,1])

if filter_data:
    data = filtered_df
else:
    data = df

with df_col:
    st.markdown("**Data**")
    # Display the filtered DataFrame
    ui.table(data=data.head(10), maxHeight=700,key="filtered_data_table")

with charts_col:    
    # Plotly bar chart
    # Check if 'registeredUsers' column exists in the DataFrame
    if 'registeredUsers' in data.columns:
        plot_barchart_top(data, 'entity_name', 'registeredUsers', f'Top {selected_tab} Analysis')
    else:
        plot_barchart_top(data, 'entity_name', 'amount', f'Top {selected_tab} Analysis')


#****************************************Data Visualisation****************************
