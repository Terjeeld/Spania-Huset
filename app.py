import streamlit as st
import pandas as pd
import os
import datetime
from streamlit_calendar import calendar

st.set_page_config(page_title="Familiebooking – Spaniahytta", layout="wide")

st.title("🏡 Familiebooking – Sommerhuset i Spania 🇪🇸")

DATAFIL = "bookings.csv"

# Last inn eller lag ny fil
if os.path.exists(DATAFIL):
    df = pd.read_csv(DATAFIL)
else:
    df = pd.DataFrame(columns=["title", "start", "end"])

# Konverter dato-kolonner til datetime
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])

# 📆 Bookingseksjon
st.subheader("📆 Book opphold")

navn = st.text_input("👤 Ditt navn")
datointervall = st.date_input(
    "Velg ankomst- og avreisedato",
    value=(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=2))
)

if st.button("Book valgte datoer"):
    if not navn:
        st.warning("⚠️ Skriv inn navnet ditt.")
    elif len(datointervall) != 2:
        st.warning("⚠️ Velg både ankomst og avreisedato.")
    else:
        start, end = datointervall
        if start > end:
            st.error("🚫 Ankomstdato kan ikke være etter avreisedato.")
        else:
            overlap = df[
                (df["start"].dt.date <= end) & (df["end"].dt.date >= start)
            ]
            if not overlap.empty:
                st.error("🚫 Datoene overlapper med eksisterende booking.")
            else:
                ny_booking = pd.DataFrame([{
                    "title": navn,
                    "start": start,
                    "end": end
                }])
                df = pd.concat([df, ny_booking], ignore_index=True)
                df.to_csv(DATAFIL, index=False)
                st.success(f"✅ Booking registrert for {navn}: {start} til {end}")
                st.rerun()

# 📅 Vis kalender etter bookingseksjon
st.subheader("📅 Kalenderoversikt")

hendelser = df.to_dict("records")

kalender_valg = {
    "initialView": "dayGridMonth",
    "locale": "nb",
    "height": 500,  # ← Mindre høyde
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth"
    },
    "editable": False,
    "selectable": False,
    "dayMaxEvents": True,
}

calendar(events=hendelser, options=kalender_valg, key="kalender")
