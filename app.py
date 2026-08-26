import traceback
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("B.Sc. Geography Study Planner")

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Pk94c2vqopKnEU2nc8Dv0aW_z0_9A_TKbFixIReMSL8/edit"

try:
    # 1. Establish connection and read data
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=SPREADSHEET_URL, ttl=0)
    
    # 2. Ensure all expected columns exist
    expected_columns = ["id", "Year", "Date", "Day", "Time Slot", "Subject", "Category", "Task / Focus", "Status"]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = ""
            
    df_filtered = df[expected_columns]
    
    # Force convert everything to string to prevent pandas float type conflicts on empty cells
    df_filtered = df_filtered.astype(str).replace({"nan": "", "None": ""})
    
    # 3. Interactive Table Editor
    st.subheader("Study Schedule & Tasks")
    edited_df = st.data_editor(
        df_filtered,
        column_config={
            "id": None,  # Hide the ID column
            "Date": st.column_config.TextColumn("Date (YYYY-MM-DD)"),
        },
        num_rows="dynamic",
        key="study_planner_editor"
    )
    
    # 4. Save changes button
    if st.button("Save Changes to Google Sheet"):
        conn.update(spreadsheet=SPREADSHEET_URL, data=edited_df)
        st.success("Changes saved to Google Sheets successfully!")

except Exception as e:
    st.error("Detailed Connection Error Traceback:")
    st.code(traceback.format_exc())
    st.stop()
