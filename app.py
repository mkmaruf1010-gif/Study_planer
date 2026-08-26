from datetime import date
import traceback
import google.generativeai as genai
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Set wide layout for the screen
st.set_page_config(
    page_title="B.Sc. Geography Study Planner & AI", layout="wide"
)

# Custom CSS for main headers
st.markdown(
    """
    <style>
        h1 {
            color: #0F172A !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        h3, h2 {
            color: #1E293B !important;
            font-weight: 700 !important;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 6px;
            margin-top: 15px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# --- GEMINI AI CONFIGURATION ---
# Make sure to add GEMINI_API_KEY in your Streamlit secrets (.streamlit/secrets.toml)
GEMINI_API_KEY = "AQ.Ab8RN6Lv_XDAlEIAUseG-fSYdiJPnPkCATUSfJHOhEcpzLl7MQ"

try:
  genai.configure(api_key=GEMINI_API_KEY)
  ai_model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
  ai_model = None

# --- SIDEBAR: AI STUDY ASSISTANT ---
with st.sidebar:
  st.markdown("### Geography AI Tutor")
  st.write(
      "Ask questions about your syllabus, concepts, or exam preparations!"
  )

  if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

  # Display chat history in sidebar
  for message in st.session_state.ai_messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # AI Input
  user_query = st.text_input(
      "Type your question here...", key="ai_query_input"
  )
  if st.button("Ask AI", type="primary"):
    if user_query:
      if ai_model:
        st.session_state.ai_messages.append(
            {"role": "user", "content": user_query}
        )
        with st.spinner("AI is thinking..."):
          try:
            prompt = f"You are an expert B.Sc. Geography and Environment professor. Explain this clearly and concisely for a student: {user_query}"
            response = ai_model.generate_content(prompt)
            ai_reply = response.text
          except Exception as e:
            ai_reply = f"Error: {e}"
        st.session_state.ai_messages.append(
            {"role": "assistant", "content": ai_reply}
        )
        st.rerun()
      else:
        st.error(
            "GEMINI_API_KEY is missing in Streamlit Secrets! Please configure"
            " it."
        )
    else:
      st.warning("Please type a question first.")

# --- MAIN APP ---
st.title("Study Planner & AI Assistant")

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

  # Convert Date column safely to date objects for the calendar picker
  if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

  for col in df.columns:
    if col != "Date":
      df[col] = (
          df[col].astype(str).replace({"nan": "", "None": "", "<NA>": ""})
      )

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

  # Year selector control at the top
  st.markdown("### 📌 Select Academic Year to Manage")
  selected_year = st.selectbox(
      "Choose Year",
      options=["1st Year", "2nd Year", "3rd Year", "4th Year"],
      label_visibility="collapsed",
  )

  # Filter DataFrame for the selected year
  df_filtered = df[df["Year"] == selected_year].copy()

  st.markdown(f"### 📅 Study Schedule & Tasks — {selected_year}")

  edited_df = st.data_editor(
      df_filtered,
      column_config={
          "id": None,
          "Year": None,
          "Date": st.column_config.DateColumn(
              "Date (YYYY-MM-DD)",
              format="YYYY-MM-DD",
              required=False,
          ),
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
              options=subjects_by_year[selected_year],
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
    edited_df["Year"] = selected_year

    save_edited = edited_df.copy()

    if "Date" in save_edited.columns:
      save_edited["Date"] = pd.to_datetime(
          save_edited["Date"], errors="coerce"
      ).dt.strftime("%Y-%m-%d")
      save_edited["Date"] = (
          save_edited["Date"].fillna("").astype(str).replace("NaT", "")
      )

    if "Status" in save_edited.columns:
      save_edited["Status"] = save_edited["Status"].apply(
          lambda x: "Completed" if x else "Pending"
      )

    df_other_years = df[df["Year"] != selected_year]
    if "Date" in df_other_years.columns:
      df_other_years["Date"] = pd.to_datetime(
          df_other_years["Date"], errors="coerce"
      ).dt.strftime("%Y-%m-%d")
      df_other_years["Date"] = (
          df_other_years["Date"].fillna("").astype(str).replace("NaT", "")
      )

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
