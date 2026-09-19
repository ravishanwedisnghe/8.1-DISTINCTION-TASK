
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Sydney House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")

model = load_model()

st.title("Sydney House Price Predictor")
st.write(
    "Enter the property information below to estimate its sale price."
)

with st.form("prediction_form"):
    suburb = st.selectbox(
        "Suburb",
        ["Penrith", "Leichhardt", "Turramurra"]
    )

    num_bed = st.number_input(
        "Number of bedrooms",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )

    num_bath = st.number_input(
        "Number of bathrooms",
        min_value=1,
        max_value=6,
        value=2,
        step=1
    )

    num_parking = st.number_input(
        "Number of parking spaces",
        min_value=0,
        max_value=10,
        value=1,
        step=1
    )

    property_size = st.number_input(
        "Property size (square metres)",
        min_value=50,
        max_value=4000,
        value=600,
        step=10
    )

    sale_year = st.selectbox(
        "Sale year",
        list(range(2016, 2022)),
        index=5
    )

    sale_month = st.selectbox(
        "Sale month",
        list(range(1, 13))
    )

    cash_rate = st.number_input(
        "Cash rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=0.10,
        step=0.10,
        format="%.2f"
    )

    property_inflation_index = st.number_input(
        "Property inflation index",
        min_value=100.0,
        max_value=300.0,
        value=180.0,
        step=0.1,
        format="%.1f"
    )

    submitted = st.form_submit_button("Predict Sale Price")

if submitted:
    input_data = pd.DataFrame({
        "num_bath": [num_bath],
        "num_bed": [num_bed],
        "num_parking": [num_parking],
        "property_size": [property_size],
        "sale_year": [sale_year],
        "sale_month": [sale_month],
        "cash_rate": [cash_rate],
        "property_inflation_index": [property_inflation_index],
        "suburb": [suburb]
    })

    predicted_price = model.predict(input_data)[0]

    st.success(
        f"Estimated sale price: AUD ${predicted_price:,.0f}"
    )

    st.subheader("Entered Property Information")
    st.dataframe(input_data, hide_index=True)

st.warning(
    "This estimate is based on 110 historical sales from 2016–2021. "
    "It should not replace a professional property valuation."
)
