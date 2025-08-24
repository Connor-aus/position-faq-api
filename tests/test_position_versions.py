import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the modules to test
from src.database.file_db import get_all_position_versions

class TestPositionVersions(unittest.TestCase):
    """Test cases for position versions functionality"""
    
    @patch('src.database.file_db.glob.glob')
    @patch('builtins.open')
    def test_get_all_position_versions(self, mock_open, mock_glob):
        """Test retrieving all versions of a position"""
        # Setup mock data
        position_id = 1001
        position_v1 = {
            "position": {
                "id": 1001,
                "companyId": 2001,
                "version": 1
            }
        }
        position_v2 = {
            "position": {
                "id": 1001,
                "companyId": 2001,
                "version": 2
            }
        }
        position_v3 = {
            "position": {
                "id": 1001,
                "companyId": 2001,
                "version": 3
            }
        }
        
        # Setup mock file paths
        mock_glob.return_value = [
            "example-data-pos-1001-1.json",
            "example-data-pos-1001-2.json",
            "example-data-pos-1001-3.json"
        ]
        
        # Setup mock file content
        mock_open.side_effect = [
            MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(position_v1))))),
            MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(position_v2))))),
            MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(position_v3)))))
        ]
        
        # Call the function
        result = get_all_position_versions(position_id)
        
        # Assertions
        self.assertEqual(len(result), 3)  # Should return all 3 versions
        
        # Check that versions are sorted in descending order (newest first)
        self.assertEqual(result[0]["position"]["version"], 3)
        self.assertEqual(result[1]["position"]["version"], 2)
        self.assertEqual(result[2]["position"]["version"], 1)
        
    @patch('src.database.file_db.glob.glob')
    def test_get_all_position_versions_not_found(self, mock_glob):
        """Test retrieving versions for a non-existent position"""
        # Setup mock data
        position_id = 9999  # Non-existent position ID
        
        # Setup mock file paths (empty list for no files found)
        mock_glob.return_value = []
        
        # Call the function
        result = get_all_position_versions(position_id)
        
        # Assertions
        self.assertEqual(len(result), 0)  # Should return an empty list
        
    @patch('src.database.file_db.glob.glob')
    @patch('builtins.open')
    def test_get_all_position_versions_with_error(self, mock_open, mock_glob):
        """Test handling file read errors gracefully"""
        # Setup mock data
        position_id = 1001
        position_v1 = {
            "position": {
                "id": 1001,
                "companyId": 2001,
                "version": 1
            }
        }
        
        # Setup mock file paths
        mock_glob.return_value = [
            "example-data-pos-1001-1.json",
            "example-data-pos-1001-2.json"  # This file will cause an error
        ]
        
        # Setup mock file content - first file works, second file raises exception
        mock_open.side_effect = [
            MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(position_v1))))),
            MagicMock(__enter__=MagicMock(side_effect=FileNotFoundError("File not found")))
        ]
        
        # Call the function
        result = get_all_position_versions(position_id)
        
        # Assertions
        self.assertEqual(len(result), 1)  # Should return only the valid version
        self.assertEqual(result[0]["position"]["version"], 1)

if __name__ == '__main__':
    unittest.main()
