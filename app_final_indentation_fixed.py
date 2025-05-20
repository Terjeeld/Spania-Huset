
import streamlit as st
import pandas as pd
import os
import datetime
from streamlit_calendar import calendar

st.set_page_config(page_title="Familiebooking – Spaniahytta", layout="wide")

st.title("🏡 Familiebooking – Hytta i Spania 🇪🇸")

DATAFIL = os.path.join(os.path.dirname(__file__), "bookings.csv")

# Last inn eller lag ny fil
if os.path.exists(DATAFIL):
    df = pd.read_csv(DATAFIL)
else:
    df = pd.DataFrame(columns=["title", "start", "end"])

# Konverter dato-kolonner til datetime
df["start"] = pd.to_datetime(df["start"], errors="coerce")
df["end"] = pd.to_datetime(df["end"], errors="coerce")
df = df.dropna(subset=["start", "end"])

if "booking_ok" not in st.session_state:
    st.session_state.booking_ok = False


# 📆 Bookingseksjon
st.subheader("📆 Book opphold")

# 👤 Brukerinndata
navn = st.text_input("👤 Ditt navn")
datointervall = st.date_input(
    "Velg ankomst- og avreisedato",
    value=(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=2))
)


if st.button("Book valgte datoer"):
    if not navn:
        st.warning("⚠️ Skriv inn navnet ditt.")
    elif not isinstance(datointervall, tuple) or len(datointervall) != 2:
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

                try:
                    with open(DATAFIL, "w", encoding="utf-8") as f:
                        df.to_csv(f, index=False)
                        f.flush()
                        os.fsync(f.fileno())  # 🔒 ensures flush to disk

                    st.write("📄 FORSØKTE Å LAGRE TIL:", os.path.abspath(DATAFIL))

                    test_df = pd.read_csv(DATAFIL)
                    st.write("📄 Innhold etter skriving:", test_df)

                    st.session_state.booking_ok = True
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Klarte ikke lagre filen: {e}")


# ✅ Show success message after rerun
if st.session_state.booking_ok:
    st.success("✅ Booking registrert!")
    st.session_state.booking_ok = False

# 📅 Vis kalender etter bookingseksjon
st.subheader("📅 Kalenderoversikt")

hendelser = [
    {
        "title": row["title"],
        "start": pd.to_datetime(row["start"]).isoformat(),
        "end": (pd.to_datetime(row["end"]) + pd.Timedelta(days=1)).isoformat()  # +1 dag for å inkludere sluttdagen
    }
    for _, row in df.iterrows()
]

kalender_valg = {
    "initialView": "dayGridMonth",
    "locale": "nb",
    "height": 500,
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
