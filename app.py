import io
import pandas as pd
import streamlit as st

# 1. Page Configuration & Theme
st.set_page_config(
    page_title="7-Day Revision & Task Planner", page_icon="📅", layout="wide"
)

st.markdown(
    """
<style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .stButton>button { background-color: #38bdf8; color: #0f172a; font-weight: bold; border-radius: 6px; border: none; }
    .stButton>button:hover { background-color: #0284c7; color: #ffffff; }
    div[data-testid="stMetricValue"] { color: #38bdf8; }
</style>
""",
    unsafe_allow_html=True,
)

# 2. Application Header
st.title("📅 7-Day Intensive Revision Planner")
st.caption("All-in-one interactive study schedule and task tracker")

# 3. Default Dataset Initialization
DEFAULT_SCHEDULE = {
    "Mon (Day 1)": {
        "Subject": "Geographical Thoughts & Concepts",
        "Topic": "Core Paradigms, Determinism vs Possibilism",
        "Time": "07:00 AM - 09:00 AM",
    },
    "Tue (Day 2)": {
        "Subject": "Oceanography & Coastal Geomorphology",
        "Topic": "Marine Relief & Shoreline Dynamics",
        "Time": "07:00 AM - 09:00 AM",
    },
    "Wed (Day 3)": {
        "Subject": "Environmental Hazards & Disaster Mgmt",
        "Topic": "Flood & Cyclone Dynamics",
        "Time": "07:00 AM - 09:00 AM",
    },
    "Thu (Day 4)": {
        "Subject": "Applied GIS & Remote Sensing",
        "Topic": "Digital Image Processing & NDWI/NDVI",
        "Time": "07:00 AM - 09:00 AM",
    },
    "Fri (Day 5)": {
        "Subject": "Urban Geography & Settlement Studies",
        "Topic": "Urban Structure Models & UHI Patterns",
        "Time": "07:00 AM - 09:00 AM",
    },
    "Sat (Day 6)": {
        "Subject": "Geography of Asia & Regional Dev",
        "Topic": "Asian Economy & Resource Distribution",
        "Time": "07:00 AM - 09:00 AM",
    },
    "Sun (Day 7)": {
        "Subject": "Research Methodology & Practical",
        "Topic": "Sampling, Quantitative Methods & Viva Prep",
        "Time": "07:00 AM - 09:00 AM",
    },
}

if "tracker_data" not in st.session_state:
    st.session_state.tracker_data = pd.DataFrame([
        {
            "Subject": "Geographical Thoughts",
            "Theory Revised": True,
            "Past Papers Solved": True,
            "Diagrams Prepared": False,
            "Status": "In Progress",
        },
        {
            "Subject": "Oceanography & Coastal",
            "Theory Revised": True,
            "Past Papers Solved": False,
            "Diagrams Prepared": True,
            "Status": "In Progress",
        },
        {
            "Subject": "Environmental Hazards",
            "Theory Revised": False,
            "Past Papers Solved": False,
            "Diagrams Prepared": False,
            "Status": "Not Started",
        },
        {
            "Subject": "Applied GIS & RS",
            "Theory Revised": True,
            "Past Papers Solved": True,
            "Diagrams Prepared": True,
            "Status": "Completed",
        },
        {
            "Subject": "Urban Geography",
            "Theory Revised": False,
            "Past Papers Solved": False,
            "Diagrams Prepared": False,
            "Status": "Not Started",
        },
        {
            "Subject": "Geography of Asia",
            "Theory Revised": False,
            "Past Papers Solved": False,
            "Diagrams Prepared": False,
            "Status": "Not Started",
        },
        {
            "Subject": "Research Methodology",
            "Theory Revised": False,
            "Past Papers Solved": False,
            "Diagrams Prepared": False,
            "Status": "Not Started",
        },
    ])

# 4. Multi-Tab Navigation Interface
tab1, tab2, tab3 = st.tabs(
    ["🗓️ Daily Schedule Planner", "📊 Syllabus Revision Tracker", "📥 Export Data"]
)

# Tab 1: Interactive Time Blocks
with tab1:
  selected_day = st.selectbox(
      "Select Day:", list(DEFAULT_SCHEDULE.keys())
  )
  day_info = DEFAULT_SCHEDULE[selected_day]

  c1, c2, c3 = st.columns([2, 2, 1])
  c1.metric("Subject Focus", day_info["Subject"])
  c2.metric("Target Topics", day_info["Topic"])
  c3.metric("Primary Slot", day_info["Time"])

  st.markdown("---")
  st.subheader(f"Time Blocks for {selected_day}")

  blocks_df = pd.DataFrame([
      {
          "Time Slot": "07:00 AM - 09:00 AM",
          "Block": "Deep Work 1",
          "Task": f"{day_info['Subject']}: Core Concepts",
          "Completed": True,
      },
      {
          "Time Slot": "10:00 AM - 01:00 PM",
          "Block": "Deep Work 2",
          "Task": f"{day_info['Topic']} Analysis",
          "Completed": False,
      },
      {
          "Time Slot": "03:30 PM - 05:30 PM",
          "Block": "Light Work",
          "Task": "Diagrams, Maps & Notes Review",
          "Completed": False,
      },
      {
          "Time Slot": "07:00 PM - 09:00 PM",
          "Block": "Revision",
          "Task": "Past Board Questions Practice",
          "Completed": False,
      },
  ])

  st.data_editor(
      blocks_df,
      num_rows="dynamic",
      use_container_width=True,
      key=f"blocks_{selected_day}",
  )

# Tab 2: Interactive Subject Tracker
with tab2:
  st.subheader("Subject-Wise Progress Matrix")

  edited_tracker = st.data_editor(
      st.session_state.tracker_data,
      column_config={
          "Theory Revised": st.column_config.CheckboxColumn("Theory Done"),
          "Past Papers Solved": st.column_config.CheckboxColumn(
              "Papers Solved"
          ),
          "Diagrams Prepared": st.column_config.CheckboxColumn("Diagrams Done"),
          "Status": st.column_config.SelectboxColumn(
              "Status", options=["Not Started", "In Progress", "Completed"]
          ),
      },
      num_rows="dynamic",
      use_container_width=True,
      key="tracker_editor",
  )
  st.session_state.tracker_data = edited_tracker

# Tab 3: Export Features
with tab3:
  st.subheader("Download Schedule & Data")

  csv_bytes = st.session_state.tracker_data.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 Download Tracker as CSV",
      data=csv_bytes,
      file_name="Revision_Tracker.csv",
      mime="text/csv",
  )
