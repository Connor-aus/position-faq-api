import unittest
from unittest.mock import patch, MagicMock
from src.handlers.workflow_handler import handle_workflow_request

class TestWorkflowHandler(unittest.TestCase):
    @patch('src.handlers.workflow_handler.validate_input')
    @patch('src.handlers.workflow_handler.process_input')
    def test_handle_workflow_request_success(self, mock_process, mock_validate):
        # Setup mocks
        mock_process.return_value = {
            "success": True,
            "response": "Test response"
        }
        
        # Test
        result = handle_workflow_request("Test input")
        
        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(result["response"], "Test response")
        mock_validate.assert_called_once_with("Test input")
        mock_process.assert_called_once_with("Test input")

    @patch('src.handlers.workflow_handler.validate_input')
    @patch('src.handlers.workflow_handler.process_input')
    def test_handle_workflow_request_failure(self, mock_process, mock_validate):
        # Setup mocks
        mock_process.return_value = {
            "success": False,
            "error": "Test error"
        }
        
        # Test
        result = handle_workflow_request("Test input")
        
        # Assert
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Test error")
        mock_validate.assert_called_once_with("Test input")
        mock_process.assert_called_once_with("Test input")

    @patch('src.handlers.workflow_handler.validate_input')
    def test_handle_workflow_request_validation_error(self, mock_validate):
        # Setup mock
        mock_validate.side_effect = ValueError("Validation error")
        
        # Test
        result = handle_workflow_request("Test input")
        
        # Assert
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Validation error")
        mock_validate.assert_called_once_with("Test input")

    @patch('src.handlers.workflow_handler.validate_input')
    @patch('src.handlers.workflow_handler.process_input')
    def test_handle_workflow_request_exception(self, mock_process, mock_validate):
        # Setup mock
        mock_process.side_effect = Exception("Test exception")
        
        # Test
        result = handle_workflow_request("Test input")
        
        # Assert
        self.assertFalse(result["success"])
        self.assertIn("unexpected error", result["error"])
        mock_validate.assert_called_once_with("Test input")
        mock_process.assert_called_once_with("Test input")

if __name__ == '__main__':
    unittest.main()
