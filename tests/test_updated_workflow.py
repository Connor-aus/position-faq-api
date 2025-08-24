"""
Tests for the updated workflow using the file database interface
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.workflow.workflow import process_input

class TestUpdatedWorkflow(unittest.TestCase):
    """Test cases for the updated workflow"""
    
    @patch('src.workflow.workflow.get_position_data')
    @patch('src.workflow.workflow.get_company_data')
    @patch('src.workflow.workflow.llm')
    def test_workflow_with_position_and_company_data(self, mock_llm, mock_get_company_data, mock_get_position_data):
        """Test the workflow with both position and company data"""
        # Mock position data
        mock_position_data = {
            "position": {
                "id": 1001,
                "companyId": 2001,
                "positionDescription": "Test position",
                "version": 1
            },
            "positionFAQs": [
                {
                    "id": 50001,
                    "positionId": 1001,
                    "question": "Test question",
                    "response": "Test response"
                }
            ],
            "positionInfo": [
                {
                    "id": 60001,
                    "positionId": 1001,
                    "subject": "Test subject",
                    "answer": "Test answer"
                }
            ]
        }
        
        # Mock company data
        mock_company_data = {
            "companyFAQs": [
                {
                    "id": 70001,
                    "companyId": 2001,
                    "question": "Test company question",
                    "answer": "Test company answer"
                }
            ],
            "companyInfo": [
                {
                    "id": 80001,
                    "companyId": 2001,
                    "subject": "Test company subject",
                    "answer": "Test company answer"
                }
            ]
        }
        
        # Set up the mocks
        mock_get_position_data.return_value = mock_position_data
        mock_get_company_data.return_value = mock_company_data
        
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.content = "This is a test response from the LLM"
        mock_llm.invoke.return_value = mock_response
        
        # Call the function
        result = process_input("What is the work schedule?", 1001)
        
        # Verify the result
        self.assertTrue(result["success"])
        self.assertEqual(result["response"], "This is a test response from the LLM")
        
        # Verify that the functions were called with the right parameters
        mock_get_position_data.assert_called_once_with(1001)
        mock_get_company_data.assert_called_once_with(2001)
        
        # Verify that the LLM was called with both position and company data
        llm_call_args = mock_llm.invoke.call_args[0][0]
        self.assertIn("Test position", llm_call_args)
        self.assertIn("Test company question", llm_call_args)
    
    @patch('src.workflow.workflow.get_position_data')
    @patch('src.workflow.workflow.get_company_data')
    @patch('src.workflow.workflow.llm')
    def test_workflow_with_missing_company_data(self, mock_llm, mock_get_company_data, mock_get_position_data):
        """Test the workflow when company data is missing"""
        # Mock position data
        mock_position_data = {
            "position": {
                "id": 1001,
                "companyId": 2001,
                "positionDescription": "Test position",
                "version": 1
            },
            "positionFAQs": [],
            "positionInfo": []
        }
        
        # Set up the mocks
        mock_get_position_data.return_value = mock_position_data
        mock_get_company_data.return_value = None
        
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.content = "This is a test response with missing company data"
        mock_llm.invoke.return_value = mock_response
        
        # Call the function
        result = process_input("What is the work schedule?", 1001)
        
        # Verify the result
        self.assertTrue(result["success"])
        self.assertEqual(result["response"], "This is a test response with missing company data")
        
        # Verify that the functions were called with the right parameters
        mock_get_position_data.assert_called_once_with(1001)
        mock_get_company_data.assert_called_once_with(2001)
        
        # Verify that the LLM was called with empty company data
        llm_call_args = mock_llm.invoke.call_args[0][0]
        self.assertIn("Test position", llm_call_args)
        self.assertIn("COMPANY FAQs:", llm_call_args)
        self.assertIn("[]", llm_call_args)

if __name__ == "__main__":
    unittest.main()
