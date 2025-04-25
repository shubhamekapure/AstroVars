import streamlit as st
from llm_handler import run_llm

st.set_page_config(page_title="AstroVars: AI Astrology", page_icon="🔮", layout="centered")
st.title("🔮 AstroVars: AI Astrology App")
st.write("Enter your birth details to receive a personalized astrological interpretation from our AI astrologer.")

with st.form("astrovars_form"):
    name = st.text_input("Name")
    place = st.text_input("Place of Birth (City, Country)")
    date = st.date_input("Date of Birth")
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
