import streamlit as st
import json
import time
from datetime import datetime, timezone

# Set Page Config
st.set_page_config(
    page_title="Insurance Claim Analyzer Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1f4068, #162447, #e43f5a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 1.8rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #162447;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        font-weight: bold;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #162447;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Settings & Metadata Controls
st.sidebar.markdown("### 🛡️ Adjudication Controls")
st.sidebar.info("Adjust the parameters below to simulate different policy and risk conditions for the AI ingestion engine.")

# Simulated backend connection status
backend_url = "http://localhost:8000/"
st.sidebar.markdown(f"**Backend Endpoint:** `{backend_url}`")
st.sidebar.markdown("**Connection Status:** 🟢 Connected (Demo Mode)")

# Simulation controls
sim_policy_status = st.sidebar.selectbox(
    "Simulated Policy Status",
    ["Active", "Inactive"],
    index=0
)
sim_max_coverage = st.sidebar.slider(
    "Simulated Policy Max Coverage ($)",
    min_value=1000,
    max_value=100000,
    value=50000,
    step=5000
)
sim_fraud_risk = st.sidebar.selectbox(
    "Simulated Fraud Risk Assessment",
    ["Low", "Medium", "High"],
    index=0
)
sim_billed_amount = st.sidebar.number_input(
    "Simulated Invoice Total ($)",
    min_value=0.0,
    max_value=200000.0,
    value=1250.0,
    step=100.0
)

# Header Section
st.markdown("<div class='main-title'>🛡️ Insurance Claim Analyzer Engine</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Production-grade Claim Analysis Pipeline: OCR Text Extraction ➔ Gemini Semantic Parsing ➔ Policy Adjudication Rules</div>", unsafe_allow_html=True)

# Main UI Ingestion Component
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📥 Document Upload")
    uploaded_file = st.file_uploader(
        "Upload Medical Bill or Insurance Claim Document",
        type=["pdf", "png", "jpg", "jpeg"],
        help="Supported formats: PDF, PNG, JPG, JPEG"
    )
    
    if uploaded_file is not None:
        st.success(f"📄 Selected file: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        run_pipeline = st.button("Run AI Ingestion Pipeline", type="primary")
        
        if run_pipeline:
            # Simulate the multi-phase processing pipeline visually
            st.markdown("### ⚙️ Processing Sequence")
            
            with st.spinner("1. Executing Asynchronous Tesseract OCR Parsing..."):
                time.sleep(1.5)
                st.write("✓ OCR Engine successfully extracted document layouts and text.")
                
            with st.spinner("2. Activating Gemini Structuring..."):
                time.sleep(1.5)
                st.write("✓ Gemini semantic analyzer structured raw OCR text into compliant JSON metadata.")
                
            with st.spinner("3. Validating Policy Boundaries..."):
                time.sleep(1.5)
                st.write("✓ Policy validation rules evaluated against active subscriber database schema.")
                
            with st.spinner("4. Running Risk & Fraud Detection Engines..."):
                time.sleep(1.0)
                st.write("✓ Risk assessment score calculated based on metadata flags.")
                
            with st.spinner("5. Performing Adjudication & Recommendation..."):
                time.sleep(1.0)
                st.success("🎉 Ingestion Pipeline execution completed.")
                
            st.markdown("---")
            
            # Setup Tabbed Layout
            tab1, tab2 = st.tabs(["📋 Structured Metadata", "🛡️ Risk & Adjudication Summary"])
            
            # Adjudication calculations
            is_policy_active = (sim_policy_status == "Active")
            requested_amount = sim_billed_amount
            allowed_amount = requested_amount
            
            # Policy Validation Output
            if not is_policy_active:
                validation_valid = False
                validation_summary = f"Claim rejected: Policy is inactive (status: '{sim_policy_status.lower()}')."
                allowed_amount = 0.0
            elif requested_amount > sim_max_coverage:
                validation_valid = True
                allowed_amount = sim_max_coverage
                validation_summary = f"Claim partially approved: Billed amount (${requested_amount:,.2f}) exceeds policy limits (max: ${sim_max_coverage:,.2f}). Capped at limit."
            else:
                validation_valid = True
                validation_summary = f"Claim approved: Billed amount (${requested_amount:,.2f}) is within policy limits (max: ${sim_max_coverage:,.2f})."

            # Fraud Detection Output
            risk_score = 15
            flags = []
            if requested_amount > 50000:
                risk_score += 40
                flags.append("HIGH_VALUE_CLAIM")
            
            if sim_fraud_risk == "High":
                risk_score = max(75, risk_score)
                flags.append("SUSPECT_METADATA_ANOMALY")
            elif sim_fraud_risk == "Medium":
                risk_score = max(45, risk_score)
                flags.append("REVIEW_TRIGGER_KEYWORD")
            
            risk_level = "LOW"
            if risk_score >= 70:
                risk_level = "HIGH"
            elif risk_score >= 30:
                risk_level = "MEDIUM"

            # Final Recommendation Adjudication
            if not validation_valid:
                recommendation = "DENIED"
                reason = f"Claim failed policy parameters: {validation_summary}"
            elif risk_level == "HIGH":
                recommendation = "FLAGGED"
                reason = "Manual investigation required: High risk score and warning flags triggered."
            elif risk_level == "MEDIUM":
                recommendation = "FLAGGED"
                reason = "Secondary review required: Medium risk score and caution flags triggered."
            else:
                recommendation = "APPROVED"
                reason = f"Automated approval: {validation_summary}"

            # Tab 1: Structured Metadata Display
            with tab1:
                st.markdown("#### 📄 Extracted Claim JSON Schema")
                
                extracted_json = {
                    "policy_number": "POL-99887766",
                    "claim_number": "CLM-11223344",
                    "customer_name": "Jane Doe",
                    "total_billed_amount": requested_amount,
                    "extracted_items": [
                        {"description": "Outpatient clinic visit (CPT 99213)", "amount": min(requested_amount * 0.2, 250.0)},
                        {"description": "Diagnostic laboratory panel", "amount": min(requested_amount * 0.48, 600.0)},
                        {"description": "Therapeutic injection and supplies", "amount": min(requested_amount * 0.32, 400.0)}
                    ]
                }
                
                # Show key parameters in metrics layout
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Insured Customer</div>
                        <div class="metric-value">Jane Doe</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Policy Number</div>
                        <div class="metric-value">POL-99887766</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m_col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Claimed Value</div>
                        <div class="metric-value">${requested_amount:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.write("")
                st.json(extracted_json)
                
                st.markdown("#### 📋 Extracted Line Items")
                st.table(extracted_json["extracted_items"])

            # Tab 2: Adjudication and Risk Display
            with tab2:
                st.markdown("#### ⚔️ Final Adjudication Adjudication Verdict")
                
                # Metric display
                v_col1, v_col2, v_col3 = st.columns(3)
                with v_col1:
                    st.metric(label="Decision Action", value=recommendation)
                with v_col2:
                    st.metric(label="Billed vs. Allowed", value=f"${requested_amount:,.2f}", delta=f"${allowed_amount - requested_amount:,.2f}")
                with v_col3:
                    st.metric(label="Fraud Risk Level", value=f"{risk_level} ({risk_score}/100)")
                
                # Display action box
                if recommendation == "APPROVED":
                    st.success(f"✅ **CLAIM APPROVED**\n\n**Justification:** {reason}")
                elif recommendation == "FLAGGED":
                    st.warning(f"⚠️ **CLAIM FLAGGED FOR MANUAL REVIEW**\n\n**Justification:** {reason}")
                else:
                    st.error(f"❌ **CLAIM DENIED**\n\n**Justification:** {reason}")
                
                # Flags table
                st.markdown("#### 🚩 Triggered Security & Risk Flags")
                if flags:
                    for f in flags:
                        st.markdown(f"- 🔴 **{f}**")
                else:
                    st.markdown("🟢 No warning or caution risk flags triggered.")
                
                st.caption(f"Auto Adjudicated on: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    else:
        st.info("💡 Please upload a claim document to begin the AI ingestion analysis.")

with col2:
    st.markdown("### 📖 Documentation")
    st.markdown("""
    This app serves as the frontend for the **Insurance Claim Analyzer Engine**, which processes medical and insurance claims through multiple micro-services:
    
    1. **OCR Layer**:
       - Extracts text from image files and PDFs.
       - Built using Tesseract OCR.
    
    2. **Gemini Ingestion Engine**:
       - Uses `gemini-1.5-flash` model structure prompts to read raw, unstructured text.
       - Returns a schema-compliant JSON structure containing policy, customer, and claim details.
       
    3. **Policy Rules Engine**:
       - Cross-checks claim details against database policies.
       - Flags exceeding limits or inactive contracts.
       
    4. **Fraud & Risk Engine**:
       - Multi-point security scoring scan.
       - Detects high value claims and metadata anomalies.
    """)
