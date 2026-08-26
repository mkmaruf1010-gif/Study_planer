import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Study Schedule & Task Planner",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Interactive Study & Task Planner")
st.caption("Customize your daily schedule, edit task statuses, and manage multiple sheets seamlessly.")

# 2. Session State Initialization
if "sheet1_data" not in st.session_state:
    st.session_state.sheet1_data = pd.DataFrame({
        "Time Block": ["07:00 AM - 09:00 AM", "10:00 AM - 01:00 PM", "03:30 PM - 05:30 PM", "07:00 PM - 09:00 PM"],
        "Subject / Module": ["Geographical Thoughts", "Oceanography & Coastal", "Spatial Analysis Practice", "Board Question Revision"],
        "Target Output": ["Core Paradigms", "Landform Evolution", "GIS Workflow Sketches", "2018-2023 Board Questions"],
        "Priority": ["High", "High", "Medium", "High"]
    })

if "sheet2_data" not in st.session_state:
    st.session_state.sheet2_data = pd.DataFrame({
        "Course Code": ["GEO-401", "GEO-402", "GEO-403", "GEO-404"],
        "Subject Title": ["Geographical Thoughts", "Oceanography", "Disaster Mgmt", "Applied GIS & RS"],
        "Theory Revised": [True, False, False, True],
        "Past Board Qs": [True, False, True, False],
        "Status": ["In Progress", "Not Started", "In Progress", "Completed"]
    })

# 3. Tab Layout
tab1, tab2, tab3 = st.tabs(["📌 Weekly Schedule Planner", "📊 Subject Progress Tracker", "➕ Add Custom Sheet"])

# TAB 1: Schedule Planner
with tab1:
    st.subheader("Weekly Schedule Matrix")
    st.write("Click on any cell to edit the schedule in real time:")

    edited_df1 = st.data_editor(
        st.session_state.sheet1_data,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_sheet1"
    )
    st.session_state.sheet1_data = edited_df1

    # Row addition control
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Add Row to Schedule"):
            new_row = pd.DataFrame([["00:00 AM - 00:00 AM", "New Subject", "New Target", "Low"]], 
                                   columns=st.session_state.sheet1_data.columns)
            st.session_state.sheet1_data = pd.concat([st.session_state.sheet1_data, new_row], ignore_index=True)
            st.rerun()

    # Export functionality
    csv_sheet1 = st.session_state.sheet1_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Schedule to CSV",
        data=csv_sheet1,
        file_name="Study_Schedule.csv",
        mime="text/csv"
    )

# TAB 2: Progress Tracker
with tab2:
    st.subheader("Subject Completion & Revision Tracker")
    st.write("Track your completion status across courses:")

    edited_df2 = st.data_editor(
        st.session_state.sheet2_data,
        column_config={
            "Theory Revised": st.column_config.CheckboxColumn("Theory Done?"),
            "Past Board Qs": st.column_config.CheckboxColumn("Board Qs Solved?"),
            "Status": st.column_config.SelectboxColumn(
                "Overall Status",
                options=["Not Started", "In Progress", "Completed"]
            )
        },
        num_rows="dynamic",
        use_container_width=True,
        key="editor_sheet2"
    )
    st.session_state.sheet2_data = edited_df2

    csv_sheet2 = st.session_state.sheet2_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Tracker to CSV",
        data=csv_sheet2,
        file_name="Subject_Tracker.csv",
        mime="text/csv"
    )

# TAB 3: Dynamic Custom Sheet Generator
with tab3:
    st.subheader("Create a Blank Custom Sheet")
    sheet_name = st.text_input("New Sheet Name", "Custom Project Sheet")
    num_cols = st.number_input("Number of Columns", min_value=1, max_value=10, value=3)
    
    col_names = []
    cols = st.columns(num_cols)
    for i, col in enumerate(cols):
        with col:
            col_names.append(st.text_input(f"Column {i+1} Name", f"Col_{i+1}"))
            
    if st.button("Generate Custom Sheet"):
        custom_df = pd.DataFrame(columns=col_names)
        st.session_state["custom_sheet"] = custom_df
        st.success(f"Created sheet: '{sheet_name}'")

    if "custom_sheet" in st.session_state:
        st.write("### Your Custom Sheet")
        edited_custom = st.data_editor(
            st.session_state["custom_sheet"],
            num_rows="dynamic",
            use_container_width=True
        )
        st.session_state["custom_sheet"] = edited_custom
