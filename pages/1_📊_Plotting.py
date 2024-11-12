import streamlit as st
import streamlit_shadcn_ui as ui
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    initial_sidebar_state='collapsed',
    page_title="📈 Tables",
    page_icon=':chart:'
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

first_box = st.container()
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

    filter_box = st.container()

if filter_data:
    # Create columns
    col3, col4, col5, col6 = filter_box.columns(4)

    # Sidebar input widgets
    selected_years = col3.multiselect('Select Year:', sorted(df['year'].unique()), default=[2022],
                                      help='Select the Year')
    selected_quarters = col4.multiselect('Select Quarter:', sorted(df['quarter'].unique()), default=[1, 2, 3, 4])

    # Check if 'state' is a column in the DataFrame
    if 'state' in df.columns:
        selected_state = col5.multiselect('Select State/UT:', sorted(df['state'].unique()), default=['karnataka'])
        
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
        
if selected_tab == 'User Country Data':
    # Aggregate data by year and phone brand 
    agg_df = df.groupby(["year",'phone_brand']).agg({
        "phone_count": "sum",
        "Percentage": "sum"
    }).reset_index()
    data = agg_df
else:
    data = filtered_df.head()    

ui.table(data=data, maxHeight=500, key="filtered_data_table")

# ***************************************Charts*******************************

if selected_tab == 'Transaction State Data':
    # Bar chart for total transaction count by state and type of transaction
    fig1 = px.bar(
        filtered_df,
        x="state",
        y="number_of_transactions",
        color="type_of_transaction",
        barmode="group",
        title="Total Transaction Count by State and Type of Transaction",
        labels={"number_of_transactions": "Total Transaction Count", "state": "State", "type_of_transaction": "Type of Transaction"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Bar chart for total transaction amount by state and type of transaction
    fig2 = px.bar(
        filtered_df,
        x="state",
        y="total_amount",
        color="type_of_transaction",
        barmode="group",
        title="Total Transaction Amount by State and Type of Transaction",
        labels={"total_amount": "Total Transaction Amount", "state": "State", "type_of_transaction": "Type of Transaction"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Line chart for transaction count over time by state and type of transaction
    fig3 = px.line(
        filtered_df,
        x="quarter",
        y="number_of_transactions",
        color="state",
        line_dash="type_of_transaction",
        title="Transaction Count Over Time by State and Type of Transaction",
        labels={"number_of_transactions": "Transaction Count", "quarter": "Quarter", "state": "State", "type_of_transaction": "Type of Transaction"},
        facet_col="year",
        facet_col_wrap=2
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Line chart for transaction amount over time by state and type of transaction
    fig4 = px.line(
        filtered_df,
        x="quarter",
        y="total_amount",
        color="state",
        line_dash="type_of_transaction",
        title="Transaction Amount Over Time by State and Type of Transaction",
        labels={"total_amount": "Transaction Amount", "quarter": "Quarter", "state": "State", "type_of_transaction": "Type of Transaction"},
        facet_col="year",
        facet_col_wrap=2
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Treemap for transaction distribution by state, year, and type of transaction
    fig5 = px.treemap(
        filtered_df,
        path=["state", "year", "type_of_transaction"],
        values="number_of_transactions",
        title="Transaction Distribution by State, Year, and Type of Transaction",
        labels={"number_of_transactions": "Transaction Count", "state": "State", "type_of_transaction": "Type of Transaction"}
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Treemap for transaction amount distribution by state, year, and type of transaction
    fig6 = px.treemap(
        filtered_df,
        path=["state", "year", "type_of_transaction"],
        values="total_amount",
        title="Transaction Amount Distribution by State, Year, and Type of Transaction",
        labels={"total_amount": "Transaction Amount", "state": "State", "type_of_transaction": "Type of Transaction"}
    )
    st.plotly_chart(fig6, use_container_width=True)

    # Scatter plot for transaction count vs. amount by state and type of transaction
    fig7 = px.scatter(
        filtered_df,
        x="number_of_transactions",
        y="total_amount",
        color="state",
        symbol="type_of_transaction",
        title="Transaction Count vs. Amount by State and Type of Transaction",
        labels={"number_of_transactions": "Transaction Count", "total_amount": "Transaction Amount", "state": "State", "type_of_transaction": "Type of Transaction"}
    )
    st.plotly_chart(fig7, use_container_width=True)

    # Sunburst chart for transaction distribution by state, year, quarter, and type of transaction
    fig8 = px.sunburst(
        filtered_df,
        path=["state", "year", "quarter", "type_of_transaction"],
        values="number_of_transactions",
        title="Transaction Distribution by State, Year, Quarter, and Type of Transaction",
        labels={"number_of_transactions": "Transaction Count", "state": "State", "type_of_transaction": "Type of Transaction"}
    )
    st.plotly_chart(fig8, use_container_width=True)

elif selected_tab == 'Insurance Data':
    # Bar chart for total insurance transaction count by year and quarter
    fig1 = px.bar(
        filtered_df,
        x="year",
        y="count",
        color="quarter",
        barmode="group",
        title="Total Insurance Transaction Count by Year and Quarter",
        labels={"count": "Total Transaction Count", "year": "Year", "quarter": "Quarter"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Bar chart for total insurance transaction amount by year and quarter
    fig2 = px.bar(
        filtered_df,
        x="year",
        y="amount",
        color="quarter",
        barmode="group",
        title="Total Insurance Transaction Amount by Year and Quarter",
        labels={"amount": "Total Transaction Amount", "year": "Year", "quarter": "Quarter"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Line chart for insurance transaction count over time
    fig3 = px.line(
        filtered_df,
        x="quarter",
        y="count",
        color="year",
        title="Insurance Transaction Count Over Time",
        labels={"count": "Transaction Count", "quarter": "Quarter", "year": "Year"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Line chart for insurance transaction amount over time
    fig4 = px.line(
        filtered_df,
        x="quarter",
        y="amount",
        color="year",
        title="Insurance Transaction Amount Over Time",
        labels={"amount": "Transaction Amount", "quarter": "Quarter", "year": "Year"}
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Treemap for insurance transaction distribution by year and quarter
    fig5 = px.treemap(
        filtered_df,
        path=["year", "quarter"],
        values="count",
        title="Insurance Transaction Distribution by Year and Quarter",
        labels={"count": "Transaction Count", "year": "Year", "quarter": "Quarter"}
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Treemap for insurance transaction amount distribution by year and quarter
    fig6 = px.treemap(
        filtered_df,
        path=["year", "quarter"],
        values="amount",
        title="Insurance Transaction Amount Distribution by Year and Quarter",
        labels={"amount": "Transaction Amount", "year": "Year", "quarter": "Quarter"}
    )
    st.plotly_chart(fig6, use_container_width=True)

    # Scatter plot for insurance transaction count vs. amount
    fig7 = px.scatter(
        filtered_df,
        x="count",
        y="amount",
        color="year",
        symbol="quarter",
        title="Insurance Transaction Count vs. Amount",
        labels={"count": "Transaction Count", "amount": "Transaction Amount", "year": "Year", "quarter": "Quarter"}
    )
    st.plotly_chart(fig7, use_container_width=True)

    # Sunburst chart for insurance transaction distribution by year, quarter, and type of transaction
    fig8 = px.sunburst(
        filtered_df,
        path=["year", "quarter", "type_of_transaction"],
        values="count",
        title="Insurance Transaction Distribution by Year, Quarter, and Type of Transaction",
        labels={"count": "Transaction Count", "year": "Year", "quarter": "Quarter", "type_of_transaction": "Type of Transaction"}
    )
    st.plotly_chart(fig8, use_container_width=True)


if selected_tab == "Insurance State Data":
    st.subheader("Insurance Transactions Overview")
    
    # Plot 1: Number of Transactions by Quarter
    st.write("### Number of Transactions by Quarter")
    fig1 = px.bar(filtered_df, x='quarter', y='number_of_transactions', 
                  labels={'quarter': 'Quarter', 'number_of_transactions': 'Number of Transactions'},
                  title=f"Number of Insurance Transactions")
    st.plotly_chart(fig1)
    
    # Plot 2: Total Amount by Quarter
    st.write("### Total Amount by Quarter")
    fig2 = px.line(filtered_df, x='quarter', y='total_amount', 
                   labels={'quarter': 'Quarter', 'total_amount': 'Total Amount'},
                   title=f"Total Amount of Insurance Transactions")
    st.plotly_chart(fig2)
    
    # Plot 3: Combined View (Number of Transactions and Total Amount)
    st.write("### Combined View: Number of Transactions and Total Amount")
    fig3 = px.scatter(filtered_df, x='number_of_transactions', y='total_amount', color='quarter',
                      labels={'number_of_transactions': 'Number of Transactions', 'total_amount': 'Total Amount'},
                      title=f"Combined View of Insurance Transactions")
    st.plotly_chart(fig3)
# else:
#     # Bar chart for total transaction count by category
#     fig1 = px.bar(
#         filtered_df,
#         x="name",
#         y="count",
#         title="Total Transaction Count by Category",
#         labels={"count": "Total Transaction Count", "name": "Category"}
#     )
#     st.plotly_chart(fig1, use_container_width=True)

#     # Bar chart for total transaction amount by category
#     fig2 = px.bar(
#         filtered_df,
#         x="name",
#         y="amount",
#         title="Total Transaction Amount by Category",
#         labels={"amount": "Total Transaction Amount", "name": "Category"}
#     )
#     st.plotly_chart(fig2, use_container_width=True)

#     # Line chart for transaction count over time
#     fig3 = px.line(
#         filtered_df,
#         x="quarter",
#         y="count",
#         color="name",
#         line_dash="name",
#         title="Transaction Count Over Time by Category",
#         labels={"count": "Transaction Count", "quarter": "Quarter", "name": "Category"},
#         facet_col="year",
#         facet_col_wrap=2
#     )
#     st.plotly_chart(fig3, use_container_width=True)

#     # Line chart for transaction amount over time
#     fig4 = px.line(
#         filtered_df,
#         x="quarter",
#         y="amount",
#         color="name",
#         line_dash="name",
#         title="Transaction Amount Over Time by Category",
#         labels={"amount": "Transaction Amount", "quarter": "Quarter", "name": "Category"},
#         facet_col="year",
#         facet_col_wrap=2
#     )
#     st.plotly_chart(fig4, use_container_width=True)

#     # Treemap for transaction distribution by category and year
#     fig5 = px.treemap(
#         filtered_df,
#         path=["year", "name"],
#         values="count",
#         title="Transaction Distribution by Category and Year",
#         labels={"count": "Transaction Count", "name": "Category"}
#     )
#     st.plotly_chart(fig5, use_container_width=True)

#     # Treemap for transaction amount distribution by category and year
#     fig6 = px.treemap(
#         filtered_df,
#         path=["year", "name"],
#         values="amount",
#         title="Transaction Amount Distribution by Category and Year",
#         labels={"amount": "Transaction Amount", "name": "Category"}
#     )
#     st.plotly_chart(fig6, use_container_width=True)

#     # Scatter plot for transaction count vs. amount
#     fig7 = px.scatter(
#         filtered_df,
#         x="count",
#         y="amount",
#         color="name",
#         title="Transaction Count vs. Amount by Category",
#         labels={"count": "Transaction Count", "amount": "Transaction Amount", "name": "Category"}
#     )
#     st.plotly_chart(fig7, use_container_width=True)

#     # Sunburst chart for transaction distribution by year, quarter, and category
#     fig8 = px.sunburst(
#         filtered_df,
#         path=["year", "quarter", "name"],
#         values="count",
#         title="Transaction Distribution by Year, Quarter, and Category",
#         labels={"count": "Transaction Count", "name": "Category"}
#     )
#     st.plotly_chart(fig8, use_container_width=True)