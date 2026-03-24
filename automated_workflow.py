import logging
from ai_models import decision_model
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_incoming_data(payload: dict) -> dict:
    """
    Main entry point for processing incoming API payload.
    1. Validates/transforms data.
    2. Consults AI model.
    3. Triggers downstream actions if necessary.
    """
    logger.info(f"Received payload for processing: {payload}")
    
    # 1. Transform data if needed for the AI model
    mapped_data = {
        'amount': payload.get('transaction_amount', 0.0),
        'frequency': payload.get('user_transaction_frequency', 1.0),
        'time_of_day': payload.get('hour_of_day', 12.0)
    }
    
    # 2. Get AI Prediction using the pre-loaded ML model
    ai_result = decision_model.predict(mapped_data)
    logger.info(f"AI Model Decision: {ai_result}")
    
    # 3. Trigger Actions based on prediction
    actions_taken = trigger_actions(payload, ai_result)
    
    return {
        "status": "success",
        "processed_data": mapped_data,
        "ai_analysis": ai_result,
        "actions_taken": actions_taken
    }

def trigger_actions(original_payload: dict, ai_result: dict) -> list:
    """
    Executes business logic based on AI output.
    Supports integration with external APIs based on decisions.
    """
    actions = []
    
    if ai_result.get("action_required"):
        # E.g., block transaction, alert admin, call external API
        logger.warning("Action required: Flagged as anomalous. Triggering alerts...")
        actions.append("alert_admin")
        
        # Mock external API integration snippet:
        # try:
        #     response = requests.post("https://api.external-service.com/alerts", json=original_payload, timeout=5)
        #     if response.status_code == 200:
        #         actions.append("external_alert_dispatched")
        # except requests.RequestException as e:
        #     logger.error(f"Failed to dispatch external alert: {e}")
            
    else:
        logger.info("No action required. Payload looks normal.")
        actions.append("approve_transaction")
        
    return actions
