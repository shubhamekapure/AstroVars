import streamlit as st
import datetime
from handler import run_llm

st.set_page_config(page_title="AstroVars", page_icon="🌬️", layout="centered")
st.title("🔮 AstroVars: Ideal Partner by Astrology")
st.write("Enter your birth details to receive astrological interpretation of your (soon) ideal life partner.")

with st.form("astrovars_form"):
    name = st.text_input("Name")
    place = st.text_input("Place of Birth (City, Country)")
    date = st.date_input("Date of Birth", min_value=datetime.date(1950, 1, 1))
    time = st.time_input("Time of Birth")
    submit = st.form_submit_button("Get AI Interpretation")

if submit:
    if not (name and place and date and time):
        st.error("Please fill in all fields.")
    else:
        st.info("Getting AI interpretation...")
        try:
            llm_output = run_llm(
                name,
                date.strftime("%Y-%m-%d"),
                time.strftime("%H:%M"),
                place
            )
            st.markdown("---")
            st.subheader("AI Interpretation")
            st.write(llm_output)
        except Exception as e:
            st.error(f"Error calling LLM: {e}")
