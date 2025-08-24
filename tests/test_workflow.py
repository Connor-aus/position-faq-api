import unittest
from unittest.mock import patch, MagicMock
from src.workflow.workflow import identify_question_type, fetch_position_data, fetch_company_data, process_input

class TestWorkflow(unittest.TestCase):
    @patch('src.workflow.workflow.llm')
    def test_identify_question_type_position(self, mock_llm):
        # Setup mock
        mock_response = MagicMock()
        mock_response.content = '{"is_question": true, "about_position": true, "about_company": false}'
        mock_llm.invoke.return_value = mock_response
        
        # Test
        result = identify_question_type("What skills are needed for a Software Engineer position?")
        
        # Assert
        self.assertTrue(result["is_question"])
        self.assertTrue(result["about_position"])
        self.assertFalse(result["about_company"])
        mock_llm.invoke.assert_called_once()

    @patch('src.workflow.workflow.llm')
    def test_identify_question_type_company(self, mock_llm):
        # Setup mock
        mock_response = MagicMock()
        mock_response.content = '{"is_question": true, "about_position": false, "about_company": true}'
        mock_llm.invoke.return_value = mock_response
        
        # Test
        result = identify_question_type("What is the culture like at Google?")
        
        # Assert
        self.assertTrue(result["is_question"])
        self.assertFalse(result["about_position"])
        self.assertTrue(result["about_company"])
        mock_llm.invoke.assert_called_once()

    @patch('src.workflow.workflow.llm')
    def test_fetch_position_data(self, mock_llm):
        # Setup mock
        mock_response = MagicMock()
        mock_response.content = "Position information"
        mock_llm.invoke.return_value = mock_response
        
        # Test
        result = fetch_position_data("What skills are needed for a Software Engineer position?")
        
        # Assert
        self.assertEqual(result, "Position information")
        mock_llm.invoke.assert_called_once()

    @patch('src.workflow.workflow.llm')
    def test_fetch_company_data(self, mock_llm):
        # Setup mock
        mock_response = MagicMock()
        mock_response.content = "Company information"
        mock_llm.invoke.return_value = mock_response
        
        # Test
        result = fetch_company_data("What is the culture like at Google?")
        
        # Assert
        self.assertEqual(result, "Company information")
        mock_llm.invoke.assert_called_once()

    @patch('src.workflow.workflow.identify_question_type')
    @patch('src.workflow.workflow.fetch_position_data')
    def test_process_input_position(self, mock_fetch_position, mock_identify):
        # Setup mocks
        mock_identify.return_value = {
            "is_question": True,
            "about_position": True,
            "about_company": False
        }
        mock_fetch_position.return_value = "Position information"
        
        # Test
        result = process_input("What skills are needed for a Software Engineer position?")
        
        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(result["response"], "Position information")
        mock_identify.assert_called_once()
        mock_fetch_position.assert_called_once()

    @patch('src.workflow.workflow.identify_question_type')
    @patch('src.workflow.workflow.fetch_company_data')
    def test_process_input_company(self, mock_fetch_company, mock_identify):
        # Setup mocks
        mock_identify.return_value = {
            "is_question": True,
            "about_position": False,
            "about_company": True
        }
        mock_fetch_company.return_value = "Company information"
        
        # Test
        result = process_input("What is the culture like at Google?")
        
        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(result["response"], "Company information")
        mock_identify.assert_called_once()
        mock_fetch_company.assert_called_once()

    @patch('src.workflow.workflow.identify_question_type')
    def test_process_input_not_question(self, mock_identify):
        # Setup mock
        mock_identify.return_value = {
            "is_question": False,
            "about_position": False,
            "about_company": False
        }
        
        # Test
        result = process_input("Hello there")
        
        # Assert
        self.assertTrue(result["success"])
        self.assertIn("I can answer questions", result["response"])
        mock_identify.assert_called_once()

if __name__ == '__main__':
    unittest.main()
