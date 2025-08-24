import os
import sys
import json
import unittest
from fastapi.testclient import TestClient

# Add the parent directory to sys.path so we can import modules properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app

class TestPositionDetailsUpdate(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
    def test_update_position_details(self):
        # First, get the current position data
        position_id = 1001
        response = self.client.get(f"/v1/position/{position_id}/versions")
        self.assertEqual(response.status_code, 200)
        
        # Get the latest version
        versions = response.json()["versions"]
        self.assertTrue(len(versions) > 0)
        
        # Create updated position data
        current_data = versions[0]  # Latest version is first in the list
        updated_data = {
            "position": current_data["position"],
            "positionFAQs": current_data["positionFAQs"],
            "positionInfo": current_data["positionInfo"]
        }
        
        # Make a change to the position title
        updated_data["position"]["positionTitle"] = "Updated Senior Full Stack Engineer (Payments)"
        
        # Add a new FAQ
        new_faq = {
            "id": 50010,
            "positionId": position_id,
            "generatedByUser": True,
            "answeredByHR": True,
            "timesAsked": 1,
            "question": "What is the expected start date?",
            "response": "We're looking for someone who can start within 4 weeks of offer acceptance.",
            "version": 1,
            "timestamp": "2025-09-01T10:00:00+10:00"
        }
        updated_data["positionFAQs"].append(new_faq)
        
        # Send the update request
        response = self.client.put(
            f"/v1/position/{position_id}/details",
            json=updated_data
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["positionId"], position_id)
        self.assertTrue(result["version"] > current_data["position"]["version"])
        
        # Verify the update by getting the latest version
        response = self.client.get(f"/v1/position/{position_id}/versions")
        self.assertEqual(response.status_code, 200)
        
        # Check the updated data
        updated_versions = response.json()["versions"]
        self.assertTrue(len(updated_versions) > len(versions))
        latest_version = updated_versions[0]
        
        # Verify the changes
        self.assertEqual(latest_version["position"]["positionTitle"], "Updated Senior Full Stack Engineer (Payments)")
        print(f"Latest version title: {latest_version['position']['positionTitle']}")
        
        # Find the new FAQ
        found_new_faq = False
        for faq in latest_version["positionFAQs"]:
            if faq["question"] == "What is the expected start date?":
                found_new_faq = True
                break
        
        self.assertTrue(found_new_faq)

if __name__ == "__main__":
    unittest.main()
