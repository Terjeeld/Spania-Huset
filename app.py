import streamlit as st
import pandas as pd
import os
import datetime
from streamlit_calendar import calendar

st.set_page_config(page_title="Familiebooking – Spaniahytta", layout="wide")

st.title("🏡 Familiebooking – Sommerhuset i Spania 🇪🇸")

DATAFIL = "bookinger.csv"

# Last inn eller lag ny CSV
if os.path.exists(DATAFIL):
    df = pd.read_csv(DATAFIL, parse_dates=["start", "end"])
else:
    df = pd.DataFrame(columns=["title", "start", "end"])

# Vis eksisterende bookinger i kalender
st.subheader("📅 Kalenderoversikt (lesevisning)")
hendelser = df.to_dict("records")

kalender_valg = {
    "initialView": "dayGridMonth",
    "locale": "nb",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek"
    },
    "editable": False,
    "selectable": False,
    "dayMaxEvents": True,
}

calendar(events=hendelser, options=kalender_valg, key="kalender")

# Brukerbooking med dato-velger
st.subheader("📆 Book opphold")
navn = st.text_input("👤 Navn")
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
            # Sjekk overlapp
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
