from src.utils.logger import log
from src.api.workflow_request_validation import validate_input
from src.workflow.workflow import process_input

def handle_workflow_request(input_text: str) -> dict:
    """
    Handles a workflow request by validating the input and processing it through the workflow.
    
    Args:
        input_text: The input text from the user
        
    Returns:
        A dictionary with the response and success status
    """
    log.info("Validating and processing workflow request")

    try:
        # Validate the input
        validate_input(input_text)
        log.info("Workflow request validated")        
        
        # Process the input through the workflow
        result = process_input(input_text)
        
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
