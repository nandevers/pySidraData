from dataclasses import dataclass, field
from typing import List, Dict, Any
import requests
import pandas as pd

# Define data classes for structured data
@dataclass
class Aggregate:
    id: str
    nome: str

@dataclass
class Research:
    id: str
    nome: str
    agregados: List[Aggregate] = field(default_factory=list)

@dataclass
class RootData:
    research_list: List[Research]

class RootDataIterator:
    def __init__(self, research_list: List[Research]):
        self.research_list = research_list
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.research_list):
            result = self.research_list[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

class Client:
    BASE_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"

    def get_root_data(self) -> RootData:
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

    def get_metadata(self, aggregate_id: str) -> Dict[str, Any]:
        """Fetch metadata for a specific aggregate ID."""
        response = requests.get(f"{self.BASE_URL}/{aggregate_id}/metadados")
        response.raise_for_status()
        return response.json()

    def get_root_data_as_dataframe(self) -> pd.DataFrame:
        """Fetch the root data from the API and convert it to a Pandas DataFrame."""
        response = requests.get(f"{self.BASE_URL}")
        response.raise_for_status()
        data = response.json()

        # Flatten the nested structure for DataFrame creation
        records = []
        for item in data:
            for agg in item.get('agregados', []):
                records.append({
                    'research_id': item['id'],
                    'research_name': item['nome'],
                    'aggregate_id': agg['id'],
                    'aggregate_name': agg['nome']
                })

        df = pd.DataFrame(records)
        return df

    def get_root_data_iterable(self) -> RootDataIterator:
        """Fetch the root data and return an iterable object."""
        root_data = self.get_root_data()
        return RootDataIterator(root_data.research_list)

# Example usage
client = Client()

# Get structured data using data classes
root_data = client.get_root_data()
for research in root_data.research_list:
    print(f"Research ID: {research.id}, Name: {research.nome}")
    for aggregate in research.agregados:
        print(f"  Aggregate ID: {aggregate.id}, Name: {aggregate.nome}")

# Get data as a Pandas DataFrame
df = client.get_root_data_as_dataframe()
print(df.head())

# Use custom iterator for direct iteration
root_data_iter = client.get_root_data_iterable()
for research in root_data_iter:
    print(f"ID: {research.id}, Name: {research.nome}")
