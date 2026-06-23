import logging

# Setup app logger
logger = logging.getLogger("app")

class PolicyValidationEngine:
    """
    Engine to validate claim amount against policy status and coverage limits.
    """
    async def validate_coverage(self, db_policy, extracted_claim_data: dict) -> dict:
        logger.info(f"Core business coverage validation check started for Policy ID: {getattr(db_policy, 'id', 'Unknown')}")
        
        try:
            # Extract billing amount safely, default to 0.0 if not present or None
            raw_billed_amount = extracted_claim_data.get("total_billed_amount")
            requested_amount = float(raw_billed_amount) if raw_billed_amount is not None else 0.0
            
            policy_status = getattr(db_policy, "status", "unknown")
            max_coverage = float(getattr(db_policy, "max_coverage_amount", 0.0))
            
            # 1. Check if policy is active
            if str(policy_status).lower() != "active":
                summary = f"Claim rejected: Policy is inactive (status: '{policy_status}')."
                logger.info(summary)
                return {
                    "is_valid": False,
                    "policy_status": policy_status,
                    "requested_amount": requested_amount,
                    "allowed_amount": 0.0,
                    "validation_summary": summary
                }
            
            # 2. Compare total billed amount against max coverage amount
            if requested_amount <= max_coverage:
                summary = f"Claim approved: Billed amount ({requested_amount}) is within policy limits (max: {max_coverage})."
                logger.info(summary)
                return {
                    "is_valid": True,
                    "policy_status": policy_status,
                    "requested_amount": requested_amount,
                    "allowed_amount": requested_amount,
                    "validation_summary": summary
                }
            else:
                summary = f"Claim partially approved: Billed amount ({requested_amount}) exceeds policy limits (max: {max_coverage}). Capped at limit."
                logger.info(summary)
                return {
                    "is_valid": True,
                    "policy_status": policy_status,
                    "requested_amount": requested_amount,
                    "allowed_amount": max_coverage,
                    "validation_summary": summary
                }
                
        except Exception as e:
            error_msg = f"Zero-crash pipeline fallback: Error occurred during policy validation: {str(e)}"
            logger.error(error_msg)
            return {
                "is_valid": False,
                "policy_status": "error",
                "requested_amount": 0.0,
                "allowed_amount": 0.0,
                "validation_summary": error_msg
            }
