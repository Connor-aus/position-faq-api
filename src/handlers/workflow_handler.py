from src.utils.logger import log
from src.api.workflow_request_validation import validate_input
from src.workflow.workflow import process_input
from typing import Optional, Dict, Any

def handle_workflow_request(input_text: str, position_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Handles a workflow request by validating the input and processing it through the workflow.
    
    Args:
        input_text: The question from the user
        position_id: The ID of the position (optional for backward compatibility)
        
    Returns:
        A dictionary with the response and success status
    """
    log.info(f"Validating and processing workflow request for position ID: {position_id}")

    try:
        # Validate the input
        validate_input(input_text)
        log.info("Workflow request validated")        
        
        # Process the input through the workflow
        result = process_input(input_text, position_id)
        
        log.info(f"Workflow response: {result}")
        return result

    except ValueError as ve:
        log.warning(f"Validation error: {str(ve)}")
        return {
            "success": False,
            "error": str(ve)
        }
    except Exception as e:
        log.exception("Workflow processing failed")
        return {
            "success": False,
            "error": "An unexpected error occurred while processing your request. Please try again later."
        }
