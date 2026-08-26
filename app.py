import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("B.Sc. Geography Study Planner")

# Create connection
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Pk94c2vqopKnEU2nc8Dv0aW_z0_9A_TKbFixIReMSL8/edit"
    
    # Read the first worksheet automatically
    df = conn.read(spreadsheet="SPREADSHEET_URL", ttl=0)
    
    st.success("Successfully connected to Google Sheets!")
    
    # Display the raw data to confirm everything works
    st.dataframe(df)
    
except Exception as e:
    st.error(f"Detailed Connection Error: {e}")
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
    conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1Pk94c2vqopKnEU2nc8Dv0aW_z0_9A_TKbFixIReMSL8/edit?"
, worksheet="Sheet1", data=df)
    st.toast("Saved to Google Sheets!", icon="☁️")
