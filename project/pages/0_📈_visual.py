import plotly.express as px
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import streamlit_shadcn_ui as ui

# Set Streamlit page configuration
st.set_page_config(
    page_title="Visualisation",
    layout="wide",
    initial_sidebar_state = "collapsed",
    page_icon=":graph:",
)


# Create a function to load data from the SQLite database
def load_data_from_db(query):
    sqlite_file = 'project/test.sqlite'
    engine = create_engine(f'sqlite:///{sqlite_file}')
    df = pd.read_sql(query, engine)
    return df





# # Fetch data from SQLite based on user selection from dropdown
# dropdown_options = {
#     '---': None,
#     "Nationwise Aggregated User Data": "aggregated_user_counry",
#     "Nationwise Aggregated Insurence Data": "aggregated_insurence_counry",
#     "Statewise Map Transaction Data": "map_transaction_hover_state",
#     "Nationwise Top Transaction Data": "top_transaction_country",
#     "Statewise Top Insurence Data": "top_insurence_state",
#     "Statewise Aggregated Transaction Data": "aggregated_transaction_state",
#     "Nationwise Map User Data": "map_user_hover_contry",
#     "Nationwise Map Insurence Data": "map_insurence_hover_counry",
#     "Statewise Aggregated User Data": "aggregated_user_state",
#     "Statewise Map User Data": "map_user_hover_state",
#     "Nationwise Map Transaction Data": "map_transaction_hover_counry",
#     "Nationwise Top Insurence Data": "top_insurence_country",
#     "Statewise Aggregated Insurence Data": "aggregated_insurence_state",
#     "Nationwise Aggregated Transaction Data": "aggregated_transaction_country",
#     "Nationwise Top User Data": "top_user_country",
#     "Statewise Top User Data": "top_user_state",
#     "Top Ten States Transactions": "your_table_name WHERE ...",
#     "Top Ten Districts": "your_table_name WHERE ...",
#     "Top Ten Pincodes": "your_table_name WHERE ...",
# }

# # Streamlit app
# st.title("SQL Table Visualization")


query = 'SELECT * FROM aggregated_insurence_state;'
df = load_data_from_db(query)

# Aggregate data by summing quarter amounts and transactions per year
agg_df = df.groupby(["state", "year"]).agg({
    "number_of_transactions": "sum",
    "total_amount": "sum"
}).reset_index()


# Display metrics in two columns
cols = st.columns(2)
with cols[0]:
    ui.metric_card(title="Total Insurence Amount", content=f"₹{df.total_amount.sum()}", description="Total insurence amount from state transactions", key="card1")
with cols[1]:
    ui.metric_card(title="Total Number of Transactions", content=f"{df.number_of_transactions.sum()}", description="Total Number of Transactions from state insurence", key="card2")
# st.markdown('---')
ui.table(data=df.head(), maxHeight=300)
# Create a scatter plot using Plotly Express
fig1 = px.scatter(
    df,
    x="number_of_transactions",
    y="total_amount",
    size="total_amount",  # Use 'total_amount' for size
    color="state",
    hover_name="state",
    log_x=True,
    size_max=50,
)

# Display the scatter plot
st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

# Load data for pie charts
query1 = 'SELECT * FROM aggregated_insurence_state;'
df1 = load_data_from_db(query1)

# Create pie charts
fig2 = px.pie(df1, values='total_amount', names='year')
fig3 = px.pie(df1, values='total_amount', names='state', hole=.6, hover_data=['number_of_transactions'], title='Total Insurence Amount')

# Display the pie charts in columns
col1, col2 = st.columns([1, 3])

with col1:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with col2:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

charts= st.container(border=True)
charts.write("Total transaction proportion by year")
charts.plotly_chart(fig2, theme="streamlit", use_container_width=True)
charts.header('container check')


# Showing metric data
temp = st.container()
col1, col2, col3 = temp.columns(3)
one = col1.container(border=True)
two = col2.container(border=True)
three = col3.container(border=True)

# Metrics for column one
one.metric(label= "__Total Insurence Amount__", value=f"₹{df.total_amount.sum()}", delta="Total insurence amount from state transactions", delta_color = 'off')
# Metrics for column two
two.metric(label="Wind", value="17 mph", delta="-8%")
# Metrics for column three
three.metric(label="Humidity", value="86%", delta="4%")