import json
import os
from typing import Dict, Any, Optional
from src.utils.logger import log

def load_position_data(position_id: int) -> Optional[Dict[str, Any]]:
    """
    Load position data from the example_data.json file based on position ID
    
    Args:
        position_id: The ID of the position to retrieve data for
        
    Returns:
        A dictionary containing the position data, or None if not found
    """
    try:
        # Path to the example data file
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               "staticFiles", "example_data.json")
        
        log.info(f"Loading position data from {file_path} for position ID: {position_id}")
        
        # Read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Check if the position ID matches
        if data.get("position", {}).get("id") != position_id:
            log.warning(f"Position ID {position_id} not found in data")
            return None
            
        return data
        
    except FileNotFoundError:
        log.error(f"Example data file not found")
        return None
    except json.JSONDecodeError:
        log.error(f"Error decoding JSON from example data file")
        return None
    except Exception as e:
        log.exception(f"Unexpected error loading position data: {str(e)}")
        return None
