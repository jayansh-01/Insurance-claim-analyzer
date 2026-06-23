import logging

# Setup app logger
logger = logging.getLogger("app")

class FraudDetectionEngine:
    """
    Engine to assess risk and trigger automated fraud detection checks on claim data.
    """
    async def analyze_risk(self, extracted_data: dict) -> dict:
        logger.info("Automated fraud analysis sequence commenced.")
        
        try:
            risk_score = 0
            flags = []
            
            # 1. Total Billed Amount Check
            raw_amount = extracted_data.get("total_billed_amount")
            try:
                billed_amount = float(raw_amount) if raw_amount is not None else 0.0
            except (ValueError, TypeError):
                billed_amount = 0.0
                
            if billed_amount > 50000:
                risk_score += 40
                flags.append("HIGH_VALUE_CLAIM")
                
            # 2. Customer Name Anomaly Checks
            customer_name = extracted_data.get("customer_name")
            if not customer_name or not str(customer_name).strip():
                risk_score += 20
                flags.append("MISSING_CUSTOMER_NAME")
            else:
                customer_name_lower = str(customer_name).lower()
                if any(kw in customer_name_lower for kw in ["test", "dummy", "fake", "anonymous"]):
                    risk_score += 15
                    flags.append("SUSPECT_CUSTOMER_NAME")
            
            # 3. Policy Number Checks
            policy_number = extracted_data.get("policy_number")
            if not policy_number or not str(policy_number).strip():
                risk_score += 15
                flags.append("MISSING_POLICY_NUMBER")
                
            # 4. Extracted Items Checks
            extracted_items = extracted_data.get("extracted_items")
            if not extracted_items:
                risk_score += 30
                flags.append("NO_BILLING_ITEMS_FOUND")
            elif isinstance(extracted_items, list):
                has_dummy_item = False
                for item in extracted_items:
                    desc = str(item.get("description", "")).lower()
                    if any(kw in desc for kw in ["test", "dummy", "fake"]):
                        has_dummy_item = True
                        break
                if has_dummy_item:
                    risk_score += 15
                    flags.append("DUMMY_DATA_DETECTED")
            
            # Cap the risk score at 100
            risk_score = min(risk_score, 100)
            
            # Determine risk level based on the score
            if risk_score >= 70:
                risk_level = "HIGH"
            elif risk_score >= 30:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
                
            is_suspect = (risk_level == "HIGH")
            
            result = {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "flags_triggered": flags,
                "is_suspect": is_suspect
            }
            
            logger.info(f"Automated fraud analysis completed. Score: {risk_score}, Level: {risk_level}, Triggered flags: {flags}")
            return result
            
        except Exception as e:
            logger.error(f"Resilient pipeline fallback: Error in FraudDetectionEngine: {str(e)}")
            return {
                "risk_score": 50,  # Return a neutral caution value
                "risk_level": "MEDIUM",
                "flags_triggered": ["FRAUD_DETECTION_ERROR"],
                "is_suspect": False
            }
