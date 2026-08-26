import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="B.Sc. Geography Study Planner", layout="wide")

# Custom CSS for styling to match screenshot aesthetics
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: 400;
        margin-bottom: 25px;
        color: #1A1A1A;
    }
    .metric-container {
        text-align: center;
        padding: 10px;
    }
    .metric-label {
        font-size: 13px;
        letter-spacing: 0.5px;
        color: #555555;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #1A1A1A;
        margin-top: 4px;
    }
    .divider {
        border-right: 1px solid #CCCCCC;
        height: 40px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">B.Sc. Geography Study Planner</div>', unsafe_allow_html=True)

# Sample Data Initializer
if "planner_data" not in st.session_state:
    st.session_state.planner_data = pd.DataFrame([
        {
            "id": 1,
            "Day": "Mon",
            "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)",
            "Subject": "Geographical Thoughts",
            "Category": "Theoretical",
            "Task / Focus": "Diagram / Lab Practice",
            "Status": False
        },
        {
            "id": 2,
            "Day": "Mon",
            "Time Slot": "10:00 AM - 01:00 PM (Deep Work Block 2)",
            "Subject": "Geographical Thoughts",
            "Category": "Theoretical",
            "Task / Focus": "Diagram / Lab Practice",
            "Status": False
        },
        {
            "id": 3,
            "Day": "Mon",
            "Time Slot": "03:30 PM - 05:30 PM (Light Work Block 3)",
            "Subject": "Geographical Thoughts",
            "Category": "Technical",
            "Task / Focus": "Diagram / Lab Practice",
            "Status": False
        },
        {
            "id": 4,
            "Day": "Mon",
            "Time Slot": "07:00 PM - 09:00 PM (Revision & Past Board Questions)",
            "Subject": "Geographical Thoughts",
            "Category": "Revision",
            "Task / Focus": "Past Board Questions",
            "Status": False
        },
        {
            "id": 5,
            "Day": "Tue",
            "Time Slot": "07:00 AM - 09:00 AM (Deep Work Block 1)",
            "Subject": "Geomorphology",
            "Category": "Theoretical",
            "Task / Focus": "Map Drawing",
            "Status": False
        },
        {
            "id": 6,
            "Day": "Wed",
            "Time Slot": "10:00 AM - 01:00 PM (Deep Work Block 2)",
            "Subject": "Climatology",
            "Category": "Practical",
            "Task / Focus": "Data Calculation",
            "Status": True
        }
    ])

# Helper filters logic
df = st.session_state.planner_data

# Bottom Filters Setup
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    days = ["All"] + sorted(list(df["Day"].unique()))
    selected_day = st.selectbox("Filter Day", days)

with col_filter2:
    categories = ["All"] + sorted(list(df["Category"].unique()))
    selected_category = st.selectbox("Filter Category", categories)

# Apply filtering
filtered_df = df.copy()

if selected_day != "All":
    filtered_df = filtered_df[filtered_df["Day"] == selected_day]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# Metric Display Section
total_slots = len(filtered_df)
done_tasks = int(filtered_df["Status"].sum())

m_col1, m_col2, m_col3 = st.columns([2, 0.1, 2])

with m_col1:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">FILTERED SLOTS</div>
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

# Table Display with interactive Status Checkbox
edited_df = st.data_editor(
    filtered_df[["Day", "Time Slot", "Subject", "Category", "Task / Focus", "Status"]],
    column_config={
        "Status": st.column_config.CheckboxColumn(
            "Status (Checkbox)",
            help="Toggle task completion status",
            default=False,
        )
    },
    disabled=["Day", "Time Slot", "Subject", "Category", "Task / Focus"],
    hide_index=True,
    use_container_width=True
)

# Sync table modifications back to session memory
for idx, row in edited_df.iterrows():
    st.session_state.planner_data.loc[
        st.session_state.planner_data["Time Slot"] == row["Time Slot"], "Status"
    ] = row["Status"]
