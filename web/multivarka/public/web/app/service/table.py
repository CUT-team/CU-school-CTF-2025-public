from typing import List, Dict, Any
from app.clickhouse.client import get_clickhouse_client

async def get_table(table_name: str) -> List[Dict[str, Any]]:
    client = get_clickhouse_client()

    columns_info = client.execute(f"""
    SELECT * FROM {table_name}
    """)

    return columns_info