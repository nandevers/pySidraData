import requests
import pandas as pd
import random
from typing import List, Dict, Any, Optional
from .models import RootData, Research, Aggregate

class Client:
    BASE_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"

    def __init__(self):
        self._root_data = None

    def _fetch_root_data(self) -> RootData:
        """Fetch the root data from the API and convert it to a structured Python object."""
        response = requests.get(f"{self.BASE_URL}")
        response.raise_for_status()
        data = response.json()
        
        # Convert JSON to RootData
        researches = []
        for item in data:
            agregados = [Aggregate(id=agg['id'], nome=agg['nome']) for agg in item.get('agregados', [])]
            research = Research(id=item['id'], nome=item['nome'], agregados=agregados)
            researches.append(research)
        
        return RootData(research_list=researches)

    def get_root_data(self) -> RootData:
        """Retrieve or fetch the root data."""
        if self._root_data is None:
            self._root_data = self._fetch_root_data()
        return self._root_data

    def get_metadata(self, aggregate_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch metadata for a specific aggregate ID. If no ID is provided, fetch a random one."""
        # Fetch the list of all aggregate IDs
        all_aggregate_ids = self.list_all_aggregate_ids()
        
        # Validate the provided aggregate_id or select a random one if none is provided
        if aggregate_id is None:
            aggregate_id = random.choice(all_aggregate_ids)
        elif aggregate_id not in all_aggregate_ids:
            raise ValueError(f"Invalid aggregate ID. Choose from the following: {all_aggregate_ids}")
        
        # Fetch metadata for the selected aggregate ID
        response = requests.get(f"{self.BASE_URL}/{aggregate_id}/metadados")
        response.raise_for_status()
        return response.json()

    def search_data(self, query: Dict[str, str]) -> Dict[str, Any]:
        """Search for data with specific parameters."""
        response = requests.get(f"{self.BASE_URL}/search", params=query)
        response.raise_for_status()
        return response.json()

    def get_root_data_as_dataframe(self) -> pd.DataFrame:
        """Fetch the root data from the API and convert it to a Pandas DataFrame."""
        root_data = self.get_root_data()
        records = []
        for research in root_data.research_list:
            for aggregate in research.agregados:
                records.append({
                    'research_id': research.id,
                    'research_name': research.nome,
                    'aggregate_id': aggregate.id,
                    'aggregate_name': aggregate.nome
                })

        df = pd.DataFrame(records)
        return df

    def list_all_aggregate_ids(self) -> List[str]:
        """List all available aggregate IDs."""
        root_data = self.get_root_data()
        aggregate_ids = []
        for research in root_data.research_list:
            for aggregate in research.agregados:
                aggregate_ids.append(aggregate.id)
        return aggregate_ids

    def __repr__(self):
        return f"<Client with {len(self)} research items>"

    def __len__(self):
        """Return the number of research items."""
        return len(self.get_root_data().research_list)

    def __getitem__(self, index):
        """Get a research item by index."""
        return self.get_root_data().research_list[index]

    def __iter__(self):
        """Return an iterator over the research items."""
        return iter(self.get_root_data().research_list)
