import streamlit as st
import pandas as pd
from utils.request import send_post_request

def get_form():
    st.set_page_config(page_title="FortiFraud")
    st.title("Wpisz dane :")

    with st.form("insurance_form"):
        month = st.selectbox("Month", ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        week_of_month = st.selectbox("WeekOfMonth", ["", 1, 2, 3, 4, 5, 6 ,7])
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
            errors = []
            if make == "":
                 errors.append("Pole 'Make' (producent pojazdu) nie może być puste.")
            if month == "":
                 errors.append("Wybierz miesiąc.")
            if week_of_month == "":
                errors.append("Wybierz tydzień miesiąca.")
            if accident_area == "":
                errors.append("Wybierz obszar wypadku.")
            if month_claimed == "":
                errors.append("Wybierz miesiac wypadku.")   
            if marital_status == "":
                errors.append("Wybierz stan cywilny.")
            if fault == "":
                errors.append("Wybierz rodzaj wypadku.")
            if vehicle_category == "":
                errors.append("Wybierz kategorie pojazdu.")
            if policy_type == "":
                errors.append("Wybierz typ polisy.")
            if deductible == "":
                errors.append("Wybierz kwote odsetek.")
            if base_policy == "":
                errors.append("Wybierz rodzaj polisy.")
            if address_change == "":
                errors.append("Wybierz rodzaj zmiany adresu.")
            if agent_type == "":
                errors.append("Wybierz rodzaj agenta.")
            if police_report_filed == "":
                errors.append("Wybierz czy została zgłoszona reklamacja.")

            if errors:
                st.error("Wystąpiły błędy na formularzu:")
                for err in errors:
                    st.write(f"- {err}")
            else:
                payload = {
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
                result = send_post_request(payload, st)
                if result:
                    st.success("Wynik predykcji:")
                    st.json(result)

    # Przycisk do CSV
    if st.button("Dane z CSV"):
        st.session_state.page = "csv"
        st.experimental_rerun()

def get_csv_upload():
    st.set_page_config(page_title="FortiFraud")
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
                    result_df.drop(columns=["status"], inplace=True)
                    st.dataframe(result_df)
                    st.download_button("Pobierz wyniki CSV", result_df.to_csv(index=False), file_name="predictions.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Błąd wczytywania pliku: {e}")


if "page" not in st.session_state:
    st.session_state.page = "form"

if st.session_state.page == "form":
    get_form()
elif st.session_state.page == "csv":
    get_csv_upload()
