import traceback
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Set wide layout for the screen
st.set_page_config(page_title="B.Sc. Geography Study Planner", layout="wide")

# Custom CSS to make headers and table headers highly visible, bold, and modern
st.markdown(
    """
    <style>
        /* Main Application Title */
        h1 {
            color: #0F172A !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        
        /* Section Subheaders / Titles */
        h3, h2 {
            color: #1E293B !important;
            font-weight: 700 !important;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 6px;
            margin-top: 15px;
        }

        /* Highlight Table / Data Editor Column Headers */
        .stDataEditor th, .stDataFrame th, div[data-testid="stDataEditor"] th {
            background-color: #1E293B !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("B.Sc. Geography Study Planner")

SPREADSHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1Pk94c2vqopKnEU2nc8Dv0aW_z0_9A_TKbFixIReMSL8/edit"
)

try:
  # Establish connection and read data
  conn = st.connection("gsheets", type=GSheetsConnection)
  df = conn.read(spreadsheet=SPREADSHEET_URL, ttl=0)

  # Ensure all expected columns exist
  expected_columns = [
      "id",
      "Year",
      "Date",
      "Day",
      "Time Slot",
      "Subject",
      "Category",
      "Task / Focus",
      "Status",
  ]
  for col in expected_columns:
    if col not in df.columns:
      df[col] = ""

  df = df[expected_columns].fillna("")
  for col in df.columns:
    df[col] = df[col].astype(str).replace({"nan": "", "None": "", "<NA>": ""})

  # Convert Status column safely to boolean format for checkboxes
  if "Status" in df.columns:
    df["Status"] = df["Status"].apply(
        lambda x: (
            True
            if str(x).lower() in ["true", "1", "yes", "completed", "done"]
            else False
        )
    )

  # Official Curriculum mapping by Academic Year
  subjects_by_year = {
      "1st Year": [
          "Geographical Thoughts and Concepts",
          "Introduction to Physical Geography",
          "Introduction to Human Geography",
          "Concept of Region and World Regional Pattern",
          "Fundamentals of English Language",
          "Fundamentals of Cartography",
          "Introduction to Computer in Geography and Environment",
          "History of the Emergence of Independent Bangladesh",
          "Field Study & Viva-Voce",
      ],
      "2nd Year": [
          "Environmental Chemistry",
          "Geomorphology",
          "Climatology",
          "Economic Geography",
          "Cultural Geography",
          "Quantitative Techniques in Geography - I",
          "Computer Cartography and Map Projection",
      ],
      "3rd Year": [
          "Oceanography",
          "Geography of Soil",
          "Biogeography",
          "Population Geography",
          "Geography of Settlement",
          "Geography of Bangladesh",
          "Environmental Analysis",
          "Introduction to GIS",
          "Surveying",
          "Research Methods in Geography",
      ],
      "4th Year": [
          "Hydrology and Fluvial Morphology",
          "Disaster Management",
          "Regional Geography and Environment of South Asia",
          "Transport Geography",
          "Urban Geography",
          "Political Geography",
          "Quantitative Techniques in Geography - II",
          "Map Interpretation",
          "Remote Sensing",
      ],
  }

  # Year selector control at the top with a prominent visual header
  st.markdown("### 📌 Select Academic Year to Manage")
  selected_year = st.selectbox(
      "Choose Year",
      options=["1st Year", "2nd Year", "3rd Year", "4th Year"],
      label_visibility="collapsed",
  )

  # Filter DataFrame for the selected year
  df_filtered = df[df["Year"] == selected_year].copy()

  # High-visibility subheader for the schedule table
  st.markdown(f"### 📅 Study Schedule & Tasks — {selected_year}")

  edited_df = st.data_editor(
      df_filtered,
      column_config={
          "id": None,
          (
              "Year"
          ): None,  # Hidden because the year selector controls it globally for this view
          "Date": st.column_config.TextColumn("Date (YYYY-MM-DD)"),
          "Day": st.column_config.SelectboxColumn(
              "Day",
              options=[
                  "Monday",
                  "Tuesday",
                  "Wednesday",
                  "Thursday",
                  "Friday",
                  "Saturday",
                  "Sunday",
              ],
              required=False,
          ),
          "Time Slot": st.column_config.SelectboxColumn(
              "Time Slot",
              options=[
                  "08:00 - 10:00",
                  "10:00 - 12:00",
                  "13:00 - 15:00",
                  "15:00 - 17:00",
                  "18:00 - 20:00",
              ],
              required=False,
          ),
          "Subject": st.column_config.SelectboxColumn(
              "Subject",
              options=subjects_by_year[
                  selected_year
              ],  # Dynamically shows ONLY the selected year's subjects!
              required=False,
          ),
          "Category": st.column_config.SelectboxColumn(
              "Category",
              options=[
                  "Theory",
                  "Practical",
                  "Assignment",
                  "Revision",
                  "Exam Prep",
              ],
              required=False,
          ),
          "Status": st.column_config.CheckboxColumn(
              "Completed?",
              default=False,
          ),
      },
      num_rows="dynamic",
      use_container_width=True,
      height=500,
      key=f"editor_{selected_year}",
  )

  # Save changes button
  if st.button("Save Changes to Google Sheet", type="primary"):
    # Automatically tag any newly added rows with the correct active year
    edited_df["Year"] = selected_year

    save_edited = edited_df.copy()
    if "Status" in save_edited.columns:
      save_edited["Status"] = save_edited["Status"].apply(
          lambda x: "Completed" if x else "Pending"
      )

    # Merge updated rows back into the main dataset, preserving other years' data
    df_other_years = df[df["Year"] != selected_year]
    final_save_df = pd.concat(
        [df_other_years, save_edited], ignore_index=True
    )

    conn.update(spreadsheet=SPREADSHEET_URL, data=final_save_df)
    st.success(
        f"Changes for {selected_year} saved to Google Sheets successfully!"
    )

except Exception as e:
  st.error("Detailed Connection Error Traceback:")
  st.code(traceback.format_exc())
  st.stop()
