from datetime import datetime, timezone
import logging

# Setup app logger
logger = logging.getLogger("app")

class RecommendationEngine:
    """
    Engine to make a final approval, rejection, or referral decision for claims.
    """
    async def generate_recommendation(self, validation_results: dict, fraud_results: dict) -> dict:
        logger.info("Final adjudication scoring sequence initiated.")
        
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            
            is_valid = validation_results.get("is_valid", False)
            validation_summary = validation_results.get("validation_summary", "No validation details available.")
            
            fraud_risk_level = str(fraud_results.get("risk_level", "LOW")).upper()
            
            # Rule 1: If policy validation fails, the claim is denied.
            if not is_valid:
                action = "DENIED"
                reason = f"Claim failed policy parameters: {validation_summary}"
                
            # Rule 2: If policy is valid but fraud risk is high, it is flagged for manual investigation.
            elif fraud_risk_level == "HIGH":
                action = "FLAGGED"
                reason = "Manual investigation required: High risk score and warning flags triggered."
                
            # Rule 3: If fraud risk is medium, it is flagged for a secondary review.
            elif fraud_risk_level == "MEDIUM":
                action = "FLAGGED"
                reason = "Secondary review required: Medium risk score and caution flags triggered."
                
            # Rule 4: If policy is valid and fraud risk is low, it is approved.
            else:
                action = "APPROVED"
                reason = f"Automated approval: {validation_summary}"
            
            result = {
                "recommended_action": action,
                "justification_reason": reason,
                "auto_adjudicated_at": timestamp
            }
            
            logger.info(f"Final adjudication completed. Decision: {action}. Reason: {reason}")
            return result
            
        except Exception as e:
            logger.error(f"Resilient pipeline fallback: Error in RecommendationEngine: {str(e)}")
            return {
                "recommended_action": "FLAGGED",
                "justification_reason": f"System error occurred during automated adjudication: {str(e)}. Defaulting to manual review.",
                "auto_adjudicated_at": datetime.now(timezone.utc).isoformat()
            }
