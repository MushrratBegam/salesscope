import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path 



# Load dataset
# df = pd.read_excel("./salesscope/dataset/Financial_Sample.xlsx")
df = pd.read_excel(Path(__file__).parent / "dataset" / "Financial_Sample.xlsx")



# Removing Missing Values
for col in df.columns:
    if df[col].isnull().sum()>0:
        if df [col].dtype == 'str':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].mean())
            
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)
st.title("Sales_Analysis_Dashboard")
filtered_df = df.copy()
col1 , col2 , col3 , col4 , col5 = st.columns(5)
with col1:
    country = st.selectbox("Select Country", ['All']+list(filtered_df['Country'].unique()))
    if country != "All":
      filtered_df = filtered_df[filtered_df['Country'] == country]
with col2:
    Segment = st.selectbox("Select Segment", ['All']+list(df["Segment"].unique()))
    if Segment != "All":
        filtered_df = filtered_df[filtered_df['Segment'] == Segment]
with col3:
    product = st.selectbox("Select Product",["All"]+list(df["Product"].unique()))
    if product != "All":
        filtered_df = filtered_df[filtered_df['Product'] == product]
with col4:
    db = st.selectbox("Select Discount Band",["All"]+list(df['Discount Band'].unique()))
    if db    != "All":
        filtered_df = filtered_df[filtered_df['Discount Band'] == db] 
with col5:
    year = st.selectbox("Select Year",["All"]+list(df['Year'].unique()))
    if year != "All":
        filtered_df = filtered_df[filtered_df['Year'] == year]
        
# KPI : Key Point Indicator
# col1 , col2 , col3 , col4 , col5 , col6 = st.columns([2,1.5,1,1,1,1])
# with col1:
#     st.metric("Total Sales", round(filtered_df[' Sales'].sum(),2))
# with col2:
#     st.metric("Total Profit", round(filtered_df['Profit'].sum(),2))
# with col3:
#     st.metric("Total Sold Quantity", round(filtered_df['Units Sold'].sum(),2))
# with col4:
#     st.metric("Total Discount", round(filtered_df['Discounts'].sum(),2))
# with col5:
#     st.metric("Total Orders", filtered_df.shape[0])
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Sales", f"{filtered_df[' Sales'].sum()/1e6:.2f}M")
with col2:
    st.metric("Total Profit", f"{filtered_df['Profit'].sum()/1e6:.2f}M")
with col3:
    st.metric("Total Sold Quantity", f"{filtered_df['Units Sold'].sum()/1e6:.2f}M")
with col4:
    st.metric("Total Discount", f"{filtered_df['Discounts'].sum()/1e6:.2f}M")
with col5:
    st.metric("Total Orders", f"{filtered_df.shape[0]:,}")
    
col1 , col2 = st.columns(2)
with col1:
    fig = px.bar(
        filtered_df.groupby("Segment", as_index=False)["Profit"].mean(),
        x="Segment", y="Profit", color="Segment",
        title = "Profit by Segment",
        template="plotly_dark",
        
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.histogram(
        filtered_df, x="Profit", nbins=50, marginal="box",
        color_discrete_sequence=["#00D4FF"],
        title = "Profit Distribution",
        template="plotly_dark",
        
    )
    st.plotly_chart(fig, use_container_width=True)

sbm = (
    filtered_df.groupby(["Month Number", "Month Name"], as_index=False)[" Sales"].sum()
    .sort_values("Month Number")
)
fig = px.line(
    sbm, x="Month Name", y=" Sales", markers=True,
    title="Monthly Sales Trend",
    template="plotly_dark",
)
fig.update_traces(line_color="#FF4B8B", line_width=3)
st.plotly_chart(fig, use_container_width=True)
st.dataframe(filtered_df, height=350)

    


    

