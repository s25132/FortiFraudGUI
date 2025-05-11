import streamlit as st
import pandas as pd
from utils.request import send_post_request
from datetime import datetime

def configure_app():
    st.set_page_config(page_title="FortiFraud")

def validate_form_data(data):
    errors = []
    required_fields = {
        "Make": "Pole 'Make' (producent pojazdu) nie może być puste.",
        "Month": "Wybierz miesiąc.",
        "WeekOfMonth": "Wybierz tydzień miesiąca.",
        "AccidentArea": "Wybierz obszar wypadku.",
        "MonthClaimed": "Wybierz miesiąc wypadku.",
        "MaritalStatus": "Wybierz stan cywilny.",
        "Fault": "Wybierz rodzaj wypadku.",
        "VehicleCategory": "Wybierz kategorię pojazdu.",
        "PolicyType": "Wybierz typ polisy.",
        "Deductible": "Wybierz kwotę odsetek.",
        "BasePolicy": "Wybierz rodzaj polisy.",
        "AddressChange_Claim": "Wybierz rodzaj zmiany adresu.",
        "AgentType": "Wybierz rodzaj agenta.",
        "PoliceReportFiled": "Wybierz czy została zgłoszona reklamacja."
    }
    for field, error_message in required_fields.items():
        if data.get(field, "") == "":
            errors.append(error_message)
    return errors

def handle_prediction_form():
    configure_app()
    st.title("Wpisz dane :")

    with st.form("insurance_form"):
        month = st.selectbox("Month", ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        week_of_month = st.selectbox("WeekOfMonth", ["", 1, 2, 3, 4, 5, 6, 7])
        make = st.selectbox("Make", ["", "Pontiac", "Toyota", "Honda", "Mazda", "Chevrolet", "Accura", "Ford", "VW", "Dodge", "Saab", "Mercury", "Saturn", "Nisson", "BMW", "Jaguar", "Porche", "Mecedes", "Ferrari", "Lexus"])
        accident_area = st.selectbox("AccidentArea", ["", "Urban", "Rural"])
        month_claimed = st.selectbox("MonthClaimed", ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "?", "none"])
        marital_status = st.selectbox("MaritalStatus", ["", "Single", "Married", "Widow", "Divorced"])
        fault = st.selectbox("Fault", ["", "Policy Holder", "Third Party"])
        policy_type = st.selectbox("PolicyType", ["", "Sedan - All Perils", "Sedan - Collision", "Sedan - Liability", "Sport - Collision", "Sport - All Perils", "Sport - Liability", "Utility - All Perils", "Utility - Collision", "Utility - Liability"])
        vehicle_category = st.selectbox("VehicleCategory", ["", "Sedan", "Sport", "Utility"])
        deductible = st.selectbox("Deductible", ["", 300, 400, 500, 700])
        police_report_filed = st.selectbox("PoliceReportFiled", ["", "Yes", "No"])
        agent_type = st.selectbox("AgentType", ["", "Internal", "External"])
        address_change = st.selectbox("AddressChange_Claim", ["", "no change", "under 6 months", "1 year", "2 to 3 years", "4 to 8 years"])
        year = st.number_input("Year", min_value=1900, max_value=2050, value=2025)
        base_policy = st.selectbox("BasePolicy", ["", "Liability", "Collision", "All Perils"])

        submit = st.form_submit_button("Wyślij do predykcji")

    if submit:
        form_data = {
            "Month": month,
            "WeekOfMonth": week_of_month,
            "Make": make,
            "AccidentArea": accident_area,
            "MonthClaimed": month_claimed,
            "MaritalStatus": marital_status,
            "Fault": fault,
            "PolicyType": policy_type,
            "VehicleCategory": vehicle_category,
            "Deductible": deductible,
            "PoliceReportFiled": police_report_filed,
            "AgentType": agent_type,
            "AddressChange_Claim": address_change,
            "Year": year,
            "BasePolicy": base_policy
        }

        errors = validate_form_data(form_data)

        if errors:
            st.error("Wystąpiły błędy na formularzu:")
            for err in errors:
                st.write(f"- {err}")
        else:
            result = send_post_request(form_data, st)
            if result:
                st.success("Wynik predykcji:")
                st.json(result)

    if st.button("Dane z CSV"):
        st.session_state.page = "csv"
        st.experimental_rerun()

def handle_csv_upload():
    configure_app()
    st.title("Wyślij dane z pliku CSV do predykcji")

    uploaded_file = st.file_uploader("Upload plik CSV", type=["csv"])

    if st.button("Wróć do głownego menu"):
        st.session_state.page = "form"
        st.experimental_rerun()

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)

            if st.button("Wyślij dane"):
                predictions = []
                for _, row in df.iterrows():
                    payload = row.to_dict()
                    prediction = send_post_request(payload, st)
                    if prediction:
                        payload.update(prediction)
                        predictions.append(payload)

                if predictions:
                    st.success("Wyniki predykcji:")
                    result_df = pd.DataFrame(predictions)
                    result_df.drop(columns=["status"], inplace=True, errors="ignore")
                    st.dataframe(result_df)
                    st.download_button(
                        "Pobierz wyniki CSV",
                        result_df.to_csv(index=False),
                        file_name=f"predictions_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv",
                        mime="text/csv"
                    )
        except Exception as e:
            st.error(f"Błąd wczytywania pliku: {e}")

# Routing logiki strony
if "page" not in st.session_state:
    st.session_state.page = "form"

if st.session_state.page == "form":
    handle_prediction_form()
elif st.session_state.page == "csv":
    handle_csv_upload()
