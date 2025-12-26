import streamlit as st
import pandas as pd
import os
import plotly.express as px


st.set_page_config(page_title="Sierra Mining and Crushing Dashboard", layout="wide", page_icon="⛏️")

st.title("Income Breakdown")



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
    data = data.loc[:, ~data.columns.duplicated(keep="last")]  # Drop rows where all elements are NaN
    return data

data = load_data()

# Add a side bar with a date range selector to filter the data.
st.sidebar.header("Filter Date Range")
start_date = st.sidebar.date_input("Start Date", data['Date'].min())
end_date = st.sidebar.date_input("End Date", data['Date'].max())
filtered_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]


# Create weekly data from filtered data
weekly_data = filtered_data.groupby('Week').agg({"Total Income": "sum",
                                                 "Discounts Given": "sum",
                                                 "Income": "sum",
                                                 "Income-Dump Fees": "sum",
                                                 "Income-Hauling": "sum",
                                                 "Income-Materials": "sum",
                                                 "Interest Income": "sum",
                                                 "Total Sierra Waste and Recycling": "sum"}).reset_index()

# Get totals from filtered data from
# Total Income, Discounts Given, Income, Income-Dump Fees, Income-Hauling, Income Materials,
# Interest Income, Total Sierra Waste and Recycling.
total_income = filtered_data['Total Income'].sum()
total_discounts = filtered_data['Discounts Given'].sum()
income_sum = filtered_data['Income'].sum()
total_income_dump_fees = filtered_data['Income-Dump Fees'].sum()
total_income_hauling = filtered_data['Income-Hauling'].sum()
total_income_materials = filtered_data['Income-Materials'].sum()
total_interest_income = filtered_data['Interest Income'].sum()
total_sierra_waste_recycling = filtered_data['Total Sierra Waste and Recycling'].sum()



row = st.container(horizontal=True)
with row:
    st.metric("Total Income", f"${total_income:,.2f}", border=True)
    st.metric("Discounts Given", f"${total_discounts:,.2f}", border=True)
    st.metric("Income", f"${income_sum:,.2f}", border=True)
    st.metric("Income-Dump Fees", f"${total_income_dump_fees:,.2f}", border=True)
    st.metric("Income-Hauling", f"${total_income_hauling:,.2f}", border=True)
    st.metric("Income Materials", f"${total_income_materials:,.2f}", border=True)
    st.metric("Interest Income", f"${total_interest_income:,.2f}", border=True)
    st.metric("Total Sierra Waste and Recycling", f"${total_sierra_waste_recycling:,.2f}", border=True)
    

# Create the plot with week on the x-axis and total income on the y-axis.
def plot_total_income(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Total Income', title='Weekly Total Income Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)

def plot_discounts_given(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Discounts Given', title='Weekly Discounts Given Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)

def plot_income_components(weekly_data):
    fig = px.line(weekly_data, x='Week', y=['Income-Dump Fees', 'Income-Hauling', 'Income-Materials', 'Interest Income', 'Total Sierra Waste and Recycling'],
                  title='Weekly Income Components Over Time', markers=True)
    return st.plotly_chart(fig, use_container_width=True)


# Display the plots in containers with borders.
st.subheader("Weekly Total Income Over Time")
container1 = st.container(border=True)
with container1:
    plot_total_income(weekly_data)
st.subheader("Weekly Discounts Given Over Time")
container2 = st.container(border=True)
with container2:
    plot_discounts_given(weekly_data)
st.subheader("Weekly Income Components Over Time")
container3 = st.container(border=True)
with container3:
    plot_income_components(weekly_data)
    
    