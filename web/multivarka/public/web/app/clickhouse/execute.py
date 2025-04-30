from .client import get_clickhouse_client

def clickhouse_execute(query: str):
    client = get_clickhouse_client()
    for i in query.split(";"):
        client.execute(i)