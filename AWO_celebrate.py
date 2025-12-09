import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("Afoosha Walgargaarsa Odaa – (Local data)")

# --- Load local Excel file ---
local_file = r"C:\Users\walfaanaam\Desktop\AWO_Celebrate\members.xlsx"

try:
    members = pd.read_excel(local_file)
except Exception as e:
    st.error(f"Cannot load local Excel file: {e}")
    st.stop()

# --- Scheduling logic ---
start_date = datetime(2025, 1, 1)
members["celebration_date"] = [start_date + timedelta(days=90 * i) for i in range(len(members))]

today = datetime.today()

def status(date):
    if date < today:
        return "✔️ Completed"
    elif (date - today).days <= 90:
        return "⭐ Next in Line"
    else:
        return "⏳ Waiting"

members["status"] = members["celebration_date"].apply(status)

st.subheader("Celebration Schedule")
st.dataframe(members)

# --- Restart round if all completed ---
if all(members["celebration_date"] < today):
    st.warning("All members completed! Starting a new round...")
    new_start = today
    members["celebration_date"] = [new_start + timedelta(days=90 * i) for i in range(len(members))]
    st.dataframe(members)
