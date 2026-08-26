import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="B.Sc. Geography Study Planner", layout="wide")

# Custom CSS for Dark Theme and Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 25px;
        color: #00E5FF;
        text-shadow: 0 0 10px rgba(0,229,255,0.3);
    }
    .metric-container {
        text-align: center;
        padding: 15px;
        background-color: #1E1E1E;
        border-radius: 10px;
        border: 1px solid #333333;
    }
    .metric-label {
        font-size: 13px;
        letter-spacing: 0.5px;
        color: #A0A0A0;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #00E5FF;
        margin-top: 5px;
    }
    .divider {
        border-right: 1px solid #333333;
        height: 50px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">B.Sc. Geography Study Planner</div>', unsafe_allow_html=True)

# 1. Syllabus Courses Mapping (from Dhaka University Syllabus)
YEAR_COURSES = {
    "1st Year": [
        "GETh: 1001 - Geographical Thoughts and Concepts",
        "GETh: 1002 - Introduction to Physical Geography",
        "GETh: 1003 - Introduction to Human Geography",
        "GETh: 1004 - Concept of Region and World Regional Pattern",
        "GETh: 1005 - Fundamentals of English Language",
        "GELb: 1006 - Fundamentals of Cartography",
        "GELb: 1007 - Introduction to Computer in Geography and Environment",
        "211501 - History of the Emergence of Independent Bangladesh",
        "GEV: 1008 - Field Study + Viva Voce"
    ],
    "2nd Year": [
        "GETh: 2001 - Environmental Chemistry",
        "GETh: 2002 - Geomorphology",
        "GETh: 2003 - Climatology",
        "GETh: 4004 - Economic Geography",
        "GETh: 2005 - Cultural Geography",
        "GETh: 2006 - Quantitative Techniques in Geography - I",
        "GELb: 2007 - Computer Cartography and Map Projection",
        "GELb: 2008 - Field Work in Physical Geography",
        "GEV: 2009 - Viva Voce"
    ],
    "3rd Year": [
        "GETh: 3001 - Oceanography",
        "GETh: 3002 - Geography of Soil",
        "GETh: 3003 - Biogeography",
        "GETh: 3004 - Population Geography",
        "GETh: 3005 - Geography of Settlement",
        "GETh: 3006 - Geography of Bangladesh",
        "GELb: 3007 - Environmental Analysis",
        "GELb: 3008 - Introduction to GIS",
        "GELb: 3009 - Surveying",
        "GELb: 3010 - Research Methods in Geography",
        "GELb: 3011 - Field Work in Human Geography",
        "GEV: 3012 - Viva-voce"
    ],
    "4th Year": [
        "GETh: 4001 - Hydrology and Fluvial Morphology",
        "GETh: 4002 - Disaster Management",
        "GETh: 4003 - Regional Geography and Environment of South Asia",
        "GETh: 4004 - Transport Geography",
        "GETh: 4005 - Urban Geography",
        "GETh: 4006 - Political Geography",
        "GELb: 4007 - Quantitative Techniques in Geography - II",
        "GELb: 4008 - Map Interpretation",
        "GELb: 4009 - Remote Sensing",
        "GELb: 4010 - Land Use Survey",
        "GEV: 4011 - Viva-voce"
    ]
}

# 2. Function to load fresh default data
def load_initial_data():
    return pd.DataFrame([
        # 1st Year Schedule
        {"Year": "1st Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 1001 - Geographical Thoughts and Concepts", "Category": "Theoretical", "Task / Focus": "Qus", "Status": False},
        {"Year": "1st Year", "Day": "Mon", "Time Slot": "10:00 AM - 01:00 PM (Deep Work Block 2)", "Subject": "GETh: 1001 - Geographical Thoughts and Concepts", "Category": "Theoretical", "Task / Focus": "Diagram / Lab Practice", "Status": False},
        {"Year": "1st Year", "Day": "Tue", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 1002 - Introduction to Physical Geography", "Category": "Theoretical", "Task / Focus": "Earth Crust & Lithosphere Notes", "Status": True},
        {"Year": "1st Year", "Day": "Wed", "Time Slot": "03:30 PM - 05:30 PM (Light Work Block 3)", "Subject": "GELb: 1006 - Fundamentals of Cartography", "Category": "Technical", "Task / Focus": "Scale Calculations", "Status": False},
        {"Year": "1st Year", "Day": "Thu", "Time Slot": "07:00 PM - 09:00 PM (Revision)", "Subject": "GETh: 1005 - Fundamentals of English Language", "Category": "Revision", "Task / Focus": "Grammar Practice", "Status": False},
        {"Year": "1st Year", "Day": "Fri", "Time Slot": "09:00 AM - 11:30 AM (Morning Study)", "Subject": "GELb: 1007 - Introduction to Computer in Geography and Environment", "Category": "Practical", "Task / Focus": "MS Excel Practice", "Status": False},
        {"Year": "1st Year", "Day": "Sat", "Time Slot": "04:00 PM - 06:00 PM (Lab Block)", "Subject": "GETh: 1003 - Introduction to Human Geography", "Category": "Theoretical", "Task / Focus": "Population Dynamics", "Status": False},
        {"Year": "1st Year", "Day": "Sun", "Time Slot": "08:00 PM - 10:00 PM (Weekly Review)", "Subject": "GEV: 1008 - Field Study + Viva Voce", "Category": "Practical", "Task / Focus": "Fieldwork Report Draft", "Status": False},
        
        # 2nd Year Schedule
        {"Year": "2nd Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 2002 - Geomorphology", "Category": "Theoretical", "Task / Focus": "Davisian Cycle of Erosion", "Status": False},
        {"Year": "2nd Year", "Day": "Wed", "Time Slot": "10:00 AM - 01:00 PM (Deep Work Block 2)", "Subject": "GETh: 2003 - Climatology", "Category": "Technical", "Task / Focus": "Inversion of Temperature", "Status": False},
        {"Year": "2nd Year", "Day": "Sat", "Time Slot": "02:00 PM - 05:00 PM (Practical)", "Subject": "GELb: 2007 - Computer Cartography and Map Projection", "Category": "Practical", "Task / Focus": "Mercator Projection Construction", "Status": True},
 {"Year": "2nd Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 2002 - Geomorphology", "Category": "Theoretical", "Task / Focus": "Davisian Cycle of Erosion", "Status": False},
         {"Year": "2nd Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 2002 - Geomorphology", "Category": "Theoretical", "Task / Focus": "Davisian Cycle of Erosion", "Status": False},
         {"Year": "2nd Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 2002 - Geomorphology", "Category": "Theoretical", "Task / Focus": "Davisian Cycle of Erosion", "Status": False},
         {"Year": "2nd Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 2002 - Geomorphology", "Category": "Theoretical", "Task / Focus": "Davisian Cycle of Erosion", "Status": False},
         {"Year": "2nd Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 2002 - Geomorphology", "Category": "Theoretical", "Task / Focus": "Davisian Cycle of Erosion", "Status": False},
         {"Year": "2nd Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 2002 - Geomorphology", "Category": "Theoretical", "Task / Focus": "Davisian Cycle of Erosion", "Status": False},
         {"Year": "2nd Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 2002 - Geomorphology", "Category": "Theoretical", "Task / Focus": "Davisian Cycle of Erosion", "Status": False},
        # 3rd Year Schedule
        {"Year": "3rd Year", "Day": "Tue", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 3001 - Oceanography", "Category": "Theoretical", "Task / Focus": "Ocean Currents & Waves", "Status": False},
        {"Year": "3rd Year", "Day": "Thu", "Time Slot": "10:00 AM - 01:00 PM (GIS Lab)", "Subject": "GELb: 3008 - Introduction to GIS", "Category": "Practical", "Task / Focus": "ArcMap Digitizing & Overlaying", "Status": True},

        # 4th Year Schedule
        {"Year": "4th Year", "Day": "Mon", "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)", "Subject": "GETh: 4001 - Hydrology and Fluvial Morphology", "Category": "Theoretical", "Task / Focus": "Drainage Basin Analysis", "Status": False},
        {"Year": "4th Year", "Day": "Fri", "Time Slot": "03:00 PM - 06:00 PM (RS Lab)", "Subject": "GELb: 4009 - Remote Sensing", "Category": "Technical", "Task / Focus": "NDVI Image Classification", "Status": False}
    ])

# Safety check: Initialize or reset state if 'Year' column is missing
if "planner_data" not in st.session_state or "Year" not in st.session_state.planner_data.columns:
    st.session_state.planner_data = load_initial_data()

df = st.session_state.planner_data

# 3. Dropdowns and Filters Selection
col_year, col_day, col_cat = st.columns(3)

with col_year:
    selected_year = st.selectbox("Select Academic Year (Syllabus)", list(YEAR_COURSES.keys()))

with col_day:
    week_days = ["All", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    selected_day = st.selectbox("Filter Day", week_days)

with col_cat:
    categories = ["All"] + sorted(list(df["Category"].unique()))
    selected_category = st.selectbox("Filter Category", categories)

# Apply dynamic filtering logic safely
filtered_df = df[df["Year"] == selected_year].copy()

if selected_day != "All":
    filtered_df = filtered_df[filtered_df["Day"] == selected_day]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# 4. Filtered Stats Metrics
total_slots = len(filtered_df)
done_tasks = int(filtered_df["Status"].sum()) if total_slots > 0 else 0

m_col1, m_col2, m_col3 = st.columns([2, 0.1, 2])

with m_col1:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">FILTERED SLOTS ({selected_year.upper()})</div>
            <div class="metric-value">{total_slots}</div>
        </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">TASKS DONE</div>
            <div class="metric-value">{done_tasks} / {total_slots}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# 5. Table Display
edited_df = st.data_editor(
    filtered_df[["Day", "Time Slot", "Subject", "Category", "Task / Focus", "Status"]],
    column_config={
        "Subject": st.column_config.SelectboxColumn(
            "Subject",
            help="Syllabus-defined subjects for selected year",
            options=YEAR_COURSES[selected_year],
            required=True
        ),
        "Day": st.column_config.SelectboxColumn(
            "Day",
            options=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            required=True
        ),
        "Status": st.column_config.CheckboxColumn(
            "Status (Checkbox)",
            help="Toggle task completion",
            default=False
        )
    },
    disabled=["Time Slot", "Category", "Task / Focus"],
    hide_index=True,
    use_container_width=True
)

# Sync table modifications back to session memory
for idx, row in edited_df.iterrows():
    st.session_state.planner_data.loc[
        (st.session_state.planner_data["Year"] == selected_year) & 
        (st.session_state.planner_data["Time Slot"] == row["Time Slot"]), 
        ["Status", "Subject", "Day"]
    ] = [row["Status"], row["Subject"], row["Day"]]
