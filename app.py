import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Summer House Booking", layout="centered")

st.title("🏡 Summer House Booking Calendar")
st.markdown("Use this app to book days at the family summer house in Spain 🇪🇸")

# Load or create bookings
DATA_FILE = "bookings.csv"

if os.path.exists(DATA_FILE):
    bookings = pd.read_csv(DATA_FILE)
else:
    bookings = pd.DataFrame(columns=["Date", "Name"])

# Convert date column to datetime
if not bookings.empty:
    bookings["Date"] = pd.to_datetime(bookings["Date"]).dt.date

# Booking form
st.subheader("Make a Booking")
name = st.text_input("👤 Your name")
date = st.date_input("📅 Select a date", min_value=datetime.date.today())

if st.button("Book Date"):
    if not name:
        st.warning("Please enter your name.")
    elif date in bookings["Date"].values:
        st.error(f"That date ({date}) is already booked!")
    else:
        new_booking = pd.DataFrame({"Date": [date], "Name": [name]})
        bookings = pd.concat([bookings, new_booking], ignore_index=True)
        bookings.to_csv(DATA_FILE, index=False)
        st.success(f"🎉 {name}, you have booked {date}!")

# Show existing bookings
st.subheader("📖 Current Bookings")
if bookings.empty:
    st.info("No bookings yet.")
else:
    st.dataframe(bookings.sort_values("Date").reset_index(drop=True))
