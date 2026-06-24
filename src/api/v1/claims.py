from fastapi import APIRouter, status, UploadFile, File, Form
from src.services.ocr.ocr_engine import OCREngineService
from src.services.gemini.extractor import GeminiExtractorService
from src.services.validation.policy_engine import PolicyValidationEngine
from src.services.fraud.detector import FraudDetectionEngine
from src.services.recommendation.advisor import RecommendationEngine

router = APIRouter(prefix="/claims", tags=["Claims"])

class MockPolicy:
    id = 12345
    def __init__(self, status: str, max_coverage_amount: float):
        self.status = status
        self.max_coverage_amount = max_coverage_amount

@router.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
async def analyze_claim(
    file: UploadFile = File(...),
    policy_status: str = Form("Active"),
    max_coverage: float = Form(50000.0),
    fraud_risk: str = Form("Low"),
    billed_amount: float = Form(1250.0)
):
    """
    Endpoint to run the complete automated claim ingestion pipeline.
    Accepts the document file and UI mock configurations to process the policy checks.
    """
    # 1. OCR Text Extraction
    ocr_service = OCREngineService()
    file_bytes = await file.read()
    raw_text = await ocr_service.extract_text_from_bytes(file_bytes, file.filename)
    
    # 2. Gemini Semantic Structuring
    gemini_service = GeminiExtractorService()
    extracted_data = await gemini_service.extract_structured_json(raw_text)
    
    # Override/augment the claim amount and items dynamically based on user input
    extracted_data["total_billed_amount"] = billed_amount
    
    # Adjust mock items to sum to billed_amount for realistic display
    if "extracted_items" in extracted_data and isinstance(extracted_data["extracted_items"], list):
        items = extracted_data["extracted_items"]
        if len(items) > 0:
            items[0]["amount"] = round(billed_amount * 0.2, 2)
            if len(items) > 1:
                items[1]["amount"] = round(billed_amount * 0.48, 2)
            if len(items) > 2:
                items[2]["amount"] = round(billed_amount * 0.32, 2)
                
    # 3. Policy Boundaries Check
    validation_engine = PolicyValidationEngine()
    db_policy = MockPolicy(status=policy_status, max_coverage_amount=max_coverage)
    validation_results = await validation_engine.validate_coverage(db_policy, extracted_data)
    
    # 4. Fraud Risk Assessment
    fraud_engine = FraudDetectionEngine()
    fraud_results = await fraud_engine.analyze_risk(extracted_data)
    
    # If the user explicitly simulated Medium or High fraud risk, adjust the results to match
    if fraud_risk.lower() == "high":
        fraud_results["risk_score"] = max(75, fraud_results.get("risk_score", 0))
        fraud_results["risk_level"] = "HIGH"
        fraud_results["is_suspect"] = True
        if "SUSPECT_METADATA_ANOMALY" not in fraud_results["flags_triggered"]:
            fraud_results["flags_triggered"].append("SUSPECT_METADATA_ANOMALY")
    elif fraud_risk.lower() == "medium":
        fraud_results["risk_score"] = max(45, fraud_results.get("risk_score", 0))
        fraud_results["risk_level"] = "MEDIUM"
        fraud_results["is_suspect"] = False
        if "REVIEW_TRIGGER_KEYWORD" not in fraud_results["flags_triggered"]:
            fraud_results["flags_triggered"].append("REVIEW_TRIGGER_KEYWORD")
            
    # 5. Adjudication & Recommendation
    advisor_engine = RecommendationEngine()
    recommendation = await advisor_engine.generate_recommendation(validation_results, fraud_results)
    
    return {
        "status": "success",
        "message": "Claim analysis complete.",
        "extracted_data": extracted_data,
        "validation_results": validation_results,
        "fraud_results": fraud_results,
        "recommendation": recommendation
    }
