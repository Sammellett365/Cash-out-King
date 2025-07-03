import streamlit as st
from calculator.calculator import calculate_cashout_value
from scenarios.scenarios import get_best_case
from ocr.extract_text import extract_betslip_text

st.title("Betting Slip Analyzer")

uploaded_file = st.file_uploader("Upload your betslip screenshot", type=["png", "jpg", "jpeg"])
if uploaded_file:
    betslip_data = extract_betslip_text(uploaded_file)
    st.write("Extracted Betslip Data:", betslip_data)

    current_offer = st.number_input("Enter current cashout offer", min_value=0.0)
    if st.button("Analyze"):
        analysis = calculate_cashout_value(betslip_data, current_offer)
        st.write("Cashout Analysis:", analysis)
