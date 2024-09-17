import unittest
from pySidraData.client import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        """Set up the Client instance for testing."""
        self.client = Client()

    def test_get_root_data(self):
        """Test fetching root data."""
        root_data = self.client.get_root_data()
        self.assertIsNotNone(root_data)
        self.assertTrue(len(root_data.research_list) > 0)

    def test_list_all_aggregate_ids(self):
        """Test listing all aggregate IDs."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        self.assertIsInstance(aggregate_ids, list)
        self.assertTrue(len(aggregate_ids) > 0)

    def test_get_metadata_random(self):
        """Test getting metadata for a random aggregate ID."""
        metadata = self.client.get_metadata()
        self.assertIsNotNone(metadata)
        self.assertIsInstance(metadata, dict)

    def test_get_metadata_specific(self):
        """Test getting metadata for a specific aggregate ID."""
        # Assuming '8418' is a valid aggregate ID (you may need to update this based on available IDs)
        aggregate_ids = self.client.list_all_aggregate_ids()
        if aggregate_ids:
            aggregate_id = aggregate_ids[0]
            metadata = self.client.get_metadata(aggregate_id)
            self.assertIsNotNone(metadata)
            self.assertIsInstance(metadata, dict)

    def test_get_root_data_as_dataframe(self):
        """Test converting root data to a DataFrame."""
        df = self.client.get_root_data_as_dataframe()
        self.assertFalse(df.empty)

if __name__ == "__main__":
    unittest.main()
