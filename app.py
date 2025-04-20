import streamlit as st
from astrology import calculate_big_three
from timezone_utils import get_timezone_name, local_to_utc
from datetime import datetime

st.title('Astro-Vars: Ideal Partner Traits by Astrology')

st.markdown('Enter your birth details to discover your Big Three and (soon) your ideal partner traits!')

from geopy.geocoders import Nominatim

with st.form('birth_form'):
    name = st.text_input('Name')
    gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
    place = st.text_input('Place of Birth (City, Country)')
    import datetime
    min_date = datetime.date(1950, 1, 1)
    max_date = datetime.date.today()
    date = st.date_input('Date of Birth', min_value=min_date, max_value=max_date)
    time = st.time_input('Time of Birth')
    submitted = st.form_submit_button('Submit')

if submitted:
    geolocator = Nominatim(user_agent="astro_vars_app")
    location = geolocator.geocode(place)
    if not location:
        st.error('Could not find the location. Please check the spelling or try a nearby city.')
    else:
        lat, lon = location.latitude, location.longitude
        tz_name = get_timezone_name(lat, lon)
        if not tz_name:
            st.error('Could not determine timezone for the location.')
        else:
            import datetime as dtmod
            dt_local = dtmod.datetime.combine(date, time)
            dt_utc = local_to_utc(dt_local, tz_name)
            date_str = dt_utc.strftime('%Y-%m-%d')
            time_str = dt_utc.strftime('%H:%M')
            # Calculate full chart JSON
            from astrology import calculate_big_three, calculate_full_chart
            big_three = calculate_big_three(date_str, time_str, lat, lon)
            chart_json = calculate_full_chart(date_str, time_str, lat, lon)
            st.success(f"**Sun:** {big_three['Sun']} | **Moon:** {big_three['Moon']} | **Ascendant:** {big_three['Ascendant']}")
            # Prepare user info
            user_info = {
                'name': name,
                'gender': gender,
                'place': place,
                'date': str(date),
                'time': str(time)
            }
            # Build prompt and get LLM output
            from prompt_engine import build_prompt
            from llm_handler import run_llm
            prompt = build_prompt(chart_json, user_info)
            llm_output = run_llm(prompt)
            st.markdown("### Ideal Partner Traits (AI Interpretation)")
            st.markdown(llm_output)
