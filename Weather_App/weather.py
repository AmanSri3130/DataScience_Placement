import requests
import streamlit as st
from datetime import datetime

# Embedded OpenWeatherMap API key (requested). Replace this with your key if needed.
API_KEY = "75becada79d325ea1ac080891a407835"

st.set_page_config(
    page_title="WeatherX-Weather Dekho, Weather Jaano!",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }
    .stApp {
        background: radial-gradient(circle at 0% 0%, rgba(56, 189, 248, 0.18), transparent 25%),
                    radial-gradient(circle at 100% 0%, rgba(129, 140, 248, 0.16), transparent 24%),
                    radial-gradient(circle at 100% 100%, rgba(251, 191, 36, 0.14), transparent 24%),
                    linear-gradient(135deg, #050816 0%, #0c1c3c 36%, #112e5d 72%, #173f71 100%);
        color: #f8fbff;
    }
    .css-18e3th9 {
        padding-top: 1rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #38bdf8, #a5b4fc);
        color: #0f172a;
        font-weight: 700;
        border-radius: 999px;
        border: none;
        padding: 0.9rem 1.9rem;
        box-shadow: 0 20px 50px rgba(56, 189, 248, 0.2);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .stButton>button:hover {
        transform: translateY(-4px);
        box-shadow: 0 26px 64px rgba(56, 189, 248, 0.28);
    }
    .weather-card,
    .metric-card,
    .info-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 28px;
        box-shadow: 0 28px 80px rgba(3, 10, 30, 0.3);
        backdrop-filter: blur(18px);
    }
    .weather-card {
        padding: 2.4rem;
        animation: float 12s ease-in-out infinite;
    }
    .metric-card {
        padding: 1.4rem 1.5rem;
        margin-bottom: 1.1rem;
    }
    .info-card {
        padding: 1.25rem 1.35rem;
        margin-top: 0.9rem;
    }
    .hero-title {
        font-size: clamp(3rem, 4vw, 4.8rem);
        margin: 0;
        font-weight: 900;
        letter-spacing: -0.07em;
        line-height: 0.98;
    }
    .hero-subtitle {
        color: #cbd5e1;
        font-size: 1.05rem;
        line-height: 1.8;
        margin-top: 0.8rem;
        max-width: 760px;
    }
    .weather-icon {
        width: 120px;
        height: 120px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 4.8rem;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.11);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.08);
        animation: pulse 2.4s ease-in-out infinite;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.92rem;
        margin-bottom: 0.45rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-value {
        color: #eff6ff;
        font-size: 1.55rem;
        font-weight: 800;
        line-height: 1.05;
    }
    .status-banner {
        color: #a5f3fc;
        font-size: 0.97rem;
        margin-top: 1.1rem;
    }
    .pill {
        display: inline-block;
        padding: 0.6rem 1rem;
        border-radius: 999px;
        color: #e2e8f0;
        background: rgba(32, 129, 226, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.18);
        font-size: 0.95rem;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-14px); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.08); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="hero-title">WeatherX-Weather Dekho, Weather Jaano!</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">A bold Streamlit weather experience with motion, glassmorphism, and a modern dashboard feel. Enter any city and get instant weather insight.</p>', unsafe_allow_html=True)

search_col, info_col = st.columns([1.4, 0.85])
with search_col:
    with st.form(key="weather_form"):
        city = st.text_input("Search city", value="Mumbai", max_chars=50, help="Example: London, Tokyo, New York.")
        submitted = st.form_submit_button("Update Weather")
        if submitted and not city.strip():
            st.warning("Please enter a city name to continue.")

with info_col:
    st.markdown(
        "<div class='info-card'><strong>Why WeatherFlow?</strong><br>Elegant cards, smooth animation, and clear weather status for every city.</div>",
        unsafe_allow_html=True,
    )

if submitted and city.strip():
    city_name = city.strip()
    with st.spinner("Fetching weather and building the dashboard..."):
        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city_name}&appid={API_KEY}&units=metric"
            )
            response = requests.get(url, timeout=10)
            payload = response.json()

            if response.status_code != 200:
                message = payload.get("message", "Unable to retrieve weather data.")
                st.error(f"Error: {message.capitalize()}")
            else:
                main = payload.get("main", {})
                weather = payload.get("weather", [{}])[0]
                wind = payload.get("wind", {})
                sys_info = payload.get("sys", {})
                city_label = payload.get("name", "Unknown")
                country = sys_info.get("country", "")
                condition = weather.get("main", "Clear")
                description = weather.get("description", "Clear").title()
                temp = main.get("temp", "N/A")
                feels_like = main.get("feels_like", "N/A")
                humidity = main.get("humidity", "N/A")
                wind_speed = wind.get("speed", "N/A")
                pressure = main.get("pressure", "N/A")
                local_time = datetime.utcfromtimestamp(payload.get("dt", 0) + payload.get("timezone", 0)).strftime("%b %d, %Y %H:%M")

                def icon_for_condition(name: str) -> str:
                    value = name.lower()
                    if "cloud" in value:
                        return "☁️"
                    if "rain" in value or "drizzle" in value:
                        return "🌧️"
                    if "storm" in value or "thunder" in value:
                        return "⛈️"
                    if "snow" in value:
                        return "❄️"
                    if "mist" in value or "fog" in value or "haze" in value:
                        return "🌫️"
                    return "☀️"

                weather_icon = icon_for_condition(condition)
                wind_descriptor = "Calm breeze" if isinstance(wind_speed, (int, float)) and wind_speed < 6 else "Windy"

                st.markdown(
                    f"""
                    <div class='weather-card'>
                        <div style='display:flex; align-items:center; justify-content:space-between; gap:28px; flex-wrap:wrap;'>
                            <div style='max-width:60%;'>
                                <div style='color:#94a3b8; font-size:0.95rem; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.65rem;'>Current location</div>
                                <div style='font-size:2.75rem; font-weight:900; margin-bottom:0.3rem; color:#eef2ff;'>{city_label}, {country}</div>
                                <div style='font-size:1rem; color:#cbd5e1; margin-bottom:1rem;'>{description}</div>
                                <div style='display:flex; flex-wrap:wrap; gap:0.85rem;'>
                                    <span class='pill'>Local time: {local_time}</span>
                                    <span class='pill'>Feels like: {feels_like} °C</span>
                                </div>
                            </div>
                            <div class='weather-icon'>{weather_icon}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                left, right = st.columns(2)
                with left:
                    st.markdown(
                        f"""
                        <div class='metric-card'>
                            <div class='metric-title'>Temperature</div>
                            <div class='metric-value'>{temp} °C</div>
                        </div>
                        <div class='metric-card'>
                            <div class='metric-title'>Humidity</div>
                            <div class='metric-value'>{humidity}%</div>
                        </div>
                        <div class='metric-card'>
                            <div class='metric-title'>Pressure</div>
                            <div class='metric-value'>{pressure} hPa</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with right:
                    st.markdown(
                        f"""
                        <div class='metric-card'>
                            <div class='metric-title'>Wind speed</div>
                            <div class='metric-value'>{wind_speed} m/s</div>
                        </div>
                        <div class='metric-card'>
                            <div class='metric-title'>Wind mood</div>
                            <div class='metric-value'>{wind_descriptor}</div>
                        </div>
                        <div class='metric-card'>
                            <div class='metric-title'>Sky</div>
                            <div class='metric-value'>{condition}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    "<div class='info-card'>"
                    "<strong style='font-size:1.05rem; color:#f8fafc;'>Detailed weather note</strong>"
                    f"<p style='margin-top:0.85rem; color:#cbd5e1; line-height:1.75;'>The atmosphere in {city_label} is {description.lower()} with {humidity}% humidity and a temperature near {temp}°C. Expect a {wind_descriptor.lower()} experience.</p>"
                    "</div>",
                    unsafe_allow_html=True,
                )

                
        except requests.RequestException:
            st.error("Network error. Please check your connection and try again.")
        except Exception as exc:
            st.error("An unexpected error occurred.")
            st.write(f"Debug: {exc}")

st.markdown(
    "<div class='status-banner'>Powered by OpenWeatherMap · Smooth motion · Responsive dashboard · Instant city lookup.</div>",
    unsafe_allow_html=True,
)

