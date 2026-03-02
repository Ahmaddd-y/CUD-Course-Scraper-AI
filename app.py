import os
import asyncio
import streamlit as st
import pandas as pd
import base64
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from Scraper import AiAgent
from Support import Offerings
from langchain_openai import ChatOpenAI



# Load environment variables from a .env file
load_dotenv()

# Async function to run the scraper with the selected LLM backend
async def run_scraper(username, password, semester, llm_choice):
    if llm_choice == "Cloud (Gemini)":
        # Use Gemini API for cloud-based LLM
        api_key = os.getenv("GEMINI_API_KEY")
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key, temperature=0.0)
    else:  # Use local LLM (DeepSeek)
        llm = ChatOllama(model="llama3.2", num_ctx=32000)


    # Initialize the scraper agent with the selected LLM and user inputs
    agent = AiAgent(llm=llm, username=username, password=password, semester=semester)
    return await agent.run()
    

# Save the scraped course data to a CSV file
def save_courses_to_csv(course_data, save_path):
    # Convert course data to a DataFrame and save it as a CSV
    df = pd.DataFrame([course.model_dump() for course in course_data.courses])
    df.to_csv(save_path, index=False)
    return df

# Encode the CUD logo image to Base64 for embedding in the GUI
def get_logo_base64():
    with open("CUD Logo.jpg", "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

# Main function to define the Streamlit GUI
def main():
    # Set the page configuration for the Streamlit app
    st.set_page_config(page_title="CUD Course Scraper", layout="centered")

    # Display the header with the CUD logo and titles
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/jpeg;base64,{get_logo_base64()}" width="120" />
            <h2 style="color:#b30838;">Canadian University Dubai</h2>
            <h4 style="color:#333;">Course Scraper Portal</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create a form for user input
    with st.form("input_form"):
        st.markdown("### Enter your credentials")
        # Input fields for username, password, semester, and LLM choice
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        semester = st.text_input("Semester")
        llm_choice = st.radio("Choose Model Backend", ["Cloud (Gemini)", "Local (DeepSeek)"])

        st.markdown("### Save Options")
        # Input fields for save directory and filename
        save_dir = st.text_input("Directory to save CSV", value=os.getcwd())
        filename = st.text_input("Filename (with .csv)", value="Final_Results.csv")

        # Submit button to run the scraper
        submitted = st.form_submit_button("Run Scraper", type="primary")

    # Handle form submission
    if submitted:
        if not all([username, password, semester, save_dir, filename]):
            # Show an error if any field is empty
            st.error("Please fill in all fields.")
        else:
            # Construct the save path for the CSV file
            save_path = os.path.join(save_dir, filename)
            with st.spinner("Running scraper..."):
                try:
                    # Run the scraper and save the results
                    course_data = asyncio.run(run_scraper(username, password, semester, llm_choice))
                    if course_data and course_data.courses:
                        df = save_courses_to_csv(course_data, save_path)
                        st.session_state.courses_df = df  # Save to session
                        st.success(f"✅ Saved {len(df)} courses to `{save_path}`")

                        st.markdown("### Filter Results")

                        # Filters
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            course_codes = ["All"] + sorted(df["Course_code"].unique())
                            selected_code = st.selectbox("Filter by Course Code", course_codes)

                        with col2:
                            instructors = ["All"] + sorted(df["instructor"].unique())
                            selected_instructor = st.selectbox("Filter by Instructor", instructors)

                        with col3:
                            days_options = ["All"] + sorted(df["days"].unique())
                            selected_days = st.selectbox("Filter by Days", days_options)

                        # Apply filters
                        filtered_df = df.copy()
                        if selected_code != "All":
                            filtered_df = filtered_df[filtered_df["Course_code"] == selected_code]
                        if selected_instructor != "All":
                            filtered_df = filtered_df[filtered_df["instructor"] == selected_instructor]
                        if selected_days != "All":
                            filtered_df = filtered_df[filtered_df["days"] == selected_days]

                        st.markdown(f"### Filtered Results ({len(filtered_df)} rows)")
                        st.dataframe(filtered_df)

                        # Download buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            csv_data = filtered_df.to_csv(index=False).encode("utf-8")
                            st.download_button("Download as CSV", csv_data, file_name="filtered_courses.csv", mime="text/csv")
                        with col2:
                            excel_path = "filtered_courses.xlsx"
                            filtered_df.to_excel(excel_path, index=False)
                            with open(excel_path, "rb") as f:
                                st.download_button("Download as Excel", f.read(), file_name=excel_path, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    else:
                        st.warning("No course data was extracted.")  # Display the DataFrame in the GUI
                except Exception as e:
                    # Show an error message if the scraper fails
                    st.error(f"Error: {e}")


    st.markdown("### Or Load Course Data from File")

    uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state.courses_df = df
            st.success(f"Loaded {len(df)} records from uploaded file.")

            # Reuse the filtering logic
            st.markdown("### Filter Results")

            col1, col2, col3 = st.columns(3)
            with col1:
                course_codes = ["All"] + sorted(df["Course_code"].unique())
                selected_code = st.selectbox("Filter by Course Code", course_codes)

            with col2:
                instructors = ["All"] + sorted(df["instructor"].unique())
                selected_instructor = st.selectbox("Filter by Instructor", instructors)

            with col3:
                days_options = ["All"] + sorted(df["days"].unique())
                selected_days = st.selectbox("Filter by Days", days_options)

            filtered_df = df.copy()
            if selected_code != "All":
                filtered_df = filtered_df[filtered_df["Course_code"] == selected_code]
            if selected_instructor != "All":
                filtered_df = filtered_df[filtered_df["instructor"] == selected_instructor]
            if selected_days != "All":
                filtered_df = filtered_df[filtered_df["days"] == selected_days]

            st.markdown(f"### Filtered Results ({len(filtered_df)} rows)")
            st.dataframe(filtered_df)

            col1, col2 = st.columns(2)
            with col1:
                csv_data = filtered_df.to_csv(index=False).encode("utf-8")
                st.download_button("Download as CSV", csv_data, file_name="filtered_courses.csv", mime="text/csv")
            with col2:
                excel_path = "filtered_courses.xlsx"
                filtered_df.to_excel(excel_path, index=False)
                with open(excel_path, "rb") as f:
                    st.download_button("Download as Excel", f.read(), file_name=excel_path, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            st.error(f"Failed to load file: {e}")


# Entry point for the script
if __name__ == "__main__":
    main()
