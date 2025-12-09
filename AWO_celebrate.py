import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime, timedelta

st.title("Afoosha Walgargaarsa Odaa – Celebration Schedule")

# --- Load Excel file from GitHub ---
github_excel_url = "https://raw.githubusercontent.com/Walfaanaa/AWO_c/main/members.xlsx"

try:
    file_content = requests.get(github_excel_url).content
    members = pd.read_excel(BytesIO(file_content))
except Exception as e:
    st.error(f"Cannot load Excel file from GitHub: {e}")
    st.stop()

# --- Scheduling logic ---
start_date = datetime(2025, 1, 1)
members["celebration_date"] = [
    start_date + timedelta(days=90 * i) for i in range(len(members))
]

today = datetime.today()

def status(date):
    days_left = (date - today).days
    if date < today:
        return "✔️ Completed"
    elif days_left <= 90:
        return "⭐ Next in Line"
    else:
        return "⏳ Waiting"

members["status"] = members["celebration_date"].apply(status)

# --- Display results ---
st.subheader("Celebration Schedule")
st.dataframe(members)

# --- Restart round if all are completed ---
if all(members["celebration_date"] < today):
    st.warning("All members completed! Starting a new round...")

    new_start = today
    members["celebration_date"] = [
        new_start + timedelta(days=90 * i) for i in range(len(members))
    ]

    members["status"] = members["celebration_date"].apply(status)

    st.subheader("New Round Schedule")
    st.dataframe(members)
