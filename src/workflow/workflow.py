from src.llms.llm import llm
from src.utils.logger import log
from src.utils.data_loader import load_position_data
from typing import Dict, Any, Literal, Optional
import json

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

def process_question_with_llm(question: str, position_data: Dict[str, Any]) -> str:
    """
    Process a question using the LLM with position data.
    
    Args:
        question: The question from the user
        position_data: The position data from the database
        
    Returns:
        The response from the LLM
    """
    log.info("Processing question with LLM")
    
    # Format the position data for the prompt
    position_info = position_data.get("position", {})
    position_faqs = position_data.get("positionFAQs", [])
    position_details = position_data.get("positionInfo", [])
    company_faqs = position_data.get("companyFAQs", [])
    company_info = position_data.get("companyInfo", [])
    
    # Create a formatted string of the data for the prompt
    position_data_str = f"""
    POSITION DESCRIPTION:
    {position_info.get('positionDescription', 'No description available')}
    
    POSITION FAQs:
    {json.dumps(position_faqs, indent=2)}
    
    POSITION INFO:
    {json.dumps(position_details, indent=2)}
    
    COMPANY FAQs:
    {json.dumps(company_faqs, indent=2)}
    
    COMPANY INFO:
    {json.dumps(company_info, indent=2)}
    """
    
    # Create the prompt for the LLM
    prompt = f"""
    You are an AI assistant that helps answer questions about job positions. 
    You have been provided with the following information about a position:
    
    {position_data_str}
    
    A user has asked the following question: "{question}"
    
    Please follow these steps:
    
    1. Ensure that the user's input is a question. If it's not a question, politely ask them to rephrase as a question.
    
    2. Identify if the question is about the company or the position.
    
    3. Use the position or company information provided above to answer the question, or state that there is no answer available in the provided information.
    
    4. If there is no answer to the question within the provided information, but the question is very similar to one of the FAQs that has "response": null and "generatedByUser": true, then respond with: "This question has been passed to the hiring manager."
    
    5. If there is no answer to the question within the provided information and the question is not very similar to any existing FAQ question, respond with: "This question has been added to the question list for the Hiring Manager."
    
    6. If there is an answer to the question within the provided information, provide an appropriate and concise answer.
    
    Respond with ONLY the final answer, without explaining your reasoning or listing the steps you followed.
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        log.error(f"Error processing question with LLM: {str(e)}")
        return "I'm sorry, I couldn't process your question at the moment. Please try again later."

def process_input(input_text: str, position_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Main workflow function that processes the input and returns the appropriate response.
    
    Args:
        input_text: The question from the user
        position_id: The ID of the position
        
    Returns:
        A dictionary with the response and success status
    """
    log.info(f"Processing input for position ID {position_id}: {input_text}")
    
    try:
        # If no position ID is provided, use the old workflow
        if position_id is None:
            return process_legacy_input(input_text)
            
        # Step 1: Retrieve data for the position
        position_data = load_position_data(position_id)
        if position_data is None:
            return {
                "success": False,
                "error": f"Position with ID {position_id} not found"
            }
            
        # Step 2: Process the question using the LLM
        response_content = process_question_with_llm(input_text, position_data)
        
        return {
            "success": True,
            "response": response_content
        }
            
    except Exception as e:
        log.error(f"Error in workflow processing: {str(e)}")
        return {
            "success": False,
            "error": "An unexpected error occurred while processing your request. Please try again later."
        }
        
def process_legacy_input(input_text: str) -> Dict[str, Any]:
    """
    Legacy workflow function that processes the input without position data.
    
    Args:
        input_text: The input text from the user
        
    Returns:
        A dictionary with the response and success status
    """
    log.info(f"Processing legacy input: {input_text}")
    
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
        log.error(f"Error in legacy workflow processing: {str(e)}")
        return {
            "success": False,
            "error": "An unexpected error occurred while processing your request. Please try again later."
        }