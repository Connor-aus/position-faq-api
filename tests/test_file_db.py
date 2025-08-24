"""
Tests for the file database interface
"""

import os
import sys
import json
import unittest
from typing import Dict, Any

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.file_db import (
    get_company_data,
    get_position_data,
    save_company_data,
    save_position_data,
    _get_next_id,
    _parse_file_info
)

class TestFileDB(unittest.TestCase):
    """Test cases for file database interface"""
    
    def test_parse_file_info(self):
        """Test parsing file info from filename"""
        file_path = "example-data-com-2001-1.json"
        data_type, data_id, version = _parse_file_info(file_path)
        
        self.assertEqual(data_type, "com")
        self.assertEqual(data_id, 2001)
        self.assertEqual(version, 1)
        
    def test_get_company_data(self):
        """Test retrieving company data"""
        # This test assumes example-data-com-2001-1.json exists
        data = get_company_data(2001)
        
        self.assertIsNotNone(data)
        self.assertIn("companyFAQs", data)
        self.assertIn("companyInfo", data)
        
    def test_get_position_data(self):
        """Test retrieving position data"""
        # This test assumes example-data-pos-1001-1.json exists
        data = get_position_data(1001)
        
        self.assertIsNotNone(data)
        self.assertIn("position", data)
        self.assertIn("positionFAQs", data)
        self.assertIn("positionInfo", data)
        
    def test_save_and_retrieve_company_data(self):
        """Test saving and retrieving company data"""
        # Create sample company data
        company_data = {
            "companyFAQs": [
                {
                    "id": 70001,
                    "companyId": 9999,  # Will be updated by save function
                    "generatedByUser": False,
                    "answeredByHR": True,
                    "timesAsked": 1,
                    "question": "Test question",
                    "answer": "Test answer",
                    "version": 1,
                    "timestamp": "2025-08-24T10:20:00+10:00"
                }
            ],
            "companyInfo": [
                {
                    "id": 80001,
                    "companyId": 9999,  # Will be updated by save function
                    "generatedByUser": False,
                    "answeredByHR": True,
                    "subject": "Test subject",
                    "answer": "Test answer",
                    "version": 1,
                    "timestamp": "2025-08-24T10:05:00+10:00"
                }
            ]
        }
        
        # Save the data with a new ID
        success, company_id, version = save_company_data(company_data)
        
        self.assertTrue(success)
        self.assertGreater(company_id, 0)
        self.assertEqual(version, 1)
        
        # Retrieve the data
        retrieved_data = get_company_data(company_id)
        
        self.assertIsNotNone(retrieved_data)
        self.assertIn("companyFAQs", retrieved_data)
        self.assertIn("companyInfo", retrieved_data)
        
        # Update the data and save again
        retrieved_data["companyFAQs"][0]["answer"] = "Updated answer"
        success, updated_id, updated_version = save_company_data(retrieved_data, company_id)
        
        self.assertTrue(success)
        self.assertEqual(updated_id, company_id)
        self.assertEqual(updated_version, 2)
        
    def test_save_and_retrieve_position_data(self):
        """Test saving and retrieving position data"""
        # Create sample position data
        position_data = {
            "position": {
                "id": 9999,  # Will be updated by save function
                "companyId": 2001,
                "positionDescription": "Test position",
                "version": 1,
                "timestamp": "2025-08-24T15:05:00+10:00"
            },
            "positionFAQs": [
                {
                    "id": 50001,
                    "positionId": 9999,  # Will be updated by save function
                    "generatedByUser": False,
                    "answeredByHR": True,
                    "timesAsked": 1,
                    "question": "Test question",
                    "response": "Test response",
                    "version": 1,
                    "timestamp": "2025-08-24T12:10:00+10:00"
                }
            ],
            "positionInfo": [
                {
                    "id": 60001,
                    "positionId": 9999,  # Will be updated by save function
                    "generatedByUser": False,
                    "answeredByHR": True,
                    "subject": "Test subject",
                    "answer": "Test answer",
                    "version": 1,
                    "timestamp": "2025-08-24T11:55:00+10:00"
                }
            ]
        }
        
        # Save the data with a new ID
        success, position_id, version = save_position_data(position_data)
        
        self.assertTrue(success)
        self.assertGreater(position_id, 0)
        self.assertEqual(version, 1)
        
        # Retrieve the data
        retrieved_data = get_position_data(position_id)
        
        self.assertIsNotNone(retrieved_data)
        self.assertIn("position", retrieved_data)
        self.assertIn("positionFAQs", retrieved_data)
        self.assertIn("positionInfo", retrieved_data)
        
        # Update the data and save again
        retrieved_data["positionFAQs"][0]["response"] = "Updated response"
        success, updated_id, updated_version = save_position_data(retrieved_data, position_id)
        
        self.assertTrue(success)
        self.assertEqual(updated_id, position_id)
        self.assertEqual(updated_version, 2)

if __name__ == "__main__":
    unittest.main()
