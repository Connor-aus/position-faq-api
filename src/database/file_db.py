"""
Database interface for managing JSON data files in the staticFiles folder.
"""

import os
import json
import re
import glob
from typing import Dict, Any, Optional, List, Tuple
from src.utils.logger import log

# Base directory for static files
STATIC_FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "staticFiles")

def _get_file_pattern(data_type: str, data_id: Optional[int] = None) -> str:
    """
    Generate a file pattern for glob search
    
    Args:
        data_type: The type of data ('com' or 'pos')
        data_id: Optional ID to filter by
        
    Returns:
        A glob pattern string
    """
    if data_id is not None:
        return os.path.join(STATIC_FILES_DIR, f"example-data-{data_type}-{data_id}-*.json")
    return os.path.join(STATIC_FILES_DIR, f"example-data-{data_type}-*.json")

def _parse_file_info(file_path: str) -> Tuple[str, int, int]:
    """
    Parse file name to extract data type, ID and version
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple of (data_type, id, version)
    """
    file_name = os.path.basename(file_path)
    match = re.match(r'example-data-(\w+)-(\d+)-(\d+)\.json', file_name)
    if match:
        data_type, data_id, version = match.groups()
        return data_type, int(data_id), int(version)
    raise ValueError(f"Invalid file name format: {file_name}")

def _get_latest_version_file(data_type: str, data_id: int) -> Optional[str]:
    """
    Get the path to the latest version file for a specific data type and ID
    
    Args:
        data_type: The type of data ('com' or 'pos')
        data_id: The ID to look for
        
    Returns:
        Path to the latest version file or None if not found
    """
    pattern = _get_file_pattern(data_type, data_id)
    files = glob.glob(pattern)
    
    if not files:
        log.warning(f"No {data_type} files found for ID: {data_id}")
        return None
    
    # Extract versions and find the latest one
    latest_version = 0
    latest_file = None
    
    for file in files:
        _, _, version = _parse_file_info(file)
        if version > latest_version:
            latest_version = version
            latest_file = file
    
    return latest_file

def _get_next_id(data_type: str) -> int:
    """
    Get the next available ID for a data type
    
    Args:
        data_type: The type of data ('com' or 'pos')
        
    Returns:
        The next available ID
    """
    pattern = _get_file_pattern(data_type)
    files = glob.glob(pattern)
    
    if not files:
        # Default starting IDs
        return 1001 if data_type == "pos" else 2001
    
    # Find the highest ID
    max_id = 0
    for file in files:
        _, file_id, _ = _parse_file_info(file)
        max_id = max(max_id, file_id)
    
    # Return the next ID
    return max_id + 1

def get_company_data(company_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve the latest version of company data for the specified ID
    
    Args:
        company_id: The company ID to retrieve
        
    Returns:
        Company data dictionary or None if not found
    """
    file_path = _get_latest_version_file("com", company_id)
    if not file_path:
        return None
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        log.error(f"Error reading company data file: {str(e)}")
        return None

def get_position_data(position_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve the latest version of position data for the specified ID
    
    Args:
        position_id: The position ID to retrieve
        
    Returns:
        Position data dictionary or None if not found
    """
    file_path = _get_latest_version_file("pos", position_id)
    if not file_path:
        return None
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        log.error(f"Error reading position data file: {str(e)}")
        return None

def save_company_data(data: Dict[str, Any], company_id: Optional[int] = None) -> Tuple[bool, int, int]:
    """
    Save company data to a file
    
    Args:
        data: The company data to save
        company_id: Optional company ID. If None, a new ID will be generated
        
    Returns:
        Tuple of (success, company_id, version)
    """
    data_type = "com"
    
    # Determine ID and version
    if company_id is None:
        # Create new company with new ID
        company_id = _get_next_id(data_type)
        version = 1
    else:
        # Check if company exists and get next version
        file_path = _get_latest_version_file(data_type, company_id)
        if file_path:
            _, _, current_version = _parse_file_info(file_path)
            version = current_version + 1
        else:
            # Company ID specified but no file exists
            version = 1
    
    # Ensure company ID is set in the data
    if "companyInfo" in data:
        for item in data["companyInfo"]:
            if "companyId" in item:
                item["companyId"] = company_id
    
    if "companyFAQs" in data:
        for item in data["companyFAQs"]:
            if "companyId" in item:
                item["companyId"] = company_id
    
    # Create the file path
    file_name = f"example-data-{data_type}-{company_id}-{version}.json"
    file_path = os.path.join(STATIC_FILES_DIR, file_name)
    
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
        log.info(f"Saved company data to {file_path}")
        return True, company_id, version
    except Exception as e:
        log.error(f"Error saving company data: {str(e)}")
        return False, company_id, version

def save_position_data(data: Dict[str, Any], position_id: Optional[int] = None) -> Tuple[bool, int, int]:
    """
    Save position data to a file
    
    Args:
        data: The position data to save
        position_id: Optional position ID. If None, a new ID will be generated
        
    Returns:
        Tuple of (success, position_id, version)
    """
    data_type = "pos"
    
    # Determine ID and version
    if position_id is None:
        # Create new position with new ID
        position_id = _get_next_id(data_type)
        version = 1
    else:
        # Check if position exists and get next version
        file_path = _get_latest_version_file(data_type, position_id)
        if file_path:
            _, _, current_version = _parse_file_info(file_path)
            version = current_version + 1
        else:
            # Position ID specified but no file exists
            version = 1
    
    # Ensure position ID is set in the data
    if "position" in data:
        data["position"]["id"] = position_id
        # Set the version in the position data
        data["position"]["version"] = version
    
    if "positionInfo" in data:
        for item in data["positionInfo"]:
            if "positionId" in item:
                item["positionId"] = position_id
    
    if "positionFAQs" in data:
        for item in data["positionFAQs"]:
            if "positionId" in item:
                item["positionId"] = position_id
    
    # Create the file path
    file_name = f"example-data-{data_type}-{position_id}-{version}.json"
    file_path = os.path.join(STATIC_FILES_DIR, file_name)
    
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
        log.info(f"Saved position data to {file_path}")
        return True, position_id, version
    except Exception as e:
        log.error(f"Error saving position data: {str(e)}")
        return False, position_id, version

def get_positions_by_company_id(company_id: int) -> List[Dict[str, Any]]:
    """
    Retrieve all position data associated with a specific company ID
    
    Args:
        company_id: The company ID to retrieve positions for
        
    Returns:
        List of position data dictionaries
    """
    pattern = _get_file_pattern("pos")
    files = glob.glob(pattern)
    
    positions = []
    
    for file_path in files:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Check if this position belongs to the specified company
                if "position" in data and data["position"].get("companyId") == company_id:
                    # Get the position ID and check if we already have a newer version
                    position_id = data["position"]["id"]
                    
                    # Check if we already have this position in our list
                    existing_position = next((p for p in positions if p["position"]["id"] == position_id), None)
                    
                    if existing_position:
                        # Compare versions and keep the newer one
                        if data["position"].get("version", 0) > existing_position["position"].get("version", 0):
                            # Replace with newer version
                            positions.remove(existing_position)
                            positions.append(data)
                    else:
                        # Add new position
                        positions.append(data)
                        
        except (json.JSONDecodeError, FileNotFoundError) as e:
            log.error(f"Error reading position data file {file_path}: {str(e)}")
            continue
    
    log.info(f"Found {len(positions)} positions for company ID: {company_id}")
    return positions

def get_all_position_versions(position_id: int) -> List[Dict[str, Any]]:
    """
    Retrieve all versions of position data for the specified ID
    
    Args:
        position_id: The position ID to retrieve all versions for
        
    Returns:
        List of position data dictionaries, sorted by version (newest first)
    """
    pattern = _get_file_pattern("pos", position_id)
    files = glob.glob(pattern)
    
    if not files:
        log.warning(f"No position files found for ID: {position_id}")
        return []
    
    versions = []
    
    for file_path in files:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Add the file path to the data for reference
                data["_file_path"] = file_path
                versions.append(data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            log.error(f"Error reading position data file {file_path}: {str(e)}")
            continue
    
    # Sort by version (descending)
    versions.sort(key=lambda x: x["position"].get("version", 0), reverse=True)
    
    # Remove the file path reference before returning
    for version in versions:
        if "_file_path" in version:
            del version["_file_path"]
    
    log.info(f"Found {len(versions)} versions for position ID: {position_id}")
    return versions