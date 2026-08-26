import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="B.Sc. Geography Study Planner", layout="wide")
st.title("B.Sc. Geography Study Planner")

# Set your Google Sheet URL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Pk94c2vqopKnEU2nc8Dv0aW_z0_9A_TKbFixIReMSL8/edit"

# Initialize connection (reads automatically from st.secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1", ttl=0)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df["id"] = df["id"].astype(int)
except Exception as e:
    st.error(f"Could not connect to Google Sheets. Verify your secrets configuration: {e}")
    st.stop()

# Interactive Table Editor
edited_df = st.data_editor(
    df[["id", "Date", "Day", "Time Slot", "Subject", "Category", "Task / Focus", "Status"]],
    column_config={
        "id": None,
        "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD", required=True),
        "Day": st.column_config.SelectboxColumn("Day", options=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]),
        "Status": st.column_config.CheckboxColumn("Status", default=False)
    },
    disabled=["Time Slot", "Category"],
    hide_index=True,
    use_container_width=True
)

# Auto-sync changes back to Google Sheets
if not edited_df.equals(df[["id", "Date", "Day", "Time Slot", "Subject", "Category", "Task / Focus", "Status"]]):
    for idx, row in edited_df.iterrows():
        df.loc[df["id"] == row["id"], ["Date", "Day", "Subject", "Task / Focus", "Status"]] = [
            row["Date"], row["Day"], row["Subject"], row["Task / Focus"], row["Status"]
        ]
    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Sheet1", data=df)
    st.toast("Saved to Google Sheets!", icon="☁️")
