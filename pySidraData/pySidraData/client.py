import requests
import pandas as pd
import random
from typing import List, Dict, Any, Optional
from sidrapy import get_table
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
        all_aggregate_ids = self.list_all_aggregate_ids()
        
        if aggregate_id is None:
            aggregate_id = random.choice(all_aggregate_ids)
        elif aggregate_id not in all_aggregate_ids:
            raise ValueError(f"Invalid aggregate ID. Choose from the following: {all_aggregate_ids}")
        
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

    def list_available_variables(self, aggregate_id: Optional[str] = None) -> List[str]:
        """List all variables available for a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        variables = [variable['nome'] for variable in metadata['variaveis']]
        return variables

#    def list_available_periods(self, aggregate_id: Optional[str] = None) -> List[str]:
#        """List all periods available for a specific aggregate ID."""
#        if aggregate_id is None:
#            aggregate_id = random.choice(self.list_all_aggregate_ids())
#        response = requests.get(f"{self.BASE_URL}/{aggregate_id}/periodos")
#        response.raise_for_status()
#        data = response.json()
#        periods = [period['id'] for period in data['periodosDisponiveis']]
#        return periods

    def list_available_periods(self, aggregate_id: Optional[str] = None) -> List[str]:
        """List all periods available for a specific aggregate ID."""
        if aggregate_id is None:
            aggregate_id = random.choice(self.list_all_aggregate_ids())
        
        # Fetch metadata for the aggregate to get the available periods
        response = requests.get(f"{self.BASE_URL}/{aggregate_id}/metadados")
        response.raise_for_status()
        data = response.json()
        
        # Extract periods - Check the structure to ensure proper access
        periods = []
        if 'periodosDisponiveis' in data:
            periods = [period['id'] for period in data['periodosDisponiveis'] if 'id' in period]

        return periods

    def list_available_classifications(self, aggregate_id: Optional[str] = None) -> List[str]:
        """List all classifications available for a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        classifications = [classification['nome'] for classification in metadata['classificacoes']]
        return classifications

    def get_data_preview(self, table_code: str, limit: int = 5) -> pd.DataFrame:
        """Fetch a small preview of data from a SIDRA table."""
        data = get_table(table_code=table_code, territorial_level='1', ibge_territorial_code='all', period='last')
        return data.head(limit)

    def list_geographical_levels(self, aggregate_id: Optional[str] = None) -> List[str]:
        """List all geographical levels available for a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        geo_levels = [level for level in metadata['nivelTerritorial']]
        return geo_levels
    
    def list_territorial_levels(self,aggregate_id: Optional[str] = None,  territorial_type=None):
        """List all geographical levels available for a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        return [level for level in metadata['nivelTerritorial'][territorial_type]]
        

    def get_table_description(self, aggregate_id: Optional[str] = None) -> str:
        """Get a detailed description of a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        description = metadata.get('descricao', 'No description available.')
        return description

    def get_data_summary(self, table_code: str, territorial_level: str, period: str) -> pd.DataFrame:
        """Retrieve a statistical summary of the data."""
        data = get_table(table_code=table_code, territorial_level=territorial_level, ibge_territorial_code='all', period=period)
        return data.describe()

    def list_all_tables(self) -> List[Dict[str, str]]:
        """List all available tables in SIDRA."""
        root_data = self.get_root_data()
        tables = [{'id': aggregate.id, 'name': aggregate.nome} for research in root_data.research_list for aggregate in research.agregados]
        return tables

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
