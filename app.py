import traceback
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Make the page wide to expand the sheet view across the screen
st.set_page_config(page_title="B.Sc. Geography Study Planner", layout="wide")

st.title("B.Sc. Geography Study Planner")

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Pk94c2vqopKnEU2nc8Dv0aW_z0_9A_TKbFixIReMSL8/edit"

try:
    # 2. Establish connection and read data
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=SPREADSHEET_URL, ttl=0)
    
    # 3. Ensure all expected columns exist
    expected_columns = ["id", "Year", "Date", "Day", "Time Slot", "Subject", "Category", "Task / Focus", "Status"]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = ""
            
    df_filtered = df[expected_columns]
    
    # Clean up blank/NaN/None values so the table starts clean
    df_filtered = df_filtered.fillna("")
    for col in df_filtered.columns:
        df_filtered[col] = df_filtered[col].astype(str).replace({"nan": "", "None": "", "<NA>": ""})
        
    # Convert Status column safely to boolean format for checkboxes
    if "Status" in df_filtered.columns:
        df_filtered["Status"] = df_filtered["Status"].apply(
            lambda x: True if str(x).lower() in ["true", "1", "yes", "completed", "done"] else False
        )

    # 4. Interactive Table Editor with Official Syllabus Subjects
    st.subheader("Study Schedule & Tasks")
    edited_df = st.data_editor(
        df_filtered,
        column_config={
            "id": None,  # Hide the internal ID column
            "Year": st.column_config.SelectboxColumn(
                "Year",
                options=["1st Year", "2nd Year", "3rd Year", "4th Year"],
                required=False,
            ),
            "Date": st.column_config.TextColumn("Date (YYYY-MM-DD)"),
            "Day": st.column_config.SelectboxColumn(
                "Day",
                options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                required=False,
            ),
            "Time Slot": st.column_config.SelectboxColumn(
                "Time Slot",
                options=["08:00 - 10:00", "10:00 - 12:00", "13:00 - 15:00", "15:00 - 17:00", "18:00 - 20:00"],
                required=False,
            ),
            "Subject": st.column_config.SelectboxColumn(
                "Subject",
                options=[
                    # First Year Courses
                    "[1st Year] Geographical Thoughts and Concepts",
                    "[1st Year] Introduction to Physical Geography",
                    "[1st Year] Introduction to Human Geography",
                    "[1st Year] Concept of Region and World Regional Pattern",
                    "[1st Year] Fundamentals of English Language",
                    "[1st Year] Fundamentals of Cartography",
                    "[1st Year] Introduction to Computer in Geography and Environment",
                    "[1st Year] History of the Emergence of Independent Bangladesh",
                
                    
                    # Second Year Courses
                    "[2nd Year] Environmental Chemistry",
                    "[2nd Year] Geomorphology",
                    "[2nd Year] Climatology",
                    "[2nd Year] Economic Geography",
                    "[2nd Year] Cultural Geography",
                    "[2nd Year] Quantitative Techniques in Geography - I",
                    "[2nd Year] Computer Cartography and Map Projection",
                
                    
                    # Third Year Courses
                    "[3rd Year] Oceanography",
                    "[3rd Year] Geography of Soil",
                    "[3rd Year] Biogeography",
                    "[3rd Year] Population Geography",
                    "[3rd Year] Geography of Settlement",
                    "[3rd Year] Geography of Bangladesh",
                    "[3rd Year] Environmental Analysis",
                    "[3rd Year] Introduction to GIS",
                    "[3rd Year] Surveying",
                    "[3rd Year] Research Methods in Geography",
                   
                    
                    # Fourth Year Courses
                    "[4th Year] Hydrology and Fluvial Morphology",
                    "[4th Year] Disaster Management",
                    "[4th Year] Regional Geography and Environment of South Asia",
                    "[4th Year] Transport Geography",
                    "[4th Year] Urban Geography",
                    "[4th Year] Political Geography",
                    "[4th Year] Quantitative Techniques in Geography - II",
                    "[4th Year] Map Interpretation",
                    "[4th Year] Remote Sensing",
                    
                ],
                required=False,
            ),
            "Category": st.column_config.SelectboxColumn(
                "Category",
                options=["Theory", "Practical", "Assignment", "Revision", "Exam Prep"],
                required=False,
            ),
            "Status": st.column_config.CheckboxColumn(
                "Completed?",
                default=False,
            ),
        },
        num_rows="dynamic",
        use_container_width=True,
        height=550,
        key="study_planner_editor"
    )
    
    # 5. Save changes button
    if st.button("Save Changes to Google Sheet", type="primary"):
        save_df = edited_df.copy()
        if "Status" in save_df.columns:
            save_df["Status"] = save_df["Status"].apply(lambda x: "Completed" if x else "Pending")
            
        conn.update(spreadsheet=SPREADSHEET_URL, data=save_df)
        st.success("Changes saved to Google Sheets successfully!")

except Exception as e:
    st.error("Detailed Connection Error Traceback:")
    st.code(traceback.format_exc())
    st.stop()
