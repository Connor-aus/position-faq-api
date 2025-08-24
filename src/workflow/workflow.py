from src.llms.llm import llm
from src.utils.logger import log
from src.database.file_db import get_position_data, get_company_data
from typing import Dict, Any, Literal, Optional
import json
import re
import datetime

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

def summarize_question(question: str) -> str:
    """
    Summarize a question to make it more general for FAQ storage.
    
    Args:
        question: The original question from the user
        
    Returns:
        A summarized version of the question
    """
    log.info("Summarizing question for FAQ storage")
    
    prompt = f"""
    Summarize the following question to make it more general and suitable for an FAQ:
    
    Original question: "{question}"
    
    Your summary should:
    1. Maintain the core intent of the question
    2. Remove any personal details or specifics that wouldn't apply to other users
    3. Be concise and clear
    4. End with a question mark
    5. Be in the form of a question someone might ask about a job position
    
    Return ONLY the summarized question, without any explanation or additional text.
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        log.error(f"Error summarizing question: {str(e)}")
        # If summarization fails, return the original question
        return question

def increment_faq_times_asked(position_data: Dict[str, Any], faq_id: int) -> Dict[str, Any]:
    """
    Increment the timesAsked counter for an existing FAQ.
    
    Args:
        position_data: The position data to update
        faq_id: The ID of the FAQ to update
        
    Returns:
        Updated position data with incremented timesAsked
    """
    log.info(f"Incrementing timesAsked for FAQ ID {faq_id}")
    
    # Get existing FAQs
    position_faqs = position_data.get("positionFAQs", [])
    
    # Find the FAQ with the matching ID
    for faq in position_faqs:
        if faq.get("id") == faq_id:
            # Increment the timesAsked counter
            current_times_asked = faq.get("timesAsked", 0)
            faq["timesAsked"] = current_times_asked + 1
            
            # Update the timestamp
            faq["timestamp"] = datetime.datetime.now().isoformat()
            
            log.info(f"Incremented timesAsked for FAQ ID {faq_id} to {faq['timesAsked']}")
            break
    
    # Update the position data
    position_data["positionFAQs"] = position_faqs
    
    return position_data

def add_question_to_faqs(question: str, position_data: Dict[str, Any], position_id: int) -> Dict[str, Any]:
    """
    Add an unanswered question to the position FAQs.
    
    Args:
        question: The question to add
        position_data: The position data to update
        position_id: The ID of the position
        
    Returns:
        Updated position data with the new FAQ added
    """
    log.info(f"Adding unanswered question to FAQs for position ID {position_id}")
    
    # Summarize the question
    summarized_question = summarize_question(question)
    
    # Get existing FAQs
    position_faqs = position_data.get("positionFAQs", [])
    
    # Generate a new unique ID
    # Find the highest existing FAQ ID and increment by 1
    next_id = 50001  # Default starting ID
    for faq in position_faqs:
        if faq.get("id", 0) >= next_id:
            next_id = faq.get("id", 0) + 1
    
    # Create the new FAQ entry
    current_time = datetime.datetime.now().isoformat()
    
    new_faq = {
        "id": next_id,
        "positionId": position_id,
        "generatedByUser": True,
        "answeredByHR": False,
        "timesAsked": 1,
        "question": summarized_question,
        "response": None,
        "version": 1,
        "timestamp": current_time
    }
    
    # Add to position FAQs
    position_faqs.append(new_faq)
    position_data["positionFAQs"] = position_faqs
    
    return position_data

def process_question_with_llm(question: str, position_data: Dict[str, Any], company_data: Dict[str, Any]) -> str:
    """
    Process a question using the LLM with position data.
    
    Args:
        question: The question from the user
        position_data: The position data from the database
        company_data: The company data from the database
        
    Returns:
        The response from the LLM
    """
    log.info("Processing question with LLM")
    
    # Format the position data for the prompt
    position_info = position_data.get("position", {})
    position_faqs = position_data.get("positionFAQs", [])
    position_details = position_data.get("positionInfo", [])
    
    # Format the company data for the prompt
    company_faqs = company_data.get("companyFAQs", [])
    company_info = company_data.get("companyInfo", [])
    
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
    
    3. Check if the question is similar to any existing FAQ in the position FAQs. If it is, note the ID of the most similar FAQ.
    
    4. Use the position or company information provided above to answer the question, or state that there is no answer available in the provided information.
    
    5. Return your response in JSON format with the following structure:
       {{
         "similar_question_id": null or the ID of the most similar question found,
         "response": "Your answer to the user's question or appropriate message"
       }}
    
    If there is a similar question with an answer, provide that answer in the response field.
    If there is a similar question without an answer (response: null), set the response to: "This question has been passed to the hiring manager."
    If there is no similar question and no answer available, set the response to: "This question has been added to the question list for the Hiring Manager."
    If there is an answer available in the provided information but no similar question, provide that answer in the response field and set similar_question_id to null.
    
    Return ONLY the JSON object described above, without any additional text or explanation.
    """
    
    try:
        response = llm.invoke(prompt)
        response_text = response.content.strip()
        
        # Parse the JSON response
        try:
            # Find JSON pattern in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                log.info(f"Parsed LLM response: {result}")
                return result
            else:
                log.error("Failed to parse JSON from LLM response")
                return {
                    "similar_question_id": None,
                    "response": "I'm sorry, I couldn't process your question at the moment. Please try again later."
                }
        except json.JSONDecodeError as je:
            log.error(f"JSON decode error: {str(je)}")
            return {
                "similar_question_id": None,
                "response": response_text  # Return the raw response as fallback
            }
    except Exception as e:
        log.error(f"Error processing question with LLM: {str(e)}")
        return {
            "similar_question_id": None,
            "response": "I'm sorry, I couldn't process your question at the moment. Please try again later."
        }

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
        # If no position ID is provided, return an error
        if position_id is None:
            return {
                "success": False,
                "error": "Position ID is required"
            }
            
        # Step 1: Retrieve data for the position
        position_data = get_position_data(position_id)
        if position_data is None:
            return {
                "success": False,
                "error": f"Position with ID {position_id} not found"
            }
        
        # Step 2: Get the company ID from the position data and retrieve company data
        company_id = position_data.get("position", {}).get("companyId")
        if not company_id:
            log.warning(f"No company ID found in position data for position ID {position_id}")
            company_data = {"companyFAQs": [], "companyInfo": []}
        else:
            company_data = get_company_data(company_id)
            if company_data is None:
                log.warning(f"Company data not found for company ID {company_id}")
                company_data = {"companyFAQs": [], "companyInfo": []}
            
        # Step 3: Process the question using the LLM with both position and company data
        llm_result = process_question_with_llm(input_text, position_data, company_data)
        
        # Extract the response content and similar question ID
        response_content = llm_result.get("response", "I'm sorry, I couldn't process your question at the moment.")
        similar_question_id = llm_result.get("similar_question_id")
        
        # Step 4: Handle the response based on whether a similar question was found
        from src.database.file_db import save_position_data
        
        if similar_question_id is not None:
            # A similar question was found, increment the timesAsked counter
            log.info(f"Similar question found with ID: {similar_question_id}")
            updated_position_data = increment_faq_times_asked(position_data, similar_question_id)
            
            # Save the updated position data
            success, _, _ = save_position_data(updated_position_data, position_id)
            
            if not success:
                log.warning(f"Failed to save updated position data for position ID {position_id}")
        elif "This question has been added to the question list for the Hiring Manager" in response_content:
            # No similar question was found and the question couldn't be answered
            log.info("No similar question found, adding new question to FAQs")
            updated_position_data = add_question_to_faqs(input_text, position_data, position_id)
            
            # Save the updated position data
            success, _, _ = save_position_data(updated_position_data, position_id)
            
            if not success:
                log.warning(f"Failed to save updated position data for position ID {position_id}")
        
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