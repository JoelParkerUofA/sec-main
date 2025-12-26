import streamlit as st
import pandas as pd
import os
import plotly.express as px


st.set_page_config(page_title="Sierra Mining and Crushing Dashboard", layout="wide")



# Load the dataset Fiscal_Y2D.CSV, convert the first column to index, and transpose the dataframe,
# convert row names to column with the variable name "Date". Conver date column to datetime format.
# add a variable called week that indicates the Monday of the week for each date. 
# 
@st.cache_data
def load_data():
    data = pd.read_csv("Fiscal_Y2D.CSV").drop(columns=['TOTAL'])
    data.set_index(data.columns[0], inplace=True)
    data = data.T
    data.reset_index(inplace=True)
    data.columns = ['Date'] + list(data.columns[1:])
    data['Date'] = pd.to_datetime(data['Date'], format="%b %d, %y")
    data['Week'] = data['Date'] - pd.to_timedelta(data['Date'].dt.weekday, unit='d')
    return data

data = load_data()


# Create a sidebar with a date range selector to filter the data.
st.sidebar.header("Filter Date Range")
start_date = st.sidebar.date_input("Start Date", data['Date'].min())
end_date = st.sidebar.date_input("End Date", data['Date'].max())

filtered_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]

# Create line chart grouped by week summarizing the total income for each week.
weekly_data = filtered_data.groupby('Week').agg({"Discounts Given": "sum",
          "Income-Dump Fees": "sum",
          "Income-Hauling": "sum",
          "Income-Materials": "sum",
          "Interest Income": "sum",
          "Sierra Waste and Recycling": "sum",
          "Disposal Fees": "sum",
          "Hauling": "sum",
          "Sierra Waste and Recycling - Other": "sum",
          "Total Sierra Waste and Recycling": "sum",
          "Total Income": "sum"}).reset_index()


# Create row of metrics showing total income, Total Cost of goods and Services, Total Expenses, and Net Income
total_income = filtered_data['Total Income'].sum()
total_cogs = filtered_data['Total COGS'].sum()
total_expenses = filtered_data['Total Expense'].sum()
net_income = filtered_data['Net Income'].sum()

row = st.container(horizontal=True)
with row:
    st.metric("Total Income", f"${total_income:,.2f}", border=True)
    st.metric("Total COGS", f"${total_cogs:,.2f}", border=True)
    st.metric("Total Expenses", f"${total_expenses:,.2f}", border=True)
    st.metric("Net Income", f"${net_income:,.2f}", border=True)


# Create the plot with week on the x-axis and total income on the y-axis.
def plot_total_income(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Total Income', title='Weekly Total Income Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)

# Create plot of Total COGS over time.
def plot_total_cogs(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Total COGS', title='Weekly Total Cost of Goods and Services Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)


# Create plot of Total Expenses over time.
def plot_total_expenses(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Total Expenses', title='Weekly Total Expenses Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)

# Create plot of Net Income over time.
def plot_net_income(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Net Income', title='Weekly Net Income Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)


# Display the plot in a container with a border.

container1 = st.container(border=True)
container2 = st.container(border=True)
container3 = st.container(border=True)
container4 = st.container(border=True)

with container1:
    plot_total_income(weekly_data)
with container2:
    plot_total_cogs(weekly_data)
with container3:
    plot_total_expenses(weekly_data)
with container4:
    plot_net_income(weekly_data)
