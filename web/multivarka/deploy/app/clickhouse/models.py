from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CSVTable:
    table_name: str
    columns: List[Dict[str, str]]
    
    def create_table_sql(self):
        columns_def = ", ".join(
            f"{col['name']} {col['type']}" for col in self.columns
        )
        request = f"""CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_def}) ENGINE = MergeTree() ORDER BY tuple()""" 
        print(request)
        return request  