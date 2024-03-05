import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

def create_quarterly_rental_df(df):
    monthly_rental_df = df.resample(rule='M', on='dteday').agg({
                        "cnt": "sum"})
    monthly_rental_df.reset_index(inplace=True)
    monthly_rental_df.rename(columns={"cnt": "monthly_count"}, inplace=True)
    return monthly_rental_df

# Load cleaned data
day_df = pd.read_csv("day.csv")
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
day_df["temp_group"] = day_df.temp.apply(lambda x: "Cold" if x <= 0.25 else ("Hot" if x > 0.75 else ("Cool" if x < 0.5 else "Warm")))



# filter data
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

print(min_date, max_date)
with st.sidebar:
    st.title("Bike Rental Dashboard")
    start_date, end_date = st.date_input(label="Rentang Waktu",
                                         min_value=min_date,
                                         max_value=max_date,
                                         value=[min_date, max_date])
    
main_df = day_df[(day_df["dteday"] > pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]

# menyiapkan dataframe untuk visualisasi
monthly_rental_df = create_quarterly_rental_df(main_df)

# Visualisasi
st.title("Quarterly Bike Rental")
col1, col2 = st.columns(2)
with col1:
    total_rental = monthly_rental_df["monthly_count"].sum()
    st.metric(label="Total Rental", value=total_rental, delta=0)

with col2:
    average_rental = monthly_rental_df["monthly_count"].mean()
    st.metric(label="Average Rental per Month", value=average_rental, delta=0)

fig, ax = plt.subplots()
sns.lineplot(data=monthly_rental_df, x="dteday", y="monthly_count", ax=ax)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="cnt", 
    y="temp_group",
    data=main_df.sort_values(by="temp_group", ascending=False),
    palette=colors,
    ax=ax
)

ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.title("Bike Rental by Temperature Group")
st.pyplot(fig)