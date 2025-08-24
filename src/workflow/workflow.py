from src.llms.llm import llm
from src.utils.logger import log
from typing import Dict, Any, Literal

def identify_question_type(input_text: str) -> Dict[str, Any]:
    """
    Identifies if the input is a question and what type of question it is.
    
    Args:
        input_text: The input text from the user
        
    Returns:
        A dictionary with the analysis results
    """
    log.info("Identifying question type")
    
    prompt = f"""
    Analyze the following input and determine:
    1. Is it a question? (yes/no)
    2. If it is a question, is it about:
       - A job position (yes/no)
       - A company (yes/no)
    
    Input: "{input_text}"
    
    Return ONLY a JSON object with the following structure:
    {{
        "is_question": true/false,
        "about_position": true/false,
        "about_company": true/false
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        # Extract the JSON from the response
        response_text = response.content.strip()
        
        # Simple parsing to extract JSON (assuming the LLM follows instructions)
        import json
        import re
        
        # Find JSON pattern in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            result = json.loads(json_str)
            log.info(f"Question type identified: {result}")
            return result
        else:
            log.error("Failed to parse JSON from LLM response")
            return {
                "is_question": False,
                "about_position": False,
                "about_company": False
            }
            
    except Exception as e:
        log.error(f"Error identifying question type: {str(e)}")
        return {
            "is_question": False,
            "about_position": False,
            "about_company": False
        }

def fetch_position_data(input_text: str) -> str:
    """
    Fetches data about a position based on the input question.
    
    Args:
        input_text: The input question about a position
        
    Returns:
        Information about the position
    """
    log.info("Fetching position data")
    
    # This is a basic implementation that can be expanded later
    prompt = f"""
    The user has asked a question about a job position: "{input_text}"
    
    Provide information about the job position. This is a placeholder function that would normally
    fetch real position data from a database or API.
    
    For now, return a brief description of what a typical position in this field might involve,
    including responsibilities and required skills.
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        log.error(f"Error fetching position data: {str(e)}")
        return "I'm sorry, I couldn't retrieve information about this position at the moment."

def fetch_company_data(input_text: str) -> str:
    """
    Fetches data about a company based on the input question.
    
    Args:
        input_text: The input question about a company
        
    Returns:
        Information about the company
    """
    log.info("Fetching company data")
    
    # This is a basic implementation that can be expanded later
    prompt = f"""
    The user has asked a question about a company: "{input_text}"
    
    Provide information about the company. This is a placeholder function that would normally
    fetch real company data from a database or API.
    
    For now, return a brief description of what a typical company in this industry might be like,
    including its possible size, structure, and focus areas.
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        log.error(f"Error fetching company data: {str(e)}")
        return "I'm sorry, I couldn't retrieve information about this company at the moment."

def process_input(input_text: str) -> Dict[str, Any]:
    """
    Main workflow function that processes the input and returns the appropriate response.
    
    Args:
        input_text: The input text from the user
        
    Returns:
        A dictionary with the response and success status
    """
    log.info(f"Processing input: {input_text}")
    
    try:
        # Step 1: Identify the question type
        question_analysis = identify_question_type(input_text)
        
        # If it's not a question, return a generic response
        if not question_analysis.get("is_question", False):
            return {
                "success": True,
                "response": "I can answer questions about job positions and companies. Please ask a specific question."
            }
        
        # Step 2: Based on the question type, fetch the appropriate data
        if question_analysis.get("about_position", False):
            response_content = fetch_position_data(input_text)
            return {
                "success": True,
                "response": response_content
            }
        elif question_analysis.get("about_company", False):
            response_content = fetch_company_data(input_text)
            return {
                "success": True,
                "response": response_content
            }
        else:
            # If it's a question but not about position or company
            return {
                "success": True,
                "response": "I can only answer questions about job positions and companies. Please ask a specific question about either of these topics."
            }
            
    except Exception as e:
        log.error(f"Error in workflow processing: {str(e)}")
        return {
            "success": False,
            "error": "An unexpected error occurred while processing your request. Please try again later."
        }
