import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the modules to test
from src.database.file_db import get_positions_by_company_id

class TestCompanyPositions(unittest.TestCase):
    """Test cases for company positions functionality"""
    
    @patch('src.database.file_db.glob.glob')
    @patch('builtins.open')
    def test_get_positions_by_company_id(self, mock_open, mock_glob):
        """Test retrieving positions by company ID"""
        # Setup mock data
        company_id = 2001
        position1 = {
            "position": {
                "id": 1001,
                "companyId": 2001,
                "version": 1
            }
        }
        position2 = {
            "position": {
                "id": 1002,
                "companyId": 2001,
                "version": 1
            }
        }
        position3 = {
            "position": {
                "id": 1003,
                "companyId": 2002,  # Different company ID
                "version": 1
            }
        }
        
        # Setup mock file paths
        mock_glob.return_value = [
            "example-data-pos-1001-1.json",
            "example-data-pos-1002-1.json",
            "example-data-pos-1003-1.json"
        ]
        
        # Setup mock file content
        mock_file = MagicMock()
        mock_open.side_effect = [
            MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(position1))))),
            MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(position2))))),
            MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(position3)))))
        ]
        
        # Call the function
        result = get_positions_by_company_id(company_id)
        
        # Assertions
        self.assertEqual(len(result), 2)  # Should only return positions for company_id 2001
        self.assertEqual(result[0]["position"]["id"], 1001)
        self.assertEqual(result[1]["position"]["id"], 1002)
        
    @patch('src.database.file_db.glob.glob')
    @patch('builtins.open')
    def test_get_positions_by_company_id_with_versions(self, mock_open, mock_glob):
        """Test retrieving positions with different versions by company ID"""
        # Setup mock data
        company_id = 2001
        position1_v1 = {
            "position": {
                "id": 1001,
                "companyId": 2001,
                "version": 1
            }
        }
        position1_v2 = {
            "position": {
                "id": 1001,
                "companyId": 2001,
                "version": 2  # Newer version
            }
        }
        
        # Setup mock file paths
        mock_glob.return_value = [
            "example-data-pos-1001-1.json",
            "example-data-pos-1001-2.json"
        ]
        
        # Setup mock file content
        mock_file = MagicMock()
        mock_open.side_effect = [
            MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(position1_v1))))),
            MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(position1_v2)))))
        ]
        
        # Call the function
        result = get_positions_by_company_id(company_id)
        
        # Assertions
        self.assertEqual(len(result), 1)  # Should only return one position (the latest version)
        self.assertEqual(result[0]["position"]["id"], 1001)
        self.assertEqual(result[0]["position"]["version"], 2)  # Should be the newer version

if __name__ == '__main__':
    unittest.main()
