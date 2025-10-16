import streamlit as st
from prediction_helper import predict

# ---------------------- PAGE CONFIGURATION ----------------------
st.set_page_config(
    page_title="ML Credit Risk Predictor",
    page_icon="🤖",
    layout="wide",
)

# ---------------------- CUSTOM CSS FOR MODERN STYLING ----------------------
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stApp {
            background: linear-gradient(180deg, #0e1117 0%, #1e1e2f 100%);
        }
        .main-title {
            text-align: center;
            font-size: 2.5em;
            font-weight: 700;
            color: #00c6ff;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #bbbbbb;
            font-size: 1.1em;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #00c6ff;
            color: white;
            border-radius: 10px;
            border: none;
            font-size: 1.1em;
            font-weight: 600;
            width: 100%;
            height: 50px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #0072ff;
            transform: scale(1.05);
        }
        hr {
            border: 1px solid #30343f;
            margin: 25px 0;
        }
        .sidebar-title {
            font-size: 1.4em;
            color: #00c6ff;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .sidebar-text {
            font-size: 0.95em;
            color: #cccccc;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- SIDEBAR: ABOUT PROJECT ----------------------
st.sidebar.markdown("<h2 class='sidebar-title'>📘 About Project</h2>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div class='sidebar-text'>
<b>ML Credit Risk Predictor</b> is my FinTech-oriented machine learning project built to assess
borrower creditworthiness using a blend of statistical and ensemble learning models.<br><br>

The solution leverages <b>Logistic Regression</b> for interpretability, <b>XGBoost</b> for boosting performance, 
and <b>Random Forest</b> for handling non-linearity—achieving a balanced trade-off between accuracy, 
stability, and explainability.<br><br>

<b>Modeling Workflow:</b><br>
- Data preprocessing: handled outliers, missing values, and categorical encoding<br>
- Feature selection: applied IV, VIF, and domain-driven logic<br>
- Training split: 75% train / 25% test with scaling<br>
- Fine-tuning via <b>Optuna</b> and <b>RandomizedSearchCV</b><br><br>

<b>Evaluation Metrics:</b> AUC, KS-statistic, Gini coefficient, and classification report.<br><br>

<b>Performance Snapshot:</b><br>
- Logistic Regression: AUC 98, Gini 96<br>
- XGBoost: AUC 99, Gini 96<br>
- Random Forest: AUC 97, Gini 95<br><br>

This project reflects a passion for <b>Data Science, Financial Analytics, and Applied Machine Learning</b>,
integrating model interpretability with real-world lending decisions.
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:0.9em; color:#888;'>Developed by <b>Samarth Goswami</b><br>University of Toledo | Machine Learning • AI • FinTech</p>", unsafe_allow_html=True)

# ---------------------- HEADER SECTION ----------------------
st.markdown("<h1 class='main-title'>🤖 ML Credit Risk Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Machine Learning–powered model to assess borrower creditworthiness</p>", unsafe_allow_html=True)
st.divider()

# ---------------------- INPUT FORM ----------------------
st.markdown("### 📋 Enter Borrower Details")

row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input('Age', min_value=18, max_value=100, step=1, value=28)
with row1[1]:
    income = st.number_input('Annual Income (₹)', min_value=0, value=1200000)
with row1[2]:
    loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000)

loan_to_income_ratio = loan_amount / income if income > 0 else 0
with row2[0]:
    st.metric("Loan-to-Income Ratio", f"{loan_to_income_ratio:.2f}")

with row2[1]:
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36)
with row2[2]:
    avg_dpd_per_delinquency = st.number_input('Average DPD (Days Past Due)', min_value=0, value=20)

with row3[0]:
    delinquency_ratio = st.slider('Delinquency Ratio (%)', 0, 100, 30)
with row3[1]:
    credit_utilization_ratio = st.slider('Credit Utilization (%)', 0, 100, 30)
with row3[2]:
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)

with row4[0]:
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
with row4[1]:
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
with row4[2]:
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

st.divider()

# ---------------------- PREDICTION SECTION ----------------------
if st.button('🚀 Predict Credit Risk'):
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months,
        avg_dpd_per_delinquency, delinquency_ratio,
        credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    st.markdown("### 📈 Risk Evaluation Results")
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric("Default Probability", f"{probability:.2%}")
    with col_res2:
        st.metric("Credit Score", f"{credit_score}")
    with col_res3:
        st.metric("Risk Rating", rating)

    # Conditional visual feedback
    if probability < 0.2:
        st.success("✅ Low Risk: Applicant shows strong repayment ability.")
    elif 0.2 <= probability < 0.5:
        st.warning("⚠️ Moderate Risk: Applicant may require additional verification.")
    else:
        st.error("❌ High Risk: Applicant likely to default.")

st.divider()
st.markdown("<p style='text-align:center; color: #777;'>Developed by <b>Samarth Goswami</b> | Machine Learning • Credit Analytics • FinTech AI • Data Science </p>", unsafe_allow_html=True)
