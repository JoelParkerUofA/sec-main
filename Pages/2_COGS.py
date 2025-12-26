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



# COGS cols 
cols = [
    "Cost of Goods Sold",
    "Direct Labor",
    "Equipment Rental",
    "Equipment Repairs & Maintenance",
    "262D ODTB03831",
    "262D ODTB03833",
    "289C",
    "330",
    "345CL Excavator",
    "350 Excavator-3ML357",
    "615C",
    "7420 John Deere",
    "966E Loader",
    "966H",
    "966K ONGX00224",
    "966M",
    "966XE",
    "980G Cat Loade-S/N 2KR00957",
    "980G Loader S/N AWH00271",
    "980G Wheel Loader S/N 01819",
    "988F",
    "Bobcat",
    "Cat 3306B",
    "Cat 349E",
    "Cat 352",
    "Cat 637 Scraper",
    "Cedarapids",
    "D400",
    "D8K Dozer",
    "D8R Dozer-1473",
    "D9L Dozer",
    "D9T Dozer",
    "El Jay 1140 Crusher",
    "Finlay Wash Plants",
    "Hammel Shredder",
    "Komatsu Excavator",
    "McCloskey Crusher",
    "NEW Powerscreen",
    "Powerscreen 1700",
    "Roll Off Cans",
    "Soil Cement Plant",
    "Superior Radial Stack Conveyor",
    "Wash Plant",
    "Equipment Repairs & Maintenance - Other",
    "Total Equipment Repairs & Maintenance",
    "Fuel",
    "Landfill Fees",
    "Material Testing",
    "Materials",
    '1" Apache Red',
    '1" Coronado Brown',
    '1/2" Apache Red',
    '1/2" Coronado Brown',
    '3"-6" Coronado Brown',
    '3/8" Apache Red',
    '3/8" Coronado Brown',
    "4-8 Rip Rap",
    '4"-8" Coronado Brown',
    '6"-12" Coronado Brown',
    "ABC",
    "Cold Mix",
    "MA FINES",
    "Materials - Other",
    "Total Materials",
    "Oil & Grease",
    "Parts",
    "Repairs & Maintainence",
    "Small Tools & Supplies",
    "Subcontractor",
    "Subcontractor-SMC",
    "Uniforms",
    "Vehicle Repairs & Maintenance",
    "11 - 2005 Kenworth T800 RO",
    "110 - 2007 Western Star",
    "2001 Mack Roll Off",
    "2007 Mack",
    "2011 Ford",
    "2019 Ford F150",
    "2019 Peterbilt",
    "2021 Dodge Ram Pick Up 2500",
    "2225 - 2022 Western Star",
    "2228 - 2022 Western Star",
    "24-2016 Western Star",
    "2421 - 2024 Western Star",
    "2422 - 2022 Western Star",
    "26 - 2021 Western Star",
    "29 - 2006 Peterbilt 379 Tractor",
    "31 - 2019 Peterbilt - VIN #7391",
    "32 -2019 Peterbilt - VIN #7411",
    "34 - 2006 Peterbilt 379",
    "46-2016 Mack",
    "Autocar",
    "Lube Truck",
    "Volvo Water Truck",
    "Vehicle Repairs & Maintenance - Other",
    "Total Vehicle Repairs & Maintenance",
    "Total COGS"
]

# Get totals from filtered data
totals_filtered = filtered_data[cols].sum()


# Add metrics
row = st.container(horizontal=True)
with row:
    st.metric("Total COGS", f"${totals_filtered["Total COGS"]:,.2f}", border=True)
    st.metric("Total Vehicle Repairs & Maintenance", f"${totals_filtered["Total Vehicle Repairs & Maintenance"]:,.2f}", border=True)
    st.metric("Direct Labor", f"${totals_filtered["Direct Labor"]:,.2f}", border=True)
    st.metric("Equipment Rental", f"${totals_filtered["Equipment Rental"]:,.2f}", border=True)
    st.metric("Fuel", f"${totals_filtered["Fuel"]:,.2f}", border=True)
    st.metric("Landfill Fees", f"${totals_filtered["Landfill Fees"]:,.2f}", border=True)
    st.metric("Material Testing", f"${totals_filtered["Material Testing"]:,.2f}", border=True)
    st.metric("Total Materials", f"${totals_filtered["Total Materials"]:,.2f}", border=True)
    st.metric("Subcontractor", f"${totals_filtered["Subcontractor"]:,.2f}", border=True)
    st.metric("Subcontractor-SMC", f"${totals_filtered["Subcontractor-SMC"]:,.2f}", border=True)



# Create weekly data from filtered data by grouping by week and summing COGS columns.
weekly_data = filtered_data.groupby('Week')[cols].sum().reset_index()


# Create plot of Total COGS over time.
def plot_total_cogs(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Total COGS', title='Weekly Total Cost of Goods and Services Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)

# Create direct labor over time.
def plot_direct_labor(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Direct Labor', title='Weekly Direct Labor Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)

# Create plot of Equipment Rental over time.
def plot_equipment_rental(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Equipment Rental', title='Weekly Equipment Rental Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)


# Create equipment repairs and maintenance plot over time. Include the following components:
# - Total Equipment Repairs & Maintenance
def plot_equipment_repairs(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Total Equipment Repairs & Maintenance', title='Weekly Equipment Repairs & Maintenance Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)


# Make a plot with maintance components
## 262D ODTB03831
#262D ODTB03833
#289C
#330
#345CL Excavator
#350 Excavator-3ML357
#615C
#7420 John Deere
#966E Loader
#966H
#966K ONGX00224
#966M
#966XE
#980G Cat Loade-S/N 2KR00957
#980G Loader S/N AWH00271
#980G Wheel Loader S/N 01819
#988F
#Bobcat
#Cat 3306B
#Cat 349E
#Cat 352
#Cat 637 Scraper
#Cedarapids
#D400
#D8K Dozer
#D8R Dozer-1473
#D9L Dozer
#D9T Dozer
#El Jay 1140 Crusher
#Finlay Wash Plants
#Hammel Shredder
#Komatsu Excavator
#McCloskey Crusher
#NEW Powerscreen
#Powerscreen 1700
#Roll Off Cans
#Soil Cement Plant
#Superior Radial Stack Conveyor
#Wash Plant
#Equipment Repairs & Maintenance - Other

def plot_maintenance_components(weekly_data, vars=None):

    fig = px.line(weekly_data, x='Week', y=vars,
                  title='Weekly Equipment Maintenance Components Over Time', markers=True)
    return st.plotly_chart(fig, use_container_width=True)


# Create plot for fuel over time.
def plot_fuel(weekly_data):
    fig = px.line(weekly_data, x='Week', y='Fuel', title='Weekly Fuel Over Time',
                  markers=True)
    return st.plotly_chart(fig, use_container_width=True)

# Create plot for material components over time
# 1" Apache Red
#1" Coronado Brown
#1/2" Apache Red
##1/2" Coronado Brown
#3"-6" Coronado Brown
#3/8" Apache Red
#3/8" Coronado Brown
#4-8 Rip Rap
#4"-8" Coronado Brown
#6"-12" Coronado Brown
#ABC
#Cold Mix
#MA FINES
#Materials - Other

def plot_material_components(weekly_data, vars=None):

    fig = px.line(weekly_data, x='Week', y=vars,
                  title='Weekly Material Components Over Time', markers=True)
    return st.plotly_chart(fig, use_container_width=True)

# Create plot for vehicle repairs and maintenance over time.
## 11 - 2005 Kenworth T800 RO
#110 - 2007 Western Star
#2001 Mack Roll Off
#2007 Mack
#2011 Ford
#2019 Ford F150
#2019 Peterbilt
#2021 Dodge Ram Pick Up 2500
#2225 - 2022 Western Star
#2228 - 2022 Western Star
#24-2016 Western Star
#2421 - 2024 Western Star
#2422 - 2022 Western Star
#26 - 2021 Western Star
#29 - 2006 Peterbilt 379 Tractor
#31 - 2019 Peterbilt - VIN #7391
#32 -2019 Peterbilt - VIN #7411
#34 - 2006 Peterbilt 379
#46-2016 Mack
#Autocar
#Lube Truck
#Volvo Water Truck
#Vehicle Repairs & Maintenance - Other

def plot_vehicle_repairs(weekly_data, vars):
    
    fig = px.line(weekly_data, x='Week', y=vars,
                  title='Weekly Vehicle Repairs and Maintenance Components Over Time', markers=True)
    return st.plotly_chart(fig, use_container_width=True)


# Put each plot into a container with a border. 
container1 = st.container(border=True)
container2 = st.container(border=True)
container3 = st.container(border=True)
container4 = st.container(border=True)
container5 = st.container(border=True)
container6 = st.container(border=True)
container7 = st.container(border=True)
container8 = st.container(border=True)

with container1:
    plot_total_cogs(weekly_data)
with container2:
    plot_direct_labor(weekly_data)
with container3:
    plot_equipment_rental(weekly_data)
with container4:
    plot_equipment_repairs(weekly_data)
with container5:
    main_comps =  [
        "262D ODTB03831",
        "262D ODTB03833",
        "289C",
        "330",
        "345CL Excavator",
        "350 Excavator-3ML357",
        "615C",
        "7420 John Deere",
        "966E Loader",
        "966H",
        "966K ONGX00224",
        "966M",
        "966XE",
        "980G Cat Loade-S/N 2KR00957",
        "980G Loader S/N AWH00271",
        "980G Wheel Loader S/N 01819",
        "988F",
        "Bobcat",
        "Cat 3306B",
        "Cat 349E",
        "Cat 352",
        "Cat 637 Scraper",
        "Cedarapids",
        "D400",
        "D8K Dozer",
        "D8R Dozer-1473",
        "D9L Dozer",
        "D9T Dozer",
        "El Jay 1140 Crusher",
        "Finlay Wash Plants",
        "Hammel Shredder",
        "Komatsu Excavator",
        "McCloskey Crusher",
        "NEW Powerscreen",
        "Powerscreen 1700",
        "Roll Off Cans",
        "Soil Cement Plant",
        "Superior Radial Stack Conveyor",
        "Wash Plant",
        "Equipment Repairs & Maintenance - Other"
    ]
    
    selected_vars = st.multiselect("Select Maintenance Components to Plot", main_comps, default=main_comps)
   
    plot_maintenance_components(weekly_data, selected_vars)
with container6:
    materials = [
        '1" Apache Red',
        '1" Coronado Brown',
        '1/2" Apache Red',
        '1/2" Coronado Brown',
        '3"-6" Coronado Brown',
        '3/8" Apache Red',
        '3/8" Coronado Brown',
        '4-8 Rip Rap',
        '4"-8" Coronado Brown',
        '6"-12" Coronado Brown',
        "ABC",
        "Cold Mix",
        "MA FINES",
        "Materials - Other"
    ]
    
    selected_vars = st.multiselect("Select Material Components to Plot", materials, default=materials)
    plot_material_components(weekly_data, selected_vars)
with container7:
    components = [
        "11 - 2005 Kenworth T800 RO",
        "110 - 2007 Western Star",
        "2001 Mack Roll Off",
        "2007 Mack",
        "2011 Ford",
        "2019 Ford F150",
        "2019 Peterbilt",
        "2021 Dodge Ram Pick Up 2500",
        "2225 - 2022 Western Star",
        "2228 - 2022 Western Star",
        "24-2016 Western Star",
        "2421 - 2024 Western Star",
        "2422 - 2022 Western Star",
        "26 - 2021 Western Star",
        "29 - 2006 Peterbilt 379 Tractor",
        "31 - 2019 Peterbilt - VIN #7391",
        "32 -2019 Peterbilt - VIN #7411",
        "34 - 2006 Peterbilt 379",
        "46-2016 Mack",
        "Autocar",
        "Lube Truck",
        "Volvo Water Truck",
        "Vehicle Repairs & Maintenance - Other"
    ]
    selected_vars = st.multiselect("Select Vehicle Repair Components to Plot", components, default=components)
    
    plot_vehicle_repairs(weekly_data, selected_vars)
with container8:
    plot_fuel(weekly_data)

